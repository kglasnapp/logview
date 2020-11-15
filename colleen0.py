import win32com.client
import csv
import sys
import datetime
xlApp = win32com.client.Dispatch("Excel.Application")
print ("Excel library version:", xlApp.Version)
#xlApp.Visible = 1
filename = "c:\\FunStuff\\2020 Robot\\Logs\\LogView\\COVID Tracking Spreadsheet revised KG.xlsx"
password = '2020Covid'
wb = xlApp.Workbooks.Open(filename, False, True, None, password, password, False)
sheet = wb.Sheets("RTW")
d = sheet.Range("A1:Z20")
print("Len", len(d[1]))
print(d)
print("Show Date", str(d(2,3))[0:10])
r = sheet.UsedRange
print(type(r))
wb.SaveAs("test1.xlsx", 51 , "")
wb.Close()
