import tkinter
import tksheet

root = tkinter.Tk()
root.geometry("800x350")
root.grid_columnconfigure(0, weight = 1)
root.grid_rowconfigure(0, weight = 1)
frame = tkinter.Frame(root)
frame.grid_columnconfigure(0, weight = 1)
frame.grid_rowconfigure(0, weight = 1)
s = '1234567890'
s += s + s + s + s
data = [[0,"Test 0"],[1, "Test 1"],[2,s]]
sheet = tksheet.Sheet(frame, data=data, headers=["Port", "Description"])
sheet.grid(row=0, column=0, padx=5, pady=5,sticky='nesw')
sheet.height_and_width(200,780)
sheet.column_width(column=0, width=50)
sheet.column_width(column=1, width=750)
sheet.column_width(column=1)
frame.grid(row = 0, column = 0, sticky = "nswe")
sheet.grid(row = 0, column = 0, sticky = "nswe")
root.mainloop()