import os
import urllib
import webbrowser
import pyperclip
import requests
from datetime import datetime, timedelta
from dateutil import parser
from adal import AuthenticationContext


"""Configuration settings for console app using device flow authentication
"""
AUTHORITY_URL = 'https://login.microsoftonline.com/common'
RESOURCE = 'https://graph.microsoft.com'
API_VERSION = 'v1.0'


def api_endpoint(url):
    """Convert a relative path such as /me/photo/$value to a full URI based
    on the current RESOURCE and API_VERSION settings in config.py.
    """
    if urllib.parse.urlparse(url).scheme in ['http', 'https']:
        return url  # url is already complete
    return urllib.parse.urljoin(f'{RESOURCE}/{API_VERSION}/',
                                url.lstrip('/'))


def get_request_session(tokens):
    session = requests.Session()
    session.headers.update({'Authorization': f'Bearer {tokens["accessToken"]}',
                            'SdkVersion': 'msgraph-python-adal',
                            'x-client-SKU': 'msgraph-python-adal'})
    return session


def ensure_tokens(client_id, tokens):
    expiresOn = parser.parse(tokens['expiresOn'])

    if expiresOn < datetime.now() + timedelta(minutes=10):
        ctx = AuthenticationContext(AUTHORITY_URL, api_version=None)

        return ctx.acquire_token_with_refresh_token(tokens['refreshToken'],
                                                    client_id,
                                                    RESOURCE)

    return tokens


def acquire_token_with_device_code(client_id, auto=False):
    """Obtain an access token from Azure AD (via device flow) and create
    a Requests session instance ready to make authenticated calls to
    Microsoft Graph.
    client_id = Application ID for registered "Azure AD only" V1-endpoint app
    auto      = whether to copy device code to clipboard and auto-launch browser
    Returns Requests session object if user signed in successfully. The session
    includes the access token in an Authorization header.
    User identity must be an organizational account (ADAL does not support MSAs).
    """
    ctx = AuthenticationContext(AUTHORITY_URL, api_version=None)
    device_code = ctx.acquire_user_code(RESOURCE,
                                        client_id)

    # display user instructions
    if auto:
        pyperclip.copy(device_code['user_code'])  # copy user code to clipboard
        webbrowser.open(device_code['verification_url'])  # open browser
        print(f'The code {device_code["user_code"]} has been copied to your clipboard, '
              f'and your web browser is opening {device_code["verification_url"]}. '
              'Paste the code to sign in.')
    else:
        print(device_code['message'])

    return ctx.acquire_token_with_device_code(RESOURCE,
                                              device_code,
                                              client_id)
