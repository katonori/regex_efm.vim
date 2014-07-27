#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import re
import os
import tempfile

#pattern= (r"1>(.+)\(([0-9]+)\):(.+$)", [1, 2, 3], r"\"(.+vcxproj)\"")
#pattern= (r"1>(.+)\(([0-9]+)\):(.+$)", [1, 2, 3], r"")
#pattern= (r"(.+):([0-9]+):(.+$)", [1, 2, 3], r"make: Entering directory '(.+)'")

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

def ParseErrorLog(infile, pattern, order, dir_pattern):
    #errorPatter, patternOrder, dirCapture = pattern
    errorPatter, patternOrder, dirCapture = (pattern, order, dir_pattern)
    projdir = u"";
    errorList = []
    f = open(infile, "r")
    for line in f.readlines():
        if dirCapture != "":
            m = re.search(dirCapture, line)
            if m:
                projdir = m.group(1) + os.path.sep
                #projdir = WinDirname(line)
                DEBUG_PRINT("curDir: " + projdir)
                continue
        # parse error massage
        m = re.search(errorPatter, line)
        if m:
            filename = m.group(int(patternOrder[0]))
            lineNo = m.group(int(patternOrder[1]))
            errorMsg = m.group(int(patternOrder[2]))
            errorList.append((projdir+filename, lineNo, errorMsg))
            continue
    lines = []
    for i in errorList:
        fn, lineNo, msg = i
        msg = u"%s:%s:%s"%(fn, lineNo, msg.decode("utf-8"))
        #print msg.encode("utf-8")
        lines.append(msg.encode("utf-8"))
    return lines

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "usage: cmd file"
        sys.exit(1)
    fn = sys.argv[1]
    lines = ParseErrorLog(fn)
    for l in lines:
        print l
