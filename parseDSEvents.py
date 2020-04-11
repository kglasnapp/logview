import datetime
import os
import re
import sys

from db import db
import flags

class parseDSEvents:
    lineCount = 0
    fileName = ''
    fileNum = 0
    csvFileID = None

    def __init__(self, file):
        self.fileName = os.path.basename(file)
        self.lineCount = 0
        self.myMakeDB = flags.makeDB
        if '.dsevents' not in self.fileName or len(self.fileName.split(' ')) != 3:
            print("Attempted to process invalid file: " + self.fileName)
            return
        if flags.debug:
            print("Parse file:" + self.fileName)
        self.csvFileID = None
        if flags.CSVEventsFile != "":
            try:
                self.csvFileID = open(flags.CSVEventsFile, "a")
            except:
                s = "Error -- Unable to open file %s for writing -- is the file %s open in another program"
                print(s % (flags.CSVEventsFile, flags.CSVEventsFile))
                sys.exit(2)
            if os.path.getsize(flags.CSVEventsFile) == 0:
                # Write Header for the csv file
                self.csvFileID.write(
                    "Count,LineDate,DeltaTime,LineType,Data,FileName\n")
        stream = open(file, 'rb')
        ar = os.path.basename(file).split()
        if(len(ar) != 3):
            print("***************** Invalid file name " + os.path.basename(file))
            return
        fileDate = datetime.datetime.strptime(
            ar[0] + ar[1], "%Y_%m_%d%H_%M_%S")
        hdr = stream.read(20)
        # Return if hit end of file
        if len(hdr) == 0:
            return
        startSec = self.read_timestamp(hdr, 8)
        if flags.debug:
            print("Parse file: " + file + " date:" +
                  str(fileDate) + " StartSec:" + str(startSec))
        if(self.myMakeDB):
            if db.isFileInDB(file):  
                print("File %s is in the DB,  will not update the DB" % (file))
                self.myMakeDB = False
            else:
                self.fileNum = db.addFileData(
                    file, startSec, 0, flags.robotType, flags.compiled, flags.version)
            db.table = flags.eventsTable 
        if(self.myMakeDB or self.csvFileID):
            self.loopOverFile(stream, fileDate, startSec)
        if self.lineCount > 0:
            print("%8d events in file:%s Robot Type:%s Software Compiled:%s Version: %s" %
              (self.lineCount, file, flags.robotType, flags.compiled, flags.version))
        if(self.csvFileID):
            self.csvFileID.close()
        if self.myMakeDB:
            db.addFileData(file, fileDate, self.lineCount,
                              flags.robotType, flags.compiled, flags.version)
            db.connection.commit()
            
    def loopOverFile(self, stream, fileDate, startSec):
        lastSec = 0
        while True:
            hdr = stream.read(20)
            if len(hdr) == 0:
                break
            milli = hdr[8] * 4
            sec = self.toDec4(hdr, 4) + milli / 1000
            t = self.read_timestamp(hdr, 4) - startSec
            lineDate = fileDate + datetime.timedelta(seconds=(t))
            lineLength = self.toDec4(hdr, 16)
            if flags.debug:
                print("Line:" + str(self.lineCount) + " {:%m/%d %H:%M:%S.%f}".format(
                    lineDate)[0:-3] + " dSec:" + str(round((sec - lastSec), 4)))
            x = stream.read(lineLength)
            self.parseLine(x, lineDate)
            lastSec = sec

    def toDec4(self, d, start):
        return d[start+2] * 256 + d[start+3] + (d[start] * 256 + d[start+1]) * 256

    def toDec2(self, d, start):
        return d[start] * 256 + d[start+1]

    def read_timestamp(self, hdr, start):
        sec = self.toDec4(hdr, start)
        milli = hdr[start+4] * 4
        sec += milli / 1000
        return sec

    def parseLine(self, x, lineDate):
        # Take front and back characters off of the string
        x = str(x)[2:-2]
        # Get each of the elements for a tag line
        ar = x.split('<TagVersion>')
        typePattern = re.compile(r'\[.*?\]')
        ar.sort()
        deltaTime = ''
        if (len(ar) > 0):
            for l in ar:
                if len(l) > 0:
                    l = re.sub(r'^1 <time>.*<message> ',  '', l)
                    l = re.sub(r'^1 <time>.*<details> ',  '', l)
                    l = re.sub(r'^Warning at.*\): ',  '', l)
                    deltaTime = ""
                    lineType = typePattern.match(l)
                    if(lineType != None):
                        lineType = lineType.group()[1:-1].replace(' ', '')
                        if l[8:9].isnumeric():
                            elementDate = datetime.datetime.strptime("{:%y_%m_%d}".format(
                                lineDate) + " " + l[8:20], '%y_%m_%d %H:%M:%S.%f')
                        else:
                            elementDate = lineDate
                        deltaTime = str(
                            (elementDate - lineDate).total_seconds())
                    else:
                        lineType = "Message"
                    if flags.showLogs:
                        d = "{:%m/%d}".format(lineDate)
                        print(d + "** " + l)
                    self.getFileInfo(self.fileName, l)
                    self.lineCount += 1
                    if self.myMakeDB:
                        db.addEventData(lineDate, deltaTime,
                                           lineType, l, self.fileNum, self.fileName)
                    if(self.csvFileID):
                        self.csvFileID.write('%d,"\t%s",%d,%s,"%s",%s\n' % (
                            self.lineCount, lineDate, 0, lineType, l, self.fileName))

    def getFileInfo(self, fileName, startLine):
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



def parseFile(file):
    return parseDSEvents(file)
