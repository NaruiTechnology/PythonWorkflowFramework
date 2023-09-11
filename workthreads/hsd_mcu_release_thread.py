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
from buildingblocks.workflow.work_thread import WorkThread
from buildingblocks.decorators import hierarchyValidation
from datamodel.definitions import Consts, Environment, ReadmeTableColumn
from datamodel.definitions import TransactionStatus
from workstates.systemControlState.waitKeyStrokeState import WaitKeyStrokeState
from workstates.publish_state.publish_cleanup_state import publish_cleanup_state
from datamodel.McuHeaderInfo import McuHeaderInfo
from workstates.setup_state.setup_script_validation_state import setup_script_validation_state
from datamodel.ApiResponse import ApiResponse
import re
import os
import json
import weakref
import buildingblocks.utils as util
try:
    import queue
except ImportError:
    import Queue as queue


class hsd_mcu_release_thread(WorkThread):
    @hierarchyValidation(WorkThread)
    def __init__(self, releaseRequst, config, logger, api):
        super(hsd_mcu_release_thread, self).__init__()
        self._keyboardInterrupted = False
        self._releaseRequst = releaseRequst
        self._config = config
        self._logger = logger
        self._queue = None
        self._lastGitResults = None
        self._mcuRelease = None
        self._tag = None
        self._password = None
        self._jsonWorkSheet = None
        self._api = api
        self._hsdcache = list()

    @property
    def HsdRestApi(self):
        return self._api

    @hierarchyValidation(WorkThread)
    def StateFactory(self, workState = None):
        state = None
        try:
            if workState is None:
                state = self.IntialWork()

                if state is not None:
                    self._mcuRelease[Consts.STATUS] = TransactionStatus.PROGRESS

            elif workState._success:
                if workState._warningMessage is None:
                    self._updateTransactionStatus(workState, TransactionStatus.COMPLETED)
                else:
                    self._updateTransactionStatus(workState, TransactionStatus.ABORTED)

                if self._queue.qsize() > 0:
                    state = self._queue.get_nowait()
                else:
                    self._mcuRelease[Consts.STATUS] = TransactionStatus.COMPLETED
                    if not self._isAllMcuReleased():
                        state = self.IntialWork()
                    else:
                        self._config.TransStatus = TransactionStatus.COMPLETED.value
                '''
                else:
                    self._logger.info(Resources.COMPLETED_MSG)
                '''
            else:

                self._config.TransError = workState._errorMessage
                self._updateTransactionStatus(workState, TransactionStatus.FAILED)
                '''
                state = None
                self._queue.queue.clear()
                self.Stop()
                '''
                while self._queue.qsize() > 0:
                    state = self._queue.get_nowait()
                    if not isinstance(state, publish_cleanup_state):
                        state = None
                        continue

                if not self._keyboardInterrupted:
                    self._logger.error(Consts.FAILED_MSG)

            if state is not None:
                state.Config = self._config
                state.Logger = self._logger
                self._config.TransStatus = TransactionStatus.PROGRESS.value
                self._updateTransactionStatus(state, TransactionStatus.PROGRESS)
                self._logger.info('----------- Calling {} -----------'
                                  .format(type(state).__name__.replace(Consts.SETUP_STATE_OBJ_PREFIX, '')
                                          .replace(Consts.PUBLISH_STATE_OBJ_PREFIX, '')
                                          .replace(Consts.PROCESSION_STATE_OBJ_PREFIX, '')
                                          .replace(Consts.STATE_OBJ_SUFFIX, '')))
            elif self._config.OneTimeOnly:
                self.Stop()
        except Exception as ex:
            self._logger.error(str(ex))
            self.Stop()

        return state

    def _updateTransactionStatus(self, state, transaction):
        instancename = type(state).__name__.replace(Consts.SETUP_STATE_OBJ_PREFIX, '')\
                                           .replace(Consts.PUBLISH_STATE_OBJ_PREFIX, '')\
                                           .replace(Consts.PROCESSION_STATE_OBJ_PREFIX, '')\
                                           .replace(Consts.STATE_OBJ_SUFFIX, '')
        for s in self._config.Setup[Consts.STATES] + self._config.Processing[Consts.STATES] + self._config.Publish[Consts.STATES]:
            if list(s)[0] == instancename:
                field = list(s.items())[0][1]
                field[Consts.STATUS] = transaction.value
                if transaction == TransactionStatus.FAILED:
                    field['error'] = state.ErrorMessage
                elif transaction == TransactionStatus.ABORTED:
                    field['error'] = state._warningMessage
                break

        self._config.TransStatus = transaction.value
        self._config.Save()

    def _isAllMcuReleased(self):
        isalldone = True
        for releaseLee in self._releaseRequst.ReleaseLees:
            isalldone &= releaseLee[Consts.STATUS] != TransactionStatus.IDLE.value
        return isalldone

    @hierarchyValidation(WorkThread)
    def IntialWork(self):
        state = None
        if len(self._hsdcache) == 0:
            results = self._api.QueryAll(self._config.QueryId)
            if results is not None:
                for item in results.data:
                    self._hsdcache.append(ApiResponse(json.dumps(item)))
                q = queue.Queue()
                queueRef = weakref.ref(q)
                self._queue = queueRef()

                if not self._config.Setup[Consts.SKIP]:
                    self._createStateInstances(self._config.Setup[Consts.STATES], Consts.SETUP_PACKAGE)
                    self._config.Setup[Consts.SKIP] = True

                for releaseLee in self._releaseRequst.ReleaseLees:
                    self._tag = '{}_{}'.format(util.GetCurrentTimestamp(Consts.MCU_TIME_STAMP_FORMAT),
                                               releaseLee['ReleaseTo'])
                    if releaseLee[Consts.STATUS] == TransactionStatus.IDLE.value:
                        self._mcuRelease = releaseLee
                        # To fill up the parameters using both the header information and README.md
                        # If the parameter [CpuCodename] is specified from the Json file, the values
                        # from request Json file will be used instead.
                        errorMessage = self._initializeReleaseLee(self._mcuRelease)

                        if not self._config.Processing[Consts.SKIP]:
                            self._createStateInstances(self._config.Processing[Consts.STATES], Consts.PROCESSING_PACKAGE)
                        if not self._config.Publish[Consts.SKIP]:
                            self._createStateInstances(self._config.Publish[Consts.STATES], Consts.PUBLISH_PACKAGE)
                        break

                if errorMessage is not None:
                    self._update_validation_failure_state(errorMessage)
                elif self._queue.qsize() > 0:
                    state = self._queue.get_nowait()
            else:
                self._update_validation_failure_state('Failed to query HSD via REST Api, '
                                                      'please verify the access privilege and configuration.')

        return state

    def _initializeReleaseLee(self, releaseLee):
        errorbuffer = list()
        releaseTo = releaseLee['ReleaseTo']
        NonRestrictedTarget = ['Public', 'NDA']
        automationPath = os.getcwd()
        try:
            for mcu in releaseLee[Consts.MCUS]:
                articleID = mcu[Consts.MCU]
                mcuName, content = self._api.GetAttachment(mcu[Consts.MCU], 'inc')
                if mcuName is None:
                    raise BaseException(
                        'Cannot find the MCU attachment of the article [{}] from HSD database.'.format(mcu[Consts.MCU]))

                if content is not None:
                    dropboxpath = os.path.realpath('{}/ReleaseDropBox'.format(automationPath))
                    if not os.path.isdir(dropboxpath):
                        os.mkdir(dropboxpath)
                    mcupath = self.McuDropboxPath(mcuName)
                    with open(mcupath, 'wb') as w:
                        w.write(content)
                        self._logger.info('Downloaded mcu [{}] of article ID [{}] to DropBox [{}]'
                                          .format(mcuName, mcu[Consts.MCU], dropboxpath))
                    article = [x for x in self._hsdcache if x.id == articleID]
                    if article is not None and len(article) > 0:
                        releaseItem = article[0]
                    else:
                        errorbuffer.append('Failed to download attachment [{}] of article ID [{}] from HSD database.'
                                           .format(mcu[Consts.MCU], articleID))

                    mcuheader = McuHeaderInfo(mcupath)
                    error = mcuheader.ParseError
                    if error is not None:
                        raise Exception(error)

                    mcu[Consts.MCU] = mcuName
                    mcu['ReleaseTo'] = releaseTo
                    cpuId = releaseItem['processor_signature'].rstrip('h')
                    if cpuId == '':
                        cpuId = mcuheader.CpuId
                    mcu['CpuID'] = cpuId

                    platformID = mcu['PlatformID'].strip()
                    if platformID == '':
                        platformID = mcuheader.PlatformID
                    mcu['PlatformID'] = platformID

                    cpucodename = mcu['CPUCodeName'].strip()
                    if cpucodename == '':
                        cpucodename = releaseItem['die']
                    mcu['CPUCodeName'] = cpucodename

                    scope = mcu['Scope'].strip()
                    if scope != '' and releaseTo in NonRestrictedTarget:
                        scope = releaseTo
                    else:
                        scope = 'RestrictedPkg'
                    mcu['Scope'] = scope

                    releasetarget = mcu['ReleaseTarget'].strip()
                    if releasetarget == '':
                        releasetarget = releaseItem['patch_status']
                        if releaseTo not in NonRestrictedTarget:
                            if not mcuheader.IsDebugOnlyRelease:
                                releasetarget = releaseItem['patch_status']
                    mcu['ReleaseTarget'] = releasetarget

                    cpucodename = mcu['CPUCodeName'].strip()
                    if cpucodename == '':
                        cpucodename = releaseItem['die']
                    mcu['CPUCodeName'] = cpucodename

                    stepping = mcu['Stepping'].strip()
                    if stepping == '':
                        stepping = releaseItem['rev_step']
                        if stepping == '':
                            split = re.split(' ', releaseItem['title'])
                            for i in range(0, len(split)):
                                token = split[len(split) - i - 1]
                                if re.match(r'([A-F)[0-9]){2}', token):
                                    stepping = token
                                    break
                    mcu['Stepping'] = stepping
                    pass
        except BaseException as ex:
            errorbuffer.append('Failed to process microcode, error = {}. '
                               'Please verify the HSD article ID or the attachment name is valid'.format(str(ex)))
        if len(errorbuffer) > 0:
            return '\n'.join(errorbuffer)
        else:
            return None

    def _createStateInstances(self, states, package):
        for state in states:
            for key, val in state.items():
                stateConfig = val
                skip = stateConfig[Consts.SKIP]
                if not skip:
                    instance = util.CreateInstance(key,
                                                   package,
                                                   self)
                    instance.Config = self._config
                    instance.Logger = self._logger
                    self._queue.put(instance)
                    if val['waitkeystroke']:
                        self._queue.put(WaitKeyStrokeState(self, '{}:{}'
                                                           .format(package.replace(Consts.STATE_OBJ_SUFFIX, ''), key)))

    def _update_validation_failure_state(self, errorMessage):
        status = TransactionStatus.FAILED
        validationstate = setup_script_validation_state()
        if self._queue is not None:
            self._queue.queue.clear()
        self._config.TransStatus = status.value
        self._config.TransError = errorMessage
        validationstate._success = False
        validationstate.ErrorMessage = errorMessage
        self._updateTransactionStatus(validationstate, status)
        self._config.Save()
        self._logger.error(errorMessage)

    @property
    def LastGitResults(self):
        return self._lastGitResults

    @LastGitResults.setter
    def LastGitResults(self, val):
        self._lastGitResults = val

    def McuDropboxPath(self, mcu):
        return os.path.realpath('{}/{}/{}'.format(os.path.dirname(__file__),
                                                  '../../ReleaseAutomation/ReleaseDropBox',
                                                  mcu))
