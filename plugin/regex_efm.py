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

def ParseErrorLog(lines, pattern, order, dir_pattern):
    #errorPatter, patternOrder, dirCapture = pattern
    errorPatter, patternOrder, dirCapture = (pattern, order, dir_pattern)
    projdir = u"";
    errorList = []
    if dirCapture != "":
        for l in lines:
            m = re.search(dirCapture, l)
            if m:
                projdir = m.group(1) + os.path.sep
                #projdir = WinDirname(l)
                DEBUG_PRINT("curDir: " + projdir)
                continue
            # parse error massage
            m = re.search(errorPatter, l)
            if m:
                filename = m.group(int(patternOrder[0]))
                lineNo = m.group(int(patternOrder[1]))
                errorMsg = m.group(int(patternOrder[2]))
                if not os.path.isabs(filename):
                    filename = projdir + filename
                errorList.append((filename, lineNo, errorMsg))
                continue
    else:
        linesStr = "".join(lines)
        mList = re.findall(pattern, linesStr, re.MULTILINE)
        for m in mList:
            filename = m[int(patternOrder[0])-1]
            lineNo = m[int(patternOrder[1])-1]
            errorMsg = m[int(patternOrder[2])-1]
            errorMsg = errorMsg.replace("\n", "|")
            if not os.path.isabs(filename):
                filename = projdir + filename
            errorList.append((filename, lineNo, errorMsg))
    result = []
    for i in errorList:
        fn, lineNo, msg = i
        msg = u"%s:%s:%s"%(fn, lineNo, msg.decode("utf-8"))
        #print msg.encode("utf-8")
        result.append(msg.encode("utf-8"))
    return result

def ParseErrorLogFromFile(infile, pattern, order, dir_pattern):
    f = open(infile, "r")
    return ParseErrorLog(f.readlines(), pattern, order, dir_pattern)

if __name__ == "__main__":
#pattern= (r"1>(.+)\(([0-9]+)\):(.+$)", [1, 2, 3], r"\"(.+vcxproj)\"")
#pattern= (r"1>(.+)\(([0-9]+)\):(.+$)", [1, 2, 3], r"")
#pattern= (r"(.+):([0-9]+):(.+$)", [1, 2, 3], r"make: Entering directory '(.+)'")
    pattern = ('^\s*File\s+"(.+)", line ([0-9]+), in .+$\s+(.+\n\S+.+|.+$)', [1, 2, 3], '')

    if len(sys.argv) != 2:
        print "usage: cmd file"
        sys.exit(1)
    fn = sys.argv[1]
    ParseErrorLogFromFile(fn, pattern[0], pattern[1], pattern[2])
