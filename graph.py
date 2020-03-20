import sqlite3
import numpy
import matplotlib
import matplotlib.pyplot as plt



# get data from table
conn = sqlite3.connect('data.db')
cursor = conn.cursor()
s = "time,battery,current,"
for i in range(0,16):
    s += "pdp%d," % (i)
sql = "SELECT %s from allData_dslog;" % (s[0:-1])
print("SQL:", sql)
cursor.execute(sql)
alist = cursor.fetchall()
print("Number of elements:", len(alist))
print(alist[0])
data1 = numpy.array(alist)
print(data1[0])
float_formatter = "{:.1f}".format
numpy.set_printoptions(formatter={'float_kind':float_formatter})
cursor.close()
conn.close()
print(alist[0])
t = [row[0] for row in alist]
for i in range(0,len(t)):
    t[i] = t[i][11:19]
t = numpy.arange(0, len(t))
print(t[0])
s = [row[2:10] for row in alist]
for r in s:
    if r[0] > 200:
        print(r)

fig, ax = plt.subplots()
ax.plot(t, s)

ax.set(xlabel='time (s)', ylabel='Current (Amps)',
       title='Current for the PDP')
ax.grid()

fig.savefig("test.png")
plt.show()
