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
import sys, os
sys.path.append(os.path.split(os.path.dirname(os.getcwd()))[0])
from unittest import TestCase, expectedFailure
from buildingblocks.automation_config import AutomationConfig
from buildingblocks.SmartJsonConfig.SmartJsonConfig import SmartJsonConfig


class test_smart_json_config(TestCase):
    def setUp(self):
        PACKAGE = 'IntelWhitleyPkg'  # 'ConfigurTreeNode'
        self._smartJsonconfig = SmartJsonConfig('./EdkIIConfig.json', pkg=PACKAGE)
        self._smartJsonconfig.BuildTree('Root')
        pass


    def tearDown(self) -> None:
        pass

    def testLoadJson(self):
        self.assertTrue(self._smartJsonconfig is not None)

    def testJpath(self):
        keys = ['Root',
                'Edk2Manu',
                'Socket',
                'AdvancedPowerManagementConfiguration',
                'IIOConfiguration',
                'IOATConfiguration',
                'DisableTPH']
        for i in range(1, len(keys)):
            jpath = '.'.join(keys[0:i + 1])
            node = self._smartJsonconfig.GetConfigNodeByJPath(jpath)
            self.assertTrue(node is not None)

    @expectedFailure
    def test_testJpath_Failure(self):
        node = self._smartJsonconfig.GetConfigNodeByJPath('Foo.Doo')
        self.assertTrue(node is not None)

    def test_register_sync_events(self):
        self._smartJsonconfig.RegisterSyncEvents()

    def test_update_settings(self):
        jpath = 'Root.Edk2Manu.Socket.AdvancedPowerManagementConfiguration' \
                '.IIOConfiguration.IOATConfiguration.DisableTPH'
        instance = self._smartJsonconfig.GetConfigNodeByJPath(jpath)
        updateDictFile = './UpdateDictionary.json'
        updateDict = AutomationConfig(updateDictFile)
        updateData = updateDict.UpdateNodes[0]
        self.assertEqual(updateData['Key'], instance.JsonConfig.Key)
        self.assertNotEqual(updateData['Properties'], instance.JsonConfig.Properties)
        self.assertNotEqual(updateData['RawDataMap'], instance.JsonConfig.RawDataMap)
        instance.UpdateSettings(updateDictFile)
        self.assertDictEqual(updateData['Properties'], instance.JsonConfig.Properties)
        self.assertDictEqual(updateData['RawDataMap'], instance.JsonConfig.RawDataMap)

        socket = self._smartJsonconfig.GetConfigNodeByJPath('Root.Edk2Manu.Socket')
        socketUpdatevValue = socket.JsonConfig.UpdateDictionary[0]
        self.assertDictEqual(socket.Properties, socketUpdatevValue[instance.JsonConfig.Key][0]['1']['Properties'])
        self.assertDictEqual(socket.RawDataMap, socketUpdatevValue[instance.JsonConfig.Key][0]['1']['RawDataMap'])

        self._smartJsonconfig.WriteOut('c:/temp/test.json')