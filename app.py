import streamlit as st
from modules.data_manager import DataManager

# Your specific Google Sheet ID
SHEET_ID = "1ghC1ASAUIsu4pE_yIL5rD_QSKkiVmvDP3uDBSD69mmo"

def main():
    st.set_page_config(page_title="Investment Dashboard", layout="wide")
    st.title("📈 Investment Dashboard")
    
    # Initialize the Data Manager
    dm = DataManager(SHEET_ID)
    
    # Sidebar - Navigation
    with st.sidebar:
        st.header("Navigation")
        tabs = dm.get_all_tabs()
        
        if tabs:
            selected_tab = st.selectbox("Select a Sheet Tab", tabs)
        else:
            st.error("Could not find any tabs. Please check permissions.")
            st.stop()

    # Main Content Area
    if selected_tab:
        st.subheader(f"Data for: {selected_tab}")
        df = dm.fetch_sheet_data(selected_tab)
        
        if not df.empty:
            st.dataframe(df, use_container_width=True)
            
            # Example Metric (adjust based on your column names)
            if len(df.columns) > 1:
                st.info(f"Loaded {len(df)} rows and {len(df.columns)} columns.")
        else:
            st.warning("The selected tab is empty or could not be loaded.")

if __name__ == "__main__":
    main()