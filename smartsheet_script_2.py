#import necessary packages
import smartsheet
import logging
import os
import json
import quarters
import smtplib

#define smartsheet user-specific api token
token = "Gxr62V7JvF8IPILpsaaGVHys3sgcEp8l5CTxI"

#initiate api call by creating an object of Smartsheet class, passing user-specific API token as parameter
smart = smartsheet.Smartsheet(token)
print("api call instantiated")

#return all Brasfield & Gorrie Smartsheet users in json format
response = smart.Users.list_users(
  include = "lastLogin",
  include_all=True)
print("json users list obtained")

#write the users to a json file for transfer to python dictionary
filename = r"Z:\\Shared\\Users\\WKerby\\My Computer\\Documents\\Smartsheet_py\\python-read-write-sheet\\users.json"
with open(filename, "w") as fileobject:
    fileobject.write(str(response))

#use json package to convert json file to python dictionary
with open('users.json') as json_file:
    users = json.load(json_file)

#create respective dicts for currently licensed users and currently unlicensed users
licensed_users = {"user_id":[],"user_email":[],"sheet_count":[],"last_login":[]}
unlicensed_users = {"user_id":[],"user_email":[]}
for user in users["data"]:
    if user["licensedSheetCreator"] == True:
        licensed_users["user_id"].append(user["id"])
    else:
        unlicensed_users["user_id"].append(user["id"])

#for each user id in licensed user dictionary, instantiate a User object and add relevant fields of user info to dict
for user_id in licensed_users["user_id"]:
    user_profile = smart.Users.get_user(user_id).__dict__
    licensed_users["user_email"].append(str(user_profile["_email"]))
    licensed_users["sheet_count"].append(str(user_profile["_sheet_count"]))
    if str(user_profile["_last_login"]) == "None":
         licensed_users["last_login"].append(str(user_profile["_last_login"]))
    else:
        licensed_users["last_login"].append(str(user_profile["_last_login"])[5:7]+"/"+str(user_profile["_last_login"])[8:10]+"/"+str(user_profile["_last_login"])[:4])
print("licensed users dict created")

#for each user id in unlicensed user dictionary, instantiate a User object and add relevant fields of user info to dict
#only adding user email field to unlicensed user dictionary 
for user_id in unlicensed_users["user_id"]:
    user_profile = smart.Users.get_user(user_id).__dict__
    unlicensed_users["user_email"].append(str(user_profile["_email"]))

#verify that GET call functioned correctly
if len(unlicensed_users["user_email"]) == len(unlicensed_users["user_id"]):
    print("unlicensed users dict created")
else:
    print("Oops! unlicensed users call failed")

#------Phase 2------

#store sheet id for Smartsheet User License Requests 2.0 sheet into a variable
sheet_id = 5190433962780548

#read the Smartsheet User License Requests 2.0 sheet
sheet = smart.Sheets.get_sheet(5190433962780548) #sheet id
print("smartsheet user license requests 2.0 sheet read")

#write sheet data to a json file for transfer to python dictionary
filename = r"Z:\\Shared\\Users\\WKerby\\My Computer\\Documents\\Smartsheet_py\\python-read-write-sheet\\smartsheet_user_license_requests.json"
with open(filename, "w") as fileobject:
    fileobject.write(str(sheet))

#use json package to convert json file to python dictionary
with open('smartsheet_user_license_requests.json') as json_file:
    sheet = json.load(json_file)

#store column ids of Smartsheet User License Requests 2.0 sheet in dictionary
columns = {}
for column in sheet["columns"]:
    columns[column['title']] = column['id']

for quarter in list(quarters.quarters(sheet["rows"]).values()):
    for user_row in quarter:
        #if request line item has already been handled, pass
        if user_row['cells'][10] == True:
            pass
        else: 
            #if email entered not a bg email, if user already has a license, or if user determines he/she does not want a license, indicate that request has been handled 
            if user_row['cells'][0]['displayValue'] == "#NO MATCH" or user_row['cells'][9]['displayValue'] == "I do not want an account or a license" or user_row['cells'][6]['displayValue'] in licensed_users['user_email']:
                print("This user either does not exist in the Brasfield Gorrie domain, does not want an account/license, or already has a Smartsheet license!")
                # Build new cell value
                new_cell = smartsheet.models.Cell()
                new_cell.column_id = columns['RequestHandled?']
                new_cell.value = True
                new_cell.strict = False
                # Build the row to update
                new_row = smartsheet.models.Row()
                new_row.id = user_row["id"]
                new_row.cells.append(new_cell)
                # Update rows
                updated_row = smart.Sheets.update_rows(
                sheet_id,      # sheet_id
                [new_row])
            else:
                #bg user has a Smartsheet account
                if user_row['cells'][6]['displayValue'] in unlicensed_users['user_email']:
                    #bg user has a Smartsheet account, opting for Smartsheet account (not likely, indicate that the request has been handled)
                    if user_row['cells'][9]['displayValue'] == "I would like a Smartsheet account (unlicensed)":
                        print("HasSmartsheetAccount = Yes, ProvisionAccount = No, ProvisionLicense = No")
                        # Build new cell value
                        new_cell = smartsheet.models.Cell()
                        new_cell.column_id = columns['RequestHandled?']
                        new_cell.value = True
                        new_cell.strict = False
                        # Build the row to update
                        new_row = smartsheet.models.Row()
                        new_row.id = user_row["id"]
                        new_row.cells.append(new_cell)
                        # Update rows
                        updated_row = smart.Sheets.update_rows(
                        sheet_id,      # sheet_id
                        [new_row])
                    #bg user has a Smartsheet account, opting for a license (provision him/her a license and indicate that request has been handled)
                    else:
                        print("HasSmartsheetAccount = Yes, ProvisionAccount = No, ProvisionLicense = Yes")
                        updated_user = smart.Users.update_user(
                        unlicensed_users['user_id'][unlicensed_users['user_email'].index(user_row['cells'][6]['value'])],     # user_id
                        smartsheet.models.User({ #will need a try-except block here in case there are no available licenses
                        'licensed_sheet_creator': True,
                        'admin': False
                        }))
                        # Build new cell value
                        new_cell = smartsheet.models.Cell()
                        new_cell.column_id = columns['RequestHandled?']
                        new_cell.value = True
                        new_cell.strict = False
                        # Build the row to update
                        new_row = smartsheet.models.Row()
                        new_row.id = user_row["id"]
                        new_row.cells.append(new_cell)
                        # Update rows
                        updated_row = smart.Sheets.update_rows(
                        sheet_id,      # sheet_id
                        [new_row])
                #bg employee does not yet have a Smartsheet account
                else:
                    if user_row['cells'][9]['displayValue'] == "I would like a Smartsheet account (unlicensed)":
                        print("HasSmartsheetAccount = No, ProvisionAccount = Yes, ProvisionLicense = No")
                        new_user = smart.Users.add_user(
                        smartsheet.models.User({
                        'first_name': user_row['cells'][4]['displayValue'],
                        'last_name': user_row['cells'][5]['displayValue'],
                        'email': user_row['cells'][6]['displayValue'],
                        'admin': False,
                        'licensed_sheet_creator': False
                    })
                    )
                    else:
                        print("HasSmartsheetAccount = No, ProvisionAccount = Yes, ProvisionLicense = Yes")
                        new_user = smart.Users.add_user(
                        smartsheet.models.User({ #will need a try-except block here in case there are no available licenses
                        'first_name': user_row['cells'][4]['displayValue'],
                        'last_name': user_row['cells'][5]['displayValue'],
                        'email': user_row['cells'][6]['displayValue'],
                        'admin': False,
                        'licensed_sheet_creator': True
                    })
                    )
                    # Build new cell value
                    new_cell = smartsheet.models.Cell()
                    new_cell.column_id = columns['RequestHandled?']
                    new_cell.value = True
                    new_cell.strict = False
                    # Build the row to update
                    new_row = smartsheet.models.Row()
                    new_row.id = user_row["id"]
                    new_row.cells.append(new_cell)
                    # Update rows
                    updated_row = smart.Sheets.update_rows(
                    sheet_id,      # sheet_id
                    [new_row])
print('user license request(s) handled')
