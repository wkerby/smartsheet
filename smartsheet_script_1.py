#import necessary packages
import smartsheet
import logging
import os
import json
import quarters
import time

#define smartsheet user-specific api token
token = "Gxr62V7JvF8IPILpsaaGVHys3sgcEp8l5CTxI"

#initiate api call by creating an object of Smartsheet class, passing user-specific API token as parameter
smart = smartsheet.Smartsheet(token)
print("api call instantiated")

#turn on python exception detection for smartsheet api errors
smart.errors_as_exceptions(True)

#return all Brasfield & Gorrie Smartsheet users in json format
try:
    response = smart.Users.list_users(
        include = "lastLogin",
        include_all=True)
except Exception as e:
    print("SS API error detected")
    exc = json.loads(str(e))
    print(exc)
else:
    users = json.loads(str(response))

#create dicts for currently licensed users and currently unlicensed users
licensed_users = {"user_id":[],"user_email":[],"sheet_count":[],"last_login":[]}
unlicensed_users = {"user_id":[],"user_email":[]}
for user in users["data"]:
    if user["licensedSheetCreator"] == True:
        licensed_users["user_id"].append(user["id"])
    else:
        unlicensed_users["user_id"].append(user["id"])

#for each user id in licensed user dictionary, instantiate a User object and add relevant fields of user info to dict
try:
    for user_id in licensed_users["user_id"]:
        user_profile = smart.Users.get_user(user_id).__dict__
        licensed_users["user_email"].append(str(user_profile["_email"]))
        licensed_users["sheet_count"].append(str(user_profile["_sheet_count"]))
        if str(user_profile["_last_login"]) == "None":
            licensed_users["last_login"].append(str(user_profile["_last_login"]))
        else:
            licensed_users["last_login"].append(str(user_profile["_last_login"])[5:7]+"/"+str(user_profile["_last_login"])[8:10]+"/"+str(user_profile["_last_login"])[:4])
except Exception as e:
    print("SS API error detected")
    exc = json.loads(str(e))
    print(exc)
else:
    print("Number of licensed users:", str(len(licensed_users["user_email"])))
    print("licensed users dict created")

#for each user id in unlicensed user dictionary, instantiate a User object and add relevant fields of user info to dict
try:
    for user_id in unlicensed_users["user_id"]:
        user_profile = smart.Users.get_user(user_id).__dict__
        unlicensed_users["user_email"].append(str(user_profile["_email"]))
except Exception as e:
    print("SS API error detected")
    exc = json.loads(str(e))
    print(exc)

#verify that GET call functioned correctly
if len(unlicensed_users["user_email"]) == len(unlicensed_users["user_id"]):
    print("Number of unlicensed users:", str(len(unlicensed_users["user_email"])))
    print("unlicensed users dict created")
else:
    print("Oops! unlicensed users call failed")

#------Phase 1------

#obtain column ids of Smartsheet Licensed Users sheet with "get sheet"
try:
    sheet = smart.Sheets.get_sheet(2955863947274116) #sheet id
except Exception as e:
    print("SS API error detected")
    exc = json.loads(str(e))
    print(exc)
else:
    sheet = json.loads(str(sheet))

#obtain list of current row_ids in Smartsheet licensed users grid
row_ids = []
for row in sheet["rows"]:
    row_ids.append(row["id"])
print("Number of rows to delete from Smartsheet Licensed Users sheet:", str(len(row_ids)))

#turn off python exception detection for smartsheet api errors
smart.errors_as_exceptions(False)

#wipe out all current rows in the sheet
for quarter in list(quarters.quarters(row_ids).values()): #for every separate quarter list in the row_ids list
    for row_id in quarter:
        smart.Sheets.delete_rows(
        2955863947274116,                       # sheet_id
        [row_id ])     # row_ids
print("rows wiped out of smartsheet licensed users sheet")

#turn on python exception detection for smartsheet api errors
smart.errors_as_exceptions(True)

#add user information in licensed_users py dict to "Smartsheet Licensed Users" grid in Smartsheet
try:
    for quarter in list(quarters.quarters(licensed_users['user_id']).values()):
        for employee in quarter:

            row_a = smartsheet.models.Row()
            row_a.to_bottom = True
            row_a.cells.append({
            'column_id': 1442733793535876,#column id for user email
            'value': licensed_users['user_email'][licensed_users["user_id"].index(employee)],
            'strict': False
            })
            row_a.cells.append({
            'column_id': 5946333420906372, #column id for sheet count
            'value': licensed_users['sheet_count'][licensed_users["user_id"].index(employee)],
            'strict': False
            })
            row_a.cells.append({
            'column_id': 3694533607221124, #column id for sheet count
            'value': licensed_users['last_login'][licensed_users["user_id"].index(employee)],
            'strict': False
            })

            #add rows to sheet
            response = smart.Sheets.add_rows(
            2955863947274116,       # sheet_id
            [row_a])
except Exception as e:
    print("SS API error detected")
    exc = json.loads(str(e))
    print(exc)
else:
    print("licensed user rows added to smartsheet licensed users sheet")

                        


                
                


                    
