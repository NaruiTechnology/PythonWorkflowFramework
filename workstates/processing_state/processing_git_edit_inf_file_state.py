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
from workstates.processing_state.processing_git_state import ProcessingGitState
from datamodel.definitions import Consts
import os
import re
import shutil
import uuid


class processing_git_edit_inf_file_state(ProcessingGitState):
    @hierarchyValidation(ProcessingGitState)
    def DoWork(self):
        modifiedRepositoryIni = False
        infs = list()
        cwd = os.getcwd()
        inf_build_py = 'inf_build.py'
        try:
            workfolder = self.StateConfig['path']
            if self._isGitRepo(workfolder):
                os.chdir(workfolder)
                releaseLee = self._parentWorkThread._mcuRelease
                for mcu in releaseLee[Consts.MCUS]:
                    intFileName = self._formatedInfFileName(mcu)
                    infPath = mcu['PkgPath']
                    inf = '{}/{}'.format(infPath, intFileName)
                    baseName = '{}_{}'.format(intFileName.replace('.inf', ''), self._parentWorkThread._tag)
                    if not os.path.isdir(infPath):
                        os.makedirs(infPath, exist_ok=True)
                    if not os.path.isfile(inf):
                        template = '{}/{}/{}'.format(os.path.dirname(__file__), self.StateConfig['parameters'][0],
                                                     intFileName)
                        if os.path.isfile(template):
                            shutil.copy(template, inf)
                            self._logger.info('Copy missing inf file to [{}]'.format(inf))
                    if os.path.isfile(inf):
                        if self._edit_inf_file(inf, mcu, baseName):
                            infs.append(inf)
                    else:
                        error = 'Cannot find the inf file [{}], please check it out.'.format(inf)
                        self._logger.error(error)
                        raise Exception(error)

                    repoini, modifiedRepositoryIni = self._verify_repository_ini_entry(releaseLee,
                                                                                       mcu,
                                                                                       modifiedRepositoryIni)
                    inf_build = inf.replace(intFileName, inf_build_py)
                    if not os.path.isfile(inf_build):
                        templateInfBuild = '{}/{}/{}'.format(os.path.dirname(__file__), self.StateConfig['parameters'][0],
                                                     inf_build_py)
                        if os.path.isfile(templateInfBuild):
                            shutil.copy(templateInfBuild, inf_build)

                comments = '{} Release'.format(releaseLee['ReleaseTo'])
                if len(infs) > 0:
                    for f in infs:
                        self._invokeGitCommandline('add', [f])
                        # comments = '{},{}'.format(comments, os.path.basename(f))
                if modifiedRepositoryIni:
                    self._invokeGitCommandline('add', [repoini])
                    # comments = '{},{}'.format(comments, os.path.basename(repoini))
                '''
                if not self._config.DryRun:
                    resp = self._gitCommit(comments)
                    self._logger.info('{}, commit response = {}'.format(comments, resp))
                    self._gitPush()
                '''
            pass
        except Exception as ex:
            self._errorMessage = str(ex)
            self._logger.error(str(ex))
            self._success = False
        finally:
            os.chdir(cwd)

    def _verify_repository_ini_entry(self, releaseLee, mcu, modifiedRepositoryIni):
        intFileName = self._formatedInfFileName(mcu)
        releaseTo = releaseLee['ReleaseTo']
        newEntry = '{}/{}'.format(releaseTo, intFileName)
        isProduction = releaseTo in ['Public', 'NDA']
        if not isProduction:
            newEntry = 'RestrictedPkg/{}'.format(newEntry)
        repoini = '{}/RepositoryList.ini'.format(self.StateConfig['path'])
        # repoini = '{}/RepositoryList.ini'.format('C:/MCUWorkspace/Sandbox/microcode_release-sandbox/InternalOnly')
        buffer = list()
        lineIndex = 0
        found = False
        modified = False
        sectionStarted = False
        if isProduction:
            tag = releaseTo
            if releaseTo != 'Public':
                tag = mcu['CpuSegment']
            sectionPattern = r'^#(#+)?(.*)?({})(w+)?(\/)?(\w+)?'.format(tag)
        else:
            sectionPattern = r'#(#+)?(.*)?({})(w+)?'.format(releaseTo)
            split = releaseTo.split('_')
            if len(split) == 2:
                sectionPattern = r'^#(#+)?(.*)?({})([_\s+]){}(w+)?$'.format(split[0], split[1])
        if os.path.isfile(repoini):
            with open(repoini, 'r') as f:
                lines = f.readlines()
                count = len(lines)
                for line in lines:
                    s = line.rstrip('\n').strip()
                    if len(re.findall(sectionPattern.lower(), s.lower())) > 0:
                        sectionStarted = True
                    elif sectionStarted:
                        if s == newEntry:
                            found = True
                        elif (lineIndex == count - 1
                              or s.startswith('#') and len(re.findall('({})'.format(releaseTo), s)) == 0)\
                                and not (found or modified):
                            self._insertNewEntry(newEntry, buffer)
                            modified = True
                            sectionStarted = False

                    buffer.append(line)
                    lineIndex = lineIndex + 1

                    if lineIndex >= count and not (found or modified):
                        if not sectionStarted:
                            buffer.append('#{}\n'.format(releaseTo))
                        self._insertNewEntry(newEntry, buffer)
                        modified = True
            if modified:
                if self._logger is not None:
                    self._logger.info('Inserted a new entry [{}] into [{}]'.format(newEntry, repoini))
                with open(repoini, 'w') as fw:
                    fw.write(''.join(buffer))
            modifiedRepositoryIni |= modified
            return repoini, modifiedRepositoryIni

    def _insertNewEntry(self, newEntry, buffer):
        buffer.append('{}\n'.format(newEntry))
        idx = len(buffer) - 1
        while idx > 0 and buffer[idx - 1] == '\n':
            buffer[idx - 1] = buffer[idx]
            buffer[idx] = '\n'
            idx -= 1

    def _edit_inf_file(self, inf, mcu, baseName):
        buffer = list()
        LISENCE_PATTERN = '^\s+.*LICENSE'
        NOTICE_FILE_PATTERN = '^\s+.*InternalOnly/NoticeFiles'
        previousInc_buffer = list()
        beginDefinesSection = None
        endDefinesSection = None
        beginSourceSection = None
        endSourceSection = None
        lineIndex = 0
        modified = False
        lineBaseName = '  BASE_NAME      = {}'.format(baseName)
        with open(inf, 'r') as f:
            lines = f.readlines()
            for line in lines:
                line = line.rstrip('\n')
                if len(re.findall(Consts.GUID_STRING, line)) > 0:
                    line = line.replace(Consts.GUID_STRING, str(uuid.uuid4()))
                if mcu['Scope'] == 'RestrictedPkg':
                    if len(re.findall(LISENCE_PATTERN, line)) > 0:
                        line = re.sub(LISENCE_PATTERN, '  ../../LICENSE', line)
                    if len(re.findall(NOTICE_FILE_PATTERN, line)) > 0:
                        line = re.sub(NOTICE_FILE_PATTERN, '  ../../InternalOnly/NoticeFiles', line)
                if line.strip().startswith('[Defines]'):
                    beginDefinesSection = True
                if beginDefinesSection and line.strip().startswith('[UserExtensions'):
                    endDefinesSection = True

                # Insert a new source

                if line.strip().startswith('[Sources]'):
                    beginSourceSection = True
                if beginSourceSection and line.strip().startswith('[UserExtensions'):
                    endSourceSection = True
                    mcuInc = mcu[Consts.MCU]
                    currentInc = 'repository/{}/{}/{}'.format(mcu[Consts.CPU_SEGMENT],
                                                              mcu['ReleaseTarget'],
                                                              mcuInc)
                    found = False
                    for x in previousInc_buffer:
                        if x.lower().endswith(mcuInc.lower()):
                            found = True
                            break
                    if not found:
                        buffer.append(currentInc + '\n')
                        modified = True
                        self._logger.info('Add the mcu {} release to inf file {}'.format(currentInc, inf))
                    beginSourceSection = False


                if re.match(r'^\s+BASE_NAME.*$', line) is not None or (beginDefinesSection and endDefinesSection):
                    #  lineIndex = lineIndex + 1
                    # continue
                    line = lineBaseName
                    modified = True
                    beginDefinesSection = endDefinesSection = None
                if line.endswith('.inc'):
                    split = line.split('/')
                    if re.match(Consts.MCU_PATTERNS, split[len(split) - 1]):
                        previousInc_buffer.append(line)
                buffer.append(line)
                lineIndex = lineIndex + 1
        if modified:
            self._logger.info('Update the INF file {}'.format(inf))
            with open(inf, 'w') as fw:
                fw.write('\n'.join(buffer))
        else:
            self._logger.info('The INF file {} has not been changed'.format(inf))
        return modified

    def _increaseRevisionNumber(self, previousInc_buffer, buffer, mcuRelease):
        mcu = mcuRelease[Consts.MCU]
        if len(previousInc_buffer) == 0:  # The case for not previous release been found
            currentInc = 'repository/{}/{}/{}\n'.format(mcuRelease[Consts.CPU_SEGMENT],
                                                        mcuRelease['ReleaseTarget'],
                                                        mcuRelease[Consts.MCU])
            buffer.append(currentInc)
        else:
            pattern = mcu[:-7]
            for pr in previousInc_buffer:
                split = pr.split('/')
                if split[len(split) - 1].startswith(pattern):
                    s = re.split(Consts.INC_FILE_PATTERNS, split[len(split) - 1])
                    x = int(s[2], 16)  # convert HEX to int
                    x += 1  # increase by 1
                    updatedMcu = '{}{}.inc'.format(mcu[:-7], format(x, '#3x').replace('x', ''))
                    self._parentWorkThread._mcuRelease[Consts.MCUS] = updatedMcu

                    buffer.append('{}{}'.format(pr[:-len(mcu)], updatedMcu))

                else:
                    buffer.append(pr)


''' ------- Unit test ------------------
if __name__ == '__main__':
    from buildingblocks.automation_config import AutomationConfig
    from datamodel.definitions import CpuSegment, ReleaseTarget
    instance = processing_git_edit_inf_file_state()
    jsonConfigPath = os.path.realpath(r'../../../ReleaseAutomation/McuReleaseRequest.json')
    releaseTos = ['NDA', 'Public', 'Supermicro_only', 'Google_only', 'WW40_2019_Hot_Fix', '20191QSR', '2018.4 QSR']
    cpuSegments = [e.value for e in CpuSegment]
    requestConfig = AutomationConfig(jsonConfigPath)
    releaseLee = requestConfig.ReleaseLees[0]
    for releaseto in releaseTos:
        releaseLee['ReleaseTo'] = releaseto
        mcu = releaseLee[Consts.MCUS][0]
        for segment in cpuSegments:
            for target in [t.value for t in ReleaseTarget]:
                mcu['CpuSegment'] = segment
                modifiedRepositoryIni = False
                mcu['CpuSegment'] = segment
                mcu['ReleaseTarget'] = target
                instance._stateConfig = {
                    "path": "D:/MCUWorkspace/Sandbox/microcode_release-sandbox/InternalOnly",
                    "command": "",
                    "parameters": ["InfTemplate"]
                }
                instance._verify_repository_ini_entry(releaseLee, mcu, modifiedRepositoryIni)
                pass
            pass
        pass
    pass
pass
'''
