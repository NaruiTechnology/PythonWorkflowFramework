from workstates.systemControlState.systemControlState import SystemControlState
from buildingblocks.decorators import hierarchyValidation
import msvcrt as ms
import sys
import msvcrt

class WaitKeyStrokeState(SystemControlState):
    @hierarchyValidation(SystemControlState)
    def __init__(self, *args, **kwargs):#who):
        super(SystemControlState, self).__init__(*args, **kwargs)
        self.__defaultExpectedkey = 13 #the ordinary value of <enter> key
        if len(args) > 1:
            self._who = args[1]

    @hierarchyValidation(SystemControlState)
    def CallSystemFunction(self):
        self._success = False
        print('\n{0} - Waiting for key stroke from users: \n[Carriage Return] = continue,\n[Ctl-C, Ctl-z, q] = exit ....\n'
              .format(self._who))
        while True:
            key = ord(ms.getwch())
            print('Received key stroke = {0}'.format(key))
            if key == self.__defaultExpectedkey:
                break
            elif key == 3 or key == 26 or key == 113: # ctl-c = 3, ctl-z = 26
                self._parentWorkThread._queue.queue.clear()
                break

        self._success = True

def main():
    while True:
        key = ord(ms.getwch())
        if key == 27:  # ESC
            break
        else:
            print(key)

if __name__ == '__main__':
    main()