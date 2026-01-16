import streamlit as st
import gspread
import google.auth
from google.auth.transport.requests import Request
from google.oauth2 import service_account
import pandas as pd
import os

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
        Authenticates using credentials.json for local development,
        or Cloud Run Service Account identity for production.
        """
        try:
            # Try to use a local credentials file first (for local development)
            # Preferred name: credentials.json
            possible_paths = ["credentials.json", "credentials.json.json"]
            credentials_path = next((p for p in possible_paths if os.path.exists(p)), None)

            if credentials_path:
                creds = service_account.Credentials.from_service_account_file(
                    credentials_path,
                    scopes=_self.scope
                )
                return gspread.authorize(creds)
            
            # Fallback to default credentials (for Cloud Run)
            try:
                creds, project = google.auth.default(scopes=_self.scope)
                if creds and not creds.valid:
                    creds.refresh(Request())
                return gspread.authorize(creds)
            except Exception:
                # If default credentials fail, show helpful error
                st.error(
                    "⚠️ Authentication Error: Please ensure you have 'credentials.json' file "
                    "in the project root, or you're running on Google Cloud with proper service account."
                )
                return None
        except Exception as e:
            st.error(f"Authentication Error: {e}")
            st.info("💡 Tip: Place your Google Service Account 'credentials.json' file in the project root.")
            return None

    def get_all_tabs(self):
        """Fetches all non-hidden worksheet titles from the spreadsheet."""
        try:
            client = self.get_client()
            if not client:
                return []

            sh = client.open_by_key(self.spreadsheet_id)

            # Filter out hidden worksheets (compatible with older gspread versions)
            all_worksheets = sh.worksheets()
            visible_worksheets = [
                ws
                for ws in all_worksheets
                if not getattr(ws, "_properties", {}).get("hidden", False)
            ]

            return [ws.title for ws in visible_worksheets]
        except Exception as e:
            st.error(f"Error listing tabs: {e}")
            return []

    @st.cache_data(ttl=600, show_spinner=False)
    def fetch_sheet_data(_self, worksheet_name):
        """Fetches data from a specific tab into a Pandas DataFrame."""
        try:
            client = _self.get_client()
            if not client:
                return pd.DataFrame()
            sh = client.open_by_key(_self.spreadsheet_id)
            worksheet = sh.worksheet(worksheet_name)
            data = worksheet.get_all_records()
            return pd.DataFrame(data)
        except Exception as e:
            st.error(f"Error fetching '{worksheet_name}': {e}")
            return pd.DataFrame()