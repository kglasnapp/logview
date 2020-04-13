import socket
import utils

def toHex(hdr, start, len):
    r = ""
    for i in range(start, len):
        r += "%2x " % (hdr[i])


TCP_IP = '10.39.32.2'
TCP_PORT = 1741
BUFFER_SIZE = 1024  # Normally 1024, but we want fast response

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
# s.listen(5)

#conn, addr = s.accept()
#print ('Connection address:', addr)
while True:
    data = s.recv(BUFFER_SIZE)
    if not data:
        break
    length = utils.toDec2(data, 0)
    seqNum = utils.toDec2(data, 7)
    timeSince = utils.toDec4(data, 3)
    print(length, seqNum, timeSince, data[9:])
    # conn.send(data)  # echo
s.close()


