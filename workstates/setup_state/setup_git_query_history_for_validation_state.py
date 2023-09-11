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


class setup_git_query_history_for_validation_state(SetupGitState):
    @hierarchyValidation(SetupGitState)
    def DoWork(self):
        try:
            self._queryLog()
            pass
        except Exception as ex:
            self._errorMessage = str(ex)
            self._logger.error(str(ex))
            self._success = False



