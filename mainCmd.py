import datetime
import getopt
import os
import re
import sys

import db
import flags
import parseDSEvents
import parseDSLogs
import utils


def printShortHelp():
    print(
        "python main.py -ce<csvfile> -cl<csvfile> -d9 -d8-9 -D -h -l -L -m3  -pe -pl -y2020 [path to search]")


def printLongHelp():
    print()
    printShortHelp()
    print()
    print("-c make csv file with all of data")
    print("-d only process files matching the days parameter")
    print("   for the day parameter you can specify a range -d8-10")
    print("-D make a data base of the data")
    print("-f process argument list as files")
    print("-h show this help information")
    print("-l show Debug (log) data")
    print("-L show data from logs")
    print("-m only process files matching the month parameter")
    print("-Pe process dsevents files")
    print("-pe do not process dsevents files")
    print("-Pl process dslog files -- default is to not process dslog")
    print("    dslog show motor currents and general robot status")
    print("-pl do not process dslog files")
    print("-y only process file matching the year parameter -- must be 4 digit")
    print()


def processOptions():
    # get current year, month, day
    flags.year = datetime.datetime.now().strftime('%Y')
    flags.month = datetime.datetime.now().strftime('%m')
    flags.day = datetime.datetime.now().strftime('%d')
    try:
        opts, args = getopt.getopt(sys.argv[1:], "c:d:DhlLm:p:P:y:")
        if(len(args) >= 1):
            flags.path = args[0]
        else:
            flags.path = '.'
    except:
        printLongHelp()
        sys.exit(2)
    flags.dayParm = False
    flags.monthParm = False
    for opt, arg in opts:
        if opt == '-a':
            flags.allInOne = True
        if opt[0:2] == '-c':
            if len(arg) > 1:
                if(arg[0:1] == 'e'):
                    flags.makeCSVEvents = True
                    flags.CSVEventsFile = arg[1:].strip()
                if(arg[0:1] == 'l'):
                    flags.makeCSVLog = True
                    flags.CSVLogFile = arg[1:].strip()
        if opt == '-d':
            flags.day = arg
            flags.dayParm = True
        if opt == '-D':
            flags.makeDB = True
        if opt == '-f':
            flags.files = True
        if opt == '-h':
            printLongHelp()
        if opt == '-L':
            flags.showLogs = True
        if opt == "-l":
            flags.debug = True
        if opt == '-m':
            flags.month = arg
            flags.monthParm = True
        if opt == '-P' and arg == 'e':
            flags.dsevents = True
        if opt == '-P' and arg == 'l':
            flags.dslogs = True
        if opt == '-p' and arg == 'e':
            flags.dsevents = False
        if opt == '-p' and arg == 'l':
            flags.dslogs = False
        if opt == '-y':
            flags.year = arg
    return args


def main(argv):
    if len(argv) == 0:
        printShortHelp()
        return
    args = processOptions()
    if flags.makeDB:
        db.createDB(flags.dropDataBase)
    if flags.files:
        utils.processListOfFiles(args)
    else:
        utils.processFiles(args, "dsevents")
        utils.processFiles(args, "dslog")
    if flags.makeDB:
        db.db.connection.commit()
        db.db.closeConnection()

if __name__ == "__main__":
    main(sys.argv[1:])
