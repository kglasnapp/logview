# Update a Google Sheet from Python
# https://gspread.readthedocs.io/en/latest/user-guide.html#formatting
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pprint
import sys
import os
import math
import locale
import time


def updateSheet(data):
    # Authorize the API
    scope = [
        'https://www.googleapis.com/auth/drive',
        'https://www.googleapis.com/auth/drive.file'
    ]
    file_name = 'c:/temp/client_key.json'
    creds = ServiceAccountCredentials.from_json_keyfile_name(file_name, scope)
    client = gspread.authorize(creds)
    # Fetch the sheet from Google Drive
    id = '1z18FpYI9_mnaq9YFyF2ij60kab50_0nDqtAhdvIcfZg'
    sheet = client.open_by_key(id)
    worksheet = sheet.worksheet("EdwardJones")
    python_sheet = worksheet.get_all_records()
    pp = pprint.PrettyPrinter()
    last = len(python_sheet) - 1
    print(python_sheet[last])
    total = float(str(python_sheet[last]['Total']).replace('$', '').replace(',', ''))
    print('Old Total:%s' % (locale.currency(total, grouping=True)))
    print('New Total:%s'% (locale.currency(data[9], grouping=True)))
    print('Change:%s'% (locale.currency(data[9] - total, grouping=True)))
    # pp.pprint(python_sheet)
    worksheet.format("B9:K%d" % (last + 10), {"numberFormat": {
                     "type": "CURRENCY", "pattern": "\"$\"#,##0.00"}})
    #worksheet.update('J8', '=I8-I7', raw=False)
    worksheet.append_row(data, value_input_option='RAW',
                         insert_data_option=None, table_range=None)


def getValue(start, next):
    global s
    start = s.find(start)
    t = s[start:start+300]
    result = t.find(next) + len(next)
    t = t[result:result+14]
    # print(start, t)
    result = t.find("<")
    return float(t[0:result].replace(",", ""))

locale.setlocale(locale.LC_ALL, '')
file = "z:\\Edward Jones\\Home _ Edward Jones Account Access.html"
file = "z:\\Edward Jones\\Snapshot _ Edward Jones.html"
modTimesinceEpoc = os.path.getmtime(file)
date = time.strftime('%m/%d/%Y', time.localtime(modTimesinceEpoc))
stream = open(file, 'rb')
s = ""
for t in stream:
    s += str(t)
# print("Read File:", len(s))
grand = getValue("Total Current Value", 'mat-headline">$')
joint2 = getValue('****1352', 'edj-balance">$')
cash = getValue("****1353", 'edj-balance">$')
iraKeith = getValue("****3217", 'edj-balance">$')
iraSue = getValue("****6343", 'edj-balance">$')
roth = getValue("****3238", 'edj-balance">$')

total = joint2 + cash + iraKeith + iraSue + roth
if(abs(total-grand) > .1):
    print("Delta error should be 0.0 it is: ", total - grand)
djia = getValue("DJIA", 'current-value">')
nasdq = getValue("COMPQ", 'current-value">')
sp = getValue("SPX", 'current-value">')
# Get the date -- i.e. As of
data = (date, djia, nasdq, sp, joint2, cash, iraKeith, iraSue, roth, grand)
paste = "%s,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f" % data
command = 'echo ' + paste + ' | clip'
os.system(command)
print(paste)
updateSheet(data)
