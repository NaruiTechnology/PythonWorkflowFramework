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
from workstates.processing_state.processing_script_state import ProcessingScriptState
from datamodel.definitions import Consts
from datamodel.readme_md.readme_document import readme_document
from datamodel.AutomationException import DuplicateCpuTableRowException, NewCpuReleaseException
import os
import shutil


'''
    1. The duplicate microcode entries are allowed.  A new entry will be inserted unless all doc columns match.  
      
    2. For the cases of a microcode  has never been released before 
       the entry will not presents in this README.MD and the value of "Unannounced" will be used in the MANIFEST.MD.
       after this state been executed a new entry will be inserted to this file and the correct values should be found 
       from the MANIFEST.ME after called the PrepReleaseLocal.py     
'''


class processing_edit_read_me_state(ProcessingScriptState):
    @hierarchyValidation(ProcessingScriptState)
    def DoWork(self):
        duperrors = list()
        try:
            readme = self.StateConfig['path']
            self._syncupReadmeTemplate()
            modified = False
            if os.path.isfile(readme):
                releaseLee = self._parentWorkThread._mcuRelease
                doc = readme_document(readme)
                for mcu in releaseLee[Consts.MCUS]:
                    # NOTE: should be update regardless Public or RestrictedPkg since we use README.md as the lookup
                    # data source
                    if mcu['Scope'] == 'RestrictedPkg':
                        self._logger.info('Skip edit README.md of mcu : {} for scope RestrictedPkg'
                                          .format(mcu[Consts.MCU]))
                        continue
                    try:
                        newRow = doc.InsertNewEntry(mcu)
                        modified = True
                        self._logger.info('Insert a new row [{}] into README file [{}]'.format(newRow, doc.LoadPath))
                    except NewCpuReleaseException as nex:
                        self._errorMessage = str(nex)
                        self._logger.error(str(nex))
                        self._success = False
                    except DuplicateCpuTableRowException as e:
                        error = 'Skip insert entry to README.md. {}'.format(str(e))
                        if error not in duperrors:
                            duperrors.append(error)
                            self._logger.warning(error)
                if modified:
                    doc.Save()
                    self._syncupReadmeTemplate()
                if len(duperrors) > 0:
                    self._warningMessage = '\n'.join(duperrors)
                pass

        except Exception as ex:
            self._errorMessage = str(ex)
            self._logger.error(str(ex))
            self._success = False

    def _syncupReadmeTemplate(self):
        readme = self.StateConfig['path']
        templatepath = os.path.realpath('{}/README_Template.md'.format(os.getcwd()))
        shutil.copy(readme, templatepath)


