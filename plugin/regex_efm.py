#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
#pattern= (r"1>(.+)\(([0-9]+)\):(.+$)", [1, 2, 3], r"\"(.+vcxproj)\"")
#pattern= (r"1>(.+)\(([0-9]+)\):(.+$)", [1, 2, 3], r"")
#pattern= (r"(.+):([0-9]+):(.+$)", [1, 2, 3], r"make: Entering directory '(.+)'")
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
