import os
import random

import streamlit as st
import pandas as pd

from modules.data_manager import DataManager
from modules.ui_styles import (
    inject_custom_css,
    render_home_header
)

# Your specific Google Sheet ID
SHEET_ID = "1ghC1ASAUIsu4pE_yIL5rD_QSKkiVmvDP3uDBSD69mmo"


def get_random_background_image() -> str | None:
    """Pick a random image from background_images folder (if any)."""
    folder = "background_images"
    if not os.path.isdir(folder):
        return None

    exts = (".jpg", ".jpeg", ".png", ".webp", ".gif")
    files = [f for f in os.listdir(folder) if f.lower().endswith(exts)]
    if not files:
        return None

    choice = random.choice(files)
    return os.path.join(folder, choice)


def main():
    st.set_page_config(
        page_title="My Finance",
        page_icon="💰",
        layout="wide",
        initial_sidebar_state="collapsed",
    )

    # Initialize the Data Manager and load sheet names
    dm = DataManager(SHEET_ID)
    tabs = dm.get_all_tabs()

    if not tabs:
        inject_custom_css(is_home=False)
        st.error("Could not find any tabs. Please check permissions.")
        st.stop()

    # Determine selected sheet from session state
    if "selected_tab" not in st.session_state:
        st.session_state.selected_tab = None

    selected_tab = st.session_state.selected_tab

    # HOME SCREEN: no sheet selected yet
    if not selected_tab:
        # Persist background image
        if "home_bg_image" not in st.session_state:
             st.session_state.home_bg_image = get_random_background_image()
        
        bg_image = st.session_state.home_bg_image
        inject_custom_css(is_home=True, background_image=bg_image)

        # 1. Header (Centered by CSS)
        render_home_header()
        
        # 2. Layout Strategy: Use Columns to constrain width naturally
        # [Spacer, Content, Spacer]. Ratio 1:1.2:1 roughly puts content at ~33-40% width
        # On 1200px max container, that's ~400px. Perfect.
        l_col, center_col, r_col = st.columns([1, 1.2, 1])
        
        with center_col:
            chosen = st.selectbox(
                "Select a Portfolio / Sheet",
                tabs,
                key="home_sheet_selector",
                label_visibility="collapsed",
                format_func=lambda x: x.replace("_", " ").title()
            )
            
            # Button is inside the same column, so it matches width
            if st.button("OPEN", use_container_width=False):
                st.session_state.selected_tab = chosen
                st.rerun()
            
        return

    # SHEET VIEW: a sheet has been selected
    inject_custom_css(is_home=False, background_image=None)

    # Navigation Bar
    with st.container():
        cols = st.columns([1, 6])
        with cols[0]:
            if st.button("← Back", use_container_width=True):
                st.session_state.selected_tab = None
                st.rerun()

    # Title (Formatted: "my_sheet_name" -> "My Sheet Name")
    display_title = selected_tab.replace("_", " ").title()
    st.markdown(f"<h1>{display_title}</h1>", unsafe_allow_html=True)

    # Fetch and display data
    with st.spinner("Accessing Financial Data..."):
        df = dm.fetch_sheet_data(selected_tab)

    # ROUTING LOGIC
    from modules.sheet_views import SheetViews

    if not df.empty:
        # Check specific sheet names to determine View
        # Handle variations: "important info", "important_info"
        normalized_name = selected_tab.strip().lower().replace("_", " ")
        
        if normalized_name == "important info":
            SheetViews.render_important_info(df)
        else:
            SheetViews.render_default(df)
        
    else:
        st.warning("⚠️ The selected tab is empty or could not be loaded.")


if __name__ == "__main__":
    main()