import os
import re
import datetime
import flags
import parseDSEvents
import parseDSLogs
import db
import sys
import getopt
import utils

def printShortHelp():
     print("python main.py -a -c -d<day> -d9-10 -D -h -l -L" +
          " -m<month> -r -S -s -y<year> [path to search]")

def printLongHelp():
    print()
    printShortHelp()
    print()
    print("-a put all data in one data base table vs each file to own table")
    print("-c make csv file with all of data")
    print("-d only process files matching the days parameter")
    print("   for the day parameter you can specify a range -d8-10")
    print("-D make a data base of the data")
    print("-h show this help information")
    print("-l show Debug (log) data")
    print("-L show data from logs")
    print("-m only process files matching the month parameter")
    print("-r process (recurse) all files in path")
    print("-S process dslog files -- currents / status")
    print("-s do not process dsevents files - tools process dsevents by default")
    print("-y only process file matching the year parameter -- must be 4 digit")
    print()

def processOptions():
    flags.year = datetime.datetime.now().strftime('%Y')
    flags.month = datetime.datetime.now().strftime('%m')
    flags.day = datetime.datetime.now().strftime('%d')
    try:
        opts, args = getopt.getopt(sys.argv[1:], "aDhlLrsSc:m:d:y:")
        if(len(args) >= 1):
            flags.path = args[0]
    except:
        print("Error: should be  python main.py -a -D -h -l -L -r -s -S -c<csvfile> -m<month> -d<day> -d<start-end> path")
        sys.exit(2)
    flags.dayParm = False
    flags.monthParm = False
    for opt, arg in opts:
        if opt == '-a':
            flags.allInOne = True
        if opt == '-c':
            flags.makeCSV = True
            if(len(arg) > 0):
                flags.CSVFile = arg
        if opt == '-d':
            flags.day = arg
            flags.dayParm = True
        if opt == '-D':
            flags.makeDB = True
        if opt == '-h':
            printLongHelp()
        if opt == '-L':
            flags.showLogs = True
        if opt == "-l":
            flags.debug = True
        if opt == '-m':
            flags.month = arg
            flags.monthParm = True
        if opt == '-s':
            flags.dsevents = False
        if opt == '-S':
            flags.dslogs = True
        if opt == '-y':
            flags.year = arg
   

def processFiles(argv,  fileType):
    exp = utils.getRegularExpression(
            flags.year, flags.month, flags.day, flags.monthParm, flags.dayParm, fileType)
    #flags.path = "."
    files = utils.getListOfFiles(flags.path, exp)
    print("Start argv:%s RegExp:%s Found %d Files" % (argv, exp,  len(files)))
    if flags.debug:
        for fn in files:
            print(fn)
    if flags.makeDB:
        db.db.createConnection("data.db")
        table = "allData_" + fileType
        db.db.dropTable(table)
        if fileType == "dsevents":
            db.db.createEventDataTable(table)
        if fileType == "dslog":
            db.db.createLogDataTable(table)
        db.db.createFileDataTable("files")
        db.db.connection.commit()
    utils.doFiles(files, fileType)
    if flags.makeDB:
        print("Close out DB")
        db.db.connection.commit()
        db.db.closeConnection()


def main(argv):
    if len(argv) == 0:
        printShortHelp()
    processOptions()
    if flags.dsevents:
        processFiles(argv, "dsevents")
    if flags.dslogs:
        processFiles(argv,  "dslog")

if __name__ == "__main__":
    main(sys.argv[1:])
