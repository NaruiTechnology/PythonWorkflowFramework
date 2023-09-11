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
from buildingblocks.decorators import hierarchyValidation
from workstates.setup_state.setup_git_state import SetupGitState
from datamodel.McuHeaderInfo import McuHeaderInfo
from datamodel.definitions import Consts
import os
import re


class setup_script_validation_state(SetupGitState):
    @hierarchyValidation(SetupGitState)
    def DoWork(self):
        cwd = os.getcwd()
        errorbuffer = list()
        inputErrorMessageFormat = 'The input {} value [{}] does not match the value [{}] in header of microcode {}'

        try:
            releaseToValidationError = self._releaseToValidation()
            if releaseToValidationError is not None:
                errorbuffer.append(releaseToValidationError)
            mcus = self._parentWorkThread._mcuRelease[Consts.MCUS]
            for mcu in mcus:
                mcupath = self._parentWorkThread.McuDropboxPath(mcu[Consts.MCU])
                mcuHeaderInfo = McuHeaderInfo(mcupath)
                if mcuHeaderInfo.IsDebugOnlyRelease and mcu['ReleaseTarget'] != 'debug':
                    error = inputErrorMessageFormat.format('Release target',
                                                           mcu['ReleaseTarget'],
                                                           'DebugOnlyRelease',
                                                           mcu[Consts.MCU])
                    if error not in errorbuffer:
                        errorbuffer.append(error)

                error = self._mcuFileNameValidation(mcu[Consts.MCU], mcuHeaderInfo)
                if error is not None and error not in errorbuffer:
                    errorbuffer.append(error)
            if len(errorbuffer) > 0:
                self._errorMessage = '\n'.join(errorbuffer)
                self._success = False
                self._logger.error(self._errorMessage)
        except Exception as e:
            self._errorMessage = str(e)
            self._success = False
            self._logger.error(str(e))
        finally:
            os.chdir(cwd)

    def _releaseToValidation(self):
        cwd = os.getcwd()
        releaseLee = self._parentWorkThread._mcuRelease
        for state in self._config.Setup[Consts.STATES]:
            key = list(state)[0]
            if key == 'git_clone_staging':
                repoUrl = list(state.items())[0][1][Consts.STATE_DATA]['repoUrl'] \
                    .replace(Consts.RELEASE_TO, releaseLee['ReleaseTo'].replace('_', '-'))
                idx = repoUrl.rfind('/')
                workfolder = os.path.join(self._config.WorkSpace, 'release')
                staging_dir = '{}{}'.format(workfolder, repoUrl[idx:])
                if not os.path.isdir(workfolder):
                    os.makedirs(workfolder, exist_ok=True)
                os.chdir(workfolder)
                success = False
                for i in range(0, 3):
                    if self._isGitRepo(staging_dir):
                        success = True
                        break
                    self._gitClone(repoUrl)

                os.chdir(cwd)

                if os.path.isdir(self._config.WorkSpace):
                    os.system('rmdir /S /Q "{}"'.format(self._config.WorkSpace))

                if not success:
                    return 'Submit rejected due to the selected release To [{0}] has not been configured from repo.' \
                           ' Please contact admin personal to resolve the issue ' \
                           'before to try again.  The following configurations are required : ' \
                           '(1). To create a new staging repo for [{0}] (2). To create a new ini file for GitExport. ' \
                           '(3). To create a new OTCShare repo for [{0}]'.format(releaseLee['ReleaseTo'])
                else:
                    return None

    def _mcuFileNameValidation(self, mcuRelease, mcuHeaderInfo):
        error = None
        mcuNameSpecPattern = ['^m([0-9a-f]{2})([0-9a-f]{5}|[0-9a-f]{4}|[0-9a-f]{3}|[0-9a-f]{2})'
                              '_([0-9a-f]{8}|[0-9a-f]{3}|[0-9a-f]{16}).inc$',
                              # The pattern below used to handle the case that a MCU name with multiple revision been
                              # casted, e.g. m_01_80664_80665_0b000005
                              r'^m([0-9a-f]{2})([0-9a-f]{5}|[0-9a-f]{4}|[0-9a-f]{3}|[0-9a-f]{2})_(.\w+).inc$',
                              '^m_[0-9a-f]{2}_([0-9a-f]{5}|[0-9a-f]{4}|[0-9a-f]{3}|[0-9a-f]{2})'
                              '_([0-9a-f]{8}|[0-9a-f]{3}|[0-9a-f]{16}).inc$',
                              '^m[0-9a-f]{2}([0-9a-f]{5}|[0-9a-f]{4}|[0-9a-f]{3}|[0-9a-f]{2})[0-9a-f]{2}.inc$',
                              '^m[0-9a-f]{2}[0-9a-f]{3}[0-9a-f]{2}.inc$',
                              '^mu[1-9]{1}[0-9a-f]{3}[0-9a-f]{2}.inc$']
        mcuNameFormat = ['m{}{}_{}.inc',
                         'm_{}_{}_{}.inc',
                         'mu{}{}{}.inc',
                         'm{}{}{}.inc']
        mcuRelease = mcuRelease.lower()
        revision = mcuRelease.replace('.inc', '').replace('mu', '').replace('m', '').replace('_', '')
        if mcuHeaderInfo.PlatformID is not None:
            platformID = mcuHeaderInfo.PlatformID.lower()
            revision = revision.replace(platformID, '', 1)
        if mcuHeaderInfo.CpuId is not None:
            CPUID = mcuHeaderInfo.CpuId.lstrip(r'^0+').lower()
            revision = revision.replace(CPUID, '', 1)
        platform = mcuHeaderInfo.PlatformID.lower()
        for fmt in mcuNameFormat:
            mcuName = fmt.format(platform, CPUID, revision)
            valid = False
            for p in mcuNameSpecPattern:
                if re.match(p, mcuName):
                    valid = True
                    break
            if valid:
                break
        if not valid:
            error = 'The input mcuRelease file name [{}] is not in a supported format, ' \
                  'due to fail to match the header information of CpuID [{}], Platform ID [{}], path ID [{}]'\
                  .format(mcuRelease, CPUID, platformID, mcuHeaderInfo.PatchId)
        return error

''' ------- Unit test ------------------
if __name__ == '__main__':
    from buildingblocks.automation_config import AutomationConfig
    from workthreads.mcu_release_thread import MicrocodeReleaseThread
    from buildingblocks.automation_log import AutomationLog
    import sys

    jsonConfigPath = r'../../../ReleaseAutomation'
    releaseRequst = AutomationConfig(os.path.realpath('{}/McuReleaseRequest.json'.format(jsonConfigPath)))
    config = AutomationConfig(os.path.realpath('{}/McuRelease.json'.format(jsonConfigPath)))
    logname = config.LogName
    automationlogInstance = AutomationLog(logname)
    automationlog = AutomationLog(logname)
    logger = automationlogInstance.GetLogger(logname)

    automationlog.TryAddConsole(logname)
    thread = MicrocodeReleaseThread(releaseRequst, config, logger)
    releaseLee = releaseRequst.ReleaseLees[0]
    thread._mcuRelease = releaseLee
    validationState = setup_script_validation_state()
    validationState.Config = config
    validationState.Logger = logger
    validationState._parentWorkThread = thread

    path = os.path.realpath(r'../../../ReleaseAutomation/ReleaseDropBox')
    for source in os.listdir(path):
        f = os.path.realpath('{}/{}'.format(path, source))
        try:
            releaseLee[Consts.MCUS][0][Consts.MCU] = source
            validationState.DoWork()
            if validationState._success:
                os.remove(f)
            else:
                print('Validation for [{}] failed'.format(source))
                sys.exit(1)
        except Exception as e:
            print(str(e))
        pass
pass
'''
