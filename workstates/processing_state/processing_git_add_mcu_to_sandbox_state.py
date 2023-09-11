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
from workstates.processing_state.processing_git_state import ProcessingGitState
from datamodel.definitions import Consts
import shutil
import os


class processing_git_add_mcu_to_sandbox_state(ProcessingGitState):
    @hierarchyValidation(ProcessingGitState)
    def DoWork(self):
        try:
            cwd = os.getcwd()
            addedMcusList = list()
            releaseLee = self._parentWorkThread._mcuRelease
            mcus = releaseLee[Consts.MCUS]
            for mcu in mcus:
                source = os.path.join(self.Config.McuDropBox, mcu[Consts.MCU])
                if not os.path.isfile(source):
                    raise Exception('Cannot find the source file {}'.format(source))
                repoPath = self._mcuRepoPath(mcu)
                repo = '{}/{}'.format(repoPath, mcu[Consts.MCU])
                if not os.path.isdir(repoPath):
                    os.makedirs(repoPath, exist_ok=True)

                if not os.path.isfile(repo):
                    shutil.copy(source, repo)
                    addedMcusList.append(repo)
                    self._logger.info('Copy mcu from {} to {}'.format(source, repo))
                else:
                    self._logger.info('The repo file {} already exists.'.format(repo))

                internalOnlyPath = '{}/{}'.format(self.StateConfig['path'], mcu[Consts.MCU])
                if not os.path.isfile(internalOnlyPath):
                    shutil.copy(source, internalOnlyPath)
                    addedMcusList.append(internalOnlyPath)
                    self._logger.info('Copy mcu from {} to {}'.format(source, internalOnlyPath))
                else:
                    self._logger.info('The repo file {} already exists.'.format(internalOnlyPath))

            workfolder = self.StateConfig['path']
            os.chdir(workfolder)
            if self._isGitRepo(workfolder) and len(addedMcusList) > 0:
                for f in addedMcusList:
                    self._invokeGitCommandline('add', [f])
                    self._logger.info('Add mcu file {} for committing'.format(f))
            pass
        except Exception as ex:
            self._errorMessage = str(ex)
            self._logger.error(str(ex))
            self._success = False
        finally:
            os.chdir(cwd)
