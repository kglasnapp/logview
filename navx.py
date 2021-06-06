import serial
import time
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np


# Take an angle and convert it to -180 to 180


def normalizeAngle(angle):
    a = (angle + 180) % 360
    if (a < 0):
        a += 360
    return round(a - 180, 2)

# Take an angle and convert it to 0 to 360


def unNormalilzeAngle(angle):
    a = angle % 360
    if (a < 0):
        a += 360
    return round(a, 2)


def toInt(b):
    x = b[1] * 256 + b[0]
    if(b[1] > 128):
        return x - 65536
    else:
        return x


def readNavx():
    global serNavx, debug
    serNavx.flushInput()
    while True:
        s = serNavx.read(1)
        if s == b'\r':
            s = serNavx.read(1)
            if s == b'\n':
                s = serNavx.read(4)
                b = serNavx.read(2)
                y = toInt(b) / 100
               #z = serNavx.read(s[3]-6)
                angle = unNormalilzeAngle(y)
                if debug:
                    print(s[0], s[1], s[2], s[3], y, angle, b[0], b[1])
                return angle


def readBNO055():
    global serBNO
    while True:
        s = serBNO.read(1)
        if s == b'\r':
            s = serBNO.read(1)
            if s == b'\n':
                s = serBNO.read(30).decode('UTF-8')
                angle = None
                if s.startswith('Euler'):
                    angle = unNormalilzeAngle(
                        float(s.split('(')[1].split(',')[0]))
                    return angle

if False:
    for i in range(-380, 380, 20):
        print("Norm", i, normalizeAngle(i))


    for i in range(-380, 380, 20):
        print("UnNorm", i, unNormalilzeAngle(i))



debug = False
serBNO = serial.Serial("COM8", 115200)
serNavx = serial.Serial('COM7', 9600)  # open serial port
# Open a file with access mode 'a'
file_object = open('yawData.txt', 'a')
i = 0
navxA = []
bnoA = []
x = []
startTime = time.time()
graphFN = datetime.now().strftime("yawVariance_%m-%d-%y_%H_%M.png")
print(graphFN)
while True:
    navx = normalizeAngle(readNavx())
    bno = normalizeAngle(readBNO055())
    navxA.append(navx)
    bnoA.append(bno)
    x.append(int(time.time() - startTime))
    time.sleep(.1)
    t = datetime.now().strftime("%H:%M:%S")
    data = "I:%d Seconds:%d Time:%s Navx:%.2f BNO:%.2f Diff:%.2f" % (
        i, int(time.time() - startTime), t, navx, bno, abs(navx - bno))
    file_object.write(data + '\n')
    if(i % 5 == 0):
        file_object.flush()
    print(data)
    i += 1
    if i % 10 == 0:
        plt.ylim([0, 90])
        plt.yticks(np.arange(0, 91, 5))
        plt.plot(x, navxA, label='NavX')
        plt.plot(x, bnoA, label="BNO")
        plt.xlabel('Seconds')
        plt.ylabel('Angle')
        if i == 10:
            legend = plt.legend(loc='best', shadow=True)
        plt.show(block=False)
        plt.pause(1)
        plt.savefig(graphFN)
        #time.sleep(2)
        #plt.close()
    if i == 1000:
        break
print("Done")
serNavx.close()
serBNO.close
file_object.close()
