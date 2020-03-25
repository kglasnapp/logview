import tkinter as tk

def basicLabels1(tab):
    frame = tk.Frame(tab)
    frame.grid(row=0,column=0, sticky='ns')
    lbl0 = tk.Label(frame, text="Top label")
    lbl1 = tk.Label(frame, text="Middle label")
    lbl2 = tk.Label(frame, text="Bottom label")
    lbl0.grid(row=0,column=0)
    lbl1.grid(row=1,column=0)
    lbl2.grid(row=2,column=0)
    frame.grid_rowconfigure(1, weight=1)
    

window = tk.Tk()
window.geometry("680x500")
window.grid_rowconfigure(0, weight=1)
basicLabels1(window)
window.mainloop()
