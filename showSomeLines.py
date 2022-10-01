from tkinter import Tk, Listbox, Button,  EXTENDED, END,  NSEW
import sqlite3

from pyrsistent import l
import flags

linesToShow = 15

def onClosing():
    global changes
    root.destroy()

def timeOut(reason):
    print("Change")

def getFromDB(listbox, idx):
    sql = "SELECT * FROM allData_dsevents where id >= %d and id <= %d;" % (
        idx-linesToShow, idx+linesToShow)
    conn = sqlite3.connect(flags.mainDB)
    cursor = conn.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    fileName = rows[0][6]
    for line in rows:
        listbox.insert(END, line[4])
    listbox.selection_set(linesToShow)
    conn.close()
    return fileName

def showForm(idx, fileName):
    global text, root
    root = Tk()
    root.geometry("700x560")
    listbox = Listbox(root, selectmode=EXTENDED,
                      width=110, height=linesToShow * 2 + 2)
    # call onClosing when user exits window
    root.protocol("WM_DELETE_WINDOW", onClosing)
    getFromDB(listbox, idx)
    root.title("Show Lines in File: " + fileName)
    listbox.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky=NSEW)
    btnExit = Button(root, height=1, width=10, text="Exit",
                     command=lambda: onClosing())
    btnExit.grid(row=1, column=0, padx=1, pady=1)
    root.mainloop()


text = None
root = None
if __name__ == '__main__':
    showForm(4000, "test")
