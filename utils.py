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

def getListOfFiles(dirName, reg):
    # create a list of file and sub directories
    # names in the given directory
    try:
        exp = re.compile(reg)
    except:
        print("Error -- Invalid regular expression:" + reg)
        sys.exit(0)
    try:
        listOfFile = os.listdir(dirName)
    except:
        print("Error -- Unable to find directory --> " + dirName)
        return []
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

def getRegularExpressionD(dict):
    fileType = "junk"
    if dict["dslog"]:
        fileType = "dslog"
    if dict["dsevents"]:
        fileType = "dsevents"
    if dict["dslog"] and dict["dsevents"]:
        fileType = ""
    return getRegularExpression(dict["year"], dict["month"], dict["day"], True, True, fileType)
        

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
    
def processFiles(argv, fileType):
    exp = getRegularExpression(
        flags.year, flags.month, flags.day, flags.monthParm, flags.dayParm, fileType)
    files = getListOfFiles(flags.path, exp)
    print("Start argv:%s RegExp:%s Found %d Files" % (argv, exp,  len(files)))
    processListOfFiles(files)


def processListOfFiles(files):
    totalCount = 0
    fileCount = 0
    for file in files:
        fileCount += 1
        if "dsevents" in file:
            p = parseDSEvents.parseFile(file)
            totalCount += p.lineCount
        elif "dslog" in file:
            p = parseDSLogs.parseFile(file)
            totalCount += p.lineCount
        else:
            print("Error can't process file:", file)
    print("%8d lines processed in %d files" % (totalCount, fileCount))


def deleteCSVs():
    # Delete previous csv file for Logs
    if flags.makeCSVEvents:
        try:
            os.remove(flags.CSVEventsFile)
        except:
            s = "Error -- Unable to open file %s for writing -- is the file %s open in another program like excel"
            print(s % (flags.CSVEventsFile, flags.CSVEventsFile))
            sys.exit(0)
    if flags.makeCSVLog:
        try:
            os.remove(flags.CSVLogFile)
        except:
            s = "Error -- Unable to open file %s for writing -- is the file %s open in another program like excel"
            print(s % (flags.CSVLogFile, flags.CSVLogFile))
            sys.exit(0)


def toDec4(self, d, start):
        return d[start+2] * 256 + d[start+3] + (d[start] * 256 + d[start+1]) * 256

def toDec2(self, d, start):
        return d[start] * 256 + d[start+1]
