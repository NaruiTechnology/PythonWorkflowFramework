# -------------------------------------------------------------------------------
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
# -------------- -----------------------------------------------------------------

from buildingblocks.decorators import hierarchyValidation
from workstates.script_state import ScriptState
from datamodel.definitions import Consts


class hsd_release_automation_state(ScriptState):
    @hierarchyValidation(ScriptState)
    def __init__(self, parentthread):
        super(hsd_release_automation_state, self).__init__(parentthread)
        self._releaseTo = None
        self._releaseItems = list()
        self._mcuDownloaded = list()
        self._releaseTo = None

    @property
    def ReleaseTo(self):
        return self._releaseTo

    @ReleaseTo.setter
    def ReleaseTo(self, val):
        self._releaseTo = val

    @property
    def ReleaseItems(self):
        return self._releaseItems

    @ReleaseItems.setter
    def ReleaseItems(self, val):
        self._releaseItems = val

    @property
    def McuDownloaded(self):
        return self._mcuDownloaded

    @McuDownloaded.setter
    def McuDownloaded(self, val):
        self._mcuDownloaded = val

    @property
    def ConfigGroup(self):
        return self._config.Processing[Consts.STATES]
