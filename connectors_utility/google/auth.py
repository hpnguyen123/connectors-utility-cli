"""
Shows basic usage of the Sheets API. Prints values from a Google Spreadsheet.
"""
from httplib2 import Http
from oauth2client import file, client, tools
from apiclient.discovery import build

# Setup the Sheets API
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'


def get_credentials(credentials_file, client_secret_file):
    import pdb; pdb.set_trace()
    store = file.Storage(credentials_file)
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets(client_secret_file, SCOPES)
        flags = tools.argparser.parse_args(args=[])
        creds = tools.run_flow(flow, store, flags)
    return creds


def get_service(credentials, service='sheets'):
    """ Build a service
    """
    return build(service, 'v4', http=credentials.authorize(Http()))
