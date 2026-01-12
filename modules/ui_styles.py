import streamlit as st

def inject_custom_css():
    # Hardcoded Dark Theme Constants
    colors = {
        "text": "#ffffff",
        "btn_bg": "rgba(255,255,255,0.08)",
        "border": "#00d2ff",
        "overlay": "rgba(14,17,23,0.88)",
        "grad": "linear-gradient(#00d2ff, #3a7bd5)"
    }

    lottie_url = "https://lottie.host/embed/6ca369ad-6dbf-4aa3-b873-ea3edfdc21cc/7pnY5Ztuya.lottie"

    st.markdown(f"""
        <style>
            .stApp {{ background: transparent; }}
            header, footer {{ visibility: hidden; }}
            
            /* Lottie Layer */
            .lottie-bg {{ position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: -99; pointer-events: none; }}
            iframe {{ width: 100%; height: 100%; border: none; }}
            
            /* Overlay */
            .overlay {{ position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: {colors['overlay']}; z-index: -98; pointer-events: none; }}
            
            /* Title Design */
            .main-title {{ 
                font-size: clamp(1.2rem, 5vw, 2.5rem); 
                font-weight: 800; 
                text-align: center; 
                background: -webkit-{colors['grad']}; 
                -webkit-background-clip: text; 
                -webkit-text-fill-color: transparent; 
                margin: 0px 0 20px 0; 
            }}
            
            /* Button Design */
            div.stButton > button {{ 
                width: 100%; 
                background: {colors['btn_bg']}; 
                color: {colors['text']} !important; 
                border: 1px solid {colors['border']}; 
                border-radius: 12px; 
                font-weight: 700; 
                backdrop-filter: blur(8px); 
                min-height: 55px; 
                transition: 0.3s;
            }}
            
            div.stButton > button:hover {{ 
                background: {colors['border']}; 
                color: white !important; 
                transform: scale(0.97); 
            }}

            /* Detail Page Container Fixes */
            .block-container {{
                padding-top: 1rem !important;
            }}
        </style>
        <div class="lottie-bg"><iframe src="{lottie_url}"></iframe></div>
        <div class="overlay"></div>
    """, unsafe_allow_html=True)