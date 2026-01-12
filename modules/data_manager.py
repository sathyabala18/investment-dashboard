import streamlit as st
import gspread
import google.auth
from google.auth.transport.requests import Request
import pandas as pd

class DataManager:
    def __init__(self, spreadsheet_id):
        self.scope = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
        self.spreadsheet_id = spreadsheet_id

    @st.cache_resource
    def get_client(_self):
        """
        Authenticates using the Cloud Run Service Account identity.
        No JSON keys or secrets required.
        """
        try:
            # Automatically detects credentials on Google Cloud
            creds, project = google.auth.default(scopes=_self.scope)
            
            # Refresh token if it's expired
            if creds and not creds.valid:
                creds.refresh(Request())
                
            return gspread.authorize(creds)
        except Exception as e:
            st.error(f"Authentication Error: {e}")
            return None

    def get_all_tabs(self):
        """Fetches all worksheet titles from the spreadsheet."""
        try:
            client = self.get_client()
            if not client:
                return []
            sh = client.open_by_key(self.spreadsheet_id)
            return [ws.title for ws in sh.worksheets()]
        except Exception as e:
            st.error(f"Error listing tabs: {e}")
            return []

    def fetch_sheet_data(self, worksheet_name):
        """Fetches data from a specific tab into a Pandas DataFrame."""
        try:
            client = self.get_client()
            if not client:
                return pd.DataFrame()
            sh = client.open_by_key(self.spreadsheet_id)
            worksheet = sh.worksheet(worksheet_name)
            data = worksheet.get_all_records()
            return pd.DataFrame(data)
        except Exception as e:
            st.error(f"Error fetching '{worksheet_name}': {e}")
            return pd.DataFrame()