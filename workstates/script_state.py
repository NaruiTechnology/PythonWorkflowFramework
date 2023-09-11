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
from workstates.popen_state import POpenState
from datamodel.definitions import Consts
import subprocess, os


class ScriptState(POpenState):
    @hierarchyValidation(POpenState)
    def DoWork(self):
        self._invokeSubprocess()

    @hierarchyValidation(POpenState)
    def _invokeSubprocess(self):
        lines = list()
        cwd = os.getcwd()

        try:
            dir = self.StateConfig['path']
            os.chdir(dir)
            script = self.StateConfig['script']
            p = self.StateConfig[Consts.PARAMETERS]
            parameters = ''
            if isinstance(p, list) and len(p) > 0:
                parameters = ' '.join([str(x) for x in p])
            commandline = r'python {} {}'.format(script, parameters)
            self._logger.info('Call commandline [{}]'.format(''.join(commandline)))
            resp = subprocess.Popen(commandline,
                                    stdout=subprocess.PIPE,
                                    shell=False).communicate()[0]

            for line in resp.split(b'\n'):
                # self._logger.info(line.rstrip())
                lines.append(line)
            return [x.decode('utf-8') for x in lines]

        except Exception as e:
            self._success = False
            self._logger.error(str(e))
        finally:
            os.chdir(cwd)
        return lines

    @hierarchyValidation(POpenState)
    def _dryRun(self):
        script = self.StateConfig['script']
        p = self.StateConfig[Consts.PARAMETERS]
        parameters = ''
        if isinstance(p, list) and len(p) > 0:
            parameters = ' '.join([str(x) for x in p])
        commandline = r'python {} {}'.format(script, parameters)
        self._logger.info('Dry run - commandline [{}]'.format(commandline))
