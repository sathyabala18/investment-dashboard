import gspread
import streamlit as st
from google.oauth2 import service_account
from google.cloud import secretmanager
import json

class DataManager:
    def __init__(self, sheet_id):
        self.sheet_id = sheet_id
        self.scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
              
    def _get_secret(self):
        try:
            client = secretmanager.SecretManagerServiceClient()
            # Use your actual project ID here
            name = f"projects/investment-tracking-483414/secrets/GSHEET_CREDS/versions/latest"
            response = client.access_secret_version(request={"name": name})
            
            # Decode the payload
            payload = response.payload.data.decode("UTF-8")
            
            # Load as JSON
            return json.loads(payload)
        except Exception as e:
            st.error(f"Error fetching secret: {e}")
            # Only use local fallback if file exists
            import os
            if os.path.exists("credentials.json"):
                with open("credentials.json", "r") as f:
                    return json.load(f)
            raise e



    @st.cache_resource
    def get_client(_self):
        creds_data = _self._get_secret()
        
        # FIX: Ensure the private key has correct newline characters
        if 'private_key' in creds_data:
            creds_data['private_key'] = creds_data['private_key'].replace('\\n', '\n')
            
        creds = service_account.Credentials.from_service_account_info(
            creds_data, scopes=_self.scope
        )
        return gspread.authorize(creds)

    def fetch_visible_tabs(self):
        try:
            client = self.get_client()
            ss = client.open_by_key(self.sheet_id)
            metadata = ss.fetch_sheet_metadata()
            return [
                s.get('properties', {}).get('title') 
                for s in metadata.get('sheets', []) 
                if not s.get('properties', {}).get('hidden', False)
            ]
        except Exception as e:
            return str(e)