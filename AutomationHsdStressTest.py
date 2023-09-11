from buildingblocks.automation_log import AutomationLog
from buildingblocks.automation_config import AutomationConfig
import msvcrt
import subprocess
import os,sys, time

if __name__ == '__main__':
    try:
        sessionId = '3xy0n3pavge1rucqfedblguq'
        automationPath = os.getcwd()
        logname = 'ReleaseAutomationStressTest'
        automationlogInstance = AutomationLog(logname)
        automationlog = AutomationLog(logname)
        logger = automationlogInstance.GetLogger(logname)
        automationlog.TryAddConsole(logname)
        for i in range(0, 100000):
            worksheet = r'McuRelease_HSD_{}.json'.format(sessionId)
            commandline = r'python McuReleaseAutomation.py -w {}'.format(worksheet)
            resp = subprocess.Popen(commandline,
                                    stdout=subprocess.PIPE,
                                    shell=False).communicate()[0]
            time.sleep(5)
            if os.path.isfile(worksheet) and os.stat(worksheet).st_size != 0:
                config = AutomationConfig(worksheet)
                if config['TransStatus'] == 'Failed':
                    logger.error(config['TransError'])
                    continue  # sys.exit(2)
            if msvcrt.kbhit():
                char = msvcrt.getch()
                if str(char).lower() == 'q':
                    break
    except KeyboardInterrupt as kbEx:
        sys.exit(1)
    except Exception as e:
        print(str(e))
        sys.exit(1)

