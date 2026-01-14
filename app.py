import streamlit as st
from modules.data_manager import DataManager
from modules.ui_styles import inject_custom_css, create_theme_toggle

# Your specific Google Sheet ID
SHEET_ID = "1ghC1ASAUIsu4pE_yIL5rD_QSKkiVmvDP3uDBSD69mmo"

def main():
    st.set_page_config(
        page_title="My Finance",
        page_icon="💰",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Theme Toggle and CSS Injection
    with st.sidebar:
        is_dark = create_theme_toggle()
        st.markdown("---")
    
    # Inject custom CSS based on theme with video background
    inject_custom_css(is_dark)
    
    # Main Title
    st.markdown("<h1>My Finance</h1>", unsafe_allow_html=True)
    
    # Initialize the Data Manager
    dm = DataManager(SHEET_ID)
    
    # Sidebar - Navigation (Static, always visible)
    with st.sidebar:
        st.markdown("### Navigation")
        tabs = dm.get_all_tabs()
        
        if tabs:
            selected_tab = st.selectbox(
                "Select a Sheet",
                tabs,
                key="sheet_tab_selector"
            )
        else:
            st.error("Could not find any tabs. Please check permissions.")
            st.info("💡 Make sure you have 'credentials.json' file in the project root.")
            st.stop()

    # Main Content Area
    if selected_tab:
        # Header with selected tab info
        st.markdown(f"### {selected_tab}")
        
        # Fetch and display data
        with st.spinner("Loading data..."):
            df = dm.fetch_sheet_data(selected_tab)
        
        if not df.empty:
            # Visualization Placeholder Section
            st.markdown("#### Visualizations")
            st.info("📊 Visualization placeholders - To be implemented")
            
            # Create placeholder columns for visualizations
            viz_col1, viz_col2 = st.columns(2)
            with viz_col1:
                st.markdown("**Chart 1 Placeholder**")
                st.empty()
            with viz_col2:
                st.markdown("**Chart 2 Placeholder**")
                st.empty()
            
            st.markdown("---")
            
            # Data Table Section
            st.markdown("#### Data Table")
            
            # Display metrics in columns
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Rows", len(df))
            with col2:
                st.metric("Total Columns", len(df.columns))
            with col3:
                st.metric("Data Points", len(df) * len(df.columns))
            
            st.markdown("---")
            
            # Display dataframe with enhanced styling
            st.dataframe(
                df,
                use_container_width=True,
                height=400
            )
            
            # Additional info
            st.info(f"✅ Successfully loaded {len(df)} rows and {len(df.columns)} columns from '{selected_tab}'")
        else:
            st.warning("⚠️ The selected tab is empty or could not be loaded.")

if __name__ == "__main__":
    main()