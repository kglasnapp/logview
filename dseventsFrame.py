import tkinter as tk
import tkinter.messagebox
from tkinter import (Button, Checkbutton, Entry, Label, Menu, Text, Toplevel, Listbox,
                     Scrollbar, Frame, END, ttk)
import tksheet as ts
import db as db
import myListBox

class dsevents():
    def __init__(self, tab):
        global search1V, search2V, reg1, reg2, andOrV
        self.frame = Frame(tab)
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
        label1 = Label(self.frame, text="Seach1:")
        search1 = ttk.Entry(self.frame, width=40, textvariable=search1V)
        label2 = Label(self.frame, text="Search2:")
        cb1 = Checkbutton(self.frame, text="RegEx:", command=self.onChanged,
                          variable=reg1, onvalue=True, offvalue=False)
        cb2 = Checkbutton(self.frame, text="RegEx:", command=self.onChanged,
                          variable=reg2, onvalue=True, offvalue=False)
        andOr = Checkbutton(self.frame, text="AndOr:", command=self.onChanged,
                            variable=andOrV, onvalue=True, offvalue=False)
        search2 = ttk.Entry(self.frame, width=40, textvariable=search2V)
        #listBox = self.myListBox(self.frame)

        # Position the widgets on the frame
        label1.grid(row=0, column=0, padx=5, pady=5)
        search1.grid(row=0, column=1, padx=5, pady=5)
        cb1.grid(row=0, column=2, padx=5, pady=5)
        andOr.grid(row=0, column=3, padx=5, pady=5)
        label2.grid(row=1, column=0, padx=5, pady=5)
        search2.grid(row=1, column=1, padx=5, pady=5)
        cb2.grid(row=1, column=2, padx=5, pady=5)
        #listBox.grid(row=2, column=0, columnspan=3, padx=5, pady=5)

        # Setup notifications
        search1.bind('<Key-Return>', self.onChanged1)
        search1.bind('<FocusOut>', self.onChanged1)
        search2.bind('<Key-Return>', self.onChanged1)
        search2.bind('<FocusOut>', self.onChanged1)

    def onChanged1(self, resp):
        print("-- Something Changed -- Search1:%s Search2:%s andOrV:%s reg1:%s reg2:%s" %
              (search1V.get(), search2V.get(), andOrV.get(), reg1.get(), reg2.get()))
        
    def onChanged(self):
        self.onChanged1("")
        
    def onChangeLB(self, resp):
        print("LB Changed")

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

