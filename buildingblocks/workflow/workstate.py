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

from abc import abstractmethod
from buildingblocks.workflow.work_thread import WorkThread
from buildingblocks.event_handler import EventHandler
from buildingblocks.definitions import Resources
from buildingblocks.decorators import timeElapseTimer
import buildingblocks.utils as util


class WorkstateMetaClass(type):
    def __new__(cls, name, parents, dct):
        # create a class_id if it's not specified
        if 'class_id' not in dct:
            dct['class_id'] = name.lower()
        return super(WorkstateMetaClass, cls).__new__(cls, name, parents, dct)


class WorkState(object):
    __metaclass__ = WorkstateMetaClass
    file = __file__

    def __init__(self, *args, **kwargs):
        self._timeoutTimer(0, True)
        self._success = True
        self._id = util.IdGenerator()
        self._logger = None
        self._config = None
        self._stateConfig = None
        self._parentWorkThread = None
        self._manufactureId = None
        self._outfile = None
        if len(args) > 0 and isinstance(args[0], WorkThread):
            self._parentWorkThread = args[0]
        self._errorMessage = None
        self._warningMessage = None

    def __str__(self):
        return repr("WorkState_" + self._id)

    @property
    def Config(self):
        return self._config

    @Config.setter
    def Config(self, val):
        self._config = val

    @property
    def StateConfig(self):

        self._timeoutTimer(self._config.timeout, False)

        if self._stateConfig is None:
            configName = type(self).__name__
            l_idx = configName.index('_')
            r_idx = configName.rindex('_')
            key = configName[l_idx + 1:r_idx]
            configGroup = self.ConfigGroup
            set = False
            if configGroup is not None and isinstance(configGroup, list):
                for state in configGroup:
                    if set:
                        break
                    for k, v in state.items():
                        if set:
                            break
                        if key == k:
                            for dataKey, dval in v.items():
                                if dataKey == 'stateData':
                                    self._stateConfig = dval
                                    set = True
                                    break
        return self._stateConfig

    @StateConfig.setter
    def StateConfig(self, val):
        self._stateConfig = val

    @property
    def ErrorMessage(self):
        return self._errorMessage

    @ErrorMessage.setter
    def ErrorMessage(self, val):
        self._errorMessage = val

    @property
    def WarningMessage(self):
        return self._warningMessage

    @WarningMessage.setter
    def WarningMessage(self, val):
        self._warningMessage = val

    @property
    def ParentWorkThread(self):
        return self._parentWorkThread

    @property
    def Success(self):
        self._success

    @Success.setter
    def Success(self, val):
        self._success = val

    @property
    def Logger(self, logger):
        self._logger = logger

    @Logger.setter
    def Logger(self, val):
        self._logger = val

    def GetParentWorkThread(self):
        return self._parentWorkThread

    def SetParentWorkThread(self, val):
        if val is not None and type(val).__name__.lower().endswith('thread'):
            self._parentWorkThread = val
            self._invokeFactory = val.GetInvokeFactory()
            self._config = val._config

    def Excute(self):
        try:
            self.DoWork()
        except Exception as e:
            print("!!!! error at Excute, error %s" % str(e))
            self._success = False
        finally:
            EventHandler().callback(Resources.STATE_COMPLETE_EVENT, self)

    def LogMessage(self, msg):
        print (msg)
        if self._outfile is not None:
            self._outfile.write(msg)
            self._outfile.flush()

    @timeElapseTimer
    def _timeoutTimer(self, timeout, reset):
        return self._timeoutTimer.isTimeout

    def _checkTimeout(self, timeout, reset=False):  # timeout in seconds, reset = False
        self._success = True
        if self._timeoutTimer(timeout, reset):
            self._success = False
            errorMsg = 'Timeout = [{0} sec]. Please consider increase the timeout values.'.format(timeout)
            self._errorMessage = errorMsg
            self._logger.error(errorMsg)

    @abstractmethod
    def DoWork(self):
        raise NotImplementedError("users must implement the DoWork method!")

    @property
    def ConfigGroup(self):
        raise NotImplementedError("users must implement the ConfigGroup property!")
