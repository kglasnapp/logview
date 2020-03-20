import os
import re
import datetime
import db
import struct
import flags
import bitstring
import sys
import utils
import main


class parseDSEvents:
    lineCount = 0
    fileName = ''
    fileNum = 0
    csvFileID = None

    def __init__(self, file):
        table = os.path.basename(file)
        self.fileName = table
        if flags.debug:
            print("Parse file:" + table)
        table = "Logs_" + table.split(' ')[0] + "_" + table.split(' ')[1]
        if flags.makeDB and not flags.allInOne:
            print("Make table in DB for: " + table)
            db.db.dropTable(table)
            db.db.createLogDataTable(table)
            db.db.createConnection('files')
        # Open the csvfile for writing if requested
        self.csvFileID = None
        if flags.CSVEventsFile != "":
            try:
                self.csvFileID = open(flags.CSVEventsFile, "a")
            except:
                s = "Error -- Unable to open file %s for writing -- is the file %s open in another program"
                print(s % (flags.CSVEventsFile, flags.CSVEventsFile))
                sys.exit(0)
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
        lastSec = 0
        if(flags.makeDB):
            self.fileNum = db.db.addFileData(
                file, startSec, 0, flags.robotType, flags.compiled, flags.version)
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
        print("%6d lines in file %s type %s compiled %s version %s" %
              (self.lineCount-1, file, flags.robotType, flags.compiled, flags.version))
        if(self.csvFileID):
            self.csvFileID.close()
        if flags.makeDB:
            db.db.addFileData(file, fileDate, self.lineCount-1,
                              flags.robotType, flags.compiled, flags.version)
            db.db.connection.commit()
            if not flags.allInOne:
                s = table + '_' + str(self.lineCount)
                db.db.dropTable(s)
                db.db.renameTable(s)

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
                    utils.getFileInfo(self.fileName, l)
                    self.lineCount += 1
                    if flags.makeDB:
                        db.db.addEventData(lineDate, deltaTime,
                                           lineType, l, self.fileNum, self.fileName)
                    if(self.csvFileID):
                        self.csvFileID.write('%d,"\t%s",%d,%s,"%s",%s\n' % (
                            self.lineCount, lineDate, 0, lineType, l, self.fileName))


def parseFile(file):
    return parseDSEvents(file)
