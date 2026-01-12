import streamlit as st
import gspread
import google.auth
from google.auth.transport.requests import Request
import pandas as pd

class DataManager:
    def __init__(self):
        # Define the permissions needed to access Google Sheets and Drive
        self.scope = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
        
        self.spreadsheet_id = "1ghC1ASAUIsu4pE_yIL5rD_QSKkiVmvDP3uDBSD69mmo"

    @st.cache_resource
    def get_client(_self):
        """
        Authenticates using the Cloud Run Service Account identity.
        No JSON keys required.
        """
        try:
            # Automatically detects the "Ambient" credentials on Cloud Run
            creds, project = google.auth.default(scopes=_self.scope)
            
            # Refresh the token if it has expired
            if creds and not creds.valid:
                creds.refresh(Request())
                
            return gspread.authorize(creds)
        except Exception as e:
            st.error(f"Authentication Error: {e}")
            return None

    def fetch_sheet_data(self, worksheet_name):
        """
        Fetches data from a specific tab and returns a Pandas DataFrame.
        """
        try:
            client = self.get_client()
            if not client:
                return pd.DataFrame()

            # Open the spreadsheet and the specific worksheet
            sh = client.open_by_key(self.spreadsheet_id)
            worksheet = sh.worksheet(worksheet_name)
            
            # Convert the sheet data into a list of dictionaries
            data = worksheet.get_all_records()
            return pd.DataFrame(data)
        except Exception as e:
            st.error(f"Error fetching sheet '{worksheet_name}': {e}")
            return pd.DataFrame()

    def get_all_tabs(self):
        """
        Returns a list of all visible tab names in the Google Sheet.
        """
        try:
            client = self.get_client()
            if not client:
                return []
                
            sh = client.open_by_key(self.spreadsheet_id)
            return [worksheet.title for worksheet in sh.worksheets()]
        except Exception as e:
            st.error(f"Error listing tabs: {e}")
            return []