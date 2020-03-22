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
plt.subplot(311)
plt.plot(t, s1)
plt.subplot(312)
plt.plot(t, s2)
plt.subplot(313)
plt.plot(t, s3)

plt.show()