import re
import tkinter as tk
import tkinter.messagebox
from tkinter import (Button, Checkbutton, Entry, Label, Menu, Text, Toplevel, Listbox,
                     Scrollbar, Frame, ttk)

import tksheet as ts

import db as db
import flags
import sheet as sh
import utils
import dseventsFrame


class Root(tk.Tk):
    sheet = None
    dataStale = True

    def __init__(self):
        super(Root, self).__init__()

        self.title("Team 3932 Log File Viewer")
        self.minsize(640, 400)
        self.configure(background="white")
        self.createMenu()
        self.addFilesTab(self)
        f = dseventsFrame.dsevents(self)
        #f.getFrame().grid(row=0, rowspan=3, column=4)
        f.getFrame().grid(row=0,  column=4)
        
    # def startpressed(self):
    #     new = tk.Toplevel(self)
    #     new.minsize(640, 400)
    #     new.geometry('500x300')
    #     new.configure(background="white")

    def createMenu(self):
        menubar = Menu(self)
        self.config(menu=menubar)

        file_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open")
        file_menu.add_command(label="Save")
        file_menu.add_command(label="Exit")

        help_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About Us")

    # def addingTab4(self):
    #     Label(self.tab4, text="Please Select your choice").place(x=250, y=20)
    #     Button(self.tab4, text="Submit",
    #            command=lambda: self.submit()).place(x=520, y=320)

    def addFilesTab(self, tab):
        # Button(tab, text="Refresh",
        #       command=lambda: self.submit()).grid(row=0, column=0)
        Label(tab, text="Month:").grid(row=0, column=0, padx=10, pady=10)
        self.monthV = tk.StringVar()
        self.monthV.set("3")
        month = Entry(tab, width=4, textvariable=self.monthV)
        month.grid(row=0, column=1)
        month.bind('<Key-Return>', self.bindChanged)
        month.bind('<FocusOut>', self.bindChanged)
        Label(tab, text="Day:").grid(row=0, column=2)
        self.dayV = tk.StringVar()
        self.dayV.set("8-10")
        day = ttk.Entry(tab, width=8, textvariable=self.dayV)
        day.grid(row=0, column=3)
        day.bind('<Key-Return>', self.bindChanged)
        day.bind('<FocusOut>', self.bindChanged)
        self.dslogV = tk.BooleanVar()
        Checkbutton(tab, text="dslog", command=self.checkChanged,
                    variable=self.dslogV, onvalue=True, offvalue=False).grid(row=1, column=0, columnspan=2)
        self.dseventsV = tk.BooleanVar()
        self.dseventsV.set(True)
        Checkbutton(tab, text="dsevents", command=self.checkChanged,
                    variable=self.dseventsV, onvalue=True, offvalue=False).grid(row=1, column=2, columnspan=2)
        frame = Frame(tab)
        frame.grid(row=2, column=0, columnspan=4,
                   padx=5, pady=5, sticky=tk.NSEW)

        scrollbar = Scrollbar(frame, orient=tk.VERTICAL)
        self.Lb1 = Listbox(frame, selectmode=tk.EXTENDED,
                           width=32, yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.Lb1.yview)
        self.Lb1.bind('<<ListboxSelect>>', self.onSelect)

        self.Lb1.grid(row=0, column=0, sticky=tk.NSEW)
        scrollbar.grid(row=0, column=1, sticky=tk.NSEW)
        frame.grid_rowconfigure(0, weight=1)

        self.statusText = tk.StringVar()
        self.statusBar = Label(tab,  textvariable=self.statusText)
        self.statusBar.grid(row=4, column=0, sticky=tk.S+tk.W, columnspan=4)

        self.grid_rowconfigure(2, weight=1)
        self.bindChanged("Startup")

    def onSelect(self, evt):
        w = evt.widget
        print(w.curselection())
        index = int(w.curselection()[0])
        value = w.get(index)
        print('You selected item %d: "%s"' % (index, value))
        self.updateStatusBar()

    def checkChanged(self):
        self.bindChanged("Check Box")

    def updateStatusBar(self):
        self.Lb1.curselection()
        self.statusText.set("Files:%d Selected:%d" %
                            (len(self.inData), len(self.Lb1.curselection())))

    def bindChanged(self, response):
        print("---  Something Changed ---", response)
        self.inData = self.getFiles()
        print("Found %d files" % (len(self.inData)))
        self.Lb1.delete(0, tk.END)
        count = 1
        for r in self.inData:
            self.Lb1.insert(count, r[0])
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

    def submit(self):
        newTop = Toplevel(self.master)
        Label(newTop, text="Review").pack()
        newTop.title("Review and Submit")
        newTop.focus_set()
        newTop.geometry("400x600")

    def result1(self):
        ttk.Notebook.select(self.tab7)

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
    


root = Root()
root.mainloop()
