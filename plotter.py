import tkinter

tw = 0 # Screen width pixels
th = 0 # Screen height pixels
aw = 0 # Screen width feet
ah = 0 # Screen height feet
gw = None 

def setPlotterParms(_w, _tw,_th,_aw,_ah):
    global gw,tw,th,aw,ah
    gw = _w
    tw = _tw
    th = _th
    aw = _aw
    ah = _ah
    


class Point:
    # Class to define a point of a radius and color with a label
    global gw

    def __init__(self, x, y, r, color, label, textOff=[2, 2]):
        self.x = x
        self.y = y
        self.color = color
        self.label = label
        self.r = r
        r = r * 10
        self.ov = gw.create_oval(
            rx(self.x)-r, ry(self.y)+r, rx(self.x)+r, ry(self.y)-r, fill=color)
        self.textBox = gw.create_text(
            rx(self.x) + r * textOff[0], ry(self.y) + r * textOff[1], text=label)

    def move(self, x, y):
        gw.delete(self.ov)
        gw.delete(self.textBox)
        self.ov = gw.create_oval(x-self.r, y+self.r, x +
                                self.r, y-self.r, fill=self.color)
        self.textBox = gw.create_text(
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
        self.myLine = gw.create_line(rx(self.p1.x), ry(self.p1.y), rx(self.p2.x), ry(self.p2.y),
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


# methods to scale data on screen 

def rx(p):
    # get a point on the screen given a x coordinate
    # convert feet to pixels
    return tw * p / aw


def ry(p):
    # get a point on the screen given a y coordinate
    # convert feet to pixels
    return th * (ah-p) / ah


def sx(p):
    # given a point on the screen in x get a normalize x value
    # convert pixels to feet
    return (aw * p * 2) / tw - aw


def sy(p):
    # given a point on the screen in y get a normalize y value
    # convert pixels to feet
    return (-ah * p * 2) / th + ah


def normalizeAngle(angle):
    a = angle + 180.0 % 360.0
    if a < 0.0:
        a += 360.0
    a = a - 180.0
    if a > 180:
        a -= 360
    return a

