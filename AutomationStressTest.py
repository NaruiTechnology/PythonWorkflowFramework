from buildingblocks.automation_log import AutomationLog
from buildingblocks.automation_config import AutomationConfig
from datamodel.definitions import Consts
import msvcrt
import subprocess
import os,sys
import shutil

if __name__ == '__main__':
    try:
        sessionId = '5kjevxfmtjmpbcae2rilzm1y'
        stressDataPath = 'D:/Temp/McuStressData'
        automationPath = os.getcwd()  # r'D:/Projects/McuRelease/Dev/ReleaseAutomation'
        logname = 'ReleaseAutomationStressTest'
        automationlogInstance = AutomationLog(logname)
        automationlog = AutomationLog(logname)
        logger = automationlogInstance.GetLogger(logname)
        automationlog.TryAddConsole(logname)
        while True:
            dirlist = os.listdir(stressDataPath)
            if len(dirlist) > 0:
                requestTemplate = os.path.realpath(r'{}/McuReleaseRequest.json'.format(automationPath))
                releaseRequest = AutomationConfig(requestTemplate)
                releaseLee = releaseRequest.ReleaseLees[0]
                template = releaseLee['Mcus'][0]
                mcu = dirlist[0]
                dropboxPath = os.path.realpath(r'{}/ReleaseDropBox/{}'.format(automationPath, mcu))
                source = r'{}/{}'.format(stressDataPath, mcu)
                shutil.copy(source, dropboxPath)
                mcuRelease = {}
                for k, v in template.items():
                    mcuRelease[k] = v
                mcuRelease[Consts.MCU] = mcu
                releaseLee[Consts.MCUS][0] = mcuRelease
                requestJson = 'McuReleaseRequest_{}.json'.format(releaseLee['ReleaseTo'])
                requestJsonPath = os.path.realpath(r'{}/{}'.format(automationPath, requestJson))
                releaseRequest.Save(requestJsonPath)

                worksheet = r'McuRelease_{}.json'.format(sessionId)
                commandline = r'python McuReleaseAutomation.py -r {} --worksheet {}'.format(requestJson, worksheet)
                resp = subprocess.Popen(commandline,
                                        stdout=subprocess.PIPE,
                                        shell=False).communicate()[0]
                try:
                    if os.path.isfile(worksheet) and os.stat(worksheet).st_size != 0:
                        config = AutomationConfig(worksheet)
                        if config['TransStatus'] == 'Failed':
                            logger.error(config['TransError'])
                            continue  # sys.exit(2)
                finally:
                    os.remove(source)
                    os.remove(dropboxPath)
            else:
                break
            if msvcrt.kbhit():
                char = msvcrt.getch()
                if str(char).lower() == 'q':
                    break
    except KeyboardInterrupt as kbEx:
        sys.exit(1)
    except Exception as e:
        print(str(e))
        sys.exit(1)

