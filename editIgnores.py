from tkinter import Text, Tk, INSERT, END, RAISED, SUNKEN, Button, messagebox
import sqlite3
import flags
import re


def saveInput():
    global changes
    s = text.get("1.0", "end-1c")
    open("ignores.txt", 'w').write(s)
    if saveToDB(s):
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
    sql = "select line from ignores where profile=" + str(flags.profile)
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
     # Create a database for the ignore data
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    # Create a new table with four columns
    sql = "create table if not exists ignores ( "
    sql += "id integer PRIMARY KEY AUTOINCREMENT,"
    sql += "profile integer,"
    sql += "line text,"
    sql += "regex boolean)"
    cursor.execute(sql)
    conn.commit()
    conn.close()

def saveToDB(lines):
    # Create a database for the ignore data
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute("delete from ignores where profile = " + str(flags.profile))
    # Insert the data into the ignore table
    for line in lines.split("\n"):
        try:
            re.compile(line)
        except:
            print("Unable convert '%s' to a regular expression" % (line))
            messagebox.showerror(
                "Error", "Invalid regular expression:\n\n%s\n" % (line))
            return False
        if line != '':
            cursor.execute(
                'insert into ignores (profile, line, regex) values (?, ?, ?)', (flags.profile, line, True))
        print(line)
    conn.commit()
    conn.close()
    return True


def showForm():
    global changes, text, root
    changes = False
    root = Tk()
    root.title("Edit Ignores -- Team 3932 Log File Viewer")
    text = Text(root, relief=SUNKEN)
    # call onClosing when user exits window 
    root.protocol("WM_DELETE_WINDOW", onClosing) 
    createTable()
    s = getFromDB()
    if len(s) == 0:
        try:
            fId = open("ignores.txt", 'r')
            for line in fId:
                s += line
            changes = True
        except:
            pass
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


changes = False
text = None
root = None
if __name__ == '__main__':
    showForm()
