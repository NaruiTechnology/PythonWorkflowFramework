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
from workstates.publish_state.publish_script_state import PublishScriptState
from datamodel.definitions import Consts
import os
import re


class publish_edit_manifest_file_state(PublishScriptState):
    @hierarchyValidation(PublishScriptState)
    def DoWork(self):
        try:
            releassLee = self._parentWorkThread._mcuRelease
            mcus = releassLee[Consts.MCUS]

            for mcu in mcus:
                if mcu['Scope'] == 'RestrictedPkg':
                    manifestPath = '{}/{}/{}/repository/{}/{}'.format(
                        self.StateConfig['path'],
                        mcu['Scope'],
                        releassLee['ReleaseTo'],
                        mcu['CpuSegment'],
                        mcu['ReleaseTarget'])
                else:
                    manifestPath = '{}/{}/repository/{}/{}'.format(
                        self.StateConfig['path'],
                        mcu['Scope'],
                        mcu['CpuSegment'],
                        mcu['ReleaseTarget'])

                manifest = os.path.realpath('{}/MANIFEST.md'.format(manifestPath))
                if os.path.isfile(manifest):
                    lookupUnannounced = Consts.UNANNOUNCED  # 'Unannounced'
                    buffer = list()
                    found = False
                    currentRelease = Consts.MANIFEST_EDIT_TEMPLATE\
                        .replace(lookupUnannounced, releassLee['ReleaseTo'])\
                        .replace('N/A', mcu[Consts.STEPPING])
                    with open(manifest, 'r') as f:
                        lineIndex = 0
                        for line in f.readlines():
                            line = line.strip()
                            if line == '':
                                continue
                            lookupBuffer = [x for x in line.split('|') if x != '' and x != ' ']
                            if mcu[Consts.CPU_CODE_NAME] != '' and lookupBuffer[0].strip().startswith(mcu[Consts.CPU_CODE_NAME]):
                                found = True
                                currentStepping = lookupBuffer[1].strip()
                                if len(lookupBuffer) > 1 and currentStepping != mcu[Consts.STEPPING]:
                                    buffer.append(currentRelease)
                                    self._logger.info('Update the stepping from {} to {}'.format(currentStepping,
                                                                                                 mcu[Consts.STEPPING]))
                                    continue
                            elif len(re.findall('({})'.format(lookupUnannounced), line)) > 0:
                                line = line.replace(lookupUnannounced, mcu[Consts.CPU_CODE_NAME]) \
                                    .replace('N/A', mcu[Consts.STEPPING])
                            if line.replace('|', '').strip() == '':
                                continue
                            buffer.append(line)
                            lineIndex += 1
                    with open(manifest, 'w') as fw:
                        if not self._config.DryRun:
                            fw.write('\n'.join(buffer))
                            fw.write('\n')
                        else:
                            self._logger.info('Dry run -- attempt to write manifest file {}, content = {}'
                                              .format(manifest, '\n'.join(buffer)))

                else:
                    # raise Exception('Cannot find the fie [{}]'.format(manifest))
                    raise Exception('Cannot find the fie [{}]. The selected configuration,'
                                    'release to [{}], CPU segment [{}), and release target [{}].'
                                    .format(manifest,
                                            releassLee['ReleaseTo'],
                                            mcu['CpuSegment'],
                                            mcu['ReleaseTarget']))
        except Exception as ex:
            self._errorMessage = str(ex)
            self._logger.error(str(ex))
            self._success = False


''' ------- Unit test ------------------ 
if __name__ == '__main__':
    from buildingblocks.automation_config import AutomationConfig
    from workthreads.mcu_release_thread import MicrocodeReleaseThread
    from buildingblocks.automation_log import AutomationLog
    from datamodel.McuHeaderInfo import McuHeaderInfo
    from datamodel.readme_md.readme_document import readme_document
    readmeTemplate = os.path.realpath(r'../../../ReleaseAutomation/README_Template.md')
    doc = readme_document(readmeTemplate)

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

    state = publish_edit_manifest_file_state()
    state.Config = config
    state.Logger = logger
    state._parentWorkThread = thread
    path = os.path.realpath(r'../../../ReleaseAutomation/ReleaseDropBox')
    source = 'm10806e9_000000cf_000000d0.inc'
    mcupath = os.path.realpath('{}/{}'.format(path, source))
    mcuheader = McuHeaderInfo(mcupath)
    mcu = releaseLee[Consts.MCUS][0]
    mcu[Consts.MCU] = source
    mcu['CpuSegment'] = doc.LookupCpuSegmentByCpuId(mcuheader.CpuId)
    mcu['Stepping'] = doc.LookupCpuCoreSteppingByCpuId(mcuheader.CpuId)
    mcu[Consts.CPU_CODE_NAME] = doc.LookupCpuCodeNameByCpuId(mcuheader.CpuId)
    mcu['Scope'] = releaseLee['ReleaseTo']
    mcu['ReleaseTarget'] = 'beta'
    state.DoWork()

pass
'''
