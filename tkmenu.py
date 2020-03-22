import glob
import os
import time
import tkinter as tk
import tkinter.filedialog
import tkinter.messagebox

from tksheet import Sheet


def addMenu():
    top.title("Team 3932 Log Viewer")
    menubar = tk.Menu(top)
    file = tk.Menu(menubar, tearoff=0)
    file.add_command(label="New")
    file.add_command(label="Open", command=openFile)
    file.add_command(label="Save", command=save)
    file.add_command(label="Save as...")
    file.add_command(label="Close")
    file.add_separator()
    file.add_command(label="Exit", command=top.quit)
    menubar.add_cascade(label="File", menu=file)
    edit = tk.Menu(menubar, tearoff=0)
    edit.add_command(label="Undo")
    edit.add_separator()
    edit.add_command(label="Cut")
    edit.add_command(label="Copy")
    edit.add_command(label="Paste")
    edit.add_command(label="Delete")
    edit.add_command(label="Select All")
    menubar.add_cascade(label="Edit", menu=edit)
    help = tk.Menu(menubar, tearoff=0)
    help.add_command(label="About", command=alert)
    menubar.add_cascade(label="Help", menu=help)
    top.config(menu=menubar)


def openFile():
    path = os.path.dirname(__file__) + '\\logs'
    fileName = tkinter.filedialog.askopenfiles(initialdir=path, title="Select file", filetypes=(
        ("dsevents", "*.dsevents"), ("all files", "*.*")), multiple = True)
    print(fileName)


def open():
    lBox = tk.Listbox(top, height=10, width=30, yscrollcommand=True)
    lBox.grid(row=1, column=1)
    path = os.path.dirname(__file__) + '\\logs'
    os.chdir(path)
    print("Open Log files from:", path)
    for file in glob.glob("*.dsevents"):
        lBox.insert(tk.END, file.replace(".dsevents", ""))


def save():
    print("Save Menu Activated")


def alert():
    tkinter.messagebox.showinfo("Help", "This is just a message!")

# def addButtons():
#     frame = Frame(top)
#     frame.pack(side=LEFT)
#     button = Button(frame, text="QUIT", fg="red", command=top.quit)
#     button.pack(side=LEFT)
#     hi_there = Button(frame, text="Hello", command=sayHi)
#     hi_there.pack(side=LEFT)


def sayHi():
    print("hi there, everyone!")


def printVar():
    print(var.get())

def getFirst():
    print(entry1.get())


top = tk.Tk()
#top['bg'] = 'green'
var = tk.IntVar()
var.set(0)
print("var:", var.get())

addMenu()

tk.Label(top, text="First:").grid(row=0, sticky=tk.E)
tk.Label(top, text="Second:").grid(row=1, sticky=tk.E)

textV = tk.StringVar()
textV.set("Keith")

entry1 = tk.Entry(top, width=60, textvariable=textV)
#entry1.set("Keith")
entry2 = tk.Entry(top)

entry1.grid(row=0, column=1)
entry2.grid(row=1, column=1)

checkbutton = tk.Checkbutton(
    top, text="Expand",  command=printVar, variable=var, onvalue=1, offvalue=0)
checkbutton.grid(columnspan=2, sticky=tk.W)

# # image.grid(row=0, column=2, columnspan=2, rowspan=2,
# #               sticky=W+E+N+S, padx=5, pady=5)

button1 = tk.Button(top, text="Get First", fg="red", command=getFirst)
button2 = tk.Button(top, text="QUIT", fg="red", command=top.quit)

button1.grid(row=2, column=2)
button2.grid(row=2, column=3)

top.mainloop()
