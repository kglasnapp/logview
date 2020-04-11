from tkinter import Text, Tk, INSERT, END, RAISED, SUNKEN, Button, messagebox
import sqlite3
import flags
import re
import tksheet


def saveInput():
    global changes, sheet
    data = sheet.get_sheet_data()
    s = ''
    for l in data:
        s += str(l[0]) + ',' + l[1] + "\n"
    open("PDPConfig.csv", 'w').write(s)
    saveToDB()
    changes = False


def onClosing():
    global changes, root
    if changes:
        if messagebox.askyesno("Quit", "Do you want to save your changes?"):
            saveInput()
            root.destroy()
    else:
        root.destroy()


def timeOut(reason):
    print("Change")


def getFromDB():
    sql = "select port, line from PDPConfig where profile=" + \
        str(flags.profile) + " order by port"
    conn = sqlite3.connect(flags.mainDB)
    cursor = conn.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    ar = []
    for r in rows:
        ar.append(list(r))
    conn.close()
    return ar


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


def saveToDB():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute("delete from PDPConfig where profile = " +
                   str(flags.profile))
    conn.commit()
    # Insert the data into the  PDP Configuration  table
    for line in sheet.get_sheet_data():
        try:
            port = int(line[0])
        except:
            port = 0
        if(port >= 1 and port <= 16 and len(line[1]) > 0):
            cursor.execute(
                'insert into PDPConfig (profile, port, line) values (?, ?, ?)', (flags.profile, port, line[1]))
            print(line[0], line[1])
    conn.commit()
    conn.close()
    return True


def selectCell(response):
    print("select cell", response)


def editCell(response):
    global changes
    print("edit cell", response)
    changes = True


def test(*arg):
    print(arg)


def insertRow():
    global sheet
    print("Insert Row")
    sheet.insert_row()
    sheet.refresh()


def showForm():
    global changes, root, sheet
    changes = False
    root = Tk()
    root.title("Edit PDP Configuration -- Team 3932 Log File Viewer")
    root.geometry("580x350")
    # call onClosing when user exits window
    root.protocol("WM_DELETE_WINDOW", onClosing)
    createTable()
    data = getFromDB()
    if(len(data) == 0):
        try:
            fId = open("PDPConfig.csv", 'r')
            for line in fId:
                ar = line.split(',')
                try:
                    port = int(ar[0])
                except:
                    port = 0
                if(port >= 1 and port <= 16):
                    data.append([port, ar[1].replace("\n", "")])
               
        except:
            print("Could not find file PDPConfig.csv")
        change = True # Needed to force DB update at exit when nothing in the db
    sheet = tksheet.Sheet(root, data=data, headers=["Port", "Description"], width=2000)

    btnSave = Button(root, height=1, width=10, text="Save",
                     command=lambda: saveInput())
    btnInsert = Button(root, height=1, width=10,
                       text="Insert",  command=lambda: insertRow())
    btnExit = Button(root, height=1, width=10, text="Exit",
                     command=lambda: onClosing())

    sheet.grid(row=0, column=0, columnspan=3, padx=5, pady=5, sticky="nswe")
    btnSave.grid(row=1, column=0, padx=5, pady=5)
    btnInsert.grid(row=1, column=1, padx=5, pady=5)
    btnExit.grid(row=1, column=2, padx=5, pady=5)


    sheet.enable_bindings(("rc_insert_row", "rc_delete_row", "row_select",
                           "edit_cell", "single_select", "cell_select"))
    sheet.extra_bindings([("cell_select", selectCell),
                          ("begin_edit_cell", editCell)])
    sheet.column_width(column=0, width=50)
    sheet.column_width(column=1, width=300)
    sheet.grid_columnconfigure(1, weight=1)

    root.mainloop()


sheet = None
changes = False
root = None

if __name__ == '__main__':
    showForm()
