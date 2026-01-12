import gspread
import google.auth
from google.auth.transport.requests import Request

# No more 'import json' or 'import secretmanager' needed for auth!

class DataManager:
    def __init__(self):
        self.scope = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]

    @st.cache_resource
    def get_client(_self):
        # This function automatically looks for "Ambient Credentials"
        # It works on Cloud Run without any files or secrets!
        creds, project = google.auth.default(scopes=_self.scope)
        
        # Refresh the token if it's expired
        if not creds.valid:
            creds.refresh(Request())
            
        return gspread.authorize(creds)