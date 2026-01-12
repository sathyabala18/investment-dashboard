import streamlit as st
from modules.data_manager import DataManager
from modules.ui_styles import inject_custom_css

# App Configuration
st.set_page_config(page_title="Investments", layout="wide", initial_sidebar_state="collapsed")

# Session State Init
if 'page' not in st.session_state: 
    st.session_state.page = 'Home'

# Initialize Styles and Data
dm = DataManager("1ghC1ASAUIsu4pE_yIL5rD_QSKkiVmvDP3uDBSD69mmo")
inject_custom_css()

# Routing Logic
if st.session_state.page == 'Home':
    st.markdown('<div style="height: 20px;"></div>', unsafe_allow_html=True)
    tabs = dm.fetch_visible_tabs()
    
    if isinstance(tabs, list):
        cols = st.columns(2)
        for i, tab in enumerate(tabs):
            with cols[i % 2]:
                if st.button(tab, key=tab, use_container_width=True):
                    st.session_state.page = tab
                    st.rerun()
    else:
        st.error(f"Error: {tabs}")

else:
    # Top Action Row for Detail Pages
    col_back, _ = st.columns([0.2, 0.8])
    with col_back:
        if st.button("⬅ BACK", use_container_width=True):
            st.session_state.page = 'Home'
            st.rerun()
    
    # Detail Page Content
    st.markdown(f'<div class="main-title">{st.session_state.page}</div>', unsafe_allow_html=True)
    
    # Placeholder for dynamic charts/tables
    st.markdown("""
        <div style="height:60vh; border:1px solid #00d2ff33; border-radius:20px; 
                    display:flex; align-items:center; justify-content:center; 
                    backdrop-filter:blur(20px); background: rgba(255,255,255,0.02);">
            <span style="color: #00d2ff; opacity: 0.5; font-weight: 600;">Data Visualization Area</span>
        </div>
    """, unsafe_allow_html=True)