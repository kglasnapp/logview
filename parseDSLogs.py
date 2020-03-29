import datetime
import os
import struct
import sys

import flags
from db import db

# Parse an FRC dslog file the format is documented at https://frcture.readthedocs.io/en/latest/driverstation/logging.html
class parseDSLogs:
    lineCount = 0
    fileName = ''
    linesWithCurrent = 0
    myMakeDB = False
    def __init__(self, file):
        self.lineCount = 0
        self.myMakeDB = flags.makeDB
        if flags.debug:
            print("Parse DSLog for file:" + file)
        table = os.path.basename(file)
        self.fileName = table
        #table = "Logs_" + table.split(' ')[0] + "_" + table.split(' ')[1]
        csvFileID = None
        if flags.CSVLogFile != "":
            try:
                csvFileID = open(flags.CSVLogFile, "a")
            except:
                s = "Error -- Unable to open file %s for writing -- is the file %s open in another program like excel"
                print(s % (flags.CSVLogFile, flags.CSVLogFile))
                sys.exit(0)
            if os.path.getsize(flags.CSVLogFile) == 0:
                s = ""
                for i in range(0, 16):
                    s += "PDP %d," % (i)
                csvFileID.write(
                    "Time,Count,Trip,Loss,Battery,CPU,Trace,CAN,WiFi,MB,Current," + s[:-1] + "\n")
        stream = open(file, 'rb')
        ar = os.path.basename(file).split()
        if(len(ar) != 3):
            print("********* Invalid file name " + os.path.basename(file))
            return
        fileDate = datetime.datetime.strptime(
            ar[0] + ar[1], "%Y_%m_%d%H_%M_%S")
        hdr = stream.read(20)
        # Return if hit end of file
        if len(hdr) == 0:
            return
        time = self.read_timestamp(hdr)
        if flags.debug:
            print("Parse file: " + file + " date:" +
                  str(fileDate) + " StartSec:" + str(time))
        fileNum = 0
        if self.myMakeDB:
            if db.isFileInDB(file):  
                print("File %s is in the DB, will not update the DB" % (file))
                self.myMakeDB = False
            else:
                fileNum = db.addFileData(
                file, fileDate, 0, '', '', '')
            db.table = flags.logTable 
        if(self.myMakeDB or csvFileID):
            self.loopOverFile(stream, csvFileID, fileNum, time)
        if self.lineCount > 0:
            print("%8d logs in file:%s Last Time:%s Lines with Current:%d" %
              (self.lineCount, file, time.strftime("%H:%M:%S "), self.linesWithCurrent))
        if self.myMakeDB:
            fileNum = db.addFileData(
                file, fileDate,self.lineCount, '', '', '')
            db.connection.commit()
        if(csvFileID):
            csvFileID.close()
            
    def loopOverFile(self, stream, csvFileID, fileNum, time):
        while True:
            hdr = stream.read(35)
            # Check for end of file
            if len(hdr) == 0:
                break
            # Get trace or the robot status data
            trace = self.getTrace(hdr[5])
            # Get the values for the PDP currents
            pdp = self.getPDP(hdr, 11)
            current = self.sumCurrents(pdp, False)
            if(current > 0):
                self.linesWithCurrent += 1
            battery = round((hdr[2] + hdr[3] / 256) * 10) / 10
            if battery > 15:
                battery = 0
            if flags.showLogs:
                print(time.strftime("%m/%d %H:%M:%S "), self.lineCount, " Trip:", hdr[0], " Bat:", battery, " CPU:",
                      hdr[4] / 2, " Trace:", trace, "Current:", current, pdp)
            if csvFileID:
                data = (time.strftime("%m/%d %H:%M:%S"), self.lineCount,
                        hdr[0], hdr[1]*4,  battery, hdr[4]/2,  trace, hdr[6]/2, hdr[7]/2, hdr[8], current, self.currentsToString(pdp))
                s = "\t%s,%d,%d,%d,%.1f,%.1f,%s,%.1f,%.1f,%d,%.1f,%s\n" % data
                csvFileID.write(s)
            if self.myMakeDB:
                #  s = "(fileNum, time,count,trip,loss,battery,cpu,trace,can,wifi,mb,current,"
                data = [fileNum, time, self.lineCount, hdr[0], hdr[1]*4, battery,
                        hdr[4]/2,  trace, hdr[6]/2, hdr[7]/2, hdr[8], current]
                for x in pdp:
                    data.append(x)
                #data.append(self.fileName)
                data.append("")
                db.addLogData(tuple(data))
            self.lineCount += 1
            time += datetime.timedelta(seconds=(.02))

    def currentsToString(self, pdp):
        s = ""
        for i in range(0, 16):
            s += "%.1f," % (pdp[i])
        return s[:-1]

    def sumCurrents(self, pdp, round):
        current = 0
        for i in range(0, 16):
            if(round):
                pdp[i] = round(pdp[i] * 10) / 10
            current += pdp[i]
        if(round):
            current = round(current * 10) / 10
        return current

    def read_timestamp(self, hdr):
        # Get Time from the file
        sec = struct.unpack_from('>L', hdr, 8)[0]
        millisec = hdr[12] / 256
        # Get base time for National Instrutments software
        dt = datetime.datetime(1904, 1, 1, 0, 0, 0,
                               tzinfo=datetime.timezone.utc)
        # Make the time reflect EST instead utc
        dt += datetime.timedelta(seconds=(-5 * 3600))
        # Adjust time for Time in the file
        dt += datetime.timedelta(seconds=(sec + millisec))
        return dt

    # PDP are 10 bit number and the current is obtained by dividing by 8
    # 0, 1, 2, 3, 4, 5	  60 bits + 4 padding	8 bytes
    # 6, 7, 8, 9, 10, 11  60 bits + 4 padding	8 bytes
    # 12, 13, 14, 15	  40 bits	5 bytes

    def getPDP(self, hdr, start):
        result = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.get4(hdr, 11+0, result, 0)
        self.get2(hdr, 11+5, result, 4)
        self.get4(hdr, 11+8, result, 6)
        self.get2(hdr, 11+13, result, 10)
        self.get4(hdr, 11+16, result, 12)
        return result

    def get4(self, hdr, hs, result, rs):
        result[rs+0] = (((hdr[hs+0] & 0xff) << 2) + (hdr[hs+1] >> 6)) / 8
        result[rs+1] = (((hdr[hs+1] & 0x3f) << 4) + (hdr[hs+2] >> 4)) / 8
        result[rs+2] = (((hdr[hs+2] & 0x0f) << 6) + (hdr[hs+3] >> 2)) / 8
        result[rs+3] = (((hdr[hs+3] & 0x03) << 8) + (hdr[hs+4] >> 0)) / 8

    def get2(self, hdr, hs, result, rs):
        result[rs+0] = (((hdr[hs+0] & 0xff) << 2) + (hdr[hs+1] >> 6)) / 8
        result[rs+1] = (((hdr[hs+1] & 0x3f) << 4) + (hdr[hs+2] >> 4)) / 8

    def getTrace(self, data):
        s = ""
        data = data ^ 0xff
        if data & 0x80:
            s += "BO "
        if data & 0x40:
            s += "WD "
        if data & 0x20:
            s += "DT "
        if data & 0x10:
            s += "NA "
        if data & 0x8:
            s += "DD "
        if data & 0x4:
            s += "RT "
        if data & 0x2:
            s += "RA "
        if data & 0x1:
            s += "RD "
        return "%x %s" % (data, s)


def parseFile(file):
    return parseDSLogs(file)
