# -------------------------------------------------------------------------------
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
# -------------- -----------------------------------------------------------------
from abc import abstractmethod
from buildingblocks.workflow.workstate import WorkState
from buildingblocks.event_handler import EventHandler
from buildingblocks.decorators import hierarchyValidation
from buildingblocks.definitions import Resources
from datamodel.definitions import CpuSegment
from datamodel.definitions import ReleaseTarget
from datamodel.definitions import Consts


class POpenState(WorkState):
    @hierarchyValidation(WorkState)
    def Excute(self):
        try:
            self.DoWork()
        except Exception as e:
            if not self._parentWorkThread._keyboardInterrupted:
                print("---- Generic error caught at Excute, error %s" % str(e))
            self._success = False
        finally:
            EventHandler().callback(Resources.STATE_COMPLETE_EVENT, self)

    @abstractmethod
    def _invokeSubprocess(self):
        raise NotImplementedError("user must implement the _invokeSubprocess method.")

    @abstractmethod
    def _dryRun(self):
        raise NotImplementedError("user must implement the _dryRun method.")

    def _formatedInfFileName(self, mcuRelease):
        releaseTargetMap = None
        targetSystemMap = None

        cpuSegment = mcuRelease[Consts.CPU_SEGMENT]
        if cpuSegment == CpuSegment.SERVER.value:
            releaseTargetMap = 'SRV'
        elif cpuSegment == CpuSegment.DESKTOP.value:
            releaseTargetMap = 'DT'
        elif cpuSegment == CpuSegment.MOBILE.value:
            releaseTargetMap = 'MOB'
        elif cpuSegment == CpuSegment.SOC.value:
            releaseTargetMap = 'SOC'

        releaseTarget = mcuRelease[Consts.RELEASE_TARGET]
        if releaseTarget == ReleaseTarget.DEBUG.value:
            targetSystemMap = 'D'
        elif releaseTarget == ReleaseTarget.ALPHA.value:
            targetSystemMap = 'A'
        elif releaseTarget == ReleaseTarget.BETA.value:
            targetSystemMap = 'B'
        elif releaseTarget == ReleaseTarget.PRODUCTION_CANDIDATE.value:
            targetSystemMap = 'C'
        elif releaseTarget == ReleaseTarget.PRODUCTION.value:
            targetSystemMap = 'P'
        return '{}_{}.inf'.format(releaseTargetMap, targetSystemMap)

    def _formatedStagingFolder(self, releaseLee):
        return 'microcode_release-staging-{}'.format(releaseLee['ReleaseTo'].replace('_', '-').lower())

    def _formatedGitExportIni(self, releaseTo):
        gitExportIniFile = 'IntelGenericMicrocodeRepo.ini'
        if releaseTo in Consts.MAJOR_RELEASE_TO_CUSTOMMERS:
            gitExportIniFile = 'IntelRestricted{}.ini'.format(releaseTo)
        elif releaseTo == 'Automation_Testing':
            gitExportIniFile = 'IntelRestrictedAutomationTesting.ini'
        return gitExportIniFile

    def _formatedReleaseRepoName(self, releaseLee):
        return 'Intel-Restricted-{}'.format(releaseLee['ReleaseTo'].replace('_', '-'))

    def _verifyCommitHistoryQueryResults(self, bailout=False):
        releaseLee = self._parentWorkThread._mcuRelease
        if self._parentWorkThread.LastGitResults is None or len(self._parentWorkThread.LastGitResults) == 0:
            self._errorMessage = 'No commit history of [{}] available from Git log. '.format(releaseLee['ReleaseTo'])
            self._warningMessage = self._errorMessage
            if self._config.DryRun:
                self._logger.warning(self._errorMessage)
            elif bailout:
                self._logger.error(self._errorMessage)
                self._success = False

    def _mcuRepoPath(self, mcu):
        releaseLee = self._parentWorkThread._mcuRelease
        if mcu['Scope'] == 'RestrictedPkg':
            repoPath = '{}/{}/{}/repository/{}/{}'.format(self.StateConfig['path']
                                                          .replace('/InternalOnly/repository', ''),
                                                          mcu['Scope'],
                                                          releaseLee['ReleaseTo'],
                                                          mcu['CpuSegment'].lower(),
                                                          mcu['ReleaseTarget'])
        else:
            repoPath = '{}/{}/repository/{}/{}'.format(self.StateConfig['path']
                                                       .replace('/InternalOnly/repository', ''),
                                                       releaseLee['ReleaseTo'],
                                                       mcu['CpuSegment'].lower(),
                                                       mcu['ReleaseTarget'])
        return repoPath
