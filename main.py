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

def main(argv):
    path = "."
    flags.year = datetime.datetime.now().strftime('%Y')
    flags.month = datetime.datetime.now().strftime('%m')
    flags.day = datetime.datetime.now().strftime('%d')
    try:
        opts, args = getopt.getopt(sys.argv[1:], "ahDslrm:d:y:")
        if(len(args) >= 1):
            path = args[0]
    except getopt.GetoptError:
        print("Error: should be  FRCLogToCSV -s -l -h -a -m <month> -d <day>")
        sys.exit(2)
    dayParm = False
    monthParm = False
    for opt, arg in opts:
        if opt == '-h':
            print("FRCLogToCSV -s -l -h -a -D -r -m <month> -d <day> path")
            print("-s show data from logs")
            print("-l show Debug (log) data")
            print("-h show this help information")
            print("-a put all data in one data base")
            print("-D make a data base of the data")
            print("-r process (recurse) all files in path")
            print("-m only process files matching the month parameter")
            print("-d only process files matching the days parameter")
            print("   for the day parameter you can specify a range -d8-9")
            print("-y only process file matching the year parameter -- must be 4 digit")
        if opt == '-d':
            print("Day:" + arg)
            flags.day = arg
            dayParm = True
        if opt == '-D':
            print("Make DB")
            flags.makeDB = True
        if opt == '-a':
            flags.allInOne = True
        if opt == '-m':
            print("Month:" + arg)
            flags.month = arg
            monthParm = True
        if opt == '-y':
            flags.year = arg
        if opt == '-s':
            flags.showLogs = True
        if opt == "-l":
            flags.debug = True

    # Find files to process
    exp = utils.getRegularExpression(flags.year, flags.month, flags.day, monthParm, dayParm, "dsevents")
    print("Regular Expression:", exp)
    files = utils.getListOfFiles(path, exp)
    if flags.debug:
        for fn in files:
            print(fn)
    print("Found ", len(files), " Files")
    if flags.makeDB:
        db.db.createConnection("data.db")
        table = "allData"
        db.db.dropTable(table)
        db.db.createLogDataTable(table)
        db.db.createFileDataTable("files")
        db.db.connection.commit()
    utils.doFiles(files, 'dsevents')
    if flags.makeDB:
        print("Close out DB")
        db.db.connection.commit()
        db.db.closeConnection()

print("Current Dir:", os.getcwd(), "argv:", sys.argv)
if __name__ == "__main__":
    main(sys.argv[1:])