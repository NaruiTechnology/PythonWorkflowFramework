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
from workstates.setup_state.setup_git_state import SetupGitState
from datamodel.definitions import Consts
import os
import shutil


class setup_git_commit_history_validation_state(SetupGitState):
    @hierarchyValidation(SetupGitState)
    def DoWork(self):
        self._verifyCommitHistoryQueryResults()

        if self._warningMessage is not None and not self._config.DryRun:
            try:
                cwd = os.getcwd()
                workfolder = self.StateConfig['path']
                if self._isGitRepo(workfolder):
                    releaseLee = self._parentWorkThread._mcuRelease

                    self._createInitialTagOfStaging(releaseLee['ReleaseTo'])

                    os.chdir(workfolder)
                    inf_build_py = 'inf_build.py'
                    for mcu in releaseLee[Consts.MCUS]:
                        infBuildPath = mcu['PkgPath'].replace('/repository', '') \
                            .replace('/{}'.format(mcu[Consts.CPU_SEGMENT]), '') \
                            .replace('/{}'.format(mcu['ReleaseTarget']), '')
                        infBuild = '{}/{}'.format(infBuildPath, inf_build_py)
                        if not os.path.isdir(infBuildPath):
                            os.makedirs(infBuildPath, exist_ok=True)
                        if os.path.isfile(infBuild):
                            template = '{}/{}/{}'.format(os.path.dirname(__file__), self.StateConfig['parameters'][0],
                                                         inf_build_py).replace('setup_state', 'processing_state')
                            if os.path.isfile(template):
                                tag = self._parentWorkThread._tag
                                shutil.copy(template, infBuild)
                                self._invokeGitCommandline('add', [infBuild])
                                comments = 'Initial'
                                self._gitCommit(comments)
                                self._gitCreateTag(tag, comments)
                                self._gitPush()
                                self._logger.info('Created the initial tag [{}] with comments [{}] for the release to '
                                                  '[{}]'.format(tag, comments, releaseLee['ReleaseTo']))
                                self._success = True
                                self._errorMessage = ''
                                self._warningMessage = 'The initial tag [{}] has been created.'.format(tag)
                        break
                pass
            except Exception as ex:
                self._errorMessage = str(ex)
                self._logger.error(str(ex))
                self._success = False
            finally:
                os.chdir(cwd)

    def _createInitialTagOfStaging(self, releaseTo):
        for state in self._config.Setup[Consts.STATES]:
            key = list(state)[0]
            if key == 'git_clone_staging':
                workfolder = os.path.join(self._config.WorkSpace, 'release')
                if not os.path.isdir(workfolder):
                    os.makedirs(workfolder, exist_ok=True)
                os.chdir(workfolder)
                repoUrl = list(state.items())[0][1][Consts.STATE_DATA]['repoUrl'] \
                    .replace(Consts.RELEASE_TO, releaseTo.replace('_', '-'))
                idx = repoUrl.rfind('/')
                repoFolder = '{}{}'.format(workfolder, repoUrl[idx:])
                self._gitClone(repoUrl)
                if self._isGitRepo(repoFolder):
                    os.chdir(repoFolder)
                    readme = os.path.realpath('{}/README.md'.format(repoFolder))
                    if os.path.isfile(readme):
                        readmeTemp = os.path.realpath('{}/README_Template.md'.format(repoFolder))
                        shutil.copy(readme, readmeTemp)
                        tag = self._parentWorkThread._tag
                        self._invokeGitCommandline('add', [readmeTemp])
                        comments = 'Initial'
                        self._gitCommit(comments)
                        self._gitCreateTag(tag, comments)
                        self._gitPush()
                        self._logger.info(' The initial commit tag [{}] for [{}] staging has been created.'
                                          .format(tag, releaseTo))
                os.chdir(self._config.WorkSpace)
                os.system('rmdir /S /Q "{}"'.format(workfolder))