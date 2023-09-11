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


class publish_script_prep_release_local_state(PublishScriptState):
    @hierarchyValidation(PublishScriptState)
    def DoWork(self):
        cache = list()
        try:
            print('NOTE: Begin processing {} it may take a while.'
                  .format(self.StateConfig['script']))

            self._checkTimeout(self._config.timeout)

            dev_root = '{}/release'.format(self._config.WorkSpace)

            if os.path.isdir(dev_root):
                os.system('rmdir /S /Q "{}"'.format(dev_root))
            os.mkdir(dev_root)

            filename = os.path.realpath('{}/UpdateRepository.py'.format(self.StateConfig['path']))
            cache = list()  # self._workaroundUpdateRepositoryScriptIssue(filename)  #

            resp = self._invokeSubprocess()
            self._logger.info('\n'.join(resp[-10:len(resp) - 1]))
            pattern = 'This is a good time to check in any changes and then proceed to creating a release'
            success = len([x for x in resp if re.match(pattern, x)]) > 0
            if not success:
                raise Exception('Failed to execute [PrepReleaseLocal.py], please find the failure details from log.')
            pass
        except Exception as e:
            self._errorMessage = str(e)
            self._success = False
            self._logger.error(str(e))
        finally:
            # recover the modified UpdateRepository.py
            if len(cache) > 0:
                with open(filename, 'w') as f:
                    for line in cache:
                        f.write(line)
    # The python script UpdateRepository.py used by PrepReleaseLocal.py
    # has a case sensitive comparision issue (line #415.  Without this workaround
    # some corner cases will failed for automation, e.g. MCU :NDA, M01506C2_00000014.inc + SOC + debug
    def _workaroundUpdateRepositoryScriptIssue(self, filename):
        buffer = list()
        cache = list()
        sourcecode = 'status = os.path.basename(missing_microcode) in ini_file_contents.ini_casesensitive_sourcenames'
        replacement = 'status = len([x for x in ini_file_contents.ini_casesensitive_sourcenames ' \
                      'if x.lower().endswith(os.path.basename(missing_microcode).lower())] ) > 0'
        lineindex = 0
        with open(filename, 'r') as f:
            lines = f.readlines()
            for line in lines:
                if line.lstrip().rstrip('\n').startswith(sourcecode):
                    line = line.replace(sourcecode, replacement)
                buffer.append(line)
                cache.append(line)
                lineindex += 1
        with open(filename, 'w') as f:
            for line in buffer:
                f.write(line)
        return cache

