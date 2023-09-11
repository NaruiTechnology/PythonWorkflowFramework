from buildingblocks.decorators import hierarchyValidation
from buildingblocks.automation_config import AutomationConfig
from buildingblocks.automation_log import AutomationLog
from buildingblocks.event_handler import EventHandler
from buildingblocks.BinaryDocker.binary_docker import binary_docker
from collections import OrderedDict
from datamodel.definitions import Consts
import buildingblocks.utils as util
import json
try:
    import Queue as queue
except:
    import queue as queue


class SmartJsonConfig(AutomationConfig):
    @hierarchyValidation(AutomationConfig)
    def __init__(self, source, **kwargs):
        super(SmartJsonConfig, self).__init__(source)
        self.Package = None
        if kwargs is not None and len(kwargs) > 0 and 'pkg' in kwargs.keys():
            self.Package = kwargs['pkg']
        else:
            raise BaseException("The node package is required.")

        logname = 'SmartJsonConfigTest'
        automationlogInstance = AutomationLog(logname)
        self._logger = automationlogInstance.GetLogger(logname)
        automationlogInstance.TryAddConsole(logname)

        self._configTreeNodes = []
        self._selectedNode = None
        self._sender = None
        self._binaryDocker = binary_docker()
        EventHandler().addEvent(Consts.CONFIG_CHANGED, self._binaryDocker.onConfigChanged)

    @property
    def Logger(self):
        return self._logger

    @property
    def ConfigTreeNodes(self):
        return self._configTreeNodes

    @ConfigTreeNodes.setter
    def ConfigTreeNodes(self, val):
        self._configTreeNodes = val

    def BuildTree(self, root):
        try:
            for x in self.Root:
                instance = SmartJsonConfig.CreateInstance(x['Key'], json.dumps(x), self.Package, self)  # ._logger)
                self.ConfigTreeNodes.append(instance)
                instance.Build(root, self)
            self.Root = {}
        except Exception as e:
            print(str(e))


    def GetConfigNodeByJPath(self, jpath):
        try:
            self._selectedNode = None
            self._searchImageNode(jpath, self.ConfigTreeNodes)
        except Exception as e:
            self._logger.error(str(e))
        return self._selectedNode

    def RegisterSyncEvents(self):
        for element in self.ConfigTreeNodes:
            try:
                self._selectedNode = None
                self._event_binding(element)
            except Exception as e:
                self._logger.error(str(e))

    def GetInstanceBytype(self, dummyinstance):
        for element in self.ConfigTreeNodes:
            try:
                self._get_instance_by_type(element, dummyinstance)
            except Exception as e:
                self._logger.error(str(e))
        return self._selectedNode


    @staticmethod
    def CreateInstance(key, *args, **kwargs):
        classname = key
        q = queue.Queue()
        instance = None
        try:
            m = ''
            # for x in ['buildingblocks', 'SmartJsonConfig', args[1], 'ImageNode']:
            for x in ['buildingblocks', 'SmartJsonConfig', args[1], classname]:
                m += '{0}.'.format(x)
                q.put(x)

            m = m.rstrip('.')
            module = __import__(m)
            q.get_nowait()
            instance = getattr(util._extractAttr(module, q), classname)(*args, **kwargs)
        except Exception as e:
            print('Exception caught at CreateInstance, error was :%s' % str(e))
        return instance

    def onPropertyChanged(self, sender):
        if self._sender is None or type(self._sender) != type(sender):
            self._sender = sender
            EventHandler().callback(Consts.CONFIG_CHANGED, sender)
            for jpath in sender.JsonConfig.Observer:
                observer = self.GetConfigNodeByJPath(jpath)
                if observer is not None:
                    observer.onPropertyChanged(sender)
        pass


    def WriteOut(self, path=None):
        self.Save(path)

    def __str__(self):
        dic = OrderedDict()
        dic['Root'] = self.ConfigTreeNodes
        return json.dumps(dic, default=lambda x: x.__dict__, sort_keys=False, indent=4)
# ------------------------ Protected Methods -------------------------
    def _get_instance_by_type(self, element, dummyinstance):
        if self._selectedNode is not None:
            return
        if type(element).__name__ == type(dummyinstance).__name__:
            self._selectedNode = element
        for sub in element.SubMenu:
            self._get_instance_by_type(sub, dummyinstance )

    def _event_binding(self, element):
        if self._selectedNode is not None:
            return
        for j in element.JsonConfig.Observer:
            jpath = j.strip()
            if jpath != "":
                self._selectedNode = self.GetConfigNodeByJPath(jpath)
                if self._selectedNode is not None:
                    EventHandler().addEvent(Consts.PROPERTY_CHANGED, self._selectedNode.onPropertyChanged)
        for sub in element.SubMenu:
            self._event_binding(sub)

    def _searchImageNode(self, jpath, elements):
        if self._selectedNode is not None:
            return
        for element in elements:
            if self._selectedNode is not None:
                break
            if element.JPath == jpath:
                self._selectedNode = element
            self._searchImageNode(jpath, element.SubMenu)
