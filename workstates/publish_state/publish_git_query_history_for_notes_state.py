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

class publish_git_query_history_for_notes_state(PublishGitState):
    @hierarchyValidation(PublishGitState)
    def DoWork(self):
        cwd = os.getcwd()
        parentTheread = self._parentWorkThread
        releaseLee = parentTheread._mcuRelease
        try:
            searchpattern = parentTheread._mcuRelease['ReleaseTo']
            workfolder = self.StateConfig['path']\
                .replace(Consts.RELEASE_TO, releaseLee['ReleaseTo'].replace('_', '-'))
            self.StateConfig['path'] = workfolder
            if not self._config.DryRun:
                os.chdir(workfolder)
                self._parentWorkThread.LastGitResults = self._gitQueryCommitHistory(searchpattern)
                if len(self._parentWorkThread.LastGitResults) == 0:
                    self._logger.warning('Query release history of {} and no commit been found.'.format(searchpattern))
                else:
                    for item in self._parentWorkThread.LastGitResults:
                        self._logger.info('Query staging release history of {}, results = {}'.
                                          format(searchpattern, b' : '.join(item)))
            pass
        except Exception:
            self._errorMessage = \
                'Could not find any commit log with tags in format of [yyyyMMdd_{0}] (e.g. 20191023_{0})'\
                .format(searchpattern)
            self._success = False
            self._logger.error(self._errorMessage)
        finally:
            os.chdir(cwd)

