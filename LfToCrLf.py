# Program to convert unix style line feeds into windows style carriage return line feeds

import sys
import os
import re


def convert(fn):
    fIn = open(fn, "r")
    s = ""
    lastX = ''
    for x in fIn:
        lastX = x
        l = len(lastX)
        x = x.replace("\r", '')
        x = x.replace("\n", '')
        if lastX == x:
            s += x
        else:
            s += x + '\n'

      #x = x.replace("")
    fIn.close()
    os.remove(fn)
    fOut = open(fn, "w")
    fOut.write(s)
    fOut.close()
    print("Converted %d characters in file %s" % (len(s), fn))


def getListOfFiles(dirName, reg):
    # create a list of file and sub directories
    # names in the given directory
    try:
        exp = re.compile(reg)
    except:
        print("Error -- Invalid regular expression:" + reg)
        sys.exit(0)
    try:
        listOfFile = os.listdir(dirName)
    except:
        print("Error -- Unable to find directory --> " + dirName)
        sys.exit(0)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath, reg)
        else:
            if(exp.match(fullPath)):
                allFiles.append(fullPath)
    return allFiles


dirName = sys.argv[1:][0]
if len(dirName) == 0:
    dirName = '.'
#dirName = "c:\\Temp\\2020-competition\\src\\main\\java\\frc\\robot\\"
print("Will convert linux based line feeds to windows base carriage return line feeds for all *.java file in dir:" + dirName)
files = getListOfFiles(dirName, ".*java$")
print("Found %d files" % (len(files)))
for fn in files:
    convert(fn)
