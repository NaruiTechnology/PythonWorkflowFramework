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
from threading import Event
from buildingblocks.decorators import hierarchyValidation
from buildingblocks.workflow.work_thread import WorkThread
from buildingblocks.automation_config import AutomationConfig
from datamodel.ApiResponse import ApiResponse
from datamodel.definitions import Consts
from datamodel.definitions import TransactionStatus
from datamodel.definitions import TaskFrequecy
from workstates.hsd_automation_state.hsd_download_mcu_state import hsd_download_mcu_state
from workstates.hsd_automation_state.hsd_create_request_state import hsd_create_request_state
from workstates.hsd_automation_state.hsd_update_hsd_submit_state import hsd_update_hsd_submit_state
from workstates.hsd_automation_state.hsd_send_notification_state import hsd_send_notification_state
import buildingblocks.utils as util
import json
import os
import datetime
import weakref
try:
    import queue
except ImportError:
    import Queue as queue


class HsdEsMicrocodeReleaseThread(WorkThread):
    @hierarchyValidation(WorkThread)
    def __init__(self, logger, api):
        self._evenStop = Event()
        super(HsdEsMicrocodeReleaseThread, self).__init__(StopEvent=self._evenStop)
        self._queue = None
        self._config = None
        self._logger = logger
        self._keyboardInterrupted = False
        self._api = api
        self._grantToStart = False
        print('--- Microcode release automation service stated.-----. \nPress Ctl-C to exit.')

    @property
    def HsdRestApi(self):
        return self._api

    @property
    def GrantToStart(self):
        return self._grantToStart

    @GrantToStart.setter
    def GrantToStart(self, val):
        self._grantToStart = val

    @hierarchyValidation(WorkThread)
    def Stop(self):
        self._evenStop.set()
        self._isRunning = False

    @hierarchyValidation(WorkThread)
    def StateFactory(self, workState = None):
        state = None
        try:
            if workState is None:
                state = self.IntialWork()
            else:
                if self._keyboardInterrupted:
                    self._logger.error(Consts.FAILED_MSG)
                elif isinstance(workState, hsd_download_mcu_state):
                    state = hsd_create_request_state(self)
                    state.McuDownloaded = workState.McuDownloaded
                    state.ReleaseItems = workState.ReleaseItems
                    state.ReleaseTo = workState.ReleaseTo
                elif isinstance(workState, hsd_create_request_state):
                    state = hsd_update_hsd_submit_state(self)
                    state.McuDownloaded = workState.McuDownloaded
                    state.ReleaseItems = workState.ReleaseItems
                    state.ReleaseTo = workState.ReleaseTo
                elif isinstance(workState, hsd_update_hsd_submit_state):
                    state = hsd_send_notification_state(self)
                    state.McuDownloaded = workState.McuDownloaded
                    state.ReleaseItems = workState.ReleaseItems
                    state.ReleaseTo = workState.ReleaseTo
                elif isinstance(workState, hsd_send_notification_state):
                    if self._queue.qsize() > 0:
                        state = self._queue.get_nowait()
                        self._grantToStart = True
                    elif not self._config.OneTimeOnly:
                        state = self.IntialWork()

            if state is not None:
                state.Config = self._config
                state.Logger = self._logger
                self._config.TransStatus = TransactionStatus.PROGRESS.value
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

    @hierarchyValidation(WorkThread)
    def IntialWork(self):
        state = None
        try:
            self._isOnSchedule()

            if not self._grantToStart:
                return None

            q = queue.Queue()
            queueRef = weakref.ref(q)
            self._queue = queueRef()

            debug = True
            results = self._api.QueryAll(self._config.QueryId)
            buffer = list()
            releaseItems = list()
            releaseTo = None
            if results is not None:
                for item in results.data:
                    buffer.append(ApiResponse(json.dumps(item)))

                dic = dict()
                if debug:
                    dic_debug = dict()
                for x in buffer:
                    gitkeeperScore = self._config.GitKeeperScore  # TODO - review: 0
                    # TODO: if x['Score'] is not None and x['Score'].isnumeric(): # TODO
                    # TODO: gitkeeperScore = eval(x['Score']) # TODO:
                    if gitkeeperScore != self._config.GitKeeperScore:
                        continue
                    elif releaseTo is None:
                        releaseTo = 'NDA'  # releaseItem['ReleaseTo']  # TODO
                    # TODO: if x['ReleaseTo'] != releaseTo: # TODO:
                    # TODO:    continue # TODO:

                    # group up based the compound values
                    # key = (x['processor_signature'], x['rev_step'], x['product_code'],
                    #      x['processor_flags'],  x['die'],  x['processor_flags'])
                    compoundkeys = [i.replace('%x%', 'x') for i in self._config['GroupCompoundKeys']]
                    key = eval(', '.join(compoundkeys))
                    if len([n for n in key if n.strip() != '']) != len(key):
                            continue
                    val = (x['rev'], x)
                    if key not in dic.keys():
                        dic[key] = val
                        if debug:
                            dic_debug[key] = list()
                    if debug:
                        dic_debug[key].append(val)
                    v = dic[key]
                    # take the largest revision number # TODO - review: ?
                    if eval(x['rev'].lower().lstrip('v')) > eval(v[0].lower().lstrip('v')):
                        dic[key] = val
                    else:
                        dic[key] = v

                releaseItems.clear()
                for k, v in dic.items():   # TODO : the rev is not correct column need to figure it out, e.g. update_revision or patch_stust, status
                    releaseItems.append(v[1])

                relaseTo = 'Apple_only'
                state1 = hsd_download_mcu_state(self)  # TODO - review: remove [0:2]
                state1.ReleaseItems = releaseItems[3:5]
                state1.ReleaseTo = relaseTo
                self._queue.put(state1)

                relaseTo = 'NDA'
                state2 = hsd_download_mcu_state(self)
                state2.ReleaseItems = releaseItems[10:15]
                state2.ReleaseTo = relaseTo
                self._queue.put(state2)

            if self._queue.qsize() > 0:
                state = self._queue.get_nowait()
        except Exception as ex:
            self._logger.error(str(ex))

        return state

    def _isOnSchedule(self):
        self._grantToStart = False
        jsonConfigPath = os.path.realpath(r'Json/HsdEsMicrocodeRelease.json')
        self._config = AutomationConfig(jsonConfigPath)

        timenow = datetime.datetime.strptime(util.GetCurrentTimestamp(), util.DefaultTimeStampFormat)
        lastrun = datetime.datetime.strptime(self._config.Schedule['LastRun'], util.DefaultTimeStampFormat)

        elapse = timenow - lastrun

        frequence = self._config.Schedule['Frequency']
        n = self._config.Schedule['Every']
        if n <= 0:
            n = 1
        if frequence == TaskFrequecy.MONTHLY.value:
            self._grantToStart = elapse.days >= 30 * n
        elif frequence == TaskFrequecy.DAILY.value:
            self._grantToStart = elapse.days > 1 * n
        elif frequence == TaskFrequecy.HOURLY.value:
            self._grantToStart = elapse.seconds > 60 * 60 * n

        if self._grantToStart:
            self._config.Schedule['LastRun'] = util.GetCurrentTimestamp()
            self._config.Save()
