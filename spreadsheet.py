import gspread
import pprint
from googleapiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials

def get_sheet_values(tab: str):
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('osu-mp-a553b7456a44.json', scope)
    client = gspread.authorize(creds)
    service = discovery.build('sheets', 'v4', credentials=creds)

    spreadsheet_id = '1meEdKHkZJWA1Vr51BrMOmuTybXVqHfMvPAOa3KFy39g'
    range_ = tab+"!"+'B7:I26'
    request = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=range_, majorDimension='COLUMNS')
    response = request.execute()
    if 'values' in response:
        return response['values']
    else:
        return []


