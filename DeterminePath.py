import math
import time
import json
import xmltodict
import sys
import tkinter
import csv

print("Python version", sys.version)


def distancePT(ptA, ptB):
    lx = ptA['X'] - ptB["X"]
    ly = ptA['Y'] - ptB["Y"]
    return math.sqrt(lx*lx + ly*ly)


def compress(path):
    lastPT = None
    lastAngle = 0
    dist = 0
    i = 0
    newPath = []
    deltaDist = 99
    for pt in path:
        x = pt["X"]
        y = pt["Y"]
        angle = pt["Angle"]
        if lastPT != None:
            deltaDist = distancePT(pt, lastPT)
        if(deltaDist > .4):
            lastPT = pt
            print("%d X:%.2f Y:%.2f Delta Angle:%.1f Dist:%.2f" %
                  (i, x, y, angle - lastAngle, deltaDist))
            lastAngle = angle
            newPath.append({'X': x, 'Y': y, 'Angle': angle})
        i += 1
    return newPath

# Test program to make a path for an S curve


def makeSCurvePath():
    # pose = List.of(new Pose2d(0, 0, Rotation2d.fromDegrees(0)), new Pose2d(2, 0, Rotation2d.fromDegrees(45)),
    #       new Pose2d(2, 1.5, Rotation2d.fromDegrees(90)), new Pose2d(3, 1.5, Rotation2d.fromDegrees(-90)),
    #       new Pose2d(3, 0, Rotation2d.fromDegrees(-180)), new Pose2d(0.0, 0.0, Rotation2d.fromDegrees(-180)));
    offset = .2
    data = [[0, 0 + offset, 0], [2, 0 + offset, 45], [2, 1.5 + offset, 90], [
        3, 1.5 + offset, -90], [3, 0 + offset, -189], [0, 0 + offset, -180]]
    path = []
    for p in data:
        path.append({'X': p[0], 'Y': p[1], 'Angle': p[2]})
    return path


# Data in path is in meter - convert to feet for graph
def drawGraph(master, path, clear=True):
    if clear:
        w.delete("all")
        drawGrid(w)
    pts = []
    lastP = None
    i = 0
    skip = 1
    if len(path) > 100:
        skip = 10
    if len(path) > 1000:
        skip = 50
    for pt in path:
        if i % skip == 0:
            p = Point(metersToFeet(pt['X']),  metersToFeet(pt['Y']), .5, "red", str(i))
            pts.append(p)
            if lastP != None:
                Line(lastP, p, 4, "black", "Bar")
            lastP = p
        i += 1


class Point:
    # Class to define a point of a radius and color with a label
    global w

    def __init__(self, x, y, r, color, label, textOff=[2, 2]):
        self.x = x
        self.y = y
        self.color = color
        self.label = label
        self.r = r
        r = r * 10
        self.ov = w.create_oval(
            rx(self.x)-r, ry(self.y)+r, rx(self.x)+r, ry(self.y)-r, fill=color)
        self.textBox = w.create_text(
            rx(self.x) + r * textOff[0], ry(self.y) + r * textOff[1], text=label)

    def move(self, x, y):
        w.delete(self.ov)
        w.delete(self.textBox)
        self.ov = w.create_oval(x-self.r, y+self.r, x +
                                self.r, y-self.r, fill=self.color)
        self.textBox = w.create_text(
            x + self.r * 2, y + self.r * 2, text=self.label)
        self.x = x
        self.y = y


class Line:
    # class to create a line of a given width and color between two points
    myLine = None

    def __init__(self, p1, p2, width, color, label):
        self.p1 = p1
        self.p2 = p2
        self.color = color
        self.text = label
        self.width = width
        self.drawLine()

    def drawLine(self):
        # draw the line between the two points
        self.myLine = w.create_line(rx(self.p1.x), ry(self.p1.y), rx(self.p2.x), ry(self.p2.y),
                                    width=self.width, fill=self.color)

    def getLine(self):
        return self.myLine

    def offset(self, distance):
        # determine a point that is offset by a distance from p1
        angle = math.degrees(math.atan2(
            (self.p1.y-self.p2.y), (self.p1.x - self.p2.x)))
        x = distance * cosd(angle) + self.p2.x
        y = distance * sind(angle) + self.p2.y
        p = Point(x, y, .4, "red", "")
        return p


def rx(p):
    # get a point on the screen given a x coordinate
    # return (tw * .5 / aw) * p + tw / 2
    return tw * p / aw


def ry(p):
    # get a point on the screen given a y coordinate
    # return (-th * .5 / ah) * p + th / 2
    return th * (ah-p) / ah


def sx(p):
    # given a point on the screen in x get a normalize x value
    return (aw * p * 2) / tw - aw


def sy(p):
    # given a point on the screen in y get a normalize y value
    return (-ah * p * 2) / th + ah


def normalizeAngle(angle):
    a = angle + 180.0 % 360.0
    if a < 0.0:
        a += 360.0
    a = a - 180.0
    if a > 180:
        a -= 360
    return a


def drawGrid(p):
    offset = 1
    for i in range(-int(ah), +int(ah), offset):
        if(i % 5 == 0):
            width = 3
        else:
            width = 1
        p.create_line(rx(-aw), ry(i), rx(aw), ry(i),
                      width=width, fill="light gray")
    for i in range(-int(aw), int(aw), offset):
        if(i % 5 == 0):
            width = 3
        else:
            width = 1
        p.create_line(rx(i), ry(-ah), rx(i), ry(ah),
                      width=width, fill="light gray")
        # Draw Line at the bottom of the graph
    w.create_line(rx(-aw), ry(-ah), rx(aw), ry(-ah), width=2, fill="black")
    # Draw the field points points on the graph
    for col in range(1,12):
        for row in range(1,6):
            Point(col * 2.5, row * 2.5, .2, "black", "")
def makeCode(path, fileName):
    print("Makecodes for results to file:" +
          fileName + " length:" + str(len(path)))
    for point in path:
        print("new Pose2d(%.2f, %.2f, Rotation2d.fromDegrees(%.1f))," %
              (point['X'], point['Y'], point['Angle']))


def distanceJSON(point):
    return math.sqrt(point[0] * point[0] + point[1] * point[1])


def angle(p1, p2):
    return math.degrees(math.atan2(p1[0] - p2[0], p1[1]-p2[1]))


def parseMPXML(fileName):
    print("Read and Parse Path Data from File:" + fileName)
    with open(fileName) as fd:
        a = xmltodict.parse(fd.read())
        p = a['Path']['Waypoint']
        path = []
        # path.append({'X': 0, 'Y': 0, 'Angle': 0})
        for itm in p:
            print(itm['X'], itm['Y'], itm['Angle'])
            path.append({'X': float(itm['X']) * metersPerFoot, 'Y': float(
                itm['Y']) * metersPerFoot, 'Angle': float(itm['Angle'])})
        return path

def parsePathPlannerCSV(fileName):
    path = []
    print("Read and Parse Path Data from File:" + fileName)
    with open(fileName, newline='') as csvfile:
        data = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in data:
          print(row)
          path.append({"X":float(row[0]), "Y":   7.5 * 12 * 0.0254 - float(row[1]), "Angle":float(row[2])})
    return path

def parsePathPlannerJSON(fileName):
    print("Read and Parse Path Data from File:" + fileName)
    fileID = open(fileName, 'r')
    p = json.load(fileID)
    # Print the elements of the json file
    for key in p:
        print("Key:%s Data:%s" % (key, p[key]))
    # Process the points from the file
    # Note: Every 3rd point contains a point on the path - the previous and subsequent point are used to determing the angle
    points = p['points']
    i = 0
    for a in points:
        print(i, a[0], a[1])
        i += 1
    lastDist = 0
    totalDist = distanceJSON(points[0])
    path = []
    path.append({'X': a[0], 'Y': a[1], 'Angle': 0})
    for i in range(3, len(points), 3):
        a = points[i]
        dist = distanceJSON(a)
        if lastDist == 0:
            lastDist = dist
        totalDist += abs(dist-lastDist)
        angle1 = angle(points[i-1], points[i])
        if(i != 30):
            angle2 = angle(points[i], points[i+1])
            angle3 = angle(points[i-1], points[i+1])
        print("i:%d x:%.2f y:%.2f delta dist:%.2f total:%.2f a1:%.1f a2:%.1f a3:%.1f" %
              (i, a[0], a[1], dist-lastDist, totalDist, angle1, angle2, angle3))
        lastDist = dist
        # Need correction factors for y and angle
        #path.append({'X': a[0] * 2.5 * 5.5 / 4.17, 'Y': a[1], 'Angle': angle1})
        path.append({'X':  a[0], 'Y': feetToMeters(15) - a[1], 'Angle': angle1})
    return path

def feetToMeters(f):
    return float(f) * 12 * 2.54 / 100

def metersToFeet(m):
    return float(m) * 100 / (12 * 2.54)

def parseMPJSON(fileName):
    print("Read and Parse Motion Profile Path Data from File:" + fileName)
    fileID = open(fileName, 'r')
    p = json.load(fileID)
    path = []
    for row in p:
         path.append({'X': feetToMeters(row['X Point']) , 'Y': feetToMeters(row['Y Point']), 'Angle': row['Heading']})
    return path

def makeSCurveButton():
    print("Make S Curve Path")
    path = makeSCurvePath()
    makeCode(path, "S_Curve.java")
    drawGraph(master, path)


def openPPPath():
    print("Open PathPlanner Path file")
    fileName = "Barrel.path"
    path = parsePathPlannerJSON(fileName)
    makeCode(path, fileName + ".java")
    drawGraph(master, path)


def openPPCSV():
    print("Open PathPlanner CSV file")
    fileName = "Barrel.csv"
    path = parsePathPlannerCSV(fileName )
    makeCode(path, fileName + ".java")
    drawGraph(master, path)

def openMPXML():
    global path, fileName
    print("Open Motion Profile XML file")
    fileName = "BarrelRacePath.xml"
    path = parseMPXML(fileName)
    makeCode(path, fileName + ".java")
    drawGraph(master, path)


def openMPJSON():
    print("Open Motion Profile JSON file")
    fileName = 'SLALOM_PATH_right.json'
    path = parseMPJSON(fileName)
    drawGraph(master, path)
    fileName = 'SLALOM_PATH_left.json'
    path = parseMPJSON(fileName)
    makeCode(path, fileName + ".java")
    drawGraph(master, path, clear=False)

def compressButton():
    global path, fileName
    print("Compress Button")
    path = compress(path)
    makeCode(path, fileName + "_compressed.java")
    drawGraph(master, path)


def saveButton():
    print("Save Button")
    makeCode(pathA, "test.java")
    drawGraph(master, pathA)


metersPerFoot = 12 * 2.54 / 100

# pathP = makePathFromProg()

tw = 1000
th = 500
ah = 15
aw = 30

path = []
fileName = ""
master = tkinter.Tk()
master.title("Path Drawing Tool")
w = tkinter.Canvas(master, width=tw, height=th)
w.pack()
drawGrid(w)
Point(0, 0, .5, "red", "Orig", textOff=[4, -4])
Point(30, 0, .5, "green", "(30,0)",  textOff=[-4, -4])

r = 1
c = 0
f = tkinter.Frame(master)
tkinter.Button(f, text="Open PathPlanner File (*.path)", command=openPPPath).grid(
    row=r, column=c, sticky="W", padx=2, pady=5)
c += 1
tkinter.Button(f, text="Open PathPlanner File (*.csv)", command=openPPCSV).grid(
    row=r, column=c, sticky="W", padx=2, pady=5)
c += 1
tkinter.Button(f, text="Open Motion Profile File (*.xml)", command=openMPXML).grid(
    row=r, column=c, sticky="W", padx=2, pady=5)
c += 1
tkinter.Button(f, text="Open PathPlanner File (*.json)", command=openMPJSON).grid(
    row=r, column=c, sticky="W", padx=2, pady=5)
c += 1
tkinter.Button(f, text="Make S Curve", command=makeSCurveButton).grid(
    row=r, column=c, sticky="W", padx=2, pady=5)
c += 1
tkinter.Button(f, text="Compress Path Data", command=compressButton).grid(
    row=r, column=c, sticky="W", padx=2, pady=5)
c = 0
r += 1
tkinter.Button(f, text="Save Path Data (pose)    ", command=saveButton).grid(
    row=r, column=c, sticky="W", padx=2, pady=5)
c += 1
tkinter.Button(f, text="Save Path Data (json)    ", command=saveButton).grid(
    row=r, column=c, sticky="W", padx=2, pady=5)

w.grid(row=0,  column=0)
f.grid(row=1,  column=0, sticky='W')

master.mainloop()
