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
import os


class publish_git_generate_release_notes_state(PublishGitState):
    @hierarchyValidation(PublishGitState)
    def DoWork(self):
        if self._verifyCommitHistoryQueryResults():
            return

        if not self._config.DryRun:
            try:
                releaseLee = self._parentWorkThread._mcuRelease
                cwd = None
                if len(self._parentWorkThread.LastGitResults) > 1:
                    releaseTag = self._parentWorkThread.LastGitResults[0][0].decode('utf-8')
                    previousTag = self._parentWorkThread.LastGitResults[1][0].decode('utf-8')
                elif len(self._parentWorkThread.LastGitResults) > 0:
                    releaseTag = self._parentWorkThread._tag
                    previousTag = self._parentWorkThread.LastGitResults[0][0].decode('utf-8')
                else:
                    raise BaseException('Could not find the previous commit tag  for release to from staging'
                                        .format(releaseLee['ReleaseTo']))

                cwd = os.getcwd()

                workfolder = os.path.join(self.StateConfig['path'], self._formatedStagingFolder(releaseLee))
                self.StateConfig['path'] = workfolder
                if self._isGitRepo(workfolder):
                    os.chdir(workfolder)
                    if self._config.DryRun:
                        self._dryRun()
                    else:
                        self._invokeGitCommandline('checkout', ['staging'])
                        self._invokeGitCommandline('config', ['user.name', 'mcu-administrator'])
                        self._invokeGitCommandline('config', ['user.email', 'mcu_administrator@intel.com'])
                        # Check  if rebase needed
                        '''
                        tempArg = previousTag + '..HEAD'
                        resp = self._invokeGitCommandline('rev-list', ['--count', tempArg])

                        if resp != '':
                            commitCounts = eval(resp[0].strip('\n'))
                            self._logger.info('Previous commit counts = {}'.format(commitCounts))
                            if commitCounts == 0:
                                self._logger.info('The rebase is not needed.')
                            else:
                                tempArg = 'staging~{}'.format(commitCounts)
                                self._logger.info('tempArg = {}'.format(tempArg))
                                self._invokeGitCommandline('rebase', ['-i', tempArg])
                        '''

                        self._invokeGitCommandline('checkout', ['master'])
                        self._invokeGitCommandline('merge', ['staging'])
                        self._invokeGitCommandline('push', ['-f', 'origin'])
                        self._invokeGitCommandline('branch', ['-D', 'staging'])

                        self._invokeGitCommandline('tag', [releaseTag])
                        self._invokeGitCommandline('push', ['origin', '--tags'])

                        self._generateReleaseNotesFile(releaseTag, previousTag)
                else:
                    self._logger.error('The directory [{}] is not a git repo'.format(workfolder))
                    self._success = False
            except Exception as e:
                self._errorMessage = str(e)
                self._success = False
                self._logger.error(str(e))
            finally:
                if cwd is not None:
                    os.chdir(cwd)
        pass

    def _generateReleaseNotesFile(self, releaseTag, previousTag):
        buffer = list()
        parameters = ['diff', previousTag, releaseTag]
        self.StateConfig['parameters'] = parameters + self.StateConfig['parameters']
        diffList = [x.decode('utf-8') for x in self._invokeSubprocess() if x.decode('utf-8') != '']

        for diffItem in diffList:
            path, fileName = os.path.split(diffItem)
            md_file = path + '/manifest.md'
            self._logger.info(' Generate the diff results from MD_file='.format(md_file))
            if not os.path.isfile(md_file):
                raise BaseException('Cannot find file [{}] for generate release notes'.format(md_file))

            fileName = fileName.replace('_', '\_').strip()
            self._logger.info('MD_file located, filename = {}'.format(fileName))

            with open(md_file, 'r') as f:
                record_found = False
                for line in f.readlines():
                    if not record_found:
                        if line.startswith('**') and fileName.lower() in line.lower():
                            record_found = True
                            buffer.append(line)
                    else:
                        if not line.startswith('**'):
                            buffer.append(line)
                        else:
                            break

        release_file = os.path.realpath('{}/release/release_diff.md'.format(self._config.WorkSpace))
        self._logger.info("DEBUG:  Release_file:  {}".format(release_file))

        releaseTag = releaseTag.replace('_', '\_')
        previousTag = previousTag.replace('_', '\_')

        # Write the file header
        with open(release_file, 'w+') as f:
            f.write("The following files have changed in {} since {} :\n\n___  \n".format(releaseTag,  previousTag))

        with open(release_file, 'a') as f:
            for item in buffer:
                f.write(item)
        pass

