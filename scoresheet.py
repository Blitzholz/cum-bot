import gspread
import pprint
from googleapiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials

def something(tab: str, tier: str, data: list):
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('osu-mp-a553b7456a44.json', scope)
    client = gspread.authorize(creds)
    service = discovery.build('sheets', 'v4', credentials=creds)

    spreadsheet_id = '1b9tpGXWaaIAliHVaXXr1MpsKlsjjnF_P_obym7y9veM'
    if tier == '1':
        range_ = tab+"!"+'A7:F600'
    elif tier == '2':
            range_ = tab + "!" + 'H7:M600'
    value_input_option = 'RAW'
    insert_data_option = 'INSERT_ROWS'
    value_range_body = {
        'range': range,
        'majorDimension': 'ROWS',
        'values': [data]
    }
    request = service.spreadsheets().values().append(spreadsheetId=spreadsheet_id, range=range_,
                                                     valueInputOption=value_input_option,
                                                     insertDataOption=insert_data_option, body=value_range_body)
    response = request.execute()

    pp = pprint.PrettyPrinter()
    pp.pprint(response)


something('YEET', '1', [['A7:A8']])