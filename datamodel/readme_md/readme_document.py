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
from datamodel.definitions import Consts
from datamodel.definitions import CpuTableColumn
from datamodel.readme_md.cpu_table_row import cpu_table_row
from datamodel.McuHeaderInfo import McuHeaderInfo
from datamodel.definitions import CpuSegment, ReadmeTableColumn
from datamodel.AutomationException import DuplicateCpuTableRowException, NewCpuReleaseException
import buildingblocks.utils as util
import queue as queue
import os
import re
import json


class readme_document(object):
    def __init__(self, path):
        self._documentRows = list()
        self._cpuTableRows = list()
        self._columnDic = {}
        self._location = path
        self._colums = [x for x in CpuTableColumn]
        for i in range(0, len(self._colums)):
            self._columnDic[self._colums[i]] = self.__createColumnInstance(self._colums[i].value)
        self.__load(self._location)
        pass

    @property
    def LoadPath(self):
        return self._location

    @property
    def CpuTableRowCount(self):
        return len(self._cpuTableRows)

    @property
    def ToJson(self):
        columns = Consts.README_MD_COLUMNS
        dict = {}
        for cpuSegment in CpuSegment:
            lines = list([x for x in self._cpuTableRows if x[0] == cpuSegment.value])
            lineIndex = 0
            rows = list()
            for line in lines:
                tr = {}
                for i in range(line.Count):
                    tr[columns[i]] = line[i].lstrip(' ').rstrip(' ')
                rows.append(tr)
            dict[cpuSegment.value] = rows
            lineIndex += 1
            pass
        return json.dumps(dict, default=lambda x: x.__dict__, sort_keys=False, indent=4)


    @property
    def CpuTableDictionary(self):
        dict = {}
        for k, v in self._columnDic.items():
            if k == CpuTableColumn.cpu_id:
                for i in range(v.Count):
                    entries = self.EntriesDictionaryByCpuId(v[i])
                    if len(entries) > 0:
                        dict[v[i]] = entries
                break
        return dict

    def EntriesCpuIdAndCpuSegment(self, cpuId, cpuSegment):
        if not isinstance(cpuSegment, str):
            raise Exception('The input of cpuSegment must be a string.')
        results = list()
        # cpuid = re.sub('^0+', '', cpuId.upper())
        cpuid = cpuId.zfill(8).upper()
        for segment in CpuSegment:
            if segment.value == cpuSegment:
                entries = [x for x in self._cpuTableRows if x[5].zfill(8).upper() == cpuid]  # x[5].upper().endswith(cpuid)]
                lines =list([x for x in entries if x[0] == cpuSegment])
                for i in range(len(lines)):
                    line = lines[i]
                    row = list()
                    for x in range(line.Count):
                        row.append(line[x].lstrip(' ').rstrip(' '))
                    results.append(row)
        return results

    def EntriesDictionaryByCpuId(self, cpuId):
        cpuid = cpuId.zfill(8).upper()
        dict = {}
        for cpuSegment in CpuSegment:
            entries = [x for x in self._cpuTableRows if x[5].zfill(8).upper() == cpuid]
            entries = [x for x in entries if x[0] == cpuSegment.value]
            if len(entries) > 0:
                dict[cpuSegment.value] = entries
        return dict


    def isNewCpuID(self, cpuID):
        ret = True
        val = cpuID.upper().zfill(8)
        for k, v in self._columnDic.items():
            if k == CpuTableColumn.cpu_id:
                if val in v:
                    ret = False
                break
        return ret

    def isNewMcuFile(self, mcuFile):
        ret = True
        val = mcuFile.lower()
        for k, v in self._columnDic.items():
            if k == CpuTableColumn.mcu_file_name:
                if val in v:
                    ret = False
                break
        return ret

    def isNewCpuCodeName(self, cpuColdeName):
        ret = True
        val = cpuColdeName
        for k, v in self._columnDic.items():
            if k == CpuTableColumn.cpu_code_name:
                if val in v:
                    ret = False
                break
        return ret

    def isNewPlatformID(self, platformID):
        ret = True
        val = platformID.upper()
        for k, v in self._columnDic.items():
            if k == CpuTableColumn.platform_id:
                if val in v:
                    ret = False
                break
        return ret

    def LooupTableColumnValueByCpuId(self, cpuID, column):
        if column not in [x for x in ReadmeTableColumn]:
            raise BaseException('The column must be the the type of {}'.format(ReadmeTableColumn.__name__))
        results = self.__lookupAttributeByCpuId(cpuID, column)
        return results

    def InsertNewEntry(self, mcuRelease):
        paramDict = self.ValidateReadmeTableParameters(mcuRelease)
        return self.__insertNewEntry(paramDict[ReadmeTableColumn.CPUSegment],
                                     paramDict[ReadmeTableColumn.McuFileName],
                                     paramDict[ReadmeTableColumn.CPUCodeName],
                                     paramDict[ReadmeTableColumn.CPUCoreStepping],
                                     paramDict[ReadmeTableColumn.PlatformID],
                                     paramDict[ReadmeTableColumn.CPUID])

    def ValidateReadmeTableParameters(self, mcu):
        paramDict = {}
        cpuID = paramDict[ReadmeTableColumn.CPUID] = mcu['CpuID']
        paramDict[ReadmeTableColumn.PlatformID] = mcu['PlatformID'].strip()

        if paramDict[ReadmeTableColumn.CPUID] == '' \
                or paramDict[ReadmeTableColumn.PlatformID] == '':
            raise BaseException('The CPU ID and platform ID are required.')

        paramDict[ReadmeTableColumn.CPUCodeName] = mcu['CPUCodeName'].strip()
        if paramDict[ReadmeTableColumn.CPUCodeName] == '':
            paramDict[ReadmeTableColumn.CPUCodeName] \
                = self.LooupTableColumnValueByCpuId(cpuID, ReadmeTableColumn.CPUCodeName)

        paramDict[ReadmeTableColumn.CPUSegment] = mcu[Consts.CPU_SEGMENT].strip()
        if paramDict[ReadmeTableColumn.CPUSegment] == '':
            paramDict[ReadmeTableColumn.CPUSegment] \
                = self.LooupTableColumnValueByCpuId(cpuID, ReadmeTableColumn.CPUSegment)

        paramDict[ReadmeTableColumn.CPUCoreStepping] = mcu[Consts.STEPPING].strip()
        if paramDict[ReadmeTableColumn.CPUCoreStepping] == '':
            paramDict[ReadmeTableColumn.CPUCoreStepping] \
                = self.LooupTableColumnValueByCpuId(cpuID, ReadmeTableColumn.CPUCoreStepping)

        paramDict[ReadmeTableColumn.McuFileName] = mcu['MicroCode'].strip()
        if paramDict[ReadmeTableColumn.McuFileName] == '':
            mcu = mcu[Consts.MCU].lower()
            prefix = None
            for p in ['mu', 'm']:
                if mcu.startswith(p):
                    prefix = p
                    break
            if prefix is not None:
                paramDict[ReadmeTableColumn.McuFileName] = \
                    '{}{}{}'.format(prefix,
                                    paramDict[ReadmeTableColumn.PlatformID],
                                    re.sub('^0+', '', cpuID))
        if (paramDict[ReadmeTableColumn.CPUSegment] is None
                or paramDict[ReadmeTableColumn.CPUSegment] == ''
                or paramDict[ReadmeTableColumn.McuFileName] is None
                or paramDict[ReadmeTableColumn.McuFileName] == ''
                or paramDict[ReadmeTableColumn.CPUCodeName] is None
                or paramDict[ReadmeTableColumn.CPUCodeName] == ''
                or paramDict[ReadmeTableColumn.CPUCoreStepping] is None
                or paramDict[ReadmeTableColumn.CPUCoreStepping] == ''):
            raise NewCpuReleaseException('All parameters in [CpuSegment, Platform Id, Stepping, '
                                         'MicroCode file name, CPU code name] are required to insert '
                                         'a CPU id [{}] into README table'.format(cpuID))

        return paramDict

    def Save(self, path=None):
        savePath = self._location
        if path is not None:
            if not os.listdir(path):
                os.makedirs(path, exist_ok=True)
            savePath = '{}/README.md'.format(path)
        if savePath is not None:
            with open(savePath, 'w') as f:
                f.write('\n'.join(self._documentRows))
                for row in self._cpuTableRows:
                    if row[0].startswith('CPU Segment'):
                        f.write('\n')
                    f.write(str(row) + '\n')

    def SaveJson(self, path=None):
        folder = os.path.dirname(self._location)
        if path is not None:
            if not os.listdir(path):
                os.makedirs(path, exist_ok=True)
            folder = path
        savePath = '{}/README.json'.format(folder)
        if savePath is not None:
            with open(savePath, 'w') as f:
                f.write(self.ToJson)
                pass

    # ------------------ Private methods -------------------------

    def __lookupAttributeByCpuId(self, cpuId, colIndex):
        cpuid = cpuId.upper().zfill(8).upper()
        g = [x for x in self._cpuTableRows if x[5] == cpuid]
        if g is not None and len(g) > 0:
            return g[len(g) - 1][colIndex]  # take the value from the last one in group
        return None

    def __lookupAttributeByCpuIdInGroup(self, cpuId, group, colIndex):
        cpuid = cpuId.upper().zfill(8).upper()
        if not isinstance(group, tuple):
            raise BaseException('The input parameter group must be the tuple type.')
        colIndx = group[0]
        val = group[1].strip()
        g = [x for x in self._cpuTableRows if x[5] == cpuid and x[colIndx].strip() == val]
        if g is not None and len(g) > 0:
            return g[len(g) - 1][colIndex]
        return None

    def __insertNewEntry(self, cpusegment,
                         microcodFileName,
                         cpuCodeName,
                         cpuCoreStepping,
                         platmormId,
                         cpuID,
                         CpuPublicSpecUpdate = r'https://ark.intel.com/content/www/us/en/ark.html',
                         IntelProductSpec = r'https://ark.intel.com/content/www/us/en/ark.html',
                         CpuNdaSpecUpdate = r'https://ark.intel.com/content/www/us/en/ark.html',
                         ProcessorModel = 'N/A',
                         Products = 'N/A'):

        columns = [cpusegment,
                   microcodFileName,
                   cpuCodeName,
                   cpuCoreStepping,
                   platmormId,
                   cpuID,
                   '[Update]({})'.format(CpuPublicSpecUpdate),  # cpu_public_spec_update
                   '[Specs]({})'.format(IntelProductSpec),  # intel_product_spec
                   '[Update]({})'.format(CpuNdaSpecUpdate),  # cpu_nda_spec_update
                   ProcessorModel,  # processor_model
                   Products  # products
                   ]
        newRow = cpu_table_row()
        for column in columns:
            newRow.AddColumn(column, ignoreduplicate=True)

        dupchecheck = [x for x in self._cpuTableRows if self._matchTableRows(list(newRow), list(x), 8)]
        if len(dupchecheck) > 0:
            raise DuplicateCpuTableRowException('The entry [{}] already exists in README.md table'.format(str(newRow)))

        startSegment = False
        inserted = False
        tempTablerows = list()
        rowIndex = 0
        count = len(self._cpuTableRows)
        for row in self._cpuTableRows:
            if row[0] == newRow[0]:
                startSegment = True
            if startSegment:
                if row[0] != newRow[0]:
                    tempTablerows.append(newRow)
                    inserted = True
                    rowIndex += 1
                    startSegment = False
            tempTablerows.append(row)
            rowIndex += 1
        if not inserted and rowIndex == count:
            tempTablerows.append(newRow)
            rowIndex += 1
        self._cpuTableRows.clear()
        for x in tempTablerows:
            self._cpuTableRows.append(x)
        return str(newRow)

    def __getitem__(self, cpuid):
        cpuid = re.sub('^0+', '', cpuid.upper())
        return [x for x in self._cpuTableRows if x[5].upper().endswith(cpuid)]

    def __getitem__(self, cpuSegment):
        return [x for x in self._cpuTableRows if x[0] == cpuSegment.value]

    def __load(self, readmeLoadPath):
        self._documentRows.clear()
        self._cpuTableRows.clear()
        if os.path.isfile(readmeLoadPath):
            self._location = readmeLoadPath
            lineIndex = 0
            with open(readmeLoadPath, 'r') as f:
                lines = f.readlines()
                start = False
                for line in lines:
                    line = line.rstrip('\n')
                    if not start:
                        '''
                        # TODO : add additional columns -- un-comment the following code
                        if line.startswith('| CPU Segment | Microcode File Name | CPU Code Name |'):
                            headerRow = cpu_table_row()
                            for col in Consts.README_MD_COLUMNS:
                                headerRow.AddColumn(col)
                            line = '{}{}'.format(str(headerRow), '\n')
                        '''
                        self._documentRows.append(line)
                    if len(re.findall(r'\|', line)) >= 7:
                        split = [x.lstrip(' ').rstrip(' ') for x in line.rstrip('\n').split('|') if x.strip() != '']
                        if re.match(''.join(split[0:7]), ''.join(Consts.README_MD_COLUMNS[0:7])):
                            start = True
                            self._documentRows.remove(line)
                            self.__appendCpuTableRow(split)
                            lineIndex += 1
                            continue
                        if start:
                            skipcheck = len(re.findall(':---:', line)) >= 3
                            self.__appendCpuTableRow(split, skipcheck)
                            if not skipcheck:
                                for i in range(0, len(split)):
                                    col = self._columnDic[self._colums[i]]
                                    val = split[i].strip('\n')
                                    if val not in col:
                                        col[col.Count] = val
                    lineIndex += 1

    def __appendCpuTableRow(self, columns, ignoreduplicate=False):
        row = cpu_table_row()
        for col in columns:
            row.AddColumn(col, ignoreduplicate)
        self._cpuTableRows.append(row)

    def _matchTableRows(self, x, y, numberOfColumns):
        if not(isinstance(x, list) and isinstance(y, list)):
            raise BaseException('The input parameters x and y for match must be list type')
        return ''.join(x[0:numberOfColumns]).startswith(''.join(y[0:numberOfColumns]))

    def __createColumnInstance(self, key, *args, **kwargs):
        namespaces = list(['datamodel', 'readme_md', 'cpu_table_columns'])
        namespaces.append(key)
        q = queue.Queue()
        instance = None
        try:
            m = ''
            for x in namespaces:
                m += '{0}.'.format(x)
                q.put(x)

            m = m.rstrip('.')
            module = __import__(m)
            q.get_nowait()
            instance = getattr(util._extractAttr(module, q), key)(*args, **kwargs)
        except Exception as e:
            print('Exception caught at CreateInstance, error was :%s' % str(e))
        return instance

    # ------------------ End of Private methods -------------------------


# ------- Unit test ------------------
if __name__ == '__main__':
    from buildingblocks.automation_config import AutomationConfig
    readmeTemplate = os.path.realpath(r'../../../ReleaseAutomation/README_Template.md')
    doc = readme_document(readmeTemplate)
    n = doc.isNewCpuID('906EB')
    y = doc.isNewCpuID('906EBxxx')

    cpuId = '50654'
    stepping_x = doc.LookupCpuCoreSteppingByCpuId(cpuId)

    # json = doc.ToJson
    doc.SaveJson()
    dic = doc.CpuTableDictionary

    cpuId = '406f1'  # '806a1'  #
    entriesDictionary = doc.EntriesDictionaryByCpuId(cpuId)
    entries = doc.EntriesCpuIdAndCpuSegment(cpuId, CpuSegment.SERVER.value)

    path = os.path.realpath(r'../../../ReleaseAutomation/ReleaseDropBox/SOC')

    # test case : new/obsolete CPUID
    for source in [s for s in os.listdir(path) if s.endswith('.inc')]:
        f = os.path.realpath('{}/{}'.format(path, source))
        # fx = os.path.realpath('{}/{}'.format(path, source))
        # f = os.path.realpath('{}/{}'.format(path, source.replace('TXT', 'inc')))
        # os.rename(fx, f)
        try:
            mcuHeaderInfo = McuHeaderInfo(f)
            if not doc.isNewCpuID(mcuHeaderInfo.CpuId):
                os.remove(f)
        except Exception as e:
            print(str(e))
        pass
    pass

    # test cases : insert rows
    jsonConfigPath = os.path.realpath(r'../../../ReleaseAutomation/McuReleaseRequest.json')
    requestConfig = AutomationConfig(jsonConfigPath)
    mcu = requestConfig.ReleaseLees[0][Consts.MCUS][0]
    path = os.path.realpath(r'../../../ReleaseAutomation/ReleaseDropBox/UnittestData')
    sources = [s for s in os.listdir(path) if s.endswith('.inc')]

    # test cases : insert rows -- 1. without any input except to the  mcu,
    # expect no exception thrown due to filter out the new/obsolete CPIUD
    idx = 0
    tablerowcount = doc.CpuTableRowCount
    for source in sources:
        mcupath = os.path.realpath('{}/{}'.format(path, source))
        mcuheader = McuHeaderInfo(mcupath)
        mcu['CpuID'] = mcuheader.CpuId
        if not doc.isNewCpuID(mcuheader.CpuId):
            try:
                newRow = doc.InsertNewEntry(mcu)
                idx += 1
            except DuplicateCpuTableRowException as e:
                print(str(e))
    with open(r'D:/temp/ReadmeTest_normal.md', 'w') as f:
        f.write('\n'.join(doc._documentRows))
        for row in doc._cpuTableRows:
            if row[0].startswith('CPU Segment'):
                f.write('\n')
            f.write(str(row) + '\n')
    assert doc.CpuTableRowCount == tablerowcount + idx

    # test cases : insert rows -- 2. for new new/obsolete CPUID, without any input except to the  mcu,
    # expect 0 row been inserted and exceptions been thrown
    doc = readme_document(readmeTemplate)
    for source in sources:
        mcupath = os.path.realpath('{}/{}'.format(path, source))
        try:
            mcuheader = McuHeaderInfo(mcupath)
            mcu['CpuID'] = mcuheader.CpuId
            if doc.isNewCpuID(mcuheader.CpuId):
                newRow = doc.InsertNewEntry(mcu)
        except DuplicateCpuTableRowException as e:
            print(str(e))
        except BaseException as bx:
            print(str(bx))
        except Exception as ex:
            print(str(ex))
    assert doc.CpuTableRowCount == tablerowcount + 0

    # test cases : insert rows -- 3. for new new/obsolete CPUID, manually added the parameters
    doc = readme_document(readmeTemplate)
    idx = 0
    for source in sources:
        mcupath = os.path.realpath('{}/{}'.format(path, source))
        mcuheader = McuHeaderInfo(mcupath)
        mcu['CpuID'] = mcuheader.CpuId
        if doc.isNewCpuID(mcuheader.CpuId):
            mcu['CpuSegment'] = 'PlaseHoder'
            mcu['PlatformID'] = 'PlaseHoder'
            mcu['Stepping'] = 'PlaseHoder'
            mcu['MicroCode'] = 'PlaseHoder'
            mcu['CPUCodeName'] = 'PlaseHoder'
            try:
                newRow = doc.InsertNewEntry(mcu)
                idx += 1
            except DuplicateCpuTableRowException as e:
                print(str(e))
    assert doc.CpuTableRowCount == tablerowcount + idx
    with open(r'D:/temp/ReadmeTest_newcpu.md', 'w') as f:
        f.write('\n'.join(doc._documentRows))
        for row in doc._cpuTableRows:
            if row[0].startswith('CPU Segment'):
                f.write('\n')
            f.write(str(row) + '\n')


    # test cases : insert rows -- 4. to exclude duplicate insert
    doc = readme_document(readmeTemplate)
    insertcount = 0
    newRow = None
    for source in sources:
        mcupath = os.path.realpath('{}/{}'.format(path, source))
        mcuheader = McuHeaderInfo(mcupath)
        mcu['CpuID'] = mcuheader.CpuId
        if not doc.isNewCpuID(mcuheader.CpuId):
            for i in range(0, 3):
                try:
                    newRow = doc.InsertNewEntry(mcu)
                    insertcount += 1
                except DuplicateCpuTableRowException as ex:
                    print('Duplicate exception caught, error = {}'.format(str(ex)))
        break
    assert newRow is not None
    assert insertcount == 1
    pass
