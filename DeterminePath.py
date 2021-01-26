import math
import time
import json
import xmltodict
import sys
print("Python version", sys.version)

def makeCode(path, fileName):
    for point in path:
        print("new Pose2d(%.2f, %.2f, Rotation2d.fromDegrees(%.1f))," % (point['X'], point['Y'], point['Angle']))

def distance(point):
    return math.sqrt(point[0] * point[1] + point[1] * point[1])

def angle(p1, p2):
    return math.degrees(math.atan2(p1[0] - p2[0], p1[1]-p2[1]))

def parseXML(fileName):
    print("Read and Parse Path Data from File:" + fileName)
    with open(fileName) as fd:
        a = xmltodict.parse(fd.read())
        p = a['Path']['Waypoint']
        path = []
        for itm in p:
            print(itm['X'],itm['Y'],itm['Angle'])
            path.append({'X':float(itm['X']), 'Y':float(itm['Y']), 'Angle':float(itm['Angle'])})
        return path

def parseJSON(fileName):
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
    totalDist = distance(points[0])
    path = []
    for i in range(3, len(points), 3):
        a = points[i]
        dist = distance(a)
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
        path.append({'X':a[0] * 2.5 * 5.5 / 4.17 , 'Y':a[1], 'Angle':angle1})
    return path

fileName = "Barrel.path"
path = parseJSON(fileName)
makeCode(path, fileName)
fileName = "BarrelRacePath.xml"
path = parseXML(fileName)
makeCode(path, fileName)
