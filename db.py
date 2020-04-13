import os
import datetime
import re  # Regular expression library
import sqlite3
from sqlite3 import Error
import sys
import flags


class DB:
    connection = None
    cursor = None
    table = ''
    fileTable = ''

    def createConnection(self, db_file):
       # create a database connection to a SQLite database
        try:
            self.connection = sqlite3.connect(db_file)
            #print("sqlite3 version:" + str(sqlite3.version))
        except Error as e:
            print(e)
        finally:
            return self.connection

    def closeConnection(self):
        if self.connection == None:
            self.connection.close()

    def deleteData(self, table):
        # delete all records from a table
        sql = "DELETE FROM " + table + ";"
        try:
            self.cursor = self.connection.cursor()
            self.cursor.execute(sql)
        except Error as e:
            print(e)

    def dropTable(self, table):
        # drop a table from the data base
        print("Drop table:" + table)
        sql = "DROP TABLE IF EXISTS " + table + ";"
        try:
            self.cursor = self.connection.cursor()
            self.cursor.execute(sql)
        except Error as e:
            print(e)

    def createEventDataTable(self, table):
        self.table = table
        # create a table from the create_table_sql statement
        sql = "CREATE TABLE IF NOT EXISTS " + table + """ (
            id integer PRIMARY KEY AUTOINCREMENT,
            beginDate text,
            deltaTime text,
            type text,
            logData text NOT NULL,
            fileNum integer,
            misc text); """
        try:
            self.cursor = self.connection.cursor()
            self.cursor.execute(sql)
        except Error as e:
            print(e)
        self.createIndex("dsEventsFiles", table, "fileNum")

    def addEventData(self, date, deltaTime, recType, data, fileNum, misc):
        task = (date, deltaTime, recType, data, fileNum, misc)
        sql = 'INSERT INTO ' + self.table + \
            ' (beginDate, deltaTime, type, logData, fileNum, misc)  VALUES(?,?,?,?,?,?)'
        self.cursor = self.connection.cursor()
        self.cursor.execute(sql, task)

    def createFileDataTable(self, fileTable):
        self.fileTable = fileTable
        # create a table from the create_table_sql statement
        sql = "CREATE TABLE IF NOT EXISTS " + fileTable + """ (
            id integer PRIMARY KEY AUTOINCREMENT,
            beginDate text,
            fileName text,
            fileSize integer,
            fileDate text,
            lines integer,
            robotType text,
            compiled text,
            version text); """
        try:
            self.cursor = self.connection.cursor()
            self.cursor.execute(sql)
        except Error as e:
            print(e)
            return
        self.createIndex("fileName", fileTable, "fileName")

    def addFileData(self, path, date, lines, robotType, compiled, version):
        fileName = os.path.basename(path)
        idx = self.getFileNameIndex(fileName)
        if(idx):
            # UPDATE table SET column_1 = new_value_1,     column_2 = new_value_2  WHERE     search_condition
            sql = "Update %s set lines='%s', robotType='%s', compiled='%s', version='%s' where fileName='%s'" % (
                self.fileTable, lines, robotType, compiled, version, fileName)
            self.cursor = self.connection.cursor()
            self.cursor.execute(sql)
            return idx
        else:
            fileSize = os.path.getsize(path)
            fileDate = os.path.getmtime(path)
            fileDate = datetime.datetime.fromtimestamp(
                fileDate).strftime("%m/%d %H:%M:%S")
            task = (date, fileName, fileSize, fileDate,
                    lines, robotType, compiled, version)
            sql = 'INSERT INTO ' + self.fileTable + \
                ' (beginDate, fileName, fileSize, fileDate, lines, robotType, compiled, version)  VALUES(?,?,?,?,?,?,?,?)'
            self.cursor = self.connection.cursor()
            self.cursor.execute(sql, task)
            db.connection.commit()
            return self.cursor.lastrowid

    def getFileNameIndex(self, fileName):
        cur = self.connection.cursor()
        sql = "SELECT id,fileName FROM files WHERE fileName=?"
        try:
            cur.execute(sql, (fileName, ))
        except:
            print("Error: **** ", sql)
            sys.exit(0)
        rows = cur.fetchall()
        if(len(rows) == 1):
            return rows[0][0]
        return None

    def createLogDataTable(self, table):
        self.table = table
        # create a table from the create_table_sql statement
        # Time,Count,Trip,Loss,Battery,CPU,Trace,CAN,WiFi,MB,Current,
        # PDP 0,PDP 1,PDP 2,PDP 3,PDP 4,PDP 5,PDP 6,PDP 7,PDP 8,PDP 9,PDP 10,PDP 11,PDP 12,PDP 13,PDP 14,PDP 15
        sql = "CREATE TABLE IF NOT EXISTS " + table + """ (
            id integer PRIMARY KEY AUTOINCREMENT,
            fileNum integer, time text, count integer, trip numeric,
            loss numeric, battery numeric, cpu numeric, trace numeric,
            can numeric, wifi numeric, mb numeric, current numeric,
            pdp0 numeric, pdp1 numeric, pdp2 numeric, pdp3 numeric,
            pdp4 numeric, pdp5 numeric, pdp6 numeric, pdp7 numeric,  
            pdp8 numeric, pdp9 numeric, pdp10 numeric, pdp11 numeric,  
            pdp12 numeric, pdp13 numeric, pdp14 numeric, pdp15 numeric,           
            misc text); """
        try:
            self.cursor = self.connection.cursor()
            self.cursor.execute(sql)
        except Error as e:
            print("Error creating table:", table, e)
        self.createIndex("dslogFiles", table, "fileNum")

    s = "(fileNum, time,count,trip,loss,"
    s += "battery,cpu,trace,can,wifi,mb,current,"
    s += "pdp0,pdp1,pdp2,pdp3,pdp4,pdp5,pdp6,pdp7,"
    s += "pdp8,pdp9,pdp10,pdp11,pdp12,pdp13,pdp14,pdp15,misc)"
    s += "values (?,?,?,?,?,?,?,?,?,?,?,?,"
    s += "?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"

    def addLogData(self, data):
        sql = 'INSERT INTO ' + self.table + self.s
        self.cursor = self.connection.cursor()
        self.cursor.execute(sql, data)

    def renameTable(self, newName):
        sql = 'ALTER TABLE %s RENAME TO %s;' % (self.table, newName)
        print(sql)
        self.table = newName
        self.cursor = self.connection.cursor()
        self.cursor.execute(sql)

    def writeCSV(self, table, file):
        # Export as csv file
        with open(file, "wb") as write_file:
            cursor = self.connection.cursor()
            for row in cursor.execute("SELECT * FROM %s" % table):
                writeRow = " ".join([str(i) for i in row])
                write_file.write(writeRow.encode())

    def printCSV(self, table):
        self.cursor.execute("SELECT * FROM %s" % table)
        table = self.cursor.fetchall()
        print(table)

    def getData(self, table):
        self.cursor = self.connection.cursor()
        self.cursor.execute("SELECT * FROM %s" % table)
        table = self.cursor.fetchall()
        return table

    def createIndex(self, name, table, column):
        sql = "CREATE INDEX IF NOT EXISTS %s ON %s (%s);" % (
            name, table, column)
        try:
            self.cursor = self.connection.cursor()
            self.cursor.execute(sql)
        except Error as e:
            print("Error creating index:", name, e)

    # Create the needed databases


    def createDB(self, drop):
        db.createConnection(flags.mainDB)
        if drop:
            db.dropTable(flags.eventsTable)
            db.dropTable(flags.logTable)
            db.dropTable(flags.fileTable)
        db.createEventDataTable(flags.eventsTable)
        db.createLogDataTable(flags.logTable)
        db.createFileDataTable(flags.fileTable)
        db.connection.commit()


    def isFileInDB(self, path):
        fileName = os.path.basename(path)
        cur = self.connection.cursor()
        sql = "SELECT fileSize, fileDate FROM files WHERE fileName=?"
        try:
            cur.execute(sql, (fileName, ))
        except:
            print("Error: **** ", sql)
            sys.exit(0)
        rows = cur.fetchall()
        if(len(rows) == 1):
            fileSize = os.path.getsize(path)
            if fileSize != rows[0][0]:
                return False
            fileDate = os.path.getmtime(path)
            fileDate = datetime.datetime.fromtimestamp(
                fileDate).strftime("%m/%d %H:%M:%S")
            if fileDate != rows[0][1]:
                return False
            return True
        return False


db = DB()
