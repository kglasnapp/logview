i = 10
j = 1
def sum(i):
    j = 1
    s = 0
    while j <= i:
        s += j
        j += 1
    return s

while j < 50:
    s = int(i * (i+1)/2)
    print (i,s, sum(i))
    i = i * 10
    j += 1
