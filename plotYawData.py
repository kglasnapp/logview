import matplotlib.pyplot as plt
import numpy as np

y1 = np.array([])
y2 = np.array([])
x = np.array([])
with open("yawData.txt") as file_in:
    i = 0
    for line in file_in:
        ar = line.split(' ')
        nav = float(ar[1].split(':')[1])
        bno = float(ar[2].split(':')[1])
        y1 = np.append(y1, nav)
        y2 = np.append(y2, bno)
        x = np.append(x,i)
        print(i,nav,bno)
        i += 1

plt.ylim([-90, 90])
plt.yticks(np.arange(-90, 91, 10))

plt.plot(x, y1)
plt.plot(x, y2)

plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.show()
