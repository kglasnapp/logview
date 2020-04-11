import re
#import tkinter as tk
from tkinter import (Button, Checkbutton, Entry, Frame, Label, Listbox, Menu,
                     Scrollbar, Text, Toplevel, ttk, StringVar, BooleanVar, VERTICAL, EXTENDED, END, MULTIPLE )

import db as db
import utils
import flags

class dsFiles():

    dataStale = True
    
    def __init__(self, tab):
        global monthV, dayV, dslogV, dseventsV, statusTextV, listBox, frame
        frame = Frame(tab)
        
        # declare varaibles used on the form
        monthV = StringVar()
        monthV.set("3")
        dayV = StringVar()
        dayV.set("8-10")
        dslogV = BooleanVar()
        dslogV.set(False)
        dseventsV = BooleanVar()
        dseventsV.set(True)
        statusTextV = StringVar()
        statusTextV.set("Status")
        
        # allocate the widgets for the form
        lblMonth = ttk.Label(frame, text="Month:")
        month = ttk.Entry(frame, width=4, textvariable=monthV)
        lblDay = ttk.Label(frame, text="Day:")
        day = ttk.Entry(frame, width=8, textvariable=dayV)
        cbLog = ttk.Checkbutton(frame, text="dslog", command=self.checkChanged,
                            variable=dslogV, onvalue=True, offvalue=False)
        cbEvents = ttk.Checkbutton(frame, text="dsevents", command=self.checkChanged,
                               variable=dseventsV, onvalue=True, offvalue=False)
        
        # place the widgets on the form
        lblMonth.grid(row=0, column=0)
        month.grid(row=0, column=1)
        lblDay.grid(row=0, column=2)
        day.grid(row=0, column=3)
        cbLog.grid(row=1, column=0, columnspan=2)
        cbEvents.grid(row=1, column=2, columnspan=2)
        
        # setup bindings i.e. methods that are called when things change
        month.bind('<Key-Return>', self.statusChanged)
        month.bind('<FocusOut>', self.statusChanged)
        day.bind('<Key-Return>', self.statusChanged)
        day.bind('<FocusOut>', self.statusChanged)
   
        scrollbar = Scrollbar(frame, orient=VERTICAL)
        listBox = Listbox(frame, selectmode=EXTENDED,
            width=32, yscrollcommand=scrollbar.set, exportselection=0)
        scrollbar.config(command=listBox.yview)
        
        listBox.grid(row=2, column=0, columnspan=4, sticky='NS')
        scrollbar.grid(row=2, column=4, sticky='NS')

        listBox.bind('<<ListboxSelect>>', self.onSelect)

        statusBar = Label(frame,  textvariable=statusTextV)
        statusBar.grid(row=3, column=0, sticky='NS', columnspan=4)
        
        frame.grid_rowconfigure(2, weight=1)
        self.statusChanged("Startup")
  

    def onSelect(self, evt):
        w = evt.widget
        print(w.curselection())
        index = int(w.curselection()[0])
        value = w.get(index)
        print('You selected item %d: "%s"' % (index, value))
        self.updateStatusBar()

    def checkChanged(self):
        self.statusChanged("Check Box")

    def updateStatusBar(self):
        statusTextV.set("Files:%d Selected:%d" %
                        (len(self.inData), len(listBox.curselection())))

    def statusChanged(self, response):
        print("---  Something Changed ---", response)
        self.inData = self.getFiles()
        print("Found %d files to display" % (len(self.inData)))
        listBox.delete(0, END)
        count = 0
        for r in self.inData:
            listBox.insert(count, r[0])
            count += 1
        self.updateStatusBar()

    def getValues(self):
        self.values = {
            "year": str(flags.year),
            "month": monthV.get(),
            "day": dayV.get(),
            "dslog": dslogV.get(),
            "dsevents": dseventsV.get()
        }
        return self.values
    
    def getFrame(self):
        return frame

    def getFiles(self):
        if(self.dataStale):
            db.db.createConnection("data.db")
            cur = db.db.connection.cursor()
            cur.execute("SELECT fileName FROM files order by filename;")
            data = cur.fetchall()
        exp = utils.getRegularExpressionD(self.getValues())
        print("Regular Exp:", exp)
        reg = re.compile(exp)
        files = []
        for r in data:
            if reg.match(r[0]):
                files.append(r)
        files.sort()
        self.inData = files
        return files
    
    def getSelected(self):
        sel = listBox.curselection()
        files = []
        for x in sel:
            files.append(listBox.get(x))
        return files
    
    def refresh(self):
        self.statusChanged("Refresh")
    