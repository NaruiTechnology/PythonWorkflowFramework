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
from json import JSONDecoder


class ApiResponse(object):
    def __init__(self, source=None):
        self.__dict__ = OrderedDict()
        if source is not None:
            jsonString = source
            decoder = JSONDecoder(object_hook=OrderedDict)
            self.__dict__ = decoder.decode(jsonString)

    def __getitem__(self, key):
        for k, v in self.__dict__.items():
            if k == key:
                return v
            if type(v) is dict:
                ret = self._getitem(key, v)
                if ret is not None:
                    return ret
            elif type(v) is list:
                for x in v:
                    ret = self._getitem(key, x)
                    if ret is not None:
                        return ret
        return None

    def _getitem(self, key, item):
        if key is None:
            return item
        for k, v in item.items():
            if key == k:
                return v
        if type(item) is dict:
            for k, v in item.intems():
                if k == key:
                    self._getitem(None, v)
        elif type(item) is list:
            for x in item:
                self._getitem(key, x)

    def __setitem__(self, key, val):
        if key not in self.__dict__.keys():
            self.__dict__[key] = val

    def __delitem__(self, key):
        if key in self.__dict__.keys():
            self.__dict__.remove(key)

    def __iter__(self):
        for key in self.__dict__.keys():
            node = self.__dict__[key]
            for x in node.keys():
                yield node[x]

    def __str__(self):
        dic = OrderedDict()
        for k, v in self.__dict__.items():
            if not k.startswith('_'):
                dic[k] = v
        return json.dumps(dic, default=lambda x: x.__dict__, sort_keys=False, indent=4)

    def Save(self, jsonFilePath):
        if jsonFilePath is not None:
            with open(jsonFilePath, 'w') as f:
                f.write(str(self))


