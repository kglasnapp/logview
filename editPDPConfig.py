from tkinter import Text, Tk, INSERT, END, RAISED, SUNKEN, Button, messagebox
import sqlite3
import flags
import re


def saveInput():
    global changes
    s = text.get("1.0", "end-1c")
    open("PDPConfig.csv", 'w').write(s)
    saveToDB(s)
    changes = False


def onClosing():
    global changes
    if changes:
        if messagebox.askyesno("Quit", "Do you want to save your changes?"):
            saveInput()
            root.destroy()
    else:
        root.destroy()


def onChange(event):
    global changes
    changes = True
    root.after(1000, timeOut, "Change")

def timeOut(reason):
    print("Change")

def getFromDB():
    sql = "select line from PDPConfig where profile=" + str(flags.profile)
    conn = sqlite3.connect(flags.mainDB)
    cursor = conn.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    s = ""
    for line in rows:
        s += line[0] + '\n'
    cursor.execute(sql)
    conn.close()
    return s

def createTable():
     # Create a database for the PDP Configuration data
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    # Create a new table with four columns
    sql = "create table if not exists PDPConfig ( "
    sql += "id integer PRIMARY KEY AUTOINCREMENT,"
    sql += "profile integer,"
    sql += "line text,"
    sql += "port integer)"
    cursor.execute(sql)
    conn.commit()
    conn.close()

def saveToDB(lines):
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute("delete from PDPConfig where profile = " + str(flags.profile))
    conn.commit()
    # Insert the data into the  PDP Configuration  table
    port = 1
    for line in lines.split("\n"):
        cursor.execute(
                'insert into PDPConfig (profile, line, port) values (?, ?, ?)', (flags.profile, line, port))
        print(port, line)
        port += 1
    conn.commit()
    conn.close()
    return True


def showForm():
    global changes, text, root
    changes = False
    root = Tk()
    root.title("Edit PDP Configuration -- Team 3932 Log File Viewer")
    text = Text(root, relief=SUNKEN)
    # call onClosing when user exits window 
    root.protocol("WM_DELETE_WINDOW", onClosing) 
    createTable()
    s = getFromDB()
    if len(s) == 0:
        try:
            fId = open("PDPConfig.csv", 'r')
            for line in fId:
                s += line
        except:
            print("Could not find file PDPConfig.csv")
    text.insert(INSERT, s)
    text.grid(row=0, column=0, columnspan=2, padx=5, pady=5)
    text.bind('<Key>', onChange)
    btnSave = Button(root, height=1, width=10, text="Save",
                     command=lambda: saveInput())
    btnSave.grid(row=1, column=0, padx=5, pady=5)
    btnExit = Button(root, height=1, width=10, text="Exit",
                     command=lambda: onClosing())
    btnExit.grid(row=1, column=1, padx=5, pady=5)
    root.mainloop()

if __name__ == '__main__':
    showForm()
