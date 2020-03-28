import tkinter as tk
from tkinter import Button, filedialog
import dseventsF
import dsFiles
import ignores
import flags
import utils
import db
import sys
#from tk import tkFileDialog


def createMenu(tab):
    menubar = tk.Menu()
    tab.config(menu=menubar)
    fileMenu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="File", menu=fileMenu)
    fileMenu.add_command(label="Import", command=fileImport)
    fileMenu.add_command(label="Save")
    fileMenu.add_separator()
    fileMenu.add_command(label="Exit", command=lambda : sys.exit(0))
    editMenu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Edit", menu=editMenu)
    editMenu.add_command(label="Edit Ignores", command= ignores.showForm) 
    helpMenu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Help", menu=helpMenu)
    helpMenu.add_command(label="About Us")
    
def basicLabels(tab):
    frame = tk.Frame(tab)
    frame.grid(row=0,column=0, sticky='ns')
    lbl0 = tk.Label(frame, text="Top label")
    lbl1 = tk.Label(frame, text="Middle label")
    lbl2 = tk.Label(frame, text="Bottom label")
    lbl0.grid(row=0,column=0)
    lbl1.grid(row=1,column=0)
    lbl2.grid(row=2,column=0)
    frame.grid_rowconfigure(1, weight=1)
    return frame

def fileImport():
    types = (("Robot log files","*.dslog;*.dsevents"),("dsevents", "*.dsevents"),("dslog","*.dslog"),("All files","*.*"))
    fileNames =  tk.filedialog.askopenfilename(initialdir = ".",title = "Select file",multiple=True, filetypes = types)
    if flags.debug:
        print ("Files to Import", fileNames)
    flags.makeDB = True
    #db.createDB(flags.dropDataBase)
    utils.processListOfFiles(fileNames)
    db.db.connection.commit()
    db.db.closeConnection()
    files.refresh() 


global files, evaents

window = tk.Tk()
window.geometry("780x550")
window.title("Team 3932 Log File Viewer")
window.configure(background="white")
window.grid_rowconfigure(0, weight=1)
createMenu(window)
db.db.createDB(flags.dropDataBase)

files = dsFiles.dsFiles(window)
files.getFrame().grid(row=0, column=0, padx=5, pady=5,stick='NS')

events = dseventsF.dsevents(window, files)
events.getFrame().grid(row=0, column=1, padx=5, pady=5,stick='NESW')
window.grid_columnconfigure(1, weight=1)

window.mainloop()
