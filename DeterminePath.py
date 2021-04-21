import math
import json
import xmltodict
import sys
import tkinter
import csv
from plotter import *


def distancePT(ptA, ptB):
    # get the distance between two points in a path
    lx = ptA['X'] - ptB["X"]
    ly = ptA['Y'] - ptB["Y"]
    return math.sqrt(lx*lx + ly*ly)


def compress(path):
    # compress a path i.e. if distance less than .4 meters ignore point
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


def makeSCurvePath():
    # Test program to make a path for an S curve
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


def drawGraph(master, path, clear=True, line="black"):
    # Data in path is in meter - convert to feet for graph
    if clear:
        gw.delete("all")
        drawGridForFeet(gw)
    pts = []
    lastP = None
    i = 0
    # determine number of points to skip give size of path
    skip = 1
    if len(path) > 100:
        skip = 10
    if len(path) > 1000:
        skip = 50
    for pt in path:
        if i % skip == 0:
            p = Point(metersToFeet(pt['X']),  metersToFeet(
                pt['Y']), .5, "red", str(i))
            pts.append(p)
            # draw a black line to represent the path
            if lastP != None:
                Line(lastP, p, 4, line, "Bar")
            lastP = p
        i += 1


def drawGridForFeet(p):
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
    gw.create_line(rx(-aw), ry(-ah), rx(aw), ry(-ah), width=2, fill="black")
    # Draw the field points points on the graph
    for col in range(1, 12):
        for row in range(1, 6):
            Point(col * 2.5, row * 2.5, .2, "black", "")


def drawGridForMeters(p):
    offset = 10
    i = 0
    while i < feetToCent(ah):
        if(i % 100 == 0):
            width = 3
        else:
            width = 1
        j = metersToFeet(i/100)
        p.create_line(rx(-aw), ry(j), rx(aw), ry(j),
                      width=width, fill="light gray")
        i += offset
    i = 0
    while i < feetToCent(aw):
        if(i % 100 == 0):
            width = 3
        else:
            width = 1
        j = metersToFeet(i/100)
        p.create_line(rx(j), ry(-ah), rx(j), ry(ah),
                      width=width, fill="light gray")
        i += offset
        # Draw Line at the bottom of the graph
    gw.create_line(rx(-aw), ry(-ah), rx(aw), ry(-ah), width=2, fill="black")
    # Draw the field points points on the graph
    for col in range(1, 12):
        for row in range(1, 6):
            Point(col * 2.5, row * 2.5, .2, "black", "")


def makePoseCode(path, fileName):
    print("Make pose code for file:" +
          fileName + " length:" + str(len(path)))
    s = "pose = List.of(new Pose2d(0, 0, Rotation2d.fromDegrees(0)),\n"
    for point in path:
        l = "new Pose2d(%.2f, %.2f, Rotation2d.fromDegrees(%.1f))," % (
            point['X'], point['Y'], point['Angle'])
        s += l + '\n'
        if debug:
            print(l)
    file = open(fileName, "w")
    file.write(s)
    file.close()


def makeJSONCode(path, fileName):
    print("Make json file for path:" +
          fileName + " length:" + str(len(path)))
    with open(fileName, 'w') as outfile:
        json.dump(path, outfile, indent=2)


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
            if debug:
                print(itm['X'], itm['Y'], itm['Angle'])
            path.append({'X': feetToMeters(itm['X']), 'Y': feetToMeters(
                itm['Y']), 'Angle': float(itm['Angle'])})
        return path


def parsePathPlannerCSV(fileName):
    path = []
    print("Read and Parse Path Data from File:" + fileName)
    with open(fileName, newline='') as csvfile:
        data = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in data:
            if debug:
                print(row)
            path.append({"X": float(
                row[0]), "Y":   7.5 * 12 * 0.0254 - float(row[1]), "Angle": float(row[2])})
    return path


def parseWPIJSON(fileName):
    path = []
    print("Read and Parse WPI Path Data from File:" + fileName)
    fileID = open(fileName, 'r')
    p = json.load(fileID)
    x = []
    y = []
    for point in p:
        tr = point['pose']['translation']
        x.append(tr['x'])
        y.append(tr['y'])
    #  Largest size (width or height) of trajectory
    width = max(x) - min(x)
    height = max(y) - min(y)
    print("Point 0 x:%.2f y:%.2f Avg x:%.2f y:%.2f Min x:%.2f y:%.2f Max x:%.2f y:%.2f width:%.2f height:%.2f" % (
        x[0], y[0], sum(x)/len(p), sum(y)/len(p), min(x), min(y), max(x), max(y), width, height))

    for point in p:
        pose = point['pose']
        angle = pose['rotation']['radians'] * 180 / 3.14159
        tr = pose['translation']
        path.append({'X':  tr['x'] - min(x), 'Y': -min(y) +
                     float(tr['y']), 'Angle': angle})
    # Point 0 x:2.50 y:2.97 Avg x:14.61 y:5.31
        #path.append({'X':  tr['x'] / 3.5, 'Y':float(tr['y'] /3.5 ), 'Angle': angle})
    # path = []
    # path.append({'X':  0, 'Y': 0, 'Angle':0})
    # path.append({'X':  1, 'Y': 1, 'Angle':0})
    # path.append({'X':  2, 'Y': 1, 'Angle':0})
    return path


def parsePathPlannerJSON(fileName):
    print("Read and Parse Path Data from File:" + fileName)
    fileID = open(fileName, 'r')
    p = json.load(fileID)
    # Process the points from the file
    # Note: Every 3rd point contains a point on the path - the previous and subsequent point are used to determing the angle
    points = p['points']
    if debug:
        i = 0
        for a in points:
            print(i, a[0], a[1])
            i += 1
    lastDist = 0
    totalDist = distanceJSON(points[0])
    path = []
    path.append({'X': points[0][0], 'Y': points[0][1], 'Angle': 0})
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
        if debug:
            print("i:%d x:%.2f y:%.2f delta dist:%.2f total:%.2f a1:%.1f a2:%.1f a3:%.1f" %
                  (i, a[0], a[1], dist-lastDist, totalDist, angle1, angle2, angle3))
        lastDist = dist
        path.append({'X':  a[0], 'Y': feetToMeters(
            15) - a[1], 'Angle': angle1})
    return path


# Auto Barrel
# Poses
# Pose 2 0.2 0
# Pose 3.6 -0.8 -90
# Pose 3 -1.4 -180
# Pose 2.3 -0.8 90
# Pose 4.2 0 10
# Pose 6 0.8 90
# Pose 5.2 1.35 -180
# Pose 4.6 0.8 -90
# Pose 7 -1.3 0
# Pose 7.5 -0.6 90
# Pose 7 0 -180
# End 0 0 -180

def barrel():
    p = []
    p.append({'X':0.0,'Y':0, 'Angle':0})
    p.append({'X':2.0,'Y':0.2, 'Angle':0})
    p.append({'X':3.6,'Y':-0.8, 'Angle':-90})
    p.append({'X':3.0,'Y':-1.4, 'Angle':-180})
    p.append({'X':2.3,'Y':-0.8, 'Angle':90})
    p.append({'X':4.2,'Y':0, 'Angle':10})
    p.append({'X':6.0,'Y':.8, 'Angle':90})
    p.append({'X':5.2,'Y':1.35, 'Angle':-180})
    p.append({'X':4.6,'Y':0.8, 'Angle':-90})
    p.append({'X':7.0,'Y':-1.3, 'Angle':0})
    p.append({'X':7.5,'Y':-0.6, 'Angle':90})
    p.append({'X':7.0,'Y':0, 'Angle':-180})
    p.append({'X':0.0,'Y':0, 'Angle':-180})
    for pt in p:
        pt['Y'] = pt['Y'] + 2.5
        pt['X'] = pt['X'] + feetToMeters(2.5)
    return p

def feetToMeters(f):
    return float(f) * 12 * 2.54 / 100


def feetToCent(f):
    return float(f) * 12 * 2.54


def metersToFeet(m):
    return float(m) * 100 / (12 * 2.54)


def parseMPJSON(fileName):
    print("Read and Parse Motion Profile Path Data from File:" + fileName)
    fileID = open(fileName, 'r')
    p = json.load(fileID)
    path = []
    for row in p:
        path.append({'X': feetToMeters(row['X Point']), 'Y': feetToMeters(
            row['Y Point']), 'Angle': row['Heading']})
    return path

def getValue(s, start, next):
    first = s.find(start)
    if first < 0:
        return 0.0
    last = s.find(next, first)
    r = s[first+len(start):last]
    return float(r)


def  parseProgJSON(fileName):
    print("Read and Parse Prog Log from File:" + fileName)
    fileID = open(fileName, 'r')
    p = json.load(fileID)
    path = []
    for row in p:
        if 'line' in row and row['line'].startswith('State'):
            print(row['line'])
            x = getValue(row['line'],'X:', ',') + feetToMeters(0)
            y = getValue(row['line'],'Y:', ')') + feetToMeters(2.5)
            angle = getValue(row['line'],'Deg:', ')')
            path.append({'X': x, 'Y': y, 'Angle':angle})
    return path


def makeSCurveButton():
    global path, fileName
    print("Make S Curve Path")
    path = makeSCurvePath()
    #makeCode(path, "S_Curve.java")
    drawGraph(master, path)


def openPPPath():
    global path, fileName
    print("Open PathPlanner Path file")
    fileName = "Barrel.path"
    path = parsePathPlannerJSON(fileName)
    #makeCode(path, fileName + ".java")
    drawGraph(master, path)


def openPPCSV():
    global path, fileName
    print("Open PathPlanner CSV file")
    fileName = "Barrel.csv"
    path = parsePathPlannerCSV(fileName)
    #makeCode(path, fileName + ".java")
    drawGraph(master, path)


def openMPXML():
    global path, fileName
    print("Open Motion Profile XML file")
    fileName = "BarrelRacePath.xml"
    path = parseMPXML(fileName)
    #makeCode(path, fileName + ".java")
    drawGraph(master, path)


def openMPJSON():
    global path, fileName
    print("Open Motion Profile JSON file")
    fileName = 'SLALOM_PATH_right.json'
    path = parseMPJSON(fileName)
    drawGraph(master, path)
    fileName = 'SLALOM_PATH_left.json'
    path = parseMPJSON(fileName)
    drawGraph(master, path, clear=False, line="yellow")


def makeWPIJSONButton():
    global path, fileName
    # fileName = 'Unnamed.wpilib.json' # Seems to be in feet
    fileName = 'Loop.wpilib.json'
    fileName = 'SLALOM_PATH_left.json'  # Seems to be in feet
    path = parseWPIJSON(fileName)
    drawGraph(master, path, clear=False, line="yellow")

def makeBarrelButton():
    global path, fileName
    path = barrel()
    drawGraph(master, path, clear=False, line="yellow")

def makeProgLogJson():
    global path, fileName
    fileName = 'BarrelPathLog.json'
    fileName = 'SlalomPathLog.json'
    path = parseProgJSON(fileName)
    drawGraph(master, path)


def compressButton():
    global path, fileName
    print("Compress Button")
    path = compress(path)
    #makeCode(path, fileName + "_compressed.java")
    drawGraph(master, path)


def saveJsonButton():
    global path, fileName
    print("Save Button JSON fileName:" + fileName)
    makeJSONCode(path,  fileName + ".json")


def savePoseButton():
    global path, fileName
    print("Save Button Pose fileName:" + fileName)
    makePoseCode(path, fileName + ".java")


print("Python version", sys.version)
debug = False
tw = 1000  # Width Screen in pixels
th = 500  # Height Screen in pixels
aw = 30  # Width Screen in feet
ah = 15  # Height Screen in feet
path = []  # Variable to hold path
fileName = ""  # active file on the screen
master = tkinter.Tk()  # set master to Top level window
master.title("Path Drawing Tool")
gw = tkinter.Canvas(master, width=tw, height=th)  # set gw to graph window
gw.pack()
setPlotterParms(gw, tw, th, aw, ah)  # inform the plotter of parameters
# drawGridForFeet(gw)
drawGridForMeters(gw)
# put points on screen mainly for debug
Point(0, 0, .5, "red", "Orig", textOff=[4, -4])
Point(30, 0, .5, "green", "(30,0)",  textOff=[-4, -4])

# Put the control buttons on screen
# The contol methods will plot the data on the screen when pressed
row = 1
col = 0
bf = tkinter.Frame(master)  # Create the frame for buttons
tkinter.Button(bf, text="PathPlanner File (*.path)", command=openPPPath).grid(
    row=row, column=col, sticky="W", padx=2, pady=5)
col += 1
tkinter.Button(bf, text="PathPlanner File (*.csv)", command=openPPCSV).grid(
    row=row, column=col, sticky="W", padx=2, pady=5)
col += 1
tkinter.Button(bf, text="Motion Profile File (*.xml)", command=openMPXML).grid(
    row=row, column=col, sticky="W", padx=2, pady=5)
col += 1
tkinter.Button(bf, text="Motion Profile File (*.json)", command=openMPJSON).grid(
    row=row, column=col, sticky="W", padx=2, pady=5)
col += 1
tkinter.Button(bf, text="S Curve", command=makeSCurveButton).grid(
    row=row, column=col, sticky="W", padx=2, pady=5)
col += 1
tkinter.Button(bf, text="WPI RAMSET", command=makeWPIJSONButton).grid(
    row=row, column=col, sticky="W", padx=2, pady=5)
col += 1
tkinter.Button(bf, text="Barrel", command=makeBarrelButton).grid(
    row=row, column=col, sticky="W", padx=2, pady=5)
col += 1
tkinter.Button(bf, text="ProgLog", command=makeProgLogJson).grid(
    row=row, column=col, sticky="W", padx=2, pady=5)
col = 0
row += 1
tkinter.Button(bf, text="Compress Path Data", command=compressButton).grid(
    row=row, column=col, sticky="W", padx=2, pady=5)
col += 1
tkinter.Button(bf, text="Save Path Data (pose)    ", command=savePoseButton).grid(
    row=row, column=col, sticky="W", padx=2, pady=5)
col += 1
tkinter.Button(bf, text="Save Path Data (json)    ", command=saveJsonButton).grid(
    row=row, column=col, sticky="W", padx=2, pady=5)

# put the data on the screen
gw.grid(row=0,  column=0)
bf.grid(row=1,  column=0, sticky='W')

master.mainloop()  # needed for tkinter to plot the graph and buttons
