import tkinter
import tksheet
root = tkinter.Tk()
root.geometry("800x350")
data = [[0,"Test 0"],[1, "Test 1"]]
sheet = tksheet.Sheet(root, data=data, headers=["Port", "Description"], width=800)
sheet.grid(row=0, column=0, padx=5, pady=5)
sheet.column_width(column=0, width=50)
sheet.column_width(column=1, width=600)
root.mainloop()