#-------------------------------------------------------------------------------
# This file contains 'Framework Code' and is licensed as such
# under the terms of your license agreement with Intel or your
# vendor. This file may not be modified, except as allowed by
# additional terms of your license agreement.
#
## @file
#
# Copyright (c) 2019, Intel Corporation. All rights reserved.
# This software and associated documentation (if any) is furnished
# under a license and may only be used or copied in accordance
# with the terms of the license. Except as permitted by such
# license, no part of this software or documentation may be
# reproduced, stored in a retrieval system, or transmitted in any
# form or by any means without the express written consent of
# Intel Corporation.
#-------------- -----------------------------------------------------------------

from buildingblocks.decorators import hierarchyValidation
from workstates.publish_state.publish_git_state import PublishGitState
from datamodel.definitions import Consts
import os
import re


class publish_git_commit_state(PublishGitState):
    @hierarchyValidation(PublishGitState)
    def DoWork(self):
        cwd = os.getcwd()
        try:
            workfolder = self.StateConfig['path']

            if self._isGitRepo(workfolder):
                releassLee = self._parentWorkThread._mcuRelease
                for mcu in releassLee[Consts.MCUS]:
                    if mcu['Scope'] == 'RestrictedPkg':
                        pattern = '({}/{}/(.*)((.inc)|(.inf)|(.md)))'.format(mcu['Scope'], releassLee['ReleaseTo'])
                    else:
                        pattern = '({}/(.*)((.inc)|(.inf)|(.md)))'.format(self._mcuRepoPath(mcu)
                                                                          .replace(self.StateConfig['path'], '')
                                                                          .lstrip('/'))
                    filter = '{}|'.format(pattern)
                filter = filter.rstrip('|')

                os.chdir(workfolder)
                commitList = [x for x in self._gitStagedFiles()
                              if x.upper().startswith('README.MD')
                              or x.endswith('RepositoryList.ini')
                              or len(re.findall('({}\/(.*)(.inf))'.format(releassLee['ReleaseTo'].lower()), x)) > 0
                              or len(re.findall(filter.lower(), x.lower())) > 0]

                for f in commitList:
                        self._gitAddFile(f)
                        self._logger.info('Add file {} for committing'.format(f))

                tag = self._parentWorkThread._tag
                if len(self._parentWorkThread.LastGitResults) > 0:
                    splitHistory = self._parentWorkThread.LastGitResults[0][0].decode('utf-8').split('_')
                    splitTag = tag.split('_')
                    if eval(splitHistory[0]) == eval(splitTag[0]):  # if there is a tag created in the same day
                        idx = 1
                        if len(splitHistory) > 1 and splitHistory[1].isnumeric():
                            idx = eval(splitHistory[1]) + 1
                        tag = '{}_{}_{}'.format(splitTag[0], idx, releassLee['ReleaseTo'])
                self._parentWorkThread._tag = tag  # update tag

                comments = '{} Release'.format(tag)
                if len(commitList) > 0:
                    self._logger.info('Git commit tag = {}, comments = {}, '
                                      'files = [{}]'.format(tag, comments, ', '.join(commitList)))
                    if not self._config.DryRun:
                        resp = self._gitCommit(comments)
                        self._logger.info('Commit success, response = {}'.format(resp))

                        # clean up local repository to remove all unstaged/untracked file, otherwise
                        # the push may and rebase will fail
                        self._logger.info('Clean up local repository')
                        self._invokeGitCommandline('reset', ['.'])
                        self._invokeGitCommandline('clean', ['-f'])
                        self._invokeGitCommandline('restore', ['.'])

                        self._gitCreateTag(tag, comments)
                        self._logger.info('Created tag [{}] with comments : {}'.format(tag, comments))
                        self._gitPush()
                    else:
                        self._dryRun()
                pass
            else:
                self._logger.error('The directory [{}] is not a git repo.'.format(workfolder))
                self._success = False
        except Exception as e:
            self._errorMessage = str(e)
            self._success = False
            self._logger.error(str(e))
        finally:
            os.chdir(cwd)
        pass
