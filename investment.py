# Update a Google Sheet from Python
# https://gspread.readthedocs.io/en/latest/user-guide.html#formatting
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pprint
import sys
import os
import math
import locale


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
    total = float(python_sheet[last]['Total'].replace('$', '').replace(',', ''))
    print('Old Total:%s' % (locale.currency(total, grouping=True)))
    print('New Total:%s'% (locale.currency(data[8], grouping=True)))
    print('Change:%s'% (locale.currency(data[8] - total, grouping=True)))
    # pp.pprint(python_sheet)
    worksheet.format("B8:J%d" % (last + 1), {"numberFormat": {
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
stream = open(file, 'rb')
s = ""
for t in stream:
    s += str(t)
# print("Read File:", len(s))
grand = getValue("grandTotalNumeral", ">$")
joint2 = getValue('performance.action?accountSwitch=Joint-2', 'alignRight">$')
cash = getValue("performance.action?accountSwitch=CashReserve",
                'alignRight">$')
ira = getValue("performance.action?accountSwitch=Trad+IRA-1", 'alignRight">$')
roth = getValue("performance.action?accountSwitch=Roth+IRA-1", 'alignRight">$')

total = joint2 + cash + ira + roth
if(abs(total-grand) > .1):
    print("Delta error should be 0.0 it is: ", total - grand)
djia = getValue(">DJIA<", '">')
nasdq = getValue("NASDQ", '">')
sp = getValue("S&amp;P", '">')
# Get the date -- i.e. As of
f = "As of&nbsp;"
r = s.find(f) + len(f)
d = s[r:r+10]
data = (d, djia, nasdq, sp, joint2, cash, ira, roth, grand)
paste = "%s,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f" % data
command = 'echo ' + paste + ' | clip'
os.system(command)
print(paste)
updateSheet(data)
