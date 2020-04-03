fn = "Z:\\CNC\\CNC Router Parts\\GCode\\BrushFrameV3.tap"
f = open(fn, "r")
for x in f:
    if x == '':
        continue
    if x[0] == 'X' or x[0] == 'Y' or x[0] =='Z':
       continue
    x2 = x[0:3]
    if x2 in 'G0 G1 G2 G3 ':
        continue
    print(x[:-1])
