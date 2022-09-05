#import necessary packages
#from re import L
import smartsheet
import json

#define smartsheet user-specific api token
token = "Gxr62V7JvF8IPILpsaaGVHys3sgcEp8l5CTxI"

#initiate api call by creating an object of Smartsheet class, passing user-specific API token as parameter
smart = smartsheet.Smartsheet(token)

#make all API errors Python exceptions
smart.errors_as_exceptions()

def smartsheet_error():
    raise smartsheet.exceptions.ApiError

try:
    smartsheet_error()
except smartsheet.exceptions.ApiError as apierr:
    print(apierr)


# #get sheet details for Smartsheet License Purchase Requests
# sheet = smart.Sheets.get_sheet(2686308175898500) #sheet id

# #------Add Rows------

# #test the rate limit
# try:
#     for i in range(500):
#         row_a = smartsheet.models.Row()
#         row_a.to_bottom = True
#         row_a.cells.append({
#         'column_id': 375030148294532,#column id for user email
#         'value': "test",
#         'strict': False
#         })
#         row_a.cells.append({
#         'column_id': 4878629775665028, #column id for sheet count
#         'value': "test",
#         'strict': False
#         })
#         row_a.cells.append({
#         'column_id': 1921056239839108, #column id for sheet count
#         'value': "test",
#         'strict': False
#         })
#         row_a.cells.append({
#         'column_id': 6424655867209604, #column id for sheet count
#         'value': "test",
#         'strict': False
#         })
#         row_a.cells.append({
#         'column_id': 4172856053524356, #column id for sheet count
#         'value': "test",
#         'strict': False
#         })
#         row_a.cells.append({
#         'column_id': 8676455680894852, #column id for sheet count
#         'value': "test",
#         'strict': False
#         })
#         #add rows to sheet
#         response = smart.Sheets.add_rows(
#         2686308175898500,       # sheet_id
#         [row_a])
# except smartsheet.exceptions.ApiError as apierr:
#     print(apierr)
#     # if apierr['result']['errorCode'] == 4003:
#     #     print("This test worked!")
#     # else:
#     #     print("This test failed.")

# #------Delete Rows------

# #get sheet details for Smartsheet License Purchase Requests
# sheet = smart.Sheets.get_sheet(2686308175898500) #sheet id

# #write sheet data to a json file for transfer to python dictionary
# filename = r"Z:\Shared\Users\WKerby\My Computer\Documents\Smartsheet_py\python-read-write-sheet\\exceptions_test.json"
# with open(filename, "w") as fileobject:
#     fileobject.write(str(sheet))

# #use json package to convert json file to python dictionary
# with open('exceptions_test.json') as json_file:
#     sheet = json.load(json_file)

# #obtain list of current row_ids in Smartsheet licensed users grid
# row_ids = []
# for row in sheet["rows"]:
#     row_ids.append(row["id"])

# #wipe out all current rows in the sheet
# try:
#     for row_id in row_ids:
#         smart.Sheets.delete_rows(
#         2686308175898500,                       # sheet_id
#         [row_id ])     # row_ids
# except smartsheet.exceptions.ApiError as apierr:
#     print(apierr)
# else:
#     print("rows wiped out of smartsheet licensed users sheet")    