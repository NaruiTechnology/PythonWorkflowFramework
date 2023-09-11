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
from datamodel.readme_md.readme_document import readme_document
from workstates.setup_state.setup_script_validation_state import setup_script_validation_state
import os
import weakref
import buildingblocks.utils as util
try:
    import queue
except ImportError:
    import Queue as queue


class MicrocodeReleaseThread(WorkThread):
    @hierarchyValidation(WorkThread)
    def __init__(self, releaseRequst, config, logger):
        super(MicrocodeReleaseThread, self).__init__()
        self._keyboardInterrupted = False
        self._releaseRequst = releaseRequst
        self._config = config
        self._logger = logger
        self._queue = None
        # if self._config.timeout.strip() != '':
        #    self._timeout = eval(self._config.timeout.strip())
        self._lastGitResults = None
        self._mcuRelease = None
        self._tag = None
        self._password = None
        self._jsonWorkSheet = None

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
            status = TransactionStatus.FAILED
            validationstate = setup_script_validation_state()
            self._queue.queue.clear()
            self._logger.error(errorMessage)
            self._config.TransStatus = status.value
            self._config.TransError = errorMessage
            validationstate._success = False
            validationstate.ErrorMessage = errorMessage
            self._updateTransactionStatus(validationstate, status)
            self._config.Save()
        elif self._queue.qsize() > 0:
            state = self._queue.get_nowait()

        return state

    def _initializeReleaseLee(self, releaseLee):
        errorbuffer = list()
        releaseTo = releaseLee['ReleaseTo']
        NonRestrictedTarget = ['Public', 'NDA']
        try:
            for mcu in releaseLee[Consts.MCUS]:
                readmeTemplate = os.path.realpath('{}/{}/README_Template.md'.format(os.path.dirname(__file__),
                                                                                    '../../ReleaseAutomation'))
                mcupath = self.McuDropboxPath(mcu[Consts.MCU])
                doc = readme_document(readmeTemplate)
                mcuheader = McuHeaderInfo(mcupath)
                error = mcuheader.ParseError
                if error is not None:
                    raise Exception(error)
                mcu['CpuID'] = mcuheader.CpuId
                mcu['PlatformID'] = mcuheader.PlatformID

                scope = mcu['Scope'].strip()
                if scope != '' and releaseTo in NonRestrictedTarget:
                    scope = releaseTo
                else:
                    scope = 'RestrictedPkg'
                mcu['Scope'] = scope

                releasetarget = mcu['ReleaseTarget'].strip()
                if releaseTo not in NonRestrictedTarget:
                    releasetarget = mcu['ReleaseTarget'].strip()
                if releasetarget == '' or mcuheader.IsDebugOnlyRelease:
                    releasetarget = 'debug'
                mcu['ReleaseTarget'] = releasetarget

                if doc.isNewCpuID(mcuheader.CpuId) and mcu['Scope'] != 'RestrictedPkg':
                    doc.ValidateReadmeTableParameters(mcu)
                pass
        except BaseException as ex:
            errorbuffer.append('Failed to process microcode, error = {}. '
                               'Please verify the file is valid'.format(str(ex)))
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
