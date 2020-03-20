import sqlite3
import numpy

print("Add some data to an sqlite db")
# Array of 4 columns and 100 rows
data = numpy.random.rand(100, 4)

# Create a sample database
conn = sqlite3.connect('sample.db')
cursor = conn.cursor()

# Create a new table with four columns
cursor.execute(
    '''create table if not exists data (field1 real, field2 real, field3 real, field4 real)''')
cursor.execute("delete from data")
conn.commit()

# Insert the data array into the 'data' table
cursor.executemany('''insert into data values (?, ?, ?, ?)''',
                   map(tuple,    data.tolist()))
conn.commit()

cursor.execute('SELECT * from data')
alist = cursor.fetchall()
print("Number of elements:", len(alist))
print(alist[0])
data1 = numpy.array(alist)
print(data1[0])
print(numpy.allclose(data, data1))
cursor.close()
conn.close()
