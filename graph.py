
import numpy
import sqlite3
import matplotlib
import matplotlib.pyplot as plt

# get data from table
conn = sqlite3.connect('data.db')
cursor = conn.cursor()
# Create SQL string for reading data from data base
s = "time,battery,current,"
for i in range(0,16):
    s += "pdp%d," % (i)
sql = "SELECT %s from allData_dslog;" % (s[0:-1])
print("SQL:", sql)
# Do the actual read from the data base
cursor.execute(sql)
alist = cursor.fetchall()
# Close out the data base
cursor.close()
conn.close()
print("Number of elements:", len(alist))
data1 = numpy.array(alist) # Put the data in a numpy array in preparation for grpahing
# Format the numpy array
float_formatter = "{:.1f}".format
numpy.set_printoptions(formatter={'float_kind':float_formatter})
print(alist[0]) # Print the first line for debug purposes
# Create the x axis for the Graph using the date from the data
t = [row[0] for row in alist]
for i in range(0,len(t)):
    t[i] = t[i][11:19]
t = numpy.arange(0, len(t))
# Create the Y data for the graph
s = [row[2:10] for row in alist]
# Graph the data
fig, ax = plt.subplots()
ax.plot(t, s)
ax.set(xlabel='time (s)', ylabel='Current (Amps)',
       title='Current for the PDP')
ax.grid()
# Save a png of the graph for debug
fig.savefig("test.png")
# Place the graph on the screen
plt.show()
