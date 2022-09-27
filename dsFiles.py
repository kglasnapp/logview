import re
#import tkinter as tk
from tkinter import (Button, Checkbutton, Entry, Frame, Label, Listbox, Menu,
                     Scrollbar, Text, Toplevel, ttk, StringVar, BooleanVar, VERTICAL, EXTENDED, END, MULTIPLE )

import db as db
import utils
import flags
import datetime 

class dsFiles():
    lastTime = datetime.datetime.now()
    waitCount = 0
    dataStale = True
    
    def __init__(self, tab, refreshEvents):
        frame = Frame(tab)
        self.frame = frame
        self.refreshEvents = refreshEvents
        
        # declare varaibles used on the form
        self.monthV = StringVar()
        self.monthV.set("8")
        self.dayV = StringVar()
        self.dayV.set("18")
        self.dslogV = BooleanVar()
        self.dslogV.set(False)
        self.dseventsV = BooleanVar()
        self.dseventsV.set(True)
        self.statusTextV = StringVar()
        self.statusTextV.set("Status")
        
        # allocate the widgets for the form
        lblMonth = ttk.Label(frame, text="Month:")
        month = ttk.Entry(frame, width=4, textvariable=self.monthV)
        lblDay = ttk.Label(frame, text="Day:")
        day = ttk.Entry(frame, width=8, textvariable=self.dayV)
        cbLog = ttk.Checkbutton(frame, text="dslog", command=self.checkChanged,
                            variable=self.dslogV, onvalue=True, offvalue=False)
        cbEvents = ttk.Checkbutton(frame, text="dsevents", command=self.checkChanged,
                               variable=self.dseventsV, onvalue=True, offvalue=False)
        
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
        self.listBox = listBox
        scrollbar.config(command=listBox.yview)
        
        listBox.grid(row=2, column=0, columnspan=4, sticky='NS')
        scrollbar.grid(row=2, column=4, sticky='NS')

        listBox.bind('<<ListboxSelect>>', self.onSelect)

        statusBar = Label(frame,  textvariable=self.statusTextV)
        statusBar.grid(row=3, column=0, sticky='NS', columnspan=4)
        
        frame.grid_rowconfigure(2, weight=1)
        self.statusChanged("Startup")
        
 
    
    def timeOut(self, *arg):
        diff = datetime.datetime.now() - self.lastTime
        self.waitCount -= 1
        if flags.debug:
            print("Timeout", arg[0][0], diff, arg[0][1], self.waitCount)
        self.lastTime = datetime.datetime.now()
        if self.waitCount == 0:
            self.refreshEvents()

    def onSelect(self, evt):
        w = evt.widget
        if len(w.curselection()) == 0:
            print(w.curselection())
            return
        index = int(w.curselection()[0])
        value = w.get(index)
        if flags.debug:
            print('You selected item %d: "%s"' % (index, value))
        self.updateStatusBar()
        self.waitCount += 1
        self.frame.after(1000, self.timeOut, (datetime.datetime.now(), self.waitCount))
        

    def checkChanged(self):
        self.statusChanged("Check Box")

    def updateStatusBar(self):
        self.statusTextV.set("Files:%d Selected:%d" %
                        (len(self.inData), len(self.listBox.curselection())))

    def statusChanged(self, response):
        print("---  Something Changed ---", response)
        self.inData = self.getFiles()
        print("Found %d files to display" % (len(self.inData)))
        self.listBox.delete(0, END)
        count = 0
        for r in self.inData:
            self.listBox.insert(count, r[0])
            count += 1
        self.updateStatusBar()
      
    def getValues(self):
        self.values = {
            "year": str(flags.year),
            "month": self.monthV.get(),
            "day": self.dayV.get(),
            "dslog": self.dslogV.get(),
            "dsevents": self.dseventsV.get()
        }
        return self.values
    
    def getFrame(self):
        return self.frame

    def getFiles(self):
        if(self.dataStale):
            db.db.createConnection("data.db")
            cur = db.db.connection.cursor()
            cur.execute("SELECT fileName FROM files order by filename;")
            data = cur.fetchall()
        exp = utils.getRegularExpressionD(self.getValues())
        exp = exp.replace("2020", "2022")
        print("Regular Exp:", exp)
        reg = re.compile(exp)
        files = []
        for r in data:
            if reg.match(r[0]):
                files.append(r)
        files.sort()
        self.inData = files
        #self.statusChanged("Got New Files")
        return files
    
    def getSelected(self):
        sel = self.listBox.curselection()
        files = []
        for x in sel:
            files.append(self.listBox.get(x))
        return files
    
    def refresh(self):
        self.statusChanged("Refresh")
    