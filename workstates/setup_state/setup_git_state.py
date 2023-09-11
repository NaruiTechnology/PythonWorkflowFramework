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
from workstates.git_state import GitState
from datamodel.definitions import Consts
import os


class SetupGitState(GitState):
    @property
    def ConfigGroup(self):
        return self._config.Setup[Consts.STATES]

    def _invokeGitClone(self, erasefolder=True):
        cwd = os.getcwd()
        try:
            workspaceFolder = self._config['WorkSpace']
            if not os.path.isdir(workspaceFolder):
                os.mkdir(workspaceFolder)
                os.chdir(workspaceFolder)

            targetFolder = os.path.join(workspaceFolder, self.StateConfig['path'])
            if os.path.isdir(targetFolder) and erasefolder:
                self._logger.info('Delete the folder {}'.format(targetFolder))
                os.system('rmdir /S /Q "{}"'.format(targetFolder))
            os.makedirs(targetFolder, exist_ok=True)
            os.chdir(targetFolder)
            repoUrl = self.StateConfig['repoUrl']
            idx = repoUrl.rfind('/')
            repoFolder = '{}{}'.format(targetFolder, repoUrl[idx:])
            success = False
            for i in range(0, 3):
                if success:
                    break
                self._gitClone(repoUrl)
                if self._isGitRepo(repoFolder):
                    success = True
            if not success:
                raise Exception('Failed to clone {}.'.format(repoUrl))
        except Exception as e:
            self._errorMessage = str(e)
            self._success = False
            self._logger.error(str(e))
        finally:
            os.chdir(cwd)
