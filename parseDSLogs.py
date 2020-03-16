import os
import re
import datetime
import db
import struct
import flags
import bitstring
import sys
import main

class parseDSLogs:
    lineCount = 0
    fileName = ''
    def __init__(self, file):
        if flags.debug:
            print("Parse DSLog for file:" + file)
        table = os.path.basename(file)
        self.fileName = table
        table = "Logs_" + table.split(' ')[0] + "_" + table.split(' ')[1]
        if flags.makeDB and not flags.allInOne:
            print("Make table in DB for: " + table)
            db.db.dropTable(table)
            db.db.createLogDataTable(table)
            db.db.createConnection('files')
        if flags.CSVFile != "":
            try:
                csvFileID = open(flags.CSVFile, "w+")
            except:
                print(
                    "Error -- Unable to open file %s for writing -- is the file open in another program", flags.CSVFile)
                sys.exit(0)
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
        # self.dump(hdr, 20)
        if flags.debug:
            print("Parse file: " + file + " date:" +
                  str(fileDate) + " StartSec:" + str(time))
        while True:
            hdr = stream.read(35)
            # Check for end of file
            if len(hdr) == 0:
                break
            trace = self.getTrace(hdr[5])
            # Get the values for the PDP currents
            pdp = self.getPDP(hdr, 11)
            current = self.sumCurrents(pdp, False)
            battery = round((hdr[2] + hdr[3] / 256) * 10) / 10
            if flags.showLogs:
                print(time.strftime("%m/%d %H:%M:%S "), self.lineCount, " Trip:", hdr[0], " Bat:", battery, " CPU:",
                      hdr[4] / 2, " Trace:", trace, "Current:", current, pdp)
            if csvFileID:
                s = "\t%s,%d,%d,%d,%.1f,%.1f,%s,%.1f,%.1f,%d,%.1f,%s\n" % (time.strftime("%m/%d %H:%M:%S"), self.lineCount,
                    hdr[0], hdr[1]*4,  battery, hdr[4]/2,  trace, hdr[6]/2, hdr[7]/2, hdr[8], current, self.currentsToString(pdp))
                csvFileID.write(s)
            self.lineCount += 1
            time += datetime.timedelta(seconds=(.02))
        print("Processed file:%s Last Time:%s Line count:%d" % (file, time.strftime("%H:%M:%S "), self.lineCount))
        if(csvFileID):
            csvFileID.close()
        if flags.makeDB:
            #db.addFileData(file, fileDate, self.lineCount-1, '','','')
            db.db.connection.commit()
            if not flags.allInOne:
                s = table + '_' + str(self.lineCount)
                db.db.dropTable(s)
                db.db.renameTable(s)

    def toDec4(self, d, start):
        return d[start+2] * 256 + d[start+3] + (d[start] * 256 + d[start+1]) * 256

    def toDec2(self, d, start):
        return d[start] * 256 + d[start+1]

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

    def dump(self, hdr, length):
        s = ""
        for i in range(0, length):
            s += "%x " % (hdr[i])
        print(s)

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

    def parseDataV3(self, data_bytes):
        data_bytes = data_bytes[0:10]
        raw_values = struct.unpack('>BBHBcBBH', data_bytes)
        status_bits = self.unpack_bits(raw_values[4])
        res = {
            'round_trip_time': self.shifted_float(raw_values[0], 1),
            'packet_loss': 0.04 * raw_values[1],             # not shifted
            'voltage': self.shifted_float(raw_values[2], 8),
            'rio_cpu': 0.01 * self.shifted_float(raw_values[3], 1),
            'can_usage': 0.01 * self.shifted_float(raw_values[5], 1),
            'wifi_db': self.shifted_float(raw_values[6], 1),
            'bandwidth': self.shifted_float(raw_values[7], 8),

            'robot_disabled': status_bits[7],
            'robot_auto': status_bits[6],
            'robot_tele': status_bits[5],
            'ds_disabled': status_bits[4],
            'ds_auto': status_bits[3],
            'ds_tele': status_bits[2],
            'watchdog': status_bits[1],
            'brownout': status_bits[0],
        }
        return res

    def shifted_float(self, raw_value, shift_right):
        return raw_value / (2.0**shift_right)

    def unpack_bits(self, raw_value):
        # Unpack and invert the bits in a byte
        status_bits = bitstring.Bits(bytes=raw_value)
        # invert them all
        return [not b for b in status_bits]

def parseFile(file):
    return parseDSLogs(file)