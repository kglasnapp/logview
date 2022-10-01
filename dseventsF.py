import tkinter as tk
import tkinter.messagebox
from tkinter import (Button, Checkbutton, Label,
                     Listbox, Scrollbar, Frame, END, ttk)
from turtle import clear
import tksheet as ts
import db as db
import re
import flags
import masterParms
import showSomeLines


class dsevents():
    dsfiles = None
    dataStale = True
    ids = []

    def __init__(self, tab, f0):
        self.frame = Frame(tab)
        topFrame = Frame(self.frame)
        self.dsfiles = f0
        # Define variables used in the widget
        self.search1V = tk.StringVar()
        self.search1V.set("")
        self.search2V = tk.StringVar()
        self.search2V.set("")
        self.andOrV = tk.BooleanVar()
        self.andOrV.set(False)
        self.reg1 = tk.BooleanVar()
        self.reg1.set(False)
        self.reg2 = tk.BooleanVar()
        self.reg2.set(False)
        self.statusBarV = tk.StringVar()
        self.statusBarV.set("File:?")
        # Create the various widgets for the frame
        label1 = Label(topFrame, text="Search1:")
        search1 = ttk.Entry(topFrame, width=40, textvariable=self.search1V)
        label2 = Label(topFrame, text="Search2:")
        cb1 = Checkbutton(topFrame, text="RegEx", command=self.onChanged,
                          variable=self.reg1, onvalue=True, offvalue=False)
        cb2 = Checkbutton(topFrame, text="RegEx", command=self.onChanged,
                          variable=self.reg2, onvalue=True, offvalue=False)
        andOr = Checkbutton(topFrame, text="And", command=self.onChanged,
                            variable=self.andOrV, onvalue=True, offvalue=False)
        search2 = ttk.Entry(topFrame, width=40, textvariable=self.search2V)
        refreshBtn = Button(topFrame, text="Refresh", command=self.refresh)
        saveSearchBtn = Button(
            topFrame, text="Save Search", command=self.saveSearch)
        restoreSearchBtn = Button(
            topFrame, text="Restore Search", command=self.restoreSearch)
        clearBtn = Button(topFrame, text="Clear Search",
                          command=self.clearSearch)
        #ignoresBtn = Button(topFrame, text="Ignores", command=self.ignoreBtn)
        scrollbar = Scrollbar(self.frame, orient=tk.VERTICAL)
        listBox = Listbox(self.frame, selectmode=tk.EXTENDED,
                          width=32, yscrollcommand=scrollbar.set)
        self.listBox = listBox
        scrollbar.config(command=listBox.yview)
        statusBar = Label(self.frame, textvariable=self.statusBarV)

        # Set the widgets on the grid
        topFrame.grid(row=0, column=0, sticky='W')
        label1.grid(row=0, column=0, padx=5, pady=5, sticky='W')
        search1.grid(row=0, column=1, padx=5, pady=5, sticky='W')
        cb1.grid(row=0, column=2, padx=5, pady=5)
        andOr.grid(row=0, column=3, padx=5, pady=5)
        #ignoresBtn.grid(row=0, column=4)
        label2.grid(row=1, column=0, padx=5, pady=5, sticky='W')
        search2.grid(row=1, column=1, padx=5, pady=5, sticky='W')
        cb2.grid(row=1, column=2, padx=5, pady=5)
        refreshBtn.grid(row=1, column=3)
        clearBtn.grid(row=0, column=5)
        saveSearchBtn.grid(row=0, column=4)
        restoreSearchBtn.grid(row=1, column=4)
        listBox.grid(row=2, column=0, columnspan=4, sticky=tk.NSEW)
        scrollbar.grid(row=2, column=4, sticky=tk.NSEW)
        statusBar.grid(row=3, column=0, columnspan=4, sticky='ws')

        # Setup notifications
        search1.bind('<Key-Return>', self.onChanged1)
        search1.bind('<FocusOut>', self.onChanged1)
        search2.bind('<Key-Return>', self.onChanged1)
        search2.bind('<FocusOut>', self.onChanged1)
        listBox.bind('<<ListboxSelect>>', self.onChangeLB)
        listBox.bind('<Button-3>',  self.onLBRightClick) 

        self.frame.grid_rowconfigure(2, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)
        self.fileCount = 0

    def clickListbox(self):
        print("Clicked")

    def ignoreBtn(self):
        tkinter.messagebox.showinfo(title="Ignores", message="Show Ignores")

    def refresh(self):
        # Fill in the data
        self.getData()

    def clearSearch(self):
        self.search1V.set("")
        self.search2V.set("")
        self.getData()

    def saveSearch(self):
        masterParms.set("search1", self.search1V.get())
        masterParms.set("search2", self.search2V.get())
        masterParms.saveMaster()

    def restoreSearch(self):
        self.search1V.set(masterParms.get("search1", ""))
        self.search2V.set(masterParms.get("search2", "'"))

    def onChanged1(self, resp):
        if flags.debug:
            print("-- Something Changed -- Search1:%s Search2:%s andOrV:%s reg1:%s reg2:%s" %
                  (self.search1V.get(), self.search2V.get(), self.andOrV.get(), self.reg1.get(), self.reg2.get()))
        self.getData()

    def onChanged(self):
        self.onChanged1("")
        
    def onLBRightClick(self, resp):
        sel = self.listBox.curselection()
        if len(sel) == 0:
            return
        s = self.listBox.get(sel[0])
        dbIndex = self.ids[sel[0]]
        data = self.getDataForIndex(dbIndex)
        fileName = data[0][6]
        print("LB Change file:%s id:%d s:%s" % (fileName, dbIndex, s))
        showSomeLines.showForm(dbIndex, fileName)
        self.updateStatus()

    def onChangeLB(self, resp):
        sel = self.listBox.curselection()
        print(sel)

    def getFrame(self):
        return self.frame

    def myListBox(self, frame):
        fLB = Frame(frame)
        scrollbar = Scrollbar(fLB, orient=tk.VERTICAL)
        listBox = Listbox(fLB, selectmode=tk.EXTENDED,
                          width=32, yscrollcommand=scrollbar.set)
        scrollbar.config(command=listBox.yview)
        listBox.bind('<<ListboxSelect>>', self.onChangeLB)
        listBox.grid(row=0, column=0, sticky=tk.NSEW)
        scrollbar.grid(row=0, column=1, sticky=tk.NSEW)
        for x in range(100):
            listBox.insert(END, str(x))
        #frame.grid_rowconfigure(0, weight=1)
        return fLB

    def getDataForIndex(self, idx):
        db.db.createConnection("data.db")
        cur = db.db.connection.cursor()
        cur.execute(
            "SELECT * FROM allData_dsevents where id = %d;" % (idx))
        data = cur.fetchall()
        return data

    def getData(self):
        db.db.createConnection("data.db")
        cur = db.db.connection.cursor()
        files = self.dsfiles.getSelected()
        fileNums = []
        self.fileCount = 0
        self.lineCount = 0
        self.ids = []
        for file in files:
            cur.execute("Select id from files where fileName = '%s';" % (file))
            data = cur.fetchall()
            fileNums.append(data[0][0])
            self.fileCount += 1
        self.listBox.delete(0, END)
        reg = self.getRegExp()
        for fileNum in fileNums:
            cur.execute(
                "SELECT logData,id FROM allData_dsevents where fileNum = %d;" % (fileNum))
            data = cur.fetchall()
            for r in data:
                d = r[0]
                if reg.match(d):
                    if(r[1] == 53624):
                        print("53624", len(self.ids))
                    self.ids.append(r[1])  # Append the index of the element
                    self.listBox.insert(END, d)
                    self.lineCount += 1
        self.updateStatus()
 
    def updateStatus(self):
        self.statusBarV.set("Files:%d Lines:%d Selected:%d" %
                            (self.fileCount, self.lineCount,  len(self.listBox.curselection())))

    def getListBox(self):
        return self.listBox

    def getRegExp(self):
        s1 = self.search1V.get()
        if self.reg1.get():
            exp1 = s1
        else:
            exp1 = ".*%s" % (self.updateSpecial(s1))
        s2 = self.search2V.get()
        if self.reg2.get():
            exp2 = s2
        else:
            exp2 = ".*%s" % (self.updateSpecial(s2))
        if s1 == '':
            exp = exp2
        if s2 == '':
            exp = exp1
        if s1 != '' and s2 != '':
            if self.andOrV.get():
                # And condition
                exp = "(?=%s)(?=%s)" % (exp1, exp2)
            else:
                # Or condition
                exp = "%s|%s" % (exp1, exp2)
        print("exp:%s" % (exp))
        reg = re.compile(exp, re.IGNORECASE)
        return reg

    def updateSpecial(self, sIn):
        # Regular expression special chars
        sp = "\\^$.|?*+()[{"
        s = ''
        for c in sIn:
            if c in sp:
                s += '\\'
            s += c
        return s
