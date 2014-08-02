#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2014, katonori All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without modification, are
# permitted provided that the following conditions are met:
# 
#   1. Redistributions of source code must retain the above copyright notice, this list
#      of conditions and the following disclaimer.
#   2. Redistributions in binary form must reproduce the above copyright notice, this
#      list of conditions and the following disclaimer in the documentation and/or other
#      materials provided with the distribution.
#   3. Neither the name of the katonori nor the names of its contributors may be used to
#      endorse or promote products derived from this software without specific prior
#      written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
# OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT
# SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
# TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
# BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH
# DAMAGE.

import sys
import re
import os
import tempfile

#gDebugMode = 1
gDebugMode = 0

def DEBUG_PRINT(msg):
    global gDebugMode
    if gDebugMode != 0:
        print msg

def WinDirname(str):
    m = re.search(r"\"(.+\\)([^\\]+)\"", str)
    if m:
        return (m.group(1), m.group(2))
    return None

def ParseErrorLog(lines, pattern):
    errorPatter = pattern
    curDir = u"";
    errorList = []
    linesStr = "".join(lines)
    mList = re.finditer(pattern, linesStr, re.MULTILINE)
    for m in mList:
        # dirname
        try:
            dirname = m.group("dir")
            if dirname != None:
                curDir = dirname + os.path.sep
                continue
        except IndexError: 
            None
        # filename
        try:
            filename = m.group("file")
            if not os.path.isabs(filename):
                filename = curDir + filename
        except IndexError: 
            filename = ""
        # line number
        try:
            lineNo = m.group("line")
        except IndexError: 
            lineNo = ""
        # error message
        try:
            errorMsg = m.group("msg")
        except IndexError: 
            errorMsg = ""
        errorMsg = errorMsg.replace("\n", "|")
        errorList.append((filename, lineNo, errorMsg))
    result = []
    for i in errorList:
        fn, lineNo, msg = i
        msg = u"%s:%s:%s"%(fn, lineNo, msg.decode("utf-8"))
        #print msg.encode("utf-8")
        result.append(msg.encode("utf-8"))
    return result

def ParseErrorLogFromFile(infile, pattern):
    f = open(infile, "r")
    return ParseErrorLog(f.readlines(), pattern)

if __name__ == "__main__":
    pattern = '^\s*File\s+"(?P<file>.+)", line (?P<line>[0-9]+), in .+$\s+(?P<msg>.+\n\S+.+|.+$)'
    #pattern = "(?P<file>.+):(?P<line>[0-9]+):(?P<msg>.+$)|make.+Entering directory [`'](?P<dir>.+)'"
    #pattern = "(?P<file>.+):(?P<line>[0-9]+):(?P<msg>.+$)|make.+Entering directory [`'](?P<dir>.+)'"
    #pattern = '[0-9]+>(?P<file>.+)\((?P<line>[0-9]+)(,[0-9]+)?\):(?P<msg>.+$)'
    if len(sys.argv) != 2:
        print "usage: cmd file"
        sys.exit(1)
    fn = sys.argv[1]
    for l in ParseErrorLogFromFile(fn, pattern):
        print l
