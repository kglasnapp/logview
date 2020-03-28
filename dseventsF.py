import tkinter as tk
import tkinter.messagebox
from tkinter import (Button, Checkbutton, Entry, Label, Menu, Text, Toplevel, Listbox,
                     Scrollbar, Frame, END, ttk)
import tksheet as ts
import db as db
import re


class dsevents():

    dsfiles = None
    dataStale = True
    fileCount = 0
    

    def __init__(self, tab, f0):
        global search1V, search2V, reg1, reg2, andOrV, frame, listBox, statusBarV
        frame = Frame(tab)
        topFrame = Frame(frame)
        self.dsfiles = f0

        # Define variables used in the widget
        search1V = tk.StringVar()
        search1V.set("")
        search2V = tk.StringVar()
        search2V.set("")
        andOrV = tk.BooleanVar()
        andOrV.set(False)
        reg1 = tk.BooleanVar()
        reg1.set(False)
        reg2 = tk.BooleanVar()
        reg2.set(False)
        statusBarV = tk.StringVar()
        statusBarV.set("File:?")

        # Create the various widgets for the frame
        label1 = Label(topFrame, text="Seach1:")
        search1 = ttk.Entry(topFrame, width=40, textvariable=search1V)
        label2 = Label(topFrame, text="Search2:")
        cb1 = Checkbutton(topFrame, text="RegEx", command=self.onChanged,
                          variable=reg1, onvalue=True, offvalue=False)
        cb2 = Checkbutton(topFrame, text="RegEx", command=self.onChanged,
                          variable=reg2, onvalue=True, offvalue=False)
        andOr = Checkbutton(topFrame, text="And", command=self.onChanged,
                            variable=andOrV, onvalue=True, offvalue=False)
        search2 = ttk.Entry(topFrame, width=40, textvariable=search2V)
        refreshBtn = Button(topFrame, text="Refresh", command=self.refresh)
        ignoresBtn = Button(topFrame, text="Ignores", command=self.ignoreBtn)
        scrollbar = Scrollbar(frame, orient=tk.VERTICAL)
        listBox = Listbox(frame, selectmode=tk.EXTENDED,
                          width=32, yscrollcommand=scrollbar.set)
        scrollbar.config(command=listBox.yview)
        statusBar = Label(frame, textvariable=statusBarV)

        # Set the widgets on the grid
        topFrame.grid(row=0, column=0, sticky='W')
        label1.grid(row=0, column=0, padx=5, pady=5, sticky='W')
        search1.grid(row=0, column=1, padx=5, pady=5, sticky='W')
        cb1.grid(row=0, column=2, padx=5, pady=5)
        andOr.grid(row=0, column=3, padx=5, pady=5)
        ignoresBtn.grid(row=0, column=4)
        label2.grid(row=1, column=0, padx=5, pady=5, sticky='W')
        search2.grid(row=1, column=1, padx=5, pady=5, sticky='W')
        cb2.grid(row=1, column=2, padx=5, pady=5)
        refreshBtn.grid(row=1, column=3)
        listBox.grid(row=2, column=0, columnspan=4, sticky=tk.NSEW)
        scrollbar.grid(row=2, column=4, sticky=tk.NSEW)
        statusBar.grid(row=3, column=0, columnspan=4, sticky='ws')

        # Setup notifications
        search1.bind('<Key-Return>', self.onChanged1)
        search1.bind('<FocusOut>', self.onChanged1)
        search2.bind('<Key-Return>', self.onChanged1)
        search2.bind('<FocusOut>', self.onChanged1)
        listBox.bind('<<ListboxSelect>>', self.onChangeLB)

        frame.grid_rowconfigure(2, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        self.fileCount = 0
       
    
    def ignoreBtn(self):
        tkinter.messagebox.showinfo(title="Ignores", message="Show Ignores")

    def refresh(self):
        print("Refresh Hit")
        # Fill in the data
        self.getData()

    def onChanged1(self, resp):
        print("-- Something Changed -- Search1:%s Search2:%s andOrV:%s reg1:%s reg2:%s" %
              (search1V.get(), search2V.get(), andOrV.get(), reg1.get(), reg2.get()))

    def onChanged(self):
        self.onChanged1("")

    def onChangeLB(self, resp):
        #print("LB Changed")
        self.updateStatus()

    def getFrame(self):
        return frame

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

    # Get Selected item f
    def updateListbox(self):
        sel = listBox.curselection()
        files = []
        for x in sel:
            print(listBox.get(x))
            files.append(listBox.get(x))

    def getData(self):
        global fileCount, lineCount
        db.db.createConnection("data.db")
        cur = db.db.connection.cursor()
        files = self.dsfiles.getSelected()
        fileNums = []
        fileCount = 0
        lineCount = 0
        for file in files:
            cur.execute("Select id from files where fileName = '%s';" % (file))
            data = cur.fetchall()
            fileNums.append(data[0][0])
            fileCount += 1
        listBox.delete(0, END)
        reg = self.getRegExp()
        for fileNum in fileNums:
            cur.execute(
                "SELECT logData FROM allData_dsevents where fileNum = %d;" % (fileNum))
            data = cur.fetchall()
            for r in data:
                d = r[0]
                if reg.match(d):
                    listBox.insert(END, d)
                    lineCount += 1
        self.updateStatus()

    def updateStatus(self):
        statusBarV.set("Files:%d Lines:%d Selected:%d" %
                       (fileCount, lineCount,  len(listBox.curselection())))

    def getRegExp(self):
        s1 = search1V.get()
        if reg1.get():
            exp1 = s1
        else:
            exp1 = ".*%s.*" % (self.updateSpecial(s1))
        s2 = search2V.get()
        if reg2.get():
            exp2 = s2
        else:
            exp2 = ".*%s.*" % (self.updateSpecial(s2))
        exp = exp1 + exp2
        if s1 != '' and s2 != '':
            if andOrV.get():
                # And condition
                exp = "(%s)(%s)" % (exp1, exp2)
            else:
                # Or condition
                exp = "%s|%s" % (exp1, exp2)
        print("exp:%s exp1:%s exp2:%s" % (exp, exp1, exp2))
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
