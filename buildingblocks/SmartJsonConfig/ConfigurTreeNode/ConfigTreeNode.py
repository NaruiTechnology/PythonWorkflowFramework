from buildingblocks.SmartJsonConfig.SmartJsonConfig import SmartJsonConfig
from buildingblocks.automation_config import AutomationConfig
from buildingblocks.SmartJsonConfig.ConfigurTreeNode.RawDataMap import RawDataMap
from buildingblocks.SmartJsonConfig.ConfigurTreeNode.Properties import Properties
from buildingblocks.event_handler import EventHandler
from datamodel.definitions import Consts
import buildingblocks.utils as util
import json
import os


class ConfigTreeNode(object):
    def __init__(self, *args):
        self._id = util.IdGenerator()
        self.JPath = None
        self.JsonConfig = None
        self.RawDataMap = None
        if args is not None and len(args) > 0:
            if args[0] is not None:
                jsonstring = args[0]
                self.JsonConfig = AutomationConfig(jsonstring)
                self.RawDataMap = RawDataMap(jsonstring)
                self.Properties = Properties(jsonstring)
            if len(args) > 2:
                self._parent = args[2]
        self.SubMenu = []
        pass

    @property
    def ID(self):
        return self._id

    def Build(self, parentJpath, parent):
        self.JPath = '.'.join([parentJpath, self.JsonConfig.Key])
        for x in self.JsonConfig.SubMenu:
            instance = SmartJsonConfig.CreateInstance(x['Key'], json.dumps(x), parent.Package, parent)  #self._logger)
            if instance is not None:
                EventHandler().addEvent(Consts.PROPERTY_CHANGED, parent.onPropertyChanged)
                instance.Build(self.JPath, parent)
                self.SubMenu.append(instance)

    def onPropertyChanged(self, sender):
        try:
            self._parent.Logger.info('[{}] received property changed notification from [{}]'
                                     .format(type(self).__name__, sender.JsonConfig.Key))
            senderProperties = sender.Properties
            optionIdx = senderProperties['Options'].index(senderProperties['CurrentValue'])
            for updateData in self.JsonConfig.UpdateDictionary['UpdateData']:
                if updateData['Key'] != sender.JsonConfig.Key:
                    continue
                if str(optionIdx) != updateData['Value']['OptionKey']:
                    continue
                val = updateData['Value']
                self.JsonConfig.RawDataMap = self.RawDataMap = val['RawDataMap']
                self.JsonConfig.Properties = self.Properties = val['Properties']
        except BaseException as ex:
            self._parent.Logger.error(str(ex))

    def UpdateSettings(self, jsonDataFile):
        if not os.path.isfile(jsonDataFile):
            raise BaseException('The valid update json data file is required.')
        try:
            updateDictionary = AutomationConfig(jsonDataFile)
            data = [x for x in updateDictionary.UpdateNodes if x['Key'] == type(self).__name__]
            if len(data) > 0:
                for key, val in data[0].items():
                    if val is not None and isinstance(val, dict):
                        if key == 'Properties':
                            self.JsonConfig.Properties = self.Properties = val
                        if key == 'RawDataMap':
                            self.JsonConfig.RawDataMap = self.RawDataMap = val
                        pass
            EventHandler().callback(Consts.PROPERTY_CHANGED, self)
        except Exception as ex:
            self._parent.Logger.error(str(ex))

    def __str__(self):
        return str(self.JsonConfig)