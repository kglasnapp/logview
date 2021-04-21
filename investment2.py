
# Update a Google Sheet from Python
# Needs the lastest version of chromedrive.exe which is located at c:/
# https://gspread.readthedocs.io/en/latest/user-guide.html#formatting
# https://github.com/microsoft/playwright-python to automate web

# share via pythonupdate@voice-api-203820.iam.gserviceaccount.com

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pprint
import sys
import os
import math
import locale       
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import selenium
import time

from selenium.webdriver.support.expected_conditions import staleness_of
from selenium.webdriver.support.wait import WebDriverWait

def wait_for_page_load(browser, timeout=30):
    old_page = browser.find_element_by_tag_name('html')
    yield
    WebDriverWait(browser, timeout).until(
        staleness_of(old_page)
    )
    
def getDataFromEdwardJones(file, userID, passCode):
    chromedriver = 'c:\\temp\\chromedriver.exe'
    userProfile = "C:\\Users\\kglas\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\"
    options = webdriver.ChromeOptions()
    options.add_argument("user-data-dir="+userProfile)
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(
        options=options, desired_capabilities=options.to_capabilities(), executable_path=chromedriver)
    driver.get(
        'https://accountaccess.edwardjones.com/ca-logon/logon.action?MobileSiteInd=N')
    elemN = driver.find_element_by_name("userNa")
    elemN.clear()
    elemN.send_keys(userID)
    elemN.send_keys(Keys.RETURN)
    elemP = driver.find_element_by_name("passwd")
    elemP.clear()
    elemP.send_keys(passCode)
    elemP.send_keys(Keys.RETURN)
    # No need to do a click as the return above starts the logon process.
    time.sleep(1)
    wait_for_page_load(driver) 
    
    print("Start Sleep")
    time.sleep(10)
    print("Complete Sleep")
    with open(file, 'w+', encoding="utf-8") as f:
        f.write(driver.page_source)
        f.close()
    print("File Saved")
    driver.close()


def getValue(s, start, next):
    print("Start", start)
    start = s.find(start)
    if start < 0:
        return 0.0
    t = s[start:start+300].replace(" ",'')
    result = t.find(next) + len(next)
    
    t = t[result:result+14]
    # print(start, t)
    result = t.find("<")
    return float(t[0:result].replace(",", ""))

def updateSheet(data):
    # Authorize the API
    scope = [
        'https://www.googleapis.com/auth/drive',
        'https://www.googleapis.com/auth/drive.file'
    ]
    file_name = 'c:/temp/client_key.json'
    locale.setlocale(locale.LC_ALL, '')
    creds = ServiceAccountCredentials.from_json_keyfile_name(file_name, scope)
    client = gspread.authorize(creds)
    # Fetch the sheet from Google Drive
    id = '1z18FpYI9_mnaq9YFyF2ij60kab50_0nDqtAhdvIcfZg'
    sheet = client.open_by_key(id)
    worksheet = sheet.worksheet("EdwardJones")
    python_sheet = worksheet.get_all_records()
    #pp = pprint.PrettyPrinter()
    last = len(python_sheet) - 1
    print(python_sheet[last])
    total = float(str(python_sheet[last]['Total']).replace(
        '$', '').replace(',', ''))
    print('Old Total:%s' % (locale.currency(total, grouping=True)))
    print('New Total:%s' % (locale.currency(data[9], grouping=True)))
    print('Change:%s' % (locale.currency(data[9] - total, grouping=True)))
    change = data[9] - total
    # pp.pprint(python_sheet[0])
    worksheet.format("B9:L%d" % (last + 10), {"numberFormat": {
                     "type": "CURRENCY", "pattern": "\"$\"#,##0.00"}})
    worksheet.format("M%d:T%d" % (last + 3, last + 3), {"numberFormat": {
                     "type": "PERCENT", "pattern": "#0.00%"}})
    if change < 0:
        worksheet.format("K%d" % (last + 3),
                         {'textFormat': {'foregroundColor': {'red': 1.0}}})

    worksheet.append_row(data, value_input_option='RAW',
                         insert_data_option=None, table_range=None)
    row = str(last+3)
    p = (last+3, last+2, last+3)
    worksheet.update('K' + row, '=J%d - J%d' % (last+3, last+2), raw=False)
    worksheet.update('L' + row, '=J%d - J$2' % (last+3), raw=False)
    worksheet.update('M' + row, '=(B%d - B%d)/B%d' % p, raw=False)
    worksheet.update('N' + row, '=(C%d - C%d)/C%d' % p, raw=False)
    worksheet.update('O' + row, '=(D%d - D%d)/D%d' % p, raw=False)
    worksheet.update('P' + row, '=(E%d - E%d)/E%d' % p, raw=False)
    worksheet.update('Q' + row, '=(F%d - F%d)/F%d' % p, raw=False)
    worksheet.update('R' + row, '=(G%d - G%d)/G%d' % p, raw=False)
    worksheet.update('S' + row, '=(I%d - I%d)/I%d' % p, raw=False)
    worksheet.update('T' + row, '=(J%d - J%d)/J%d' % p, raw=False)


def prepareDataForUpdate(file):
    modTimesinceEpoc = os.path.getmtime(file)
    date = time.strftime('%m/%d/%Y', time.localtime(modTimesinceEpoc))
    stream = open(file, 'rb')
    s = ""
    for t in stream:
        s += str(t)
    grand = getValue(s, "Total Current Value", 'mat-headline">$')
    joint2 = getValue(s, '****1352', 'edj-balance">$')
    cash = getValue(s, "****1353", 'edj-balance">$')
    iraKeith = getValue(s, "****3217", 'edj-balance">$')
    iraSue = getValue(s, "****6343", 'edj-balance">$')
    roth = getValue(s, "****3238", 'edj-balance">$')

    total = joint2 + cash + iraKeith + iraSue + roth
    if(abs(total-grand) > .1):
        print("Delta error should be 0.0 it is: ", total - grand)
    djia = getValue(s, "DJIA", 'current-value">')
    nasdq = getValue(s, "COMPQ", 'current-value">')
    sp = getValue(s, "SPX", 'current-value">')
    data = (date, djia, nasdq, sp, joint2, cash, iraKeith, iraSue, roth, grand)
    paste = "%s,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f" % data
    print(paste)
    return data

# Start of program to get our stock data from Edward Jones
file = "c:\\temp\\page.html"
userID = "kglasnapp"
# Get passcode from file on local PC
passFile = "c:\\Users\\kglas\\Documents\\edjones.txt"
passCode = open(passFile, 'r').readlines()[0]
getDataFromEdwardJones(file, userID, passCode)
data = prepareDataForUpdate(file)
updateSheet(data)
