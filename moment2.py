#from tkinter import *
import tkinter
import math
import time
import json


class Point:
    # Class to define a point of a radius and color with a label
    global w

    def __init__(self, x, y, r, color, label):
        self.x = x
        self.y = y
        if label == "B":
            setParm("BX", x)
            setParm("BY", y)
        if label == "C":
            setParm("CX", x)
            setParm("CY", y)
        self.color = color
        self.label = label
        self.r = r
        r = r * 10
        self.ov = w.create_oval(
            rx(self.x)-r, ry(self.y)+r, rx(self.x)+r, ry(self.y)-r, fill=color)
        self.textBox = w.create_text(
            rx(self.x) + r * 2, ry(self.y) + r * 2, text=label)

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


def callback(event):
    # Called with the mouse is moved
    move(event)
    draw(inAngle)


def sind(a):

    # get sin of angle in degrees
    return math.sin(math.radians(a))


def cosd(a):
    # get cos of angle in degrees
    return math.cos(math.radians(a))


def entrycallback(event, arg):
    # Called when data is changed
    global inAngle
    v = float(objects[arg].get())
    print("Update parm '%s' to %.2f" % (arg, v))
    setParm(arg, v)
    if arg == 'Bar Angle':
        inAngle = v
    draw(inAngle)


def move(event):
    global pc
    pc.move(sx(event.x), sy(event.y))


def determineForce():
    # Determine the forces that the cylinder can provide
    cylinderDia = getParm("Cylinder Inner Dia")
    cylinderRod = getParm("Cylinder Rod Dia")
    psi = getParm("Cylinder PSI")
    forceIn = psi * math.pi * ((cylinderDia - cylinderRod) / 2) ** 2
    forceOut = psi * math.pi * (cylinderDia / 2) ** 2
    setParm('Max Force In', forceIn)
    setParm('Max Force Out', forceOut)
    return [forceIn, forceOut]


def zoom(delta):
    # Zoom the screen based upon delta
    global aw, ah
    aw += delta
    ah += delta
    setParm('AW', aw)
    setParm('AH', ah)
    draw(inAngle)


def zoomPlus():
    # Hit the button zoom+
    zoom(-5)


def zoomMinus():
    # Hit the button zoom-
    zoom(5)


def saveData():
    # save data to fileName
    p = {}
    s = ''
    for key in parms:
        p[key] = float(getParm(key))
        s += "'%s':%s " % (key, p[key])
    print("Save file:", fileName, s)
    with open(fileName, "w") as outfile:
        json.dump(p, outfile)


def restoreData():
    # restore data from the file: filename
    try:
        f = open(fileName, 'r')  # Opening JSON file
        p = json.load(f)
    except:
        print("Unable to find file %s" % (fileName))
        return
    print("Read in Jason Data")
    s = ""
    # Iterating through the json
    for key in p:
        s += "'%s':%s " % (key, p[key])
        parms[key][0] = p[key]
    print("Restored:", s)
    f.close()


def setParm(parm, value):
    # Update a paramter in parms and on screen
    parms[parm][0] = round(value, 2)
    objects[parm].set(round(value, 2))


def getParm(parm):
    # Get a paramter
    return parms[parm][0]


def distance(p1, p2):
    # determine distance between two points
    return math.sqrt((p1.x-p2.x) ** 2 + (p1.y-p2.y) ** 2)


def rx(p):
    # get a point on the screen given a x coordinate
    return (tw * .5 / aw) * p + tw / 2


def ry(p):
    # get a point on the screen given a y coordinate
    return (-th * .5 / ah) * p + th / 2


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


def stop():
    global stopFlag
    stopFlag =True


def simulate():
    global stopFlag
    startAngle = normalizeAngle(getParm("Bar Angle Low"))
    endAngle = getParm("Bar Angle High")
    angle = startAngle
    while angle <= endAngle:
        draw(angle)
        angle += 1
        time.sleep(.1)
        if(stopFlag):
            stopFlag = False
            return
    while angle >= startAngle:
        draw(angle)
        angle -= 1
        time.sleep(.1)
        if(stopFlag):
            stopFlag = False
            return


def toggleAngle():
    global inAngle
    if inAngle == getParm("Bar Angle Low"):
        inAngle = getParm("Bar Angle High")
    else:
        inAngle = getParm("Bar Angle Low")
    draw(inAngle)

# get the angle between two line pb represents the included angle


def getAngle(pa, pb, pc):
    dab = distance(pa, pb)
    dbc = distance(pb, pc)
    dac = distance(pa, pc)
    return math.degrees(math.acos((dac * dac - dbc * dbc - dab * dab) / (-2 * dbc * dab)))


def drawGrid(p):
    offset = 2
    for i in range(-int(ah), +int(ah), offset):
        p.create_line(rx(-aw), ry(i), rx(aw), ry(i),
                      width=1, fill="light gray")
    for i in range(-int(aw), int(aw), offset):
        p.create_line(rx(i), ry(-ah), rx(i), ry(ah),
                      width=1, fill="light gray")
        # Draw Line at the bottom of the graph
    w.create_line(rx(-aw), ry(-ah), rx(aw), ry(-ah), width=2, fill="black")


def draw(inAngle):
    global w, pc, pb, f
    determineForce()
    master.update()
    w = tkinter.Canvas(master, width=tw, height=th)
    w.bind("<Button-1>", callback)
    w.bind("<B1-Motion>", move)
    drawGrid(w)
    barLength = getParm("Bar Length")
    angle = math.radians(inAngle)
    bx = math.sin(angle) * barLength
    by = math.cos(angle) * barLength
    pa = Point(0, 0, .5, "red", "A")
    pb = Point(bx, by, .5, "blue", "B")
    pw = Point(bx, by - 5, .5, "purple", "Weight=" +
               str(getParm("Weight on Bar")))
    Line(pa, pb, 4, "black", "Bar")  # Lifting bar
    Line(pb, pw, 4, "blue", "Bar")  # Weight
    # Draw the Cylinder
    if pc == None:
        pc = Point(getParm("CX"), getParm("CY"), .5, "purple", "C")
    else:
        pc = Point(pc.x, pc.y, .5, "purple", "C")
    # Calculate the force on the sylinder
    angleABC = getAngle(pa, pb, pc)
    angleABW = getAngle(pw, pb, pa)
    setParm("Angle ABC", angleABC)
    setParm("Angle ABW", angleABW)
    force = getParm("Weight on Bar") * sind(angleABW)/sind(angleABC)
    setParm("Cylinder Force", force)
    # Colorize the cylinder paramter based upon the force
    color = "light green"
    if force > getParm("Max Force In") * .7:
        color = "yellow"
    if force > getParm("Max Force In") * .9:
        color = "red"
    entries["Cylinder Force"]['bg'] = color
    # Draw the cylinder
    lbc = Line(pb, pc, 4, "green", "Cylinder")
    # Draw the rod of the Cylinder
    pd = lbc.offset(getParm('Cylinder Length'))
    lcd = Line(pc, pd, 15, "gray", "Base")
    # Update the parms that have changed
    setParm("Bar Angle", inAngle)
    # Colorize the cylinder i.e. make part red if they exceed the length and stroke of the cylinder
    cExt = distance(pb, pc)
    cStroke = getParm("Cylinder Stroke")
    cLength = getParm("Cylinder Length")
    if cExt < cLength:
        w.itemconfig(lcd.getLine(), fill="red")
    if cStroke + cLength <= cExt:
        w.itemconfig(lbc.getLine(), fill="red")
    setParm("Cylinder Extent", cExt)
    # Place the data on the screen
    w.grid(row=0,  column=0)
    f.grid(row=1,  column=0, sticky='W')


def widgetsToScreen():
    # Put the widgets on the screen
    global f
    r = 1
    c = 0
    # Show the paramters
    for key in parms:
        p = parms[key]
        objects[key] = tkinter.StringVar()
        objects[key].set(getParm(key))
        op = ""
        if len(p) == 2:
            op = p[1]
        if op != "H":
            tkinter.Label(f, text=key + ": ").grid(row=r, column=c, sticky='E')
            e = tkinter.Entry(f, width=15, textvariable=objects[key])
            entries[key] = e
            if op == "RO":
                e['bg'] = 'light gray'
            e.grid(row=r, column=c+1, sticky='W')
            e.bind('<FocusOut>', lambda event,
                   arg=key: entrycallback(event, arg))
            e.bind('<Return>', lambda event,
                   arg=key: entrycallback(event, arg))
            c += 2
            if c > 6:
                r += 1
                c = 0
    r += 1
    c = 0
    tkinter.Button(f, text="Zoom +", command=zoomPlus).grid(
        row=r, column=c, sticky="W", padx=2, pady=5)
    c += 1
    tkinter.Button(f, text="Zoom -", command=zoomMinus).grid(
        row=r, column=c, sticky="W", padx=2, pady=5)
    c += 1
    tkinter.Button(f, text="Save Data", command=saveData).grid(
        row=r, column=c, sticky="W", padx=2, pady=5)
    c += 1
    tkinter.Button(f, text="Toggle Angle", command=toggleAngle).grid(
        row=r, column=c, sticky="W", padx=2, pady=5)
    c += 1
    tkinter.Button(f, text="Simulate", command=simulate).grid(
        row=r, column=c, sticky="W", padx=2, pady=5)
    c += 1
    tkinter.Button(f, text="Stop", command=stop).grid(
        row=r, column=c, sticky="W", padx=2, pady=5)

stopFlag = False
pa = pb = pc = pd = None
tw = 800
th = 600
fileName = "parms.json"
parms = {"Bar Length": [15], "Weight on Bar": [10], "Bar Angle Low": [355], "Bar Angle High": [95], "Cylinder PSI": [50], 
         "Cylinder Length": [10], "Cylinder Stroke": [8], "Cylinder Inner Dia": [1], "Cylinder Rod Dia": [.08],
         "Max Force In": [10, "RO"], "Max Force Out": [10, "RO"], "Cylinder Force": [10, "RO"], "Bar Angle": [90],  "Cylinder Extent": [10], 
         "Angle ABC": [0, "RO"], "Angle ABW": [0, "RO"], "BX": [10, 'RO'], "BY": [10, 'RO'], "CX": [-10, "RO"], "CY": [10, "RO"],
         "AW": [20, "H"], "AH": [20, "H"]}
objects = {}
entries = {}
restoreData()  # restore the data from the file
aw = getParm("AW")
ah = getParm("AH")
master = tkinter.Tk()
master.title(
    "Linkage Analysis Tool  --  Click any point to move the Cylinder Pivot point")
f = tkinter.Frame(master)
widgetsToScreen()
inAngle = getParm('Bar Angle')
draw(inAngle)
master.mainloop()
