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
from datamodel.definitions import Consts
import re
import os


class publish_script_prep_release_phase_3_state(PublishScriptState):
    @hierarchyValidation(PublishScriptState)
    def DoWork(self):
        relnote_file = '{}/release/release_diff.md'.format(self._config.WorkSpace)
        lineCount = 0
        if os.path.isfile(relnote_file):
            with open(relnote_file, 'r') as f:
                lines = f.readlines()
                for line in lines:
                    if line.rstrip('\n').strip() != '':
                        lineCount += 1
        if lineCount <= 1:
            self._warningMessage = 'There is no release notes with updated MCUs been created, skip to push to GitHub'
        else:
            releaseLee = self._parentWorkThread._mcuRelease
            if self._verifyCommitHistoryQueryResults():
                return

            parameters = list()
            for p in self.StateConfig[Consts.PARAMETERS]:
                if p == Consts.REPO_NAME:
                    p = self._formatedReleaseRepoName(releaseLee)
                if p == Consts.STAGING:
                    p = self._formatedStagingFolder(releaseLee)
                if len(re.findall(Consts.GIT_EXPORT_INI, p)) > 0:
                    p = p.replace(Consts.GIT_EXPORT_INI,
                                  self._formatedGitExportIni(releaseLee['ReleaseTo']))
                if p == Consts.TAG:
                    if len(self._parentWorkThread.LastGitResults) > 0:
                        p = self._parentWorkThread.LastGitResults[0][0].decode('utf-8')
                    else:
                        p = self._parentWorkThread._tag
                parameters.append(p)
            self.StateConfig[Consts.PARAMETERS] = parameters

            resp = self._invokeSubprocess()
            msg = '\n'.join(resp)
            '''
            if msg != '':
                self._success = False
                self._errorMessage = msg
                self._logger.error(msg)
            '''
            if msg != '':
                self._logger.warning(msg)

