# Update a Google Sheet from Python
# https://gspread.readthedocs.io/en/latest/user-guide.html#formatting
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pprint

#Authorize the API
scope = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/drive.file'
    ]
file_name = 'c:/temp/client_key.json'
creds = ServiceAccountCredentials.from_json_keyfile_name(file_name,scope)
client = gspread.authorize(creds)


#Fetch the sheet
print("Client ------------ ", dir(client))
print("Files", client.list_spreadsheet_files())
id = '1z18FpYI9_mnaq9YFyF2ij60kab50_0nDqtAhdvIcfZg'
sheet = client.open_by_key(id)
print("Sheet ------------- ", dir(sheet))
print("Title ------------- ", sheet.title)
ws = sheet.worksheet("Sheet1")
python_sheet = ws.get_all_records()
pp = pprint.PrettyPrinter()
pp.pprint(python_sheet)
ws.format("B8:J20", {"numberFormat": {"type": "CURRENCY","pattern": "\"$\"#,##0.00"}})
ws.update_cell(8, 9, '5287800.33')
# Add a formula
ws.update('J8', '=I8-I7', raw=False)
ws.append_row(("05/20/20", 123.45, 78.56), value_input_option='RAW', insert_data_option=None, table_range=None)
