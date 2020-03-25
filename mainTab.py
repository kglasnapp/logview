import tkinter as tk
import dseventsF
import dsFiles

def createMenu(tab):
    menubar = tk.Menu()
    tab.config(menu=menubar)
    file_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(label="Open")
    file_menu.add_command(label="Save")
    file_menu.add_command(label="Exit")
    help_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Help", menu=help_menu)
    help_menu.add_command(label="About Us")
    
def basicLabels(tab):
    frame = tk.Frame(tab)
    frame.grid(row=0,column=0, sticky='ns')
    lbl0 = tk.Label(frame, text="Top label")
    lbl1 = tk.Label(frame, text="Middle label")
    lbl2 = tk.Label(frame, text="Bottom label")
    lbl0.grid(row=0,column=0)
    lbl1.grid(row=1,column=0)
    lbl2.grid(row=2,column=0)
    frame.grid_rowconfigure(1, weight=1)
    return frame

global f0, f1

window = tk.Tk()
window.geometry("780x550")
window.title("Team 3932 Log File Viewer")
window.configure(background="white")
window.grid_rowconfigure(0, weight=1)
createMenu(window)

f0 = dsFiles.dsFiles(window)
f0.getFrame().grid(row=0, column=0, padx=5, pady=5,stick='NS')

f1 = dseventsF.dsevents(window, f0)
f1.getFrame().grid(row=0, column=1, padx=5, pady=5,stick='NESW')
window.grid_columnconfigure(1, weight=1)

window.mainloop()
