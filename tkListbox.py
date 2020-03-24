from tkinter import (Scrollbar,Tk,Label,Frame,Listbox,END, EXTENDED)

def onSelect(x):
    selection = listBox.curselection()
    print(selection)
    
window = Tk()
window.geometry("680x500")

Label(window, text="Top label").pack()

frame = Frame(window)
frame.pack()

listBox = Listbox(frame, selectmode=EXTENDED, width=20, height=20, font=("Helvetica", 12))
listBox.pack(side="left", fill="y")

scrollbar = Scrollbar(frame, orient="vertical")
scrollbar.config(command=listBox.yview)
scrollbar.pack(side="right", fill="y")
listBox.bind('<<ListboxSelect>>', onSelect)
listBox.config(yscrollcommand=scrollbar.set)

for x in range(100):
    listBox.insert(END, str(x))

Label(window, text="Bottom label").pack()

window.mainloop()

