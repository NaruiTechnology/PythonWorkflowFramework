from abc import abstractmethod
from buildingblocks.decorators import hierarchyValidation
from buildingblocks.decorators import timeElapseTimer
from buildingblocks.workflow.workstate import WorkState


class SystemControlState(WorkState):
    @hierarchyValidation(WorkState)
    def __init__(self, *args, **kwargs):
        super(SystemControlState, self).__init__(*args, **kwargs)
        self._timeoutTimer(0, True)
        self._timeout = 300

    @hierarchyValidation(WorkState)
    def DoWork(self):
        self.CallSystemFunction()

    @propertyOutputFile
    def Timeout(self):
        return self._timeout

    @Timeout.setter
    def Timeout(self, val):
        self._timeout = val

    @abstractmethod
    def CallSystemFunction(self):
        raise NotImplementedError("users must implement the CallSystemFunction method!")


    @timeElapseTimer
    def _timeoutTimer(self, timeout, reset):
        return self._timeoutTimer.isTimeout

    def _checkTimeout(self, timeout=None):
        self._success = False
        if timeout is not None:
            t = timeout
        else:
            t = self._timeout
        if t is not None and t != '':
            t = t.lstrip().strip()
            if t != '':
                timeout = int(t, 0)
                if self._timeoutTimer(timeout, False):
                    self._success = True
                    if self._logger is not None:
                        self._logger.info('Timeout = {0}sec reached. Test aborted.'.format(timeout))
                    if not self._abort:
                        self._setGraceTermination()
                    self._abort = True
                    return