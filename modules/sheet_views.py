import streamlit as st
import pandas as pd
from modules.ui_styles import get_theme_colors

class SheetViews:
    """
    Handles rendering strategies for different sheets.
    """
    
    @staticmethod
    def render_default(df: pd.DataFrame):
        """Standard view for generic sheets."""
        if df.empty:
            st.warning("⚠️ The selected tab is empty or could not be loaded.")
            return

        # Summary Metrics
        st.markdown("### 📊 At a Glance")
        m_col1, m_col2, m_col3 = st.columns(3)
        with m_col1:
            st.metric("Total Records", len(df))
        with m_col2:
            st.metric("Data Fields", len(df.columns))
        with m_col3:
            st.metric("Status", "Active")

        st.markdown("---")

        # Data Table
        st.markdown("### 📝 Detailed Records")
        st.dataframe(
            df,
            use_container_width=True,
            height=500,
        )

    @staticmethod
    def render_important_info(df: pd.DataFrame):
        """
        Specialized view for 'Important Info' sheet.
        Strictly shows: Dropdowns -> Result.
        """
        if df.empty:
            st.warning("⚠️ No data found in Important Info.")
            return

        colors = get_theme_colors()

        # 1. Parsing Data
        try:
            # Assumes Column A is "Type", Columns B..N are Names
            type_col = df.columns[0]
            member_cols = df.columns[1:].tolist()
            types = df[type_col].dropna().unique().tolist()
        except IndexError:
            st.error("Data structure mismatched.")
            return

        # 2. Controls - Narrower
        st.markdown(f"""
            <div style="margin-bottom: 2rem;"></div>
        """, unsafe_allow_html=True)

        # Use 4 columns: Spacer, Control 1, Control 2, Spacer
        # [1, 1.5, 1.5, 1] ratio essentially centers the two controls and limits their width
        _, c1, c2, _ = st.columns([1, 1.5, 1.5, 1])
        
        with c1:
            selected_type = st.selectbox("Select Type", types, key="imp_info_type")
            
        with c2:
            selected_member = st.selectbox("Select Name", member_cols, key="imp_info_member")

        # 3. Lookup Logic
        # Filter row by Type
        row = df[df[type_col] == selected_type]
        
        result_value = "Not Found"
        if not row.empty:
            result_value = row.iloc[0][selected_member]

        # 4. Display Result - Single View with Copy
        st.markdown("---")
        
        # Centered container for the result
        _, r_col, _ = st.columns([1, 2, 1])
        with r_col:
            st.caption(f"Details for: {selected_member} - {selected_type}")
            # st.code provides the value AND the copy functionality in one standard UI element.
            st.code(str(result_value), language="text")

    @staticmethod
    def _render_styled_card(content: str):
        pass
