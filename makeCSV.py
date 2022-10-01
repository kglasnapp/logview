import dsFiles
import dseventsF
import db as db
import time
from tkinter import (END)

lines = 0
def makeAllFiles(files):
    print("Make a CSV of all data in all files")
    start = time.time()
    lines = 0
    numFiles = 0
    filesLB = files.getFilesList()
    saveFile = getSaveFile(filesLB[0])
    for f in filesLB:
       lines += makeCSV(f,saveFile)
       numFiles += 1
    print("Complete lines:%d files:%d seconds:%.3f" % (lines, numFiles, time.time()-start))
    
    
def makeSelectedFiles(files):
    print("Make CSV of all data in selected files")
    start = time.time()
    lines = 0
    numFiles = 0
    filesLB = files.getSelected()
    if len(filesLB) == 0:
        print("No Files are selected")
        return
    saveFile = getSaveFile(filesLB[0])
    for f in filesLB:
       lines += makeCSV(f,saveFile)
       numFiles += 1
    print("Complete lines:%d files:%d seconds:%.3f" % (lines, numFiles, time.time()-start))

def makeData(events):
    print("Make CSV of displayed data")
    start = time.time()
    lines = 0
    dataLB = events.getListBox()
    data = dataLB.get(0,END)
    if len(data) == 0:
        print("No data is displayed")
        return
    saveFile = getSaveFile("")
    f = open(saveFile, "w")
    for line in data:
        f.write(line + '\n')
        lines += 1
    f.close()
    print("Complete lines:%d seconds:%.3f" % (lines, time.time()-start))

    
def makeSelectedData(events):
    print("Make CSV of selected Data")
    start = time.time()
    lines = 0
    dataLB = events.getListBox()
    sel = dataLB.curselection()
    if len(sel) == 0:
        print("No data is delected")
        return
    saveFile = getSaveFile("")
    f = open(saveFile, "w")
    for idx in sel:
        line = dataLB.get(idx)
        f.write(line + '\n')
        lines += 1
    f.close()
    print("Complete lines:%d seconds:%.3f" % (lines, time.time()-start))


def getSaveFile(firstFile):
    return "data.csv"

def makeCSV(fileName, saveFile):
    lines = 0
    db.db.createConnection("data.db")
    cur = db.db.connection.cursor()
    cur.execute("Select id from files where fileName = '%s';" % (fileName))
    data = cur.fetchall()
    fileNum = data[0][0]
    f = open(saveFile, "a")
    cur.execute(
       "SELECT logData,id FROM allData_dsevents where fileNum = %d;" % (fileNum))
    data = cur.fetchall()
    f.write("********************* " + fileName + " ********************************************\n")
    for line in data:
        d = line[0]
        f.write(d + '\n')
        lines += 1
    f.close()
    return lines
        