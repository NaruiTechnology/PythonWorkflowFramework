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
from datamodel.readme_md.cpu_attribute import cpu_attribute


class cpu_table_row(cpu_attribute):
    @hierarchyValidation(cpu_attribute)
    def __init__(self, *args, **kwargs):
        super(cpu_table_row, self).__init__(*args, **kwargs)

    def AddColumn(self, val, ignoreduplicate=False):
        if val not in self or ignoreduplicate:
            self[self.Count] = val






