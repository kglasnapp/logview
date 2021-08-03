import matplotlib.pyplot as plt
import numpy as np

t = np.arange(0, 360, 1)
s1 = np.sin(np.radians(t))
s2 = np.cos(np.radians(t))
s3 = np.tan(np.radians(t))
tr = 3
si = s3 > tr
s3[si] = tr
si = s3 < -tr
s3[si] = -tr
plt.figure(1)
plt.subplot(411)
plt.plot(t, s1)
plt.subplot(412)
plt.plot(t, s2)
plt.subplot(413)
plt.plot(t, s3)
x = [1,2,3,4,5,6,7,8,9]
y = [2,4,6,8,10,12,14,16,18]
plt.subplot(414)
plt.plot(x,y)

plt.show()