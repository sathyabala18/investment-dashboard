import streamlit as st
import base64


def get_theme_colors():
    """Returns the Cyberpunk/Fintech theme color scheme."""
    return {
        "bg_home": "#000000",
        "bg_sheet": "#050505",  # Very deep black/grey for sheet view
        "text": "#E0E0E0",
        "text_secondary": "#A0A0A0",
        "card_bg": "rgba(20, 20, 30, 0.6)",
        "card_border": "rgba(0, 210, 255, 0.3)",
        "btn_bg": "linear-gradient(135deg, rgba(0, 210, 255, 0.1) 0%, rgba(58, 123, 213, 0.1) 100%)",
        "btn_hover": "linear-gradient(135deg, rgba(0, 210, 255, 0.2) 0%, rgba(58, 123, 213, 0.2) 100%)",
        "accent": "#00d2ff",  # Cyan neon
        "accent_secondary": "#9d50bb",  # Purple neon
        "overlay": "rgba(0, 0, 0, 0.7)",  # darker overlay for readability
        "shadow": "0 8px 32px 0 rgba(0, 0, 0, 0.37)",
    }


def local_image_to_base64(image_path: str) -> str:
    """Helper to convert local image to base64 for CSS background."""
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except Exception:
        return ""


def inject_custom_css(is_home: bool, background_image: str | None = None):
    """
    Injects custom CSS for the Fintech/Cyberpunk look.
    """
    colors = get_theme_colors()

    # Base background Logic
    app_background_css = ""
    container_css = ""
    
    if is_home and background_image:
        b64_img = local_image_to_base64(background_image)
        if b64_img:
            app_background_css = f"""
                background-image: url('data:image/png;base64,{b64_img}');
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                background-attachment: fixed;
            """
        else:
             app_background_css = f"background: {colors['bg_home']};"
        
        # Flexbox centering for home
        # Note: We rely on st.columns inside this container for width, 
        # but this centers the columns vertically.
        container_css = """
            display: flex;
            flex-direction: column;
            justify-content: center;
            min-height: 90vh;
        """
    else:
        app_background_css = f"background: {colors['bg_sheet']};"
        container_css = "display: block;"

    st.markdown(
        f"""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');

            /* Global Reset & Typography */
            html, body, [class*="css"] {{
                font-family: 'Inter', sans-serif;
                color: {colors['text']};
            }}

            h1, h2, h3 {{
                color: {colors['text']} !important;
                font-weight: 800 !important;
                text-shadow: 0 0 20px rgba(0, 210, 255, 0.3);
            }}
            
            h1 {{
                font-size: clamp(2.5rem, 8vw, 4rem) !important;
                background: linear-gradient(90deg, {colors['accent']}, {colors['text']});
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                margin-bottom: 2rem !important; /* Spacing above dropdown */
                text-align: center;
                line-height: 1.1 !important;
            }}

            #MainMenu {{visibility: hidden;}}
            footer {{visibility: hidden;}}
            header {{visibility: hidden;}}
            [data-testid="stSidebar"] {{display: none;}}

            .stApp {{
                {app_background_css}
            }}

            .bg-overlay {{
                position: fixed;
                top: 0; left: 0; width: 100%; height: 100%;
                background: {colors['overlay'] if is_home else 'transparent'};
                z-index: 0;
                pointer-events: none;
            }}

            /* MAIN CONTAINER */
            .main .block-container {{
                {container_css}
                width: 100%;
                max-width: 1200px !important; /* Restore normal width */
                padding: 1rem !important;
                z-index: 1;
                position: relative;
            }}
            
            /* --- WIDGET STYLING --- */
            
            /* Selectbox itself */
            div[data-testid="stSelectbox"] {{
                width: 100%;
            }}
            
            /* Dropdown Input Area - THE BOX YOU CLICK */
            div[data-baseweb="select"] > div {{
                background-color: #0e1117 !important; /* Solid dark background */
                border: 1px solid rgba(255, 255, 255, 0.2) !important;
                color: #ffffff !important; /* Explicit White text */
                border-radius: 12px !important;
                min-height: 48px;
                display: flex;
                align-items: center;
            }}
            
            /* Text inside the box */
            div[data-baseweb="select"] span {{
                color: #ffffff !important;
            }}
            
            /* Arrow Icon */
            div[data-baseweb="select"] svg {{
                fill: #ffffff !important;
            }}
            
            /* --- DROPDOWN MENU / LIST (The "Too Bright" Part) --- */
            
            /* Force the popover container to be dark */
            div[data-baseweb="popover"] {{
                 background-color: #0e1117 !important;
                 border: 1px solid rgba(255, 255, 255, 0.2) !important;
            }}
            
            /* Force the list inside to be dark */
            div[data-baseweb="menu"], ul {{
                background-color: #0e1117 !important;
            }}
            
            /* Individual Options */
            li[role="option"], div[role="option"] {{
                 background-color: #0e1117 !important;
                 color: #b0b0b0 !important; /* Light grey for inactive */
            }}
            
            /* Hover / Selected State */
            li[role="option"]:hover, li[role="option"][aria-selected="true"] {{
                background-color: rgba(0, 210, 255, 0.2) !important;
                color: #ffffff !important;
            }}

            /* --- OPEN BUTTON --- */
            
            /* 1. Center the button container (Flexbox) */
            div.stButton {{
                display: flex !important;
                justify-content: center !important;
                width: 100% !important;
                margin-top: 20px !important;
            }}

            /* 2. Style the button element */
            div.stButton > button {{
                width: auto !important;
                min-width: 150px; 
                margin: 0 !important; /* No auto margin, let flex parent center it */
                
                background: {colors['btn_bg']} !important;
                border: 1px solid {colors['card_border']} !important;
                color: {colors['accent']} !important;
                border-radius: 999px !important;
                font-weight: 600 !important;
                text-transform: uppercase;
                letter-spacing: 1.5px;
                transition: all 0.3s ease;
                min-height: 48px;
                font-size: 0.9rem !important;
            }}

            div.stButton > button:hover {{
                box-shadow: 0 0 15px rgba(0, 210, 255, 0.4);
                color: #fff !important;
                border-color: {colors['accent']} !important;
            }}
            
            /* Dataframes & Metrics (Sheet View) */
            .stDataFrame {{ background: rgba(0,0,0,0.3) !important; border-radius: 8px; padding: 10px; }}
            div[data-testid="stDataFrame"] {{ border: 1px solid {colors['card_border']}; border-radius: 8px; overflow: hidden; }}
            div[data-testid="stMetric"] {{ background-color: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.1); border-radius: 10px; padding: 15px; text-align: center; }}
            div[data-testid="stMetricLabel"] {{ color: {colors['text_secondary']} !important; font-size: 0.9rem; }}
            div[data-testid="stMetricValue"] {{ color: {colors['accent']} !important; font-size: 1.8rem; text-shadow: 0 0 10px rgba(0, 210, 255, 0.3); }}
            
            .stMarkdown {{ text-align: center; width: 100%; }}

        </style>
        <div class="bg-overlay"></div>
        """,
        unsafe_allow_html=True,
    )


def render_home_header():
    """Renders the fancy home header (Title only)."""
    st.markdown("<h1>My Finance</h1>", unsafe_allow_html=True)