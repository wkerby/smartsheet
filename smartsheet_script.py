#import necessary packages
# import requests as r
import smartsheet
import logging
import os
import json

#define smartsheet user-specific api token
token = "Gxr62V7JvF8IPILpsaaGVHys3sgcEp8l5CTxI"

#initiate api call by creating an object of Smartsheet class, passing user-specific API token as parameter
smart = smartsheet.Smartsheet(token)
print("call 1 executed")
#return all Brasfield & Gorrie Smartsheet users in json format
response = smart.Users.list_users(
  include = "lastLogin",
  include_all=True)
print("call 2 executed")

#write the users to a json file for transfer to python dictionary
filename = r"Z:\\Users\\WKerby\\My Computer\\Documents\\Smartsheet_py\\python-read-write-sheet\\users.json"
with open(filename, "w") as fileobject:
    fileobject.write(str(response))

#use json package to convert json file to python dictionary
with open('users.json') as json_file:
    users = json.load(json_file)

#create respective dicts for currently licensed users and current unlicensed users
licensed_users = {"user_id":[],"user_email":[],"sheet_count":[],"last_login":[]}
unlicensed_users = {"user_id":[],"user_email":[]}
for user in users["data"]:
    if user["licensedSheetCreator"] == True:
        licensed_users["user_id"].append(user["id"])
    else:
        unlicensed_users["user_id"].append(user["id"])

# test view of user profile dictionary
# print(smart.Users.get_user(licensed_users["user_id"][0]).__dict__)

#for each user id in licensed user dictionary, instantiate a User object and add relevant fields of user info to dict
for user_id in licensed_users["user_id"]:
    user_profile = smart.Users.get_user(user_id).__dict__
    licensed_users["user_email"].append(str(user_profile["_email"]))
    licensed_users["sheet_count"].append(str(user_profile["_sheet_count"]))
    if str(user_profile["_last_login"]) == "None":
         licensed_users["last_login"].append(str(user_profile["_last_login"]))
    else:
        licensed_users["last_login"].append(str(user_profile["_last_login"])[5:7]+"/"+str(user_profile["_last_login"])[8:10]+"/"+str(user_profile["_last_login"])[:4])
print("call 3 executed")
#for each user id in unlicensed user dictionary, instantiate a User object and add relevant fields of user info to dict
for user_id in unlicensed_users["user_id"]:
    user_profile = smart.Users.get_user(user_id).__dict__
    unlicensed_users["user_email"].append(str(user_profile["_email"]))

if len(unlicensed_users["user_email"]) == len(unlicensed_users["user_id"]):
    print("call 4 executed")
else:
    print("call 4 failed: not all unlicensed user emails added properly.")

# #Establish skeleton of new Smartsheet grid for licensed users 
# licensed_users_sheet = smartsheet.models.Sheet({
#   'name': 'Smartsheet Licensed Users',
#   'columns': [{
#         'title': 'User Email',
#         'type': 'CONTACT_LIST',
#       }, {
#         'title': 'Sheet Count',
#         'type': 'TEXT_NUMBER',
#         'primary': True
#       },
#         {'title': 'Last Login',
#         'type': 'DATE'}
#   ]
# })

# #create Smartsheet grid in folder inside of IT/Smartsheet folder
# response2 = smart.Folders.create_sheet_in_folder(
#   8374399494580100,       # folder_id
#   licensed_users_sheet)
# # new_sheet = response2.result

#obtain column ids of newly created sheet with "get sheet"
sheet = smart.Sheets.get_sheet(2955863947274116) #sheet id
print("call 5 executed")
#write sheet data to a json file for transfer to python dictionary
filename = r"Z:\\Users\\WKerby\\My Computer\\Documents\\Smartsheet_py\\python-read-write-sheet\\smartsheet_licensed_users.json"
with open(filename, "w") as fileobject:
    fileobject.write(str(sheet))

#use json package to convert json file to python dictionary
with open('smartsheet_licensed_users.json') as json_file:
    sheet = json.load(json_file)
# print(sheet["rows"])

#obtain list of current row_ids in Smartsheet licensed users grid
row_ids = []
for row in sheet["rows"]:
    row_ids.append(row["id"])

#wipe out all current rows in the sheet
for row_id in row_ids:
    smart.Sheets.delete_rows(
    2955863947274116,                       # sheet_id
    [row_id ])     # row_ids

print("call 6 executed")

# #add user information in licensed_users py dict to "Smartsheet Licensed Users" grid in Smartsheet
for employee in range(len(licensed_users['user_id'])):

    row_a = smartsheet.models.Row()
    row_a.to_bottom = True
    row_a.cells.append({
    'column_id': 1442733793535876,#column id for user email
    'value': licensed_users['user_email'][employee],
    'strict': False
    })
    row_a.cells.append({
    'column_id': 5946333420906372, #column id for sheet count
    'value': licensed_users['sheet_count'][employee],
    'strict': False
    })
    row_a.cells.append({
    'column_id': 3694533607221124, #column id for sheet count
    'value': licensed_users['last_login'][employee],
    'strict': False
    })

    #add rows to sheet
    response = smart.Sheets.add_rows(
    2955863947274116,       # sheet_id
    [row_a])

print("call 7 executed")
#Phase 2
#read the Smartsheet User License Requests_DEMO sheet
sheet = smart.Sheets.get_sheet(5190433962780548) #sheet id
print("call 8 executed")

#write sheet data to a json file for transfer to python dictionary
filename = r"Z:\\Users\\WKerby\\My Computer\\Documents\\Smartsheet_py\\python-read-write-sheet\\smartsheet_user_license_requests.json"
with open(filename, "w") as fileobject:
    fileobject.write(str(sheet))

#use json package to convert json file to python dictionary
with open('smartsheet_user_license_requests.json') as json_file:
    sheet = json.load(json_file)

for user_row in sheet["rows"]:
    # print(user_row['cells'][2])
    if user_row['cells'][0]['displayValue'] == "#NO MATCH" or user_row['cells'][5]['displayValue'] == "I do not want an account or a license" or user_row['cells'][6] == True:
        print("This user either does not exist in the Brasfield Gorrie domain, does not want a license, or already has a license!")
    else:
        #if bg employee has a Smartsheet account but no a license, then make him/her a licensed user
        if user_row['cells'][2]['displayValue'] in unlicensed_users['user_email']:
            updated_user = smart.Users.update_user(
            unlicensed_users['user_id'][unlicensed_users['user_email'].index(user_row['cells'][2]['value'])],     # user_id
            smartsheet.models.User({
            'licensed_sheet_creator': True,
            'admin': False
            }))
        else:
            print("user email not recongnized")
                
        print("call 9 executed")