#!/usr/bin/env python
# INTEL CONFIDENTIAL
#
# copyright 2018-2019 Intel Corporation.
#
# This software and the related documents are Intel copyrighted materials, and your use of them is governed by the express license under which they were provided to you (License). Unless the License provides otherwise, you may not use, modify, copy, publish, distribute, disclose or transmit this software or the related documents without Intel's prior written permission.
#
# This software and the related documents are provided as is, with no express or implied warranties, other than those that are expressly stated in the License.
#
#

"""
 inf_build.py 

 INTEL CONFIDENTIAL
 copyright 2018-2019 Intel Corporation

"""


from __future__ import print_function
import sys
import os
import subprocess


def _recursive_subprocess(inf_list, microcodeconverter_tool_path):
    if microcodeconverter_tool_path == None: 
        print("ERROR: no microcodeconverter_tool_path provided")
        return

    if inf_list == list():
        return
    arg_list = list()
    arg_list.append("python")
    arg_list.append(microcodeconverter_tool_path)
    arg_list.append(inf_list.pop())
    print(" calling subprocess: ", arg_list)
    new_process = subprocess.Popen(arg_list,
            stdout=None,
            stderr=None,
            shell=False,
            universal_newlines=True)
    # start the next subprocess running, then wait for the current subprocess to complete.
    _recursive_subprocess(inf_list, microcodeconverter_tool_path)
    new_process.wait()

def _locate_microcodeconverter():
    # TODO: The relative path to the MicrocodeConverter.py tool may require updating if directory structure changes. 
    microcodeconverter_tool_path = "./Tools/MicrocodeConverter/MicrocodeConverter.py"
    if os.path.isfile(os.path.join(sys.path[0], microcodeconverter_tool_path)) == False:
        microcodeconverter_tool_path = "../Tools/MicrocodeConverter/MicrocodeConverter.py"
    if os.path.isfile(os.path.join(sys.path[0], microcodeconverter_tool_path)) == False:
        microcodeconverter_tool_path = "../../Tools/MicrocodeConverter/MicrocodeConverter.py"
    if os.path.isfile(os.path.join(sys.path[0], microcodeconverter_tool_path)) == False:
        microcodeconverter_tool_path = "../../../Tools/MicrocodeConverter/MicrocodeConverter.py"
    if os.path.isfile(os.path.join(sys.path[0], microcodeconverter_tool_path)) == False:
        microcodeconverter_tool_path = "../../../../Tools/MicrocodeConverter/MicrocodeConverter.py"
    if os.path.isfile(os.path.join(sys.path[0], microcodeconverter_tool_path)) == False:
        print("ERROR: Could not locate Tools/MicrocodeConverter/MicrocodeConverter.py")
        return None
    microcodeconverter_tool_path = os.path.join(sys.path[0], microcodeconverter_tool_path)
    print("MicrocodeConverter Tool Path: ", microcodeconverter_tool_path)
    return microcodeconverter_tool_path

def autorun_microcodeconverter():
    """Autorun MicrocodeConverter.py on every local INF file. 

    Shortcut script to automate processing every microcode list INF file in
    the directory of this shortcut build script. 

    """

    microcodeconverter_tool_path = _locate_microcodeconverter()
    if microcodeconverter_tool_path == None:
            sys.exit(1)

    inf_file_list = list()
    casesensitive_filenames = os.listdir(sys.path[0])
    for filename in casesensitive_filenames:
        try:
            if ".inf" == os.path.splitext(filename)[1].lower():
                filename = os.path.join(sys.path[0], filename)
                inf_file_list.append(filename)
                print("Marked for processing: ", filename)
                continue
            print("Skip: ", filename)
        except:
            print("Exception Skip: ", filename)
            continue
    _recursive_subprocess(inf_file_list, microcodeconverter_tool_path)
    return

if __name__ == "__main__":
    if sys.version_info < (2, 7):
        print ("System python version detected less than Python 2.7.  Python 2.7 or Python 3.x support only. Exiting. ")
        sys.exit(1)
    if sys.version_info < (3, 0):
        print ("System python version detected Python 2.  Python 3 or later recommended for faster tool performance. ")
    autorun_microcodeconverter()

