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
from threading import Thread
from buildingblocks.event_handler import EventHandler
from buildingblocks.definitions import Resources
import os as os
import sys
import time
import buildingblocks.utils as util

class WorkThreadMetaClass(type):
    def __new__(cls, name, parents, dct):
        if 'class_id' not in dct:
            dct['class_id'] = name.lower()
        return super(WorkThreadMetaClass, cls).__new__(cls, name, parents, dct)

    def __get__(self, obj, objtype):
        """Support instance methods."""
        import functools
        return functools.partial(self.__call__, obj)


class WorkThread:#abstract base class
    __metaclass__ = WorkThreadMetaClass
    file = __file__

    def __init__(self, *args, **kwargs):
        self._thread = None
        self._isRunning = False
        self._recurringInterval = util.DefaultRecurringInterval
        self._evenStop = None
        if kwargs is not None and len(kwargs) > 0 and 'StopEvent' in kwargs.keys():
            self._evenStop = kwargs['StopEvent']
        '''
            NOTE: if the timeout value < 0, the life time for a work thread is infinit
        '''
        self._timeout = -1
        self._shutdownEvent = None

    @property
    def ShutdownEvent(self):
        return self._shutdownEvent

    @ShutdownEvent.setter
    def ShutdownEvent(self, val):
        self._shutdownEvent = val

    @property
    def RecurringInterval(self):
        return self._recurringInterval

    @RecurringInterval.setter
    def RecurringInterval(self, val):
        self._recurringInterval = val

    @property
    def Timeout(self):
        return self._timeout

    @Timeout.setter
    def Timeout(self, val):
        self._timeout = val

    @property
    def RecurringInterval(self):
        return self._recurringInterval

    @RecurringInterval.setter
    def RecurringInterval(self, val):
        self._recurringInterval = val

    @abstractmethod
    def IntialWork(self):
        raise NotImplementedError("user must implemente the IntialWork.")

    @abstractmethod
    def StateFactory(self, workState = None):
        raise NotImplementedError("user must implement the StateFatory.")

    def Setup(self, config):
        try:
            if config is not None:
                s = config["timeout"]
                if s is not None and s.strip() != b'':
                    self.SetTimeout(int(s))
                clsname = [type(self).__name__.replace('thread', '')]
                if clsname in config["log"].keys():
                    logfileName = config["log"][clsname]
                    if logfileName is not None and logfileName.strip() != '':
                        logpath = config["log"]["path"]
                        if logpath is not None and logpath != "current":
                            logfileName = os.path.join(logpath, logfileName)
                        self.SetLogFileName(logfileName)
                if config["recurring"] is not None:
                        recurring = config["recurring"].strip()
                        if recurring != '':
                            self._recurringInterval = int(recurring, 16)
        except:pass

    def Start(self):
        try:
            self._thread = Thread(target = self.WorkerProcess)
            self._thread.daemon = True
            if self._thread is not None:
                self._isRunning = True
                self._thread.start()
                #self._thread.join()
        except:
            type_, value_, traceback_ = sys.exc_info()
            print("type: {0}, value: {1}, traceback: {2}".format(type_, value_, traceback_))

    def Stop(self):
        if self._thread is not None:
            self._isRunning = False
            self._thread.do_run = False

    def _isShutDownSet(self):
        if self._shutdownEvent is None:
            return False
        else:
            return self._shutdownEvent.is_set()

    def WorkerProcess(self):
        startTime = time.time()
        while self._isRunning:
            state = self.StateFactory()
            elapsedTime = time.time() - startTime
            if self._timeout > 0 and elapsedTime > self._timeout or self._isShutDownSet():
                msg = "timeout {0} (sec) reached, stop now.".format(self._timeout)
                self._logger.warning(msg)
                self.Stop()
                break
            if state is not None:
                self.ExecuteState(state)

    def ExecuteState(self, state):
        if state is None:
            return
        try:
            EventHandler().addEvent(Resources.STATE_COMPLETE_EVENT, self.onStateComplete)
            state.Excute()
        except:
            type_, value_, traceback_ = sys.exc_info()
            print("type: {0}, value: {1}, traceback: {2}".format(type_, value_, traceback_))
            pass
        finally:
            pass

    def onStateComplete(self, sender):
        try:
            if self._evenStop is not None and self._evenStop.wait(self._recurringInterval):
                self.Stop()
            state = self.StateFactory(sender)
            if state is not None:
                self.ExecuteState(state)
        finally:
            EventHandler().removeEvent(Resources.STATE_COMPLETE_EVENT)
            pass
