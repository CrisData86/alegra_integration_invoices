# auth.py
from google.oauth2 import service_account
import gspread

class GoogleSheetAuth:
    def __init__(self, json_params, scope):
        self.json_params = json_params
        self.scope = scope

    def authenticate(self):
        credentials = service_account.Credentials.from_service_account_info(self.json_params)
        scoped_credentials = credentials.with_scopes(self.scope)
        return gspread.authorize(scoped_credentials)