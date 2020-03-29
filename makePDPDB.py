import sqlite3
from sqlite3 import Error

try:
    connection = sqlite3.connect("data.db")
except Error as e:
    print(e)
# create a table from the create_table_sql statement
sql = "CREATE TABLE IF NOT EXISTS pdpMap (id integer PRIMARY KEY AUTOINCREMENT, pdpNumber integer, pdpName text);"
try:
    cursor = connection.cursor()
    cursor.execute(sql)
except Error as e:
    print(e)
# Code to add data for each of the pdp's
pdp = [[0, "Left"],[1, "Right"]]
#insert the data to data base
print(pdp[1][1])
connection.commit()
connection.close()
