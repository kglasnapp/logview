from tkinter import ttk, Menu, Button, Label, Toplevel, Checkbutton, Entry, Text
import tkinter.messagebox
import tkinter as tk
import tksheet as ts
import db as db
import utils
import flags
import re
import sheet as sh


class Root(tk.Tk):
    sheet = None
    dataStale = True
    
    def __init__(self):
        super(Root, self).__init__()
        
        self.title("Team 3932 Log File Viewer")
        self.minsize(640, 400)
        self.configure(background="white")
        self.createMenu()
        self.addFilesTab(self)     
        
        # tabControl = ttk.Notebook(self)
        # self.tab1 = ttk.Frame(tabControl)
        # tabControl.add(self.tab1, text="Files")
        # self.addFilesTab(self.tab1)
        # self.tab2 = ttk.Frame(tabControl)
        # tabControl.add(self.tab2, text="Events")
        # self.addEventsTab(self.tab2)
        # self.tab3 = ttk.Frame(tabControl)
        # tabControl.add(self.tab3, text="Logs")
        # self.tab4 = ttk.Frame(tabControl)
        # tabControl.add(self.tab4, text="tab 4")
        # self.addingTab4()
        # tabControl.grid(row = 0, column = 0)
        
        
       # tabControl.pack(expand=1, fill="both")
     
        
    def drag_select_rows(self, response):
        pass
        #print (response)
        
    def deselect(self, event):
        print("Deselect - my")
        c = self.sheet.get_highlighted_cells()
        ar = []
        for x in c:
           ar.append(x[0])
           # print("File:", self.inData[x[0]][0])
        ar.sort(reverse=True)
        for r in ar:
            self.sheet.dehighlight_cells(row = r, column = 0, canvas = "table", all_ = False, redraw = False)
        self.sheet.refresh(True, True)
        
    
    def cell_select(self, response):
        print ("My Cell Select:", response)
        self.sheet.highlight_cells(row = response[1], column = 0, bg = "#ed4337", fg = "white", redraw = True)
        self.sheet.refresh()
        
    def shift_select_cells(self, response):
        print (response)

    def drag_select_cells(self, response):
        print (response)
        for r in range(response[1],response[3]):
             self.sheet.highlight_cells(row = r, column = 0, bg = "#ed4337", fg = "white", redraw = True)
        self.sheet.refresh(True, True)

    def ctrl_a(self, response):
        print (response)

    def row_select(self, response):
        print ("Row Select", response)

    def shift_select_rows(self, response):
        print ("Shift Select Rows", response)

    def startpressed(self):
        new = tk.Toplevel(self)
        new.minsize(640, 400)
        new.geometry('500x300')
        new.configure(background="white")
       # tabControl1 = ttk.Notebook(new)
        #new.tab1 = ttk.Frame(tabControl1)
        #tabControl1.add(new.tab1, text="tab 1")
        #tabControl1.pack(expand=1, fill="both")

    def createMenu(self):
        menubar = Menu(self)
        self.config(menu=menubar)

        file_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Exit")

        help_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About Us")

    def addingTab4(self):
        Label(self.tab4, text="Please Select your choice").place(x=250, y=20)
        Button(self.tab4, text="Submit",
               command=lambda: self.submit()).place(x=520, y=320)

    # def addEventsTab(self, tab):
    #     inData = [("Keith",), ("Sue",)]
    #     self.sheet = ts.Sheet(tab, data=inData, headers=["File Name"])
    #     self.sheet.grid(row=1, column=0)

    def addFilesTab(self, tab):
        Button(tab, text="Refresh",
               command=lambda: self.submit()).grid(row=0, column=0)
        Label(tab, text="Month:").grid(row=0, column=1)
        self.monthV = tk.StringVar()
        self.monthV.set("3")
        month = Entry(tab, width=4, textvariable=self.monthV)
        month.grid(row=0, column=2)
        month.bind('<Key-Return>', self.changeDay)
        month.bind('<FocusOut>', self.changeDay)
        Label(tab, text="Day:").grid(row=0, column=3)
        self.dayV = tk.StringVar()
        self.dayV.set("8-10")
        day = ttk.Entry(tab, width=8, textvariable=self.dayV,
                      validatecommand=self.on_change)
        day.grid(row=0, column=4)
        day.bind('<Key-Return>', self.changeDay)
        day.bind('<FocusOut>', self.changeDay)
        self.dslogV = tk.BooleanVar()
        Checkbutton(tab, text="dslog", command=self.vChanged,
                    variable=self.dslogV, onvalue=True, offvalue=False).grid(row=0, column=6)
        self.dseventsV = tk.BooleanVar()
        self.dseventsV.set(True)
        Checkbutton(tab, text="dsevents", command=self.vChanged,
                    variable=self.dseventsV, onvalue=True, offvalue=False).grid(row=0, column=7)
        self.inData = self.getFiles()
        #self.fileTab = tab
        self.setupSheet()
        
    def setupSheet(self):
        self.sheet = ts.Sheet(self, data=self.inData, headers=[
                              "File Name"], set_all_heights_and_widths=True,column_width = 290, width=290, height=900)
        self.sheet.grid(row=1, column=0, columnspan=6)
      
       
        self.sheet.enable_bindings(
            ("single_select", "drag_select", "column_drag_and_drop", "row_drag_and_drop",
             "column_select", "row_select", "column_width_resize", "double_click_column_resize",                                          
             "arrowkeys", "row_height_resize", "double_click_row_resize", "right_click_popup_menu",
             "rc_select", "rc_insert_column", "rc_delete_column", "rc_insert_row", "rc_delete_row",
             "copy", "cut", "paste", "delete", "undo", "edit_cell"))
        
        self.sheetBindings = [
            ("cell_select", self.cell_select),
            ("shift_cell_select", self.shift_select_cells),
            ("drag_select_cells", self.drag_select_cells),
            ("ctrl_a", self.ctrl_a),
            ("row_select", self.row_select),
            ("shift_row_select", self.shift_select_rows),
            ("drag_select_rows", self.drag_select_rows),
            ("deselect", self.deselect)]
        
        self.sheet.extra_bindings(self.sheetBindings)
    def changeDay(self, value):
        print("Day Changed", self.dayV.get(), value)
        self.vChanged()
        return True

    def on_change(self):
        print("Day Changed Bind:", self.dayV.get())
        self.vChanged()
        return True

    def vChanged(self):
        print("---  Something Changed ---")
        self.inData = self.getFiles()
        #self.sheet.data_reference(inData, reset_row_positions=False, reset_col_positions=False)
        ##self.sheet.set_sheet_data(inData,reset_row_positions=False, reset_col_positions=False)
        #self.sheet.refresh()
        self.setupSheet()
        # self.sheet = ts.Sheet(self, data=self.inData, headers=[
        #     "File Name"], set_all_heights_and_widths=True, width=400, height=700)
        # self.sheet.grid(row=1, column=0, columnspan=6)

    def getValues(self):
        self.values = {
            "year": str(flags.year),
            "month": self.monthV.get(),
            "day": self.dayV.get(),
            "dslog": self.dslogV.get(),
            "dsevents": self.dseventsV.get()
        }
        return self.values

    def submit(self):
        newTop = Toplevel(self.master)
        Label(newTop, text="Review").pack()
        newTop.title("Review and Submit")
        newTop.focus_set()
        newTop.geometry("400x600")
    
    def result1(self):
        ttk.Notebook.select(self.tab7)

    def getFiles(self):
        if(self.dataStale):
            db.db.createConnection("data.db")
            cur = db.db.connection.cursor()
            cur.execute("SELECT fileName FROM files order by filename;")
            data = cur.fetchall()
        exp = utils.getRegularExpressionD(self.getValues())
        print("Regular Exp:", exp)
        reg = re.compile(exp)
        files = []
        for r in data:
            if reg.match(r[0]):
                files.append(r)
        files.sort()
        self.inData = files
        return files


root = Root()
root.mainloop()
