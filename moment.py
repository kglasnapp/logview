import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons, TextBox
import math
import cmath


class point:
    x = 0
    y = 0
    text = ""
    color = "red"

    def __init__(self, x, y, color, name):
        self.x = x
        self.y = y
        self.color = color
        self.name = name



def distance(a,b):
    return math.sqrt((a.x - b.x) **2 + (a.y - b.y) ** 2)
    
   
def angle(a,b,c):
    dac = distance(a,c)
    dbc = distance(b,c) 
    dab = distance(a,b)
    return  math.degrees(math.acos((dac**2 - dab**2 - dbc** 2) / (-2 * dab * dbc)))


def draw():
    # plt.annotate(s='', xy=(sBar.val,sBar.val), xytext=(0,0), arrowprops=dict(arrowstyle='->'))
    ax.clear()
    ax.axis([-size, size, -size, size])
    ax.grid()
    BX = float(sBar.text) * math.sin(math.radians(sAngle.val))
    BY = float(sBar.text) * math.cos(math.radians(sAngle.val))
    # Plot the Bar
    ax.plot([0, BX], [0, BY], lineWidth=3, color="blue")
    CX = float(sCylinderX.text)
    CY = float(sCylinderY.text)
    # Plot the Cylinder
    ax.plot([CX, BX], [CY, BY], lineWidth=3, color="green")
    # Plot the Cylinder Body
    cDx = BX - CX
    cDy = BY - CY
    # cSlope = cDy / cDx
    # cIntercept = BY - cSlope * BX
    cAngle = math.degrees(math.atan2(cDy, cDx))
    cLength = math.sqrt(cDx * cDx + cDy * cDy)

    bx = float(sCylinderLength.text) * math.cos(math.radians(cAngle))
    by = float(sCylinderLength.text) * math.sin(math.radians(cAngle))
    print("Angle", cAngle, "Len", cLength)

    if cLength < (float(sCylinderLength.text) + float(sCylinderStroke.text)):
        c ="green"
    else: 
        c= "red"
   
    ax.plot([CX, BX], [CY, BY], lineWidth=3, color=c)

    if cLength > float(sCylinderLength.text):
        c ="gray"
    else: 
        c= "red"
          
    ax.plot([CX, CX+bx], [CY, CY+by], lineWidth=6, color=c)

    # ax.annotate('local max', xytext=(0,0), xy=(sBar.val ,sBar.val),
    #        arrowprops=dict(facecolor='red'),)
    # print(BX, BY, 0, BY-sWeight.val)
    ax.arrow(BX, BY, 0, -float(sWeight.text), color='black', head_length=1,
             head_width=1, lineWidth=4, length_includes_head=True)
    # plt.annotate(s='', xy=(.5,.5), xytext=(0,0), arrowprops=dict(arrowstyle='->'))
    # ax.arrow(10, -10, -20, 20, color='red', head_length=1,
    #     head_width=1, length_includes_head=True)


def update(val):
    draw()


def reset(event):
    sWeight.reset()
    sBar.reset()



pA = point(0,0, "red", "A")
pB = point( 0,4, "green", "B")
pC = point( 3,4, "gray", "C")
print(pC.x)
print(distance(pA,pC))
print(angle(pB,pA,pC))
print(angle(pA,pB,pC))
print(angle(pA,pC,pB))

v = 3 + 4j
w = 5 + 8.666j
print(cmath.polar(v))
print(cmath.polar(cmath.acos(v)))

vector_1 = [4, 3]
vector_2 = [4, 0]

unit_vector_1 = vector_1 / np.linalg.norm(vector_1)
unit_vector_2 = vector_2 / np.linalg.norm(vector_2)
dot_product = np.dot(unit_vector_1, unit_vector_2)
angle = math.degrees(np.arccos(dot_product))

print("dot angle", angle, unit_vector_1, np.linalg.norm(vector_1), dot_product)


size = 30
fig, ax = plt.subplots()
# plt.figure(figsize={6,6})
plt.subplots_adjust(left=0.25, bottom=0.35)
axcolor = 'lightgoldenrodyellow'
axAngle = plt.axes([0.25, 0.05, 0.65, 0.03], facecolor=axcolor)

axWeight = plt.axes([0.15, 0.20, 0.1, 0.05], facecolor=axcolor)
axBar = plt.axes([0.45, 0.20, 0.1, 0.05], facecolor=axcolor)

axCylinderX = plt.axes([0.15, 0.12, 0.1, 0.05], facecolor=axcolor)
axCylinderY = plt.axes([0.30, 0.12, 0.1, 0.05], facecolor=axcolor)
axCylinderLength = plt.axes([0.50, 0.12, 0.1, 0.05], facecolor=axcolor)
axCylinderStroke = plt.axes([0.70, 0.12, 0.1, 0.05], facecolor=axcolor)

sWeight = TextBox(axWeight, 'Weight: ', initial="5")
sBar = TextBox(axBar, 'Length of Bar: ', initial="20")
sAngle = Slider(axAngle, 'Angle of Bar', 0, 360, valinit=30)
sCylinderX = TextBox(axCylinderX, 'Cylinder X: ', initial="-3")
sCylinderY = TextBox(axCylinderY, 'Y: ', initial="3")
sCylinderLength = TextBox(axCylinderLength, 'Length: ', initial="12")
sCylinderStroke = TextBox(axCylinderStroke, 'Stroke: ', initial="10")
draw()
# sWeight.on_changed(update)
# sBar.on_changed(update)
sAngle.on_changed(update)
plt.show()
