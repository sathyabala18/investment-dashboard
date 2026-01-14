import streamlit as st

def get_theme_colors(is_dark=True):
    """Returns color scheme based on theme mode"""
    if is_dark:
        return {
            "bg": "#0f0f23",  # Simple dark background
            "text": "#ffffff",
            "text_secondary": "#b0b0b0",
            "card_bg": "rgba(255, 255, 255, 0.05)",
            "card_border": "rgba(255, 255, 255, 0.1)",
            "btn_bg": "rgba(255, 255, 255, 0.1)",
            "btn_hover": "rgba(255, 255, 255, 0.2)",
            "border": "#00d2ff",
            "accent": "#667eea",
            "accent_secondary": "#764ba2",
            "overlay": "rgba(15, 15, 35, 0.3)",
            "grad": "linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%)",
            "shadow": "rgba(0, 0, 0, 0.3)"
        }
    else:
        return {
            "bg": "#f5f7fa",
            "text": "#1a1a2e",
            "text_secondary": "#4a4a6e",
            "card_bg": "rgba(255, 255, 255, 0.7)",
            "card_border": "rgba(0, 0, 0, 0.1)",
            "btn_bg": "rgba(255, 255, 255, 0.8)",
            "btn_hover": "rgba(255, 255, 255, 1)",
            "border": "#667eea",
            "accent": "#667eea",
            "accent_secondary": "#764ba2",
            "overlay": "rgba(255, 255, 255, 0.1)",
            "grad": "linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%)",
            "shadow": "rgba(0, 0, 0, 0.1)"
        }

def inject_custom_css(is_dark=True):
    """Injects custom CSS with theme support"""
    colors = get_theme_colors(is_dark)
    
    st.markdown(f"""
        <style>
            /* Hide default Streamlit elements */
            header, footer, #MainMenu {{ visibility: hidden; }}
            header {{ height: 0px; }}
            
            /* Make sidebar always visible (static) - Hide collapse button */
            [data-testid="stSidebar"] {{
                min-width: 300px !important;
            }}
            
            /* Hide sidebar collapse/expand button */
            button[data-testid="baseButton-header"],
            button[kind="header"],
            [data-testid="collapsedControl"] {{
                display: none !important;
            }}
            
            /* Ensure sidebar stays visible */
            section[data-testid="stSidebar"] {{
                visibility: visible !important;
                transform: translateX(0) !important;
            }}
            
            /* Main App Background */
            .stApp {{
                background: {colors['bg']};
            }}
            
            /* Video Background */
            .video-background {{
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                z-index: -1;
                overflow: hidden;
                pointer-events: none;
            }}
            
            .video-background video {{
                width: 100%;
                height: 100%;
                object-fit: cover;
                opacity: 0.15;
            }}
            
            /* Overlay */
            .overlay {{
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: {colors['overlay']};
                z-index: 0;
                pointer-events: none;
            }}
            
            /* Main Container */
            .main .block-container {{
                padding-top: 2rem;
                padding-bottom: 2rem;
                z-index: 1;
                position: relative;
            }}
            
            /* Title Styling */
            h1 {{
                font-size: clamp(2rem, 6vw, 3.5rem) !important;
                font-weight: 900 !important;
                text-align: center;
                background: {colors['grad']};
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                margin-bottom: 1rem !important;
                text-shadow: 0 0 30px {colors['accent']};
                letter-spacing: -1px;
            }}
            
            h2, h3 {{
                color: {colors['text']} !important;
                font-weight: 700 !important;
            }}
            
            /* Sidebar Styling - Always Visible */
            [data-testid="stSidebar"] {{
                background: {colors['card_bg']} !important;
                backdrop-filter: blur(20px);
                border-right: 1px solid {colors['card_border']} !important;
            }}
            
            /* Hide sidebar collapse button */
            [data-testid="stSidebar"][aria-expanded="true"] {{
                min-width: 300px !important;
            }}
            
            /* Selectbox Styling */
            .stSelectbox > div > div {{
                background: {colors['card_bg']} !important;
                backdrop-filter: blur(10px);
                border: 1px solid {colors['card_border']} !important;
                border-radius: 12px !important;
                color: {colors['text']} !important;
            }}
            
            .stSelectbox label {{
                color: {colors['text']} !important;
                font-weight: 600 !important;
            }}
            
            /* Dataframe Styling */
            .dataframe {{
                background: {colors['card_bg']} !important;
                backdrop-filter: blur(20px);
                border-radius: 16px !important;
                border: 1px solid {colors['card_border']} !important;
                box-shadow: 0 8px 32px {colors['shadow']} !important;
                overflow: hidden;
            }}
            
            /* Button Styling */
            div.stButton > button {{
                width: 100%;
                background: {colors['btn_bg']} !important;
                color: {colors['text']} !important;
                border: 1px solid {colors['card_border']} !important;
                border-radius: 12px !important;
                font-weight: 600 !important;
                backdrop-filter: blur(10px);
                min-height: 48px;
                transition: all 0.3s ease;
                box-shadow: 0 4px 15px {colors['shadow']};
            }}
            
            div.stButton > button:hover {{
                background: {colors['btn_hover']} !important;
                transform: translateY(-2px);
                box-shadow: 0 6px 20px {colors['shadow']};
                border-color: {colors['accent']} !important;
            }}
            
            /* Info/Warning/Success Boxes */
            .stInfo, .stWarning, .stSuccess, .stError {{
                background: {colors['card_bg']} !important;
                backdrop-filter: blur(10px);
                border: 1px solid {colors['card_border']} !important;
                border-radius: 12px !important;
                color: {colors['text']} !important;
            }}
            
            /* Toggle Switch Container */
            .theme-toggle-container {{
                display: flex;
                align-items: center;
                justify-content: space-between;
                padding: 12px;
                background: {colors['card_bg']};
                backdrop-filter: blur(10px);
                border-radius: 12px;
                border: 1px solid {colors['card_border']};
                margin-bottom: 20px;
            }}
            
            .theme-toggle-label {{
                color: {colors['text']} !important;
                font-weight: 600 !important;
                font-size: 15px !important;
                margin-top: 8px;
            }}
            
            /* Streamlit Toggle Styling */
            [data-testid="stToggle"] {{
                background: {colors['card_bg']} !important;
                border-radius: 12px !important;
            }}
            
            [data-testid="stToggle"] label {{
                color: {colors['text']} !important;
            }}
            
            /* Metric Cards */
            [data-testid="stMetricValue"] {{
                color: {colors['text']} !important;
                font-weight: 700 !important;
            }}
            
            [data-testid="stMetricLabel"] {{
                color: {colors['text_secondary']} !important;
            }}
            
            /* Text Styling */
            p, span, div {{
                color: {colors['text']} !important;
            }}
            
            /* Scrollbar Styling */
            ::-webkit-scrollbar {{
                width: 8px;
                height: 8px;
            }}
            
            ::-webkit-scrollbar-track {{
                background: {colors['card_bg']};
            }}
            
            ::-webkit-scrollbar-thumb {{
                background: {colors['accent']};
                border-radius: 4px;
            }}
            
            ::-webkit-scrollbar-thumb:hover {{
                background: {colors['accent_secondary']};
            }}
        </style>
        <div class="video-background" id="video-bg"></div>
        <div class="overlay"></div>
    """, unsafe_allow_html=True)
    
    # Add video using JavaScript to ensure it loads properly
    st.markdown("""
        <script>
            function loadVideoBackground() {
                const container = document.getElementById('video-bg');
                if (!container) return;
                
                const video = document.createElement('video');
                video.autoplay = true;
                video.muted = true;
                video.loop = true;
                video.playsInline = true;
                video.style.width = '100%';
                video.style.height = '100%';
                video.style.objectFit = 'cover';
                video.style.opacity = '0.15';
                
                const source = document.createElement('source');
                source.src = 'Rupee_Coin.webm';
                source.type = 'video/webm';
                
                video.appendChild(source);
                container.appendChild(video);
            }
            
            if (document.readyState === 'loading') {
                document.addEventListener('DOMContentLoaded', loadVideoBackground);
            } else {
                loadVideoBackground();
            }
        </script>
    """, unsafe_allow_html=True)

def create_theme_toggle():
    """Creates a simple theme toggle switch in the sidebar"""
    # Initialize theme in session state if not exists (default to dark)
    if 'theme_mode' not in st.session_state:
        st.session_state.theme_mode = 'dark'
    
    current_mode = st.session_state.theme_mode
    
    # Simple toggle switch
    col1, col2 = st.columns([3, 1])
    with col1:
        theme_label = "🌙 Dark" if current_mode == 'dark' else "☀️ Light"
        st.markdown(f"<div class='theme-toggle-label'>{theme_label}</div>", unsafe_allow_html=True)
    with col2:
        is_dark = st.toggle(
            "",
            value=(current_mode == 'dark'),
            key="theme_toggle",
            label_visibility="collapsed"
        )
        st.session_state.theme_mode = 'dark' if is_dark else 'light'
    
    return st.session_state.theme_mode == 'dark'