import os
import re
import sys
import datetime
import flags
import parseDSEvents
import parseDSLogs


def doAllDSEvents(path, fileType):
    totalCount = 0
    fileCount = 0
    for file in os.listdir(path):
        if fileType in file:
            fileCount += 1
            if fileType == "dsevents":
                p = parseDSEvents.parseFile(path + '\\' + file)
            if fileType == "dslogs":
                p = parseDSLogs.parseFile(path + '\\' + file)
            totalCount += p.lineCount
    print("Total %d lines in %d files" % (totalCount, fileCount))


def doFiles(files, fileType):
    totalCount = 0
    fileCount = 0
    for file in files:
        fileCount += 1
        if fileType == "dsevents":
            p = parseDSEvents.parseFile(file)
        if fileType == "dslog":
            p = parseDSLogs.parseFile(file)
        totalCount += p.lineCount
    print("%6d lines found in %d files" % (totalCount-1, fileCount))


def getFileInfo(fileName, startLine):
    # startLine = "Robot Type Competition Started compiled:03/08/2020 20:06:49 version:0.7"
    exp = ".*Robot Type (.*) Started compiled:(.*) version:(.*)"
    result = re.match(exp, startLine)
    if(result):
        flags.robotType = result.group(1)
        flags.compiled = datetime.datetime.strptime(
            result.group(2), '%m/%d/%Y %H:%M:%S')
        flags.version = result.group(3)
        if flags.debug:
            print("Type:%s Compiled:%s Version:%s" %
                  (flags.robotType, flags.compiled, flags.version))


def getListOfFiles(dirName, reg):
    # create a list of file and sub directories
    # names in the given directory
    try:
        exp = re.compile(reg)
    except:
        print("Error -- Invalid or no paramters entered")
        sys.exit(0)
    try:
        listOfFile = os.listdir(dirName)
    except:
        print("Error -- Unable to find directory --> " + dirName)
        sys.exit(0)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath, reg)
        else:
            if(exp.match(fullPath)):
                allFiles.append(fullPath)
    return allFiles


def getRegularExpression(year, month, day, monthEntered, dayEntered, fileType):
    ar = day.split('-')
    dayLow = int(ar[0])
    dayHigh = dayLow
    if(len(ar) == 2):
        dayHigh = int(ar[1])
    if len(month) == 1:
        month = "0" + month
    # ".*2020_03_(10|09).*dsevents"
    if dayEntered:
        exp = ".*" + year + "_" + month + "_("
        for day in range(dayLow, dayHigh + 1):
            # print("Year:%s Month:%s Day:%s" % (year, month, day))
            day = str(day)
            if len(day) == 1:
                day = "0" + day
            exp += day + "|"
        exp = exp[:-1] + ").*" + fileType
        return exp
    else:
        if monthEntered:
            exp = ".*" + year + "_" + month + ".*" + fileType
            return exp
    exp = ".*" + year + ".*" + fileType
    return exp


def NationalInstrumentDateToString(seconds):
    # Get base time for National Instrutments software
    dt = datetime.datetime(1904, 1, 1, 0, 0, 0,   tzinfo=datetime.timezone.utc)
    # Make the time reflect EST instead utc
    dt += datetime.timedelta(seconds=(-5 * 3600))
    # Adjust time for Time in the file
    dt += datetime.timedelta(seconds=(seconds))
    return dt.strftime("%m/%d %H:%M:%S")

def dump(hdr, length):
    s = ""
    for i in range(0, length):
        s += "%x " % (hdr[i])
    print(s)