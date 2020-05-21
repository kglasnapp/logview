import socket
import utils
import datetime
import os

def toHex(hdr, start, len):
    r = ""
    for i in range(start, len):
        r += "%2x " % (hdr[i])

def getLogs(fileOut):
    while True:
        try:
            data = s.recv(BUFFER_SIZE)
        except:
            print("Connection Lost")
            return
        if not data:
            print("No Data Received")
            return
        if len(data) > 10:
           length = utils.toDec2(data, 0)
           seqNum = utils.toDec2(data, 7)
           timeSince = utils.toDec4(data, 3)
        else: 
            print("Short message", data)
        if(debug):
            print(length, seqNum, timeSince, data[9:])
        fileOut.write("%d,%d,%d,%s\n" % (seqNum,timeSince,length,data[9:]))

   

TCP_IP = '10.39.32.2'
TCP_PORT = 1740
BUFFER_SIZE = 1024 
ti = datetime.datetime.now()
fileName = ti.strftime("%Y_%m_%d %H_%M_%S %a.csv")
fileOut = open(fileName, "a")
if os.path.getsize(fileName) == 0:
    fileOut.write("Sequence,Time,Length,Data\n")
debug = True
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.connect((TCP_IP, TCP_PORT))
except:
    print("Unable to open connection to the robot at ip:%s port:%d" %(TCP_IP,TCP_PORT))
    fileOut.close()
    quit()
while True:
    getLogs(fileOut)  
fileOut.close()
s.close()


