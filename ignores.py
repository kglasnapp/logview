import tkinter as tk
from tkinter import (Button, Checkbutton, Entry, Label, Menu, Text, Toplevel, Listbox,
                     Scrollbar, ttk)


def addNew():
    pass
    # rint(combo.get())
    #mylbl = Label(root, text=combo.get())
    # mylbl.pack()


def isOk(r):
    pass
    #Aprint("isOK", r, combo.get())
    return True

def onSelect(resp):
    sel = lstBox.curselection()
    s = lstBox.get(sel[0])
    print(resp, sel, s)
    newIgnoreV.set(s)
    


def showForm():
    global root, lstBox, newIgnoreV
    root = tk.Tk()
    newIgnoreV = tk.StringVar()
    statusBarV = tk.StringVar()
    root.title("Edit Ignores -- They must be regular expressions")
    root.geometry("500x400")
    
    ignores = ['Keith', 'Sue', 'Doug', 'Chris']
    for i in range(100):
        ignores.append(i)
    txtBox = ttk.Entry(root, width=40, textvariable=newIgnoreV)
    addBtn = Button(root, text="Add", command=addNew)
    saveBtn = Button(root, text="Save")
    exitBtn = Button(root, text="Exit")
    scrollbar = Scrollbar(root, orient=tk.VERTICAL)
    lstBox = Listbox(root, 
                     width=32, yscrollcommand=scrollbar.set)
    scrollbar.config(command=lstBox.yview)
    statusBar = Label(root, textvariable=statusBarV)
   

    txtBox.grid(row=0, column=0, padx=5, pady=5, sticky='new')
    addBtn.grid(row=0, column=1, padx=5, pady=5,  sticky='ne')
    saveBtn.grid(row=0, column=2,  padx=5, pady=5,  sticky='ne')
    exitBtn.grid(row=0, column=3,  padx=5, pady=5,  sticky='ne')
    lstBox.grid(row=1, column=0, columnspan=3, sticky='nesw', padx=5, pady=5)
    scrollbar.grid(row=1, column=3, sticky='nesw', padx=15, pady=5)
    statusBar.grid(row=2, column=0, columnspan=2, sticky='ws', padx=5, pady=5)
    
    lstBox.bind('<<ListboxSelect>>', onSelect)
    
    
    root.grid_rowconfigure(1, weight=1)
    root.grid_columnconfigure(0, weight=1)
    
    statusBarV.set("Status: %d ignores" % (len(ignores)))
    
    for x in ignores:
        lstBox.insert(tk.END, x)

    root.mainloop()

if __name__ == '__ignores__':
    showForm()
