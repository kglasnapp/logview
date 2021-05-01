import serial
import time

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


debug = False
serBNO = serial.Serial("COM10", 115200)
serNavx = serial.Serial('COM7', 9600)  # open serial port
bno = 0
while True:
    navx = readNavx()
    bno = readBNO055()
    time.sleep(.5)

    print("Navx:%.2f BNO:%.2f Diff:%.2f" % (navx, bno, abs(navx - bno)))
print("Done")
serNavx.close()
serBNO.close
