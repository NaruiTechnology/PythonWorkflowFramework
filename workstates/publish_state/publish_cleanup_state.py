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
from workstates.publish_state.publish_script_state import PublishScriptState
import os
import re


class publish_cleanup_state(PublishScriptState):
    @hierarchyValidation(PublishScriptState)
    def DoWork(self):
        try:
            cwd = os.getcwd()
            dropbox = os.path.realpath(os.path.join(cwd, self._config.McuDropBox))
            dirlist = os.listdir(dropbox)
            for f in dirlist:
                fpath = os.path.realpath(os.path.join(dropbox, f))
                if os.path.isfile(fpath):
                    if not self._config.DryRun:
                        try:
                            os.remove(fpath)
                        except Exception as ex:
                            self._logger.error(str(ex))
                    else:
                        self._logger.info(
                            'Dry run attempt to delete mcu file [{}] from release drop box.'.format(f))
            if os.path.isfile(self._config.WorkSheet):
                os.remove(self._config.WorkSheet)

            jsonPath = os.path.realpath('{}/Json'.format(os.getcwd()))
            for f in os.listdir(jsonPath):
                if re.match('^(.*)_([a-zA-Z0-9]+).json$', os.path.basename(f)):
                    os.remove(os.path.realpath('{}/Json/{}'.format(os.getcwd(), f)))

            if os.path.isdir(self._config.WorkSpace):
                os.system('rmdir /S /Q "{}"'.format(self._config.WorkSpace))

        except Exception as ex:
            self._errorMessage = str(ex)
            self._logger.error(str(ex))
            self._success = False
        finally:
            self._config.Save()
            os.chdir(cwd)
