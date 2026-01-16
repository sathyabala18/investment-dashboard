import streamlit as st
import pandas as pd
from modules.ui_styles import get_theme_colors

class SheetViews:
    """
    Handles rendering strategies for different sheets.
    """
    
    @staticmethod
    def format_indian_currency(amount):
        """Formats a number in the Indian currency system (e.g., 12,34,567) without paisa."""
        if pd.isna(amount):
            return "₹0"
        try:
            amount = int(round(float(amount)))
        except (ValueError, TypeError):
            return "₹0"
            
        is_negative = amount < 0
        s = str(abs(amount))
        if len(s) <= 3:
            res = s
        else:
            last_three = s[-3:]
            remaining = s[:-3]
            groups = []
            while remaining:
                groups.append(remaining[-2:])
                remaining = remaining[:-2]
            res = ",".join(reversed(groups)) + "," + last_three
        return f"₹{'-' if is_negative else ''}{res}"

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
    def render_mutual_funds(df: pd.DataFrame):
        """
        Specialized view for 'Mutual_Funds' sheet.
        Header Mapping:
        Name -> Fund Name
        Goal -> Goal
        INV Date -> Investment Date
        Total Value -> Transaction Value
        Current Cost -> Current Day Value (Appreciation check)
        """
        if df.empty:
            st.warning("⚠️ No data found in Mutual Funds.")
            return
            
        # --- 1. Data Cleaning & Mapping ---
        # We need to ensure columns exist. 
        # Expected Headers based on User input: "Name", "Goal", "INV Date", "Total Value", "Current Cost"
        # Since user said "Name - Fund Name", I assume column in sheet is "Name" (or "Fund Name"?)
        # Let's normalize columns to be safe or try to guess.
        
        # Clean columns (strip whitespace)
        df.columns = [c.strip() for c in df.columns]
        
        # Map of Standard Key -> Possible Sheet Header
        col_map = {
            "fund": ["Name", "Fund Name", "Fund"],
            "goal": ["Goal"],
            "date": ["INV Date", "Inv Date", "Date", "Investment Date"],
            "trans_val": ["Total Value", "Transaction Value", "Amount"],
            "curr_val": ["Current Cost", "Current Value", "Current Day Value"]
        }
        
        def get_col(candidates):
            for c in candidates:
                if c in df.columns:
                    return c
            return None

        c_fund = get_col(col_map["fund"])
        c_goal = get_col(col_map["goal"])
        c_date = get_col(col_map["date"])
        c_trans = get_col(col_map["trans_val"])
        c_curr = get_col(col_map["curr_val"])
        
        if not all([c_fund, c_goal, c_date, c_trans, c_curr]):
            st.error(f"Missing required columns. Found: {df.columns.tolist()}")
            st.write("Expected variants of: Name, Goal, INV Date, Total Value, Current Cost")
            st.dataframe(df.head())
            return
            
        # Convert Numeric
        for c in [c_trans, c_curr]:
            # Remove commas, currency symbols
            df[c] = df[c].astype(str).str.replace(',', '').str.replace('₹', '').str.replace('$', '')
            df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0)
            
        # Convert Date
        df[c_date] = pd.to_datetime(df[c_date], errors='coerce')
        # Sort by date for the chart
        df = df.sort_values(by=c_date)

        # --- 2. Filters (Narrower) ---
        st.markdown("### 🔍 Filter Portfolio")
        
        # Use 4 columns: Spacer, Control 1, Control 2, Spacer
        _, f_col1, f_col2, _ = st.columns([1, 1.5, 1.5, 1])
        
        # Goal Filter
        goals = ["All"] + sorted(df[c_goal].dropna().unique().tolist())
        with f_col1:
            sel_goal = st.selectbox("Select Goal", goals, key="mf_goal")
            
        # Fund Filter (Dependent on Goal)
        if sel_goal != "All":
            filtered_df_step1 = df[df[c_goal] == sel_goal]
        else:
            filtered_df_step1 = df
            
        funds = ["All"] + sorted(filtered_df_step1[c_fund].dropna().unique().tolist())
        with f_col2:
            sel_fund = st.selectbox("Select Fund", funds, key="mf_fund")
            
        # Apply Final Filter
        if sel_fund != "All":
            final_df = filtered_df_step1[filtered_df_step1[c_fund] == sel_fund]
        else:
            final_df = filtered_df_step1
            
        # --- 3. Visualization & Data ---
        st.markdown("---")
        
        if final_df.empty:
            st.warning("No transactions found for this selection.")
            return

        # Prepare Chart Data
        grouped_df = final_df.groupby(c_date)[[c_trans, c_curr]].sum().sort_index()
        chart_df = grouped_df.cumsum().reset_index()
        chart_df_long = chart_df.melt(id_vars=[c_date], var_name="Metric", value_name="Amount")
        # Custom Labels for the Legend
        metric_map = {
            c_trans: "Invested",
            c_curr: "Current Value"
        }
        chart_df_long["Metric"] = chart_df_long["Metric"].map(metric_map)

        # WIDE format for Unified Tooltip (Pivot)
        chart_df_wide = chart_df.rename(columns={
             c_trans: "Invested",
             c_curr: "Current Value"
        })

        st.markdown(f"### 📈 Performance: {sel_goal} / {sel_fund}")

        # TABS for clear switching
        tab_chart, tab_data = st.tabs(["📊 Chart", "📄 Raw Data"])
        
        with tab_chart:
            import altair as alt
            
            domain = ["Invested", "Current Value"]
            range_ = ["#b0b0b0", "#00d2ff"] 

            # Base Chart (Lines & Points - uses LONG data)
            base = alt.Chart(chart_df_long).encode(
                x=alt.X(f"{c_date}:T", title=None, axis=alt.Axis(format="%b %Y", grid=False, domain=False))
            )

            # Lines
            lines = base.mark_line(strokeWidth=3, interpolate='monotone').encode(
                y=alt.Y("Amount:Q", title=None, axis=None),
                color=alt.Color("Metric:N", scale=alt.Scale(domain=domain, range=range_), legend=alt.Legend(orient="top", title=None))
            )

            # --- INTERACTION LAYER (Uses WIDE data) ---
            nearest = alt.selection_point(nearest=True, on='mouseover', fields=[c_date], empty=False)
            
            # Invisible selectors (The Rule triggering hover)
            selectors = alt.Chart(chart_df_wide).mark_rule(color="gray").encode(
                x=f"{c_date}:T",
                opacity=alt.condition(nearest, alt.value(1), alt.value(0)),
                tooltip=[
                    alt.Tooltip(f"{c_date}:T", title="Date", format="%b %d, %Y"),
                    alt.Tooltip("Invested:Q", title="Invested", format=",.0f"),
                    alt.Tooltip("Current Value:Q", title="Current Value", format=",.0f")
                ]
            ).add_params(nearest)

            highlight_points = base.mark_point(filled=True, size=100).encode(
                 y=alt.Y("Amount:Q"),
                 color=alt.Color("Metric:N")
            ).transform_filter(nearest)

            # Assemble
            final_chart = alt.layer(
                lines, selectors, highlight_points
            ).properties(
                height=350,
                background='transparent'
            ).configure_view(
                strokeWidth=0
            ).configure_axis(
                labelColor='#b0b0b0',
                titleColor='#b0b0b0'
            ).configure_legend(
                labelColor='#e0e0e0',
                labelFontSize=12
            )

            # Zoom & Anchor Fix: 
            # 1. We strictly bind to X and set domain
            # 2. nice=False/padding=0 prevents empty space
            min_date = chart_df[c_date].min()
            max_date = chart_df[c_date].max()
            
            final_chart = final_chart.encode(
                x=alt.X(f"{c_date}:T", 
                       scale=alt.Scale(domain=(min_date, max_date), nice=False, padding=0, clamp=True),
                       axis=alt.Axis(format="%b %Y", grid=False))
            ).interactive(bind_y=False)

            st.altair_chart(final_chart, use_container_width=True)

            # --- 4. Metrics & XIRR (Inside Tab) ---
            def xirr(transactions, dates):
                if not transactions or not dates: return 0.0
                combined = sorted(zip(dates, transactions))
                dates, transactions = zip(*combined)
                if len(dates) < 2: return 0.0
                t0 = dates[0]
                dt = [(d - t0).days / 365.0 for d in dates]
                guess = 0.1
                for _ in range(100):
                    f_npv = sum(t / pow(1.0 + guess, d) for t, d in zip(transactions, dt))
                    df_npv = sum(-t * d / pow(1.0 + guess, d + 1) for t, d in zip(transactions, dt))
                    if df_npv == 0: return 0.0
                    new_guess = guess - f_npv / df_npv
                    if abs(new_guess - guess) < 1e-6: return new_guess
                    guess = new_guess
                return guess

            current_val_sum = final_df[c_curr].sum()
            cf_dates = final_df[c_date].tolist() + [final_df[c_date].max()]
            cf_amounts = (-1 * final_df[c_trans]).tolist() + [current_val_sum]
            xirr_val = xirr(cf_amounts, cf_dates) * 100

            last_row = chart_df.iloc[-1]
            total_inv, total_curr = last_row[c_trans], last_row[c_curr]
            diff = total_curr - total_inv
            perc = (diff / total_inv * 100) if total_inv > 0 else 0
            
            st.markdown("""
                <style>
                .custom-metric-box {
                    background-color: rgba(255, 255, 255, 0.03);
                    border: 1px solid rgba(255, 255, 255, 0.08);
                    border-radius: 12px;
                    padding: 12px 20px;
                    text-align: center;
                    transition: all 0.3s ease;
                }
                .metric-label { font-size: 0.7rem; color: #888; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 4px; }
                .metric-value { font-size: 1.1rem; font-weight: 700; color: #fff; display: flex; align-items: center; justify-content: center; gap: 8px; }
                .glow-blue { text-shadow: 0 0 10px rgba(0, 210, 255, 0.5); color: #00d2ff; }
                .glow-green { text-shadow: 0 0 10px rgba(0, 255, 136, 0.4); color: #00ff88; }
                .glow-red { text-shadow: 0 0 10px rgba(255, 51, 51, 0.4); color: #ff3333; }
                .profit-tag { font-size: 0.85rem; font-weight: 600; }
                </style>
            """, unsafe_allow_html=True)
            
            inv_fmt = SheetViews.format_indian_currency(total_inv)
            curr_fmt = SheetViews.format_indian_currency(total_curr)
            profit_fmt = SheetViews.format_indian_currency(diff)
            p_class = "glow-green" if diff >= 0 else "glow-red"
            
            # Flex row for compact metrics as requested
            st.markdown(f'''
                <div style="display: flex; flex-wrap: wrap; gap: 15px; justify-content: center; margin-top: 20px;">
                    <div class="custom-metric-box" style="flex: 0 1 auto;">
                        <div class="metric-label">Invested</div>
                        <div class="metric-value">{inv_fmt}</div>
                    </div>
                    <div class="custom-metric-box" style="flex: 0 1 auto;">
                        <div class="metric-label">Current (P/L)</div>
                        <div class="metric-value">
                            <span>{curr_fmt}</span>
                            <span class="profit-tag {p_class}">({profit_fmt})</span>
                        </div>
                    </div>
                    <div class="custom-metric-box" style="flex: 0 1 auto;">
                        <div class="metric-label">Returns</div>
                        <div class="metric-value {p_class}">{perc:.2f}%</div>
                    </div>
                    <div class="custom-metric-box" style="flex: 0 1 auto;">
                        <div class="metric-label">XIRR</div>
                        <div class="metric-value glow-blue">{xirr_val:.2f}%</div>
                    </div>
                </div>
            ''', unsafe_allow_html=True)

        with tab_data:
            # Robust Deduplication of column names
            disp_df = final_df.copy()
            cols = []
            count = {}
            for col in disp_df.columns:
                c = str(col).strip() or "Unnamed"
                if c in count:
                    count[c] += 1
                    cols.append(f"{c}.{count[c]}")
                else:
                    count[c] = 0
                    cols.append(c)
            disp_df.columns = cols
            st.dataframe(disp_df, use_container_width=True)
