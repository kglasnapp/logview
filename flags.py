# Global flags for the log viewer
debug = False # flag true when user would like to see debug data
makeDB = False # flag true when user wants to make a sqlite data base
makeCSV = False # flag true when user wants to make a .csv file of the data
CSVFile = 'data.csv' # Default csv file name
allInOne = False # flag true when user wants to see all data in one database 
showLogs = False # flag true when user wants to see detailed logs
robotType = '' # set when a robot type is seen in dsevents file
compiled = '' # set when a compiled date number is seen in dsevents file
version = '' # set when a version number is seen in dsevents file
year = 2020 # value of the year 
month = 0 # value of the month to search for,  set by the -m option
day = 0 # value of the day to search for, set by the -d option
path = ""  # path in which the user wants to search for dsevents or dslog files
monthParm = False # a -m month option was seen
dayParm = False # a -d day option was seen
dsevents = True # Process dsevents files -- default is True, set -s flag to not process dsevents
dslogs = False # Process dslog files
