import tkinter
from tkinter import (Button, Checkbutton, Entry, Label, Menu, Text, Toplevel, Listbox,
                     Scrollbar,ttk)

def select():
    print(combo.get())
    mylbl = Label(root, text=combo.get())
    mylbl.pack()

def isOk(r):
    print("isOK", r, combo.get())
    return True
    
root = tkinter.Tk()
root.title("Combo Test")
root.geometry("400x400")
opt = ['Keith', 'Sue', 'Doug', 'Chris']
combo = ttk.Combobox(root, value=opt)
combo.current(0)
combo.pack(padx = 20, pady = 20)
combo.bind('<<ComboboxSelected>>', isOk)
okayCommand = combo.register(isOk)

btn = Button(root, text="Click me", command=select)
btn.pack()

root.mainloop()