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
import json
from collections import OrderedDict


class ApiPayload(OrderedDict):
    def __getitem__(self, key):
        for k, v in self.__dict__.items():
            if k == key:
                return v

    def __setitem__(self, key, value):
        if key not in self.__dict__.keys():
            self.__dict__[key] = value

    def __iter__(self):
        for key in self.__dict__.keys():
            yield self.__dict__[key]

    def __contains__(self, item):
        containsVal = False
        for k, v in self.__dict__.items():
            if v == item:
                containsVal = True
                break
        return containsVal

    def __str__(self):
        return json.dumps(self.__dict__, default=lambda x: x.__dict__, sort_keys=False, indent=4)

    @property
    def JSON(self):
        json.loads(str(self))

    @property
    def Count(self):
        return len(self.__dict__)


