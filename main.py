# Best tkinter documentation is at - https://docs.python.org/3.9/library/tkinter.ttk.html

import tkinter as tk
from tkinter import Button, filedialog
import dseventsF
import dsFiles
import editIgnores
import flags
import utils
import db
import sys
import editPDPConfigTKSheet
import masterParms
import makeCSV

dirForLogs = "c:\\Users\\Public\\Documents\\FRC\\Log Files\\*"
dirForLogs = "..\\Sibling\\"


def createMenu(tab):
    menubar = tk.Menu()
    tab.config(menu=menubar)
    fileMenu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="File", menu=fileMenu)
    fileMenu.add_command(label="Import Selected Files", command=fileImport)
    fileMenu.add_command(label="Import dsevent (Robot Event Logs) Files",
                         command=lambda: directoryImport("*.dsevents"))
    fileMenu.add_command(label="Import dslog (Robot Power Status) Files",
                         command=lambda: directoryImport("*.dslog"))
    fileMenu.add_command(label="Import Files in Directory",
                         command=lambda: directoryImport(".*dslog|.*dsevents"))
    fileMenu.add_command(label="Save")
    fileMenu.add_separator()
    fileMenu.add_command(label="Exit", command=lambda: sys.exit(0))
    editMenu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Edit", menu=editMenu)
    editMenu.add_command(label="Edit Ignores", command=editIgnores.showForm)
    editMenu.add_command(label="Edit PDP Configs",
                         command=editPDPConfigTKSheet.showForm)
    csvMenu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="CSV Actions", menu=csvMenu)
    csvMenu.add_command(label="Make CSV All Files",
                        command=lambda: makeCSV.makeAllFiles(files))
    csvMenu.add_command(label="Make CSV Selected Files",
                        command=lambda: makeCSV.makeSelectedFiles(files))
    csvMenu.add_command(label="Make CSV Displayed Data",
                        command=lambda: makeCSV.makeData(events))
    csvMenu.add_command(label="Make CSV Selected Data",
                        command=lambda: makeCSV.makeSelectedData(events))
    helpMenu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Help", menu=helpMenu)
    helpMenu.add_command(label="About Us")


def fileImport():
    types = [("Robot log files", "*.dslog *.dsevents"), ("dsevents",
                                                         "*.dsevents"), ("dslog", "*.dslog"), ("All files", "*.*")]
    fileNames = tk.filedialog.askopenfilename(
        initialdir=dirForLogs, title="Select file", multiple=True, filetypes=types)
    if flags.debug:
        print("Files to Import", fileNames)
    flags.makeDB = True
    utils.processListOfFiles(fileNames)
    db.db.connection.commit()
    db.db.closeConnection()
    files.refresh()


def directoryImport(reg):
    types = [("", reg),  ("All files", "*.*")]
    files = tk.filedialog.askopenfilename(
        initialdir=dirForLogs, title="Select Directory", multiple=True, filetypes=types)
    flags.makeDB = True
    #files = utils.getListOfFiles(dirName, reg)
    if len(files) > 10:
        msg = "You have requestd to import %d files into the data base\ndo you want to continue" % (
            len(files))
        result = tk.messagebox.askokcancel(title="Import Files", message=msg)
        if not result:
            return
    utils.processListOfFiles(files)


def refreshEvents():
    events.refresh()


global files, events
master = {}
masterParms.restoreMaster()

window = tk.Tk()

window.geometry("880x550")
window.title("Team 3932 Log File Viewer")
window.configure(background="white")
window.grid_rowconfigure(0, weight=1)
createMenu(window)
db.db.createDB(flags.dropDataBase)

files = dsFiles.dsFiles(window, refreshEvents)
files.getFrame().grid(row=0, column=0, padx=5, pady=5, stick='NS')

events = dseventsF.dsevents(window, files)
events.getFrame().grid(row=0, column=1, padx=5, pady=5, stick='NESW')
window.grid_columnconfigure(1, weight=1)

window.mainloop()
