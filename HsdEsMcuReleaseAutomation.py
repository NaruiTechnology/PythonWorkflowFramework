from buildingblocks.automation_log import AutomationLog
from workthreads.mcu_release_automation_thread import HsdEsMicrocodeReleaseThread
from datamodel.HSDESApi.HsdEsApi import HsdEsApi
import msvcrt

if __name__ == '__main__':
    try:
        logname = 'HsdEsMcuReleaseAutomation'
        automationlogInstance = AutomationLog(logname)
        automationlog = AutomationLog(logname)
        logger = automationlogInstance.GetLogger(logname)
        automationlog.TryAddConsole(logname)
        api = HsdEsApi("https://hsdes-api.intel.com/rest")
        thread = HsdEsMicrocodeReleaseThread(logger, api)
        thread.Start()
        while True:
            if thread is not None and not thread._isRunning:
                break
            if msvcrt.kbhit():
                char = msvcrt.getch()
                if str(char).lower() == 'q':
                    thread._keyboardInterrupted = True
                    thread.Stop()
                    break
    except KeyboardInterrupt as kbEx:
        if thread is not None:
            thread._keyboardInterrupted = True
            thread.Stop()
    except Exception as e:
        print(str(e))
