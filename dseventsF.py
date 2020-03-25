import tkinter as tk
import tkinter.messagebox
from tkinter import (Button, Checkbutton, Entry, Label, Menu, Text, Toplevel, Listbox,
                     Scrollbar, Frame, END, ttk)
import tksheet as ts
import db as db
import myListBox
#import mainTab


class dsevents():

    dsfiles = None
    dataStale = True

    def __init__(self, tab, f0):
        global search1V, search2V, reg1, reg2, andOrV, frame, listBox
        frame = Frame(tab)
        topFrame = Frame(frame)
        self.dsfiles = f0

        # Define variables used in the widget
        search1V = tk.StringVar()
        search1V.set("Search 1")
        search2V = tk.StringVar()
        search2V.set("Search 2")
        andOrV = tk.BooleanVar()
        andOrV.set(False)
        reg1 = tk.BooleanVar()
        reg1.set(False)
        reg2 = tk.BooleanVar()
        reg2.set(False)

        # Create the various widgets for the frame
        label1 = Label(topFrame, text="Seach1:")
        search1 = ttk.Entry(topFrame, width=40, textvariable=search1V)
        label2 = Label(topFrame, text="Search2:")
        cb1 = Checkbutton(topFrame, text="RegEx:", command=self.onChanged,
                          variable=reg1, onvalue=True, offvalue=False)
        cb2 = Checkbutton(topFrame, text="RegEx:", command=self.onChanged,
                          variable=reg2, onvalue=True, offvalue=False)
        andOr = Checkbutton(topFrame, text="AndOr:", command=self.onChanged,
                            variable=andOrV, onvalue=True, offvalue=False)
        search2 = ttk.Entry(topFrame, width=40, textvariable=search2V)
        refreshBtn = Button(topFrame, text="Refresh", command=self.refresh)
        scrollbar = Scrollbar(frame, orient=tk.VERTICAL)
        listBox = Listbox(frame, selectmode=tk.EXTENDED,
                          width=32, yscrollcommand=scrollbar.set)
        scrollbar.config(command=listBox.yview)

        # Set the widgets on the grid
        topFrame.grid(row=0, column=0, sticky='W')
        label1.grid(row=0, column=0, padx=5, pady=5, sticky='W')
        search1.grid(row=0, column=1, padx=5, pady=5, sticky='W')
        cb1.grid(row=0, column=2, padx=5, pady=5)
        andOr.grid(row=0, column=3, padx=5, pady=5)
        label2.grid(row=1, column=0, padx=5, pady=5, sticky='W')
        search2.grid(row=1, column=1, padx=5, pady=5, sticky='W')
        cb2.grid(row=1, column=2, padx=5, pady=5)
        refreshBtn.grid(row=1, column=3)
        listBox.grid(row=2, column=0, columnspan=4, sticky=tk.NSEW)
        scrollbar.grid(row=2, column=4, sticky=tk.NSEW)

        # Setup notifications
        search1.bind('<Key-Return>', self.onChanged1)
        search1.bind('<FocusOut>', self.onChanged1)
        search2.bind('<Key-Return>', self.onChanged1)
        search2.bind('<FocusOut>', self.onChanged1)
        listBox.bind('<<ListboxSelect>>', self.onChangeLB)

        frame.grid_rowconfigure(2, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        # Fill in the data
        for x in range(100):
            listBox.insert(END, str(x))

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
        print("LB Changed")

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
        db.db.createConnection("data.db")
        cur = db.db.connection.cursor()
        files = self.dsfiles.getSelected()
        fileNums = []
        for file in files:
            cur.execute("Select id from files where fileName = '%s';" % (file))
            data = cur.fetchall()
            fileNums.append(data[0][0])
        listBox.delete(0, END)
        for fileNum in fileNums:
            cur.execute(
                "SELECT logData FROM allData_dsevents where fileNum = %d;" % (fileNum))
            data = cur.fetchall()
            for r in data:
                listBox.insert(END, r[0])
