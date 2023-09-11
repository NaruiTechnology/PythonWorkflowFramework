from buildingblocks.decorators import hierarchyValidation
from buildingblocks.automation_config import AutomationConfig
from buildingblocks.event_handler import EventHandler
from buildingblocks.definitions import Resources
from threading import Event
import json

class JsonElement(AutomationConfig):
    @hierarchyValidation(AutomationConfig)
    def __init__(self, element):
        jstring = json.dumps(element)
        super(JsonElement, self).__init__(jstring)
        self._jpath = None
        self.__parent = element
        self.__paths = []
        self.__paths.append(self['Key'])
        self.__jpath = None

    @property
    def Parent(self):
        return self.__parent

    @Parent.setter
    def Parent(self, val):
        self.__parent = val

    @property
    def JPath(self):
        return self.__jpath

    @JPath.setter
    def JPath(self, val):
        self.__jpath = val
        for sub in self.SubMenu:
            jelement = JsonElement(sub)
            jelement.InsertJpath(self['Key'])
            jelement.Parent.JPath = str(jelement)

    def InsertJpath(self, val):
        self.__paths.insert(0, val)
        self.Parent.JPath = str(self)

    def __str__(self):
        return '.'.join(self.__paths)

    def onProperyChanged(self, sender):
        try:
            # update
            pass
        finally:
            # EventHandler().removeEvent(Resources.PROPERTY_CHANGED)
            pass
