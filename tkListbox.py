import tkinter as tk

listBox = None


def onSelect(x):
    selection = listBox.curselection()
    print(selection)


def packBased(window):
    tk.Label(window, text="Top label").pack()

    frame = tk.Frame(window)
    frame.pack()

    listBox = tk.Listbox(frame, selectmode=tk.EXTENDED, width=20,
                      height=20, font=("Helvetica", 12))
    listBox.pack(side="left", fill="y")
    scrollbar = tk.Scrollbar(frame, orient="vertical")
    scrollbar.config(command=listBox.yview)
    scrollbar.pack(side="right", fill="y")
    listBox.bind('<<ListboxSelect>>', onSelect)
    listBox.config(yscrollcommand=scrollbar.set)
    tk.Label(window, text="Bottom label").pack()
    for x in range(100):
        listBox.insert(tk.END, str(x))
    return listBox


def gridBased(frame):
    frame = tk.Frame()
    tk.Label(frame, text="Top label").grid(row=0, column=0,sticky='N')
    frame.grid(row=1, column=0)
    listBox = tk.Listbox(frame, selectmode=tk.EXTENDED,
                      width=20, font=("Helvetica", 12))
    listBox.grid(row=1, column=0, sticky="ns")
    scrollbar = tk.Scrollbar(frame, orient="vertical")
    listBox.config(yscrollcommand=scrollbar.set)
    scrollbar.grid(row=1, column=1, sticky='ns')
    scrollbar.config(command=listBox.yview)
    listBox.bind('<<ListboxSelect>>', onSelect)
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_rowconfigure(1, weight=1)
    frame.grid_rowconfigure(2, weight=1)
    #frame.grid(row=0, column=0)
    tk.Label(frame, text="Bottom label").grid(row=2, column=0, sticky='S')
    for x in range(100):
        listBox.insert(tk.END, str(x))
    return listBox

def basicLabels1(tab):
    frame = tk.Frame(tab)
    #frame.grid(sticky="nsew")
    frame.grid(row=0,column=0, sticky="nsew")
    frame.rowconfigure(0,weight=1)
    lbl0 = tk.Label(frame, text="Top label")
    lbl1 = tk.Label(frame, text="Middle label", height=20)
    lbl2 = tk.Label(frame, text="Bottom label")
    lbl0.grid(row=0,column=0)
    lbl1.grid(row=1,column=0, sticky='ns')
    lbl2.grid(row=2,column=0)
    lbl1.grid_rowconfigure(1,weight=1)
    #frame.grid_rowconfigure(0, weight=1)
    #frame.grid_rowconfigure(1, weight=1)
    #frame.grid_rowconfigure(2, weight=1)
    #frame.grid(row=0, column=0)
    
   
 
def basicLabels2(tab):
    lbl0 = tk.Label(tab, text="Top label")
    lbl1 = tk.Label(tab, text="Middle label")
    lbl2 = tk.Label(tab, text="Bottom label")
    lbl0.grid(row=0,column=0)
    lbl1.grid(row=1,column=0)
    lbl2.grid(row=2,column=0)
    tab.grid_rowconfigure(1, weight=1)
    tab.grid_rowconfigure(2, weight=1)
 
window = tk.Tk()
window.geometry("680x500")

# listBox = packBased(window)
# listBox = gridBased(window)
if True:
    basicLabels2(window)
else:
    f = tk.Frame(window)
    f.grid(row=0, column=0, sticky="nesw")
    f.rowconfigure(0,weight=1)
   
    basicLabels2(f)

window.mainloop()
