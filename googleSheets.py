from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

###############
# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'

# The ID and ranges used in the Oz config Google Spreadsheet.
DMXP_CONFIG_ID = '1YqVi_n5f_JeCSQZePawLb-8XN5EtzSkWT7EuHu7Bo5U'  # e.g. this is the ugly part of the URL when looking at the Sheet in your browser
DMXP_RANGE = 'dmxp!A2:F'
FLAVORTOWN_RANGE = 'Flavortext!A2:C'
WELCOMEINFO_CELL = 'WelcomeInformation!A2'
JUDGE_RANGE = 'judge!A2:B'
RES_RANGE = 'res!A2:D'
PFXP_RANGE = 'pfxp!A2:C'

#variables to hold the tables read from the Google Sheets
dmXProws = []
flavortextRows = []
judgetextRows = []
welcomeText = ''
resRows = []
pfXProws = []

def authorizeGoogleSheetsService():
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('sheets', 'v4',
                    http=creds.authorize(Http()))  # all this auth shit is tied to Brad's Calculon Config Sheet
    sheet = service.spreadsheets()
    return sheet

def getDmXpRows():
    sheet = authorizeGoogleSheetsService()
    result = sheet.values().get(spreadsheetId=DMXP_CONFIG_ID,
                                range=DMXP_RANGE).execute()
    values = result.get('values', [])
    if not values:
        print('No data found.')
        return 0
    else:
        print("Reading from the Google Sheet's DMXP Table:")
        for row in values:
            # append columns A through D, which correspond to indices 0 through 3.
            dmXProws.append({"level": row[0], "xpHr": row[1], "gpHr": row[2], "resHr": row[3]})
    return dmXProws

def getPfXpRows():
    sheet = authorizeGoogleSheetsService()
    result = sheet.values().get(spreadsheetId=DMXP_CONFIG_ID,
                                range=PFXP_RANGE).execute()
    values = result.get('values', [])
    if not values:
        print('No data found.')
        return 0
    else:
        print("Reading from the Google Sheet's DMXP Table:")
        for row in values:
            # append columns A through C, which correspond to indices 0 through 2.
            pfXProws.append({"level": row[0], "xpHr": row[1], "gpHr": row[2]})
    return pfXProws


def getFlavorTextRows():
    sheet = authorizeGoogleSheetsService()
    result = sheet.values().get(spreadsheetId=DMXP_CONFIG_ID,
                                range=FLAVORTOWN_RANGE).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
        return 0
    else:
        print("Reading from the Google Sheet's Flavor Text table:")
        for row in values:
            # append columns A through B, which correspond to indices 0 through 1.
            flavortextRows.append({"id": row[0], "flavortext": row[1]})
    return flavortextRows

def getJudgeTextRows():
    sheet = authorizeGoogleSheetsService()
    result = sheet.values().get(spreadsheetId=DMXP_CONFIG_ID,
                                range=JUDGE_RANGE).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
        return 0
    else:
        print("Reading from the Google Sheet's Judge Text table:")
        for row in values:
            # append columns A through B, which correspond to indices 0 through 1.
            judgetextRows.append({"id": row[0], "judgetext": row[1]})
    return judgetextRows

def getWelcomeText():
    sheet = authorizeGoogleSheetsService()
    result = sheet.values().get(spreadsheetId=DMXP_CONFIG_ID,
                                range=WELCOMEINFO_CELL).execute()
    values = result.get('values', [])
    if not values:
        print('No data found.')
        return 0
    else:
        for row in values:
            welcomeText = row[0]
    return welcomeText

def getResRows():
    sheet = authorizeGoogleSheetsService()
    result = sheet.values().get(spreadsheetId=DMXP_CONFIG_ID,
                                range=RES_RANGE).execute()
    values = result.get('values', [])
    if not values:
        print('No data found.')
        return 0
    else:
        print("Reading from the Google Sheet's resRows Table:")
        for row in values:
            # append columns A through D, which correspond to indices 0 through 3.
            resRows.append({"minPC": row[0], "XPdenominator": row[1], "maxMI": row[2], "multishotMultiplier": row[3]})
    return resRows

#########END READING CONFIG##########