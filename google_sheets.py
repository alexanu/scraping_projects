# Article: https://towardsdatascience.com/turn-google-sheets-into-your-own-database-with-python-4aa0b4360ce7

# pip install gspread
# pip install oauth2client

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

# Connect to Google Sheets
scope = ['https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive"]

credentials = ServiceAccountCredentials.from_json_keyfile_name("google-sheets-creds-python.json", scope)
client = gspread.authorize(credentials)
sheet = client.create("NewDatabase") # this new sheet is only visible to the service account we created before. 
sheet.share('oanufriyev@gmail.com', perm_type='user', role='writer') # to access this sheet with our own Google account, we must share it with our email
                    # sheet will be in the “Shared with me” section in your Google Drive

sheet = client.open("NewDatabase").sheet1

df = pd.DataFrame(sheet.get_all_records())

df1 = client.sheet_to_df(sheet)
sheet = client.open("NewDatabase").sheet1
df = pd.read_excel('C:\\...\\XXX\\SP500_indicators.xlsx',sheet_name='Sheet1', usecols='A:F')
sheet.update([df.columns.values.tolist()] + df.values.tolist()) # export df to a sheet

