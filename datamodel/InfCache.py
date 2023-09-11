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


class InfCache(object):
    def __init__(self, inf):
        self._inf = inf
        self._buffer = list()

    @property
    def Cache(self):
        return self._buffer

    @property
    def Inf(self):
        return self._inf

    @Cache.setter
    def Cache(self, val):
        self._buffer = val

    def Dump(self):
        try:
            with open(self._inf, 'w') as fw:
                fw.write('\n'.join(self._buffer))
        except IOError:
            pass


