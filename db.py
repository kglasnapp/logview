import os
import datetime
import re  # Regular expression library
import sqlite3
from sqlite3 import Error
import sys

class DB:
    connection = None
    cursor = None
    table = ''
    fileTable = ''
   
    def createConnection(self, db_file):
       # create a database connection to a SQLite database
        try:
            self.connection = sqlite3.connect(db_file)
            print("sqlite3 version:" + str(sqlite3.version))
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

    def createLogDataTable(self, table):
        print("Create table:" + table)
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

    def addData(self, date, deltaTime, recType, data, fileNum, misc):
        task = (date, deltaTime, recType, data, fileNum, misc)
        sql = 'INSERT INTO ' + self.table + \
            ' (beginDate, deltaTime, type, logData, fileNum, misc)  VALUES(?,?,?,?,?,?)'
        self.cursor = self.connection.cursor()
        self.cursor.execute(sql, task)

    def createFileDataTable(self, fileTable):
        print("Create table:" + fileTable)
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
            fileDate = datetime.datetime.fromtimestamp(fileDate).strftime("%m/%d %H:%M:%S")
            task = (date, fileName, fileSize, fileDate,
                    lines, robotType, compiled, version)
            sql = 'INSERT INTO ' + self.fileTable + \
                ' (beginDate, fileName, fileSize, fileDate, lines, robotType, compiled, version)  VALUES(?,?,?,?,?,?,?,?)'
            self.cursor = self.connection.cursor()
            self.cursor.execute(sql, task)
            return self.cursor.lastrowid

    def getFileNameIndex(self, fileName):
        cur = self.connection.cursor()
        cur.execute(
            "SELECT id,fileName FROM Files WHERE fileName=?", (fileName, ))
        rows = cur.fetchall()
        if(len(rows) == 1):
            return rows[0][0]
        return None

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


db = DB()