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
#
# Author : Haller, Nathaniel D, nathaniel.d.haller@intel.com
#          Li, Henry, henry.li@intel.com
#-------------- -----------------------------------------------------------------
from datamodel.definitions import Consts
import buildingblocks.utils as util
import os
import re
import struct


class McuHeaderInfo(object):
    def __init__(self, source):
        self._isValicMCU = True
        self._cpuIds = list()
        self._platformID = None
        self._patchId = None
        self._isDebugOnlyRelease = False
        self._filename = None
        self._parseMcuError = list()
        self._parse(source)

    @property
    def IsValidMCU(self):
        return self._isValicMCU

    @property
    def ParseError(self):
        if len(self._parseMcuError) > 0:
            return '\n'.join(self._parseMcuError)
        else:
            return None

    @property
    def CpuId(self):
        if len(self._cpuIds) > 0:
            # If there are multiple CPU ID been parsed out, select the advanced version
            # return self._cpuIds[0].zfill(8).upper()
            return self._cpuIds[len(self._cpuIds) - 1].zfill(8).upper()
        else:
            return None

    @property
    def CpuIds(self):
        formatedCpuIds = list()
        for cpuid in self._cpuIds:
            formatedCpuIds.append(cpuid.zfill(8).upper())
        return formatedCpuIds

    @property
    def PlatformID(self):
        platformID = Consts.UNANNOUNCED  # 'Unannounced'
        if self._platformID is not None and self._platformID != 0:
            platformID = util.Int2HexString(self._platformID, False).zfill(2)
        return platformID

    @property
    def PatchId(self):
        if self._patchId is not None:
            return util.Int2HexString(self._patchId, False).zfill(2)
        return None

    @property
    def IsDebugOnlyRelease(self):
        return self._isDebugOnlyRelease

    @property
    def ParseError(self):
        if len(self._cpuIds) == 0:  # is None:
            self._parseMcuError.append('Failed to parse the CPU ID from mcu header [{}]'.format(self._filename))
        if len(self._parseMcuError) == 0:
            return None
        return '\n'.join(self._parseMcuError)

    def _parse(self, source):
        buffer = list()
        headrPatternFormat = r'((\s+)?dd\s+([a-fA-F0-9]{9}h)\s+)'
        lineIndex = 0
        if os.path.isfile(source):

            self._filename = os.path.basename(source).lower()
            with open(source, 'r') as f:
                lines = f.readlines()
                for line in lines:
                    lstripped = line.rstrip('\n').strip()
                    if lstripped != '' and not(lstripped.strip().startswith(';') or lstripped.startswith('dd')):
                        self._parseMcuError.append('The MCU file [{}] is invalid.  The valid line  should be in the '
                                                   'format of [an empty line, a line starts with ";") or "dd"].'
                                                   'Please verify the contents of MCU.'.format(self._filename))
                        self._isValicMCU  = False
                        break
                    s = line.split(';')[0]
                    if re.match(headrPatternFormat, s):
                        s = s.replace('dd', '').replace('h', '').strip()
                        binary = struct.pack('<I', int(s, 16))
                        buffer.append(binary)
                        lineIndex += 1
                        if lineIndex == 2:
                            pos_2 = s[1]
                            if pos_2 == '8':
                                self._isDebugOnlyRelease = True
                if self._isValicMCU :
                    remainder = lineIndex % 4
                    if remainder > 0:  # patch if the total size if not 16 byte aligned.
                        for x in range(4 - remainder):
                            buffer.append(struct.pack('<I', 0))

                    headerContents = self._retrieveHeaderContent(buffer, 0, 9)
                    self._patchId = headerContents[1]
                    if headerContents[3] != 0:
                        self._cpuIds.append(util.Int2HexString(headerContents[3], False))
                    self._platformID = headerContents[6]
                    dataSize = headerContents[7]
                    totalSize = headerContents[8]
                    if dataSize == 0:
                        if totalSize != 0:
                            self._parseMcuError.append('Unsupported MCU header with data size = [{}] '
                                                       'and total size = [{}] has been found '
                                                       'from MCU [{}]'.format(dataSize,
                                                                              totalSize,
                                                                              source))
                        else:
                            dataSize = 2000
                            totalSize = 2048
                    if len(self._parseMcuError) == 0:
                        extendSignatureCount = 0
                        extendSignatureSize = totalSize - dataSize - 48
                        if extendSignatureSize < 0:
                            self.ParseError.append('Unsupported MCU header with extend signature size  = [{}] has '
                                                   'been caught from MCU file [{}]'.format(extendSignatureSize, source))
                        if len(self._parseMcuError) == 0:
                            if extendSignatureSize > 0:
                                if extendSignatureSize < 20:
                                    self.ParseError.append(
                                        'Unsupported MCU header with extend signature size  = [{}], that is too small'
                                        ' has been caught from MCU file [{}]'.format(extendSignatureSize, source))
                                else:
                                    extendSignatureCount = self._hex2DwordConverter(
                                        buffer[int((totalSize - extendSignatureSize)/4)])
                                if extendSignatureSize != 20 + extendSignatureCount * 12:
                                    self.ParseError.append(
                                        'Unsupported MCU header,with invalid External Signature Table size'
                                        ' has been caught from MCU file [{}]'.format(source))
                                if len(self._parseMcuError) == 0:
                                    error = self._verifyCheckSum(buffer, totalSize - extendSignatureSize, totalSize)
                                    if error is not None:
                                        self.ParseError.append('Unsupportable MCU header. Failed to verify checksum,'
                                                               'External Signature Table checksum not valid.')
                                    if len(self._parseMcuError) == 0:
                                        for i in range(0, extendSignatureCount):
                                            index = int((totalSize - extendSignatureSize + 20 + (12 * i))/4)
                                            headerContents = self._retrieveHeaderContent(buffer, index, 3)
                                            if headerContents[0] != 0:
                                                cpuid = util.Int2HexString(headerContents[0], False)
                                                if cpuid not in self._cpuIds:
                                                    self._cpuIds.append(cpuid)
                                    error = self._verifyCheckSum(buffer, 0, totalSize)
                                    if error is not None:
                                        self.ParseError.append('Unsupportable MCU header, header checksum is invalid.')
        else:
            self._parseMcuError.append('Cannot find the mcu file [{}]'.format(source))

    ###########################################
    # 0 :  Header Version
    # 1 :  Revision ID
    # 2 :  Date
    # 3 :  CPUID
    # 4 :  Checksum
    # 5 :  Load Revision
    # 6 :  Platform ID
    # 7 :  Data Size
    # 8 :  Total Size
    #############################################
    def _retrieveHeaderContent(self, buffer, index, count):
        contents = list()
        for i in range(0, count):
            contents.append(self._hex2DwordConverter(buffer[index + i]))
        return contents

    def _hex2DwordConverter(self, hexInput):
        hexInputTuple = struct.unpack(r'<BBBB', hexInput)
        hexInputUINT = hexInputTuple[0] + (hexInputTuple[1] << 8) + (hexInputTuple[2] << 16) + (hexInputTuple[3] << 24)
        return hexInputUINT

    def _verifyCheckSum(self, buffer, start, end):
        if (end - start) % 4 != 0:
            return 'Failed to verify checksum, Microcode is not dword aligned.'
        checksum_remainder = 0x00000000
        for idx in range(start, end, 4):
            checksum_remainder + self._hex2DwordConverter(buffer[int(idx/4)])
            if checksum_remainder > 0xFFFFFFFF:
                checksum_remainder = checksum_remainder - 0x100000000
        # If the checksum was correctly implemented, checksum_remainder
        # should be zero by the end of walking through the data.
        if checksum_remainder == 0x00000000:
            return None
        return 'Invalid checksum found, remainder = [{}]'.format(checksum_remainder)

''' ------- Unit test ------------------'''
if __name__ == '__main__':
    from datamodel.McuHeaderInfo import McuHeaderInfo
    for source in ['bu26.inc',
                   'm_c0_706e1_0000001e.inc',
                   'm_01_506c2_0000000e.inc',
                   'B_32_633.inc'
                   ]:
        mcusource = os.path.realpath(r'../ReleaseDropBox/' + source)
        if os.path.isfile(mcusource):
            mcuHeaderInfo = McuHeaderInfo(mcusource)
            cpuID = mcuHeaderInfo.CpuId
            platformID = mcuHeaderInfo.PlatformID
            patchID = mcuHeaderInfo.PatchId
            pass
pass

