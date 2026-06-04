import streamlit as st

def inject_kiosk_theme():
    """
    Injects custom CSS to style the Streamlit app for a 1080x1920 Kiosk setup.
    Hides standard Streamlit decorations, sets a dark theme, and creates custom glow styles.
    """
    kiosk_css = """
    <style>
        /* Hide Streamlit elements */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .stDeployButton {display:none;}
        
        /* Disable scrollbars on the main body for standard kiosk layout */
        body {
            overflow: hidden;
            background-color: #0b0f19;
            color: #e2e8f0;
            font-family: 'Inter', 'Outfit', -apple-system, BlinkMacSystemFont, sans-serif;
        }

        /* Adjust main container padding to make it tight and kiosk-friendly */
        .block-container {
            padding-top: 1.5rem !important;
            padding-bottom: 1.5rem !important;
            padding-left: 1.5rem !important;
            padding-right: 1.5rem !important;
            max-width: 100% !important;
        }

        /* Glassmorphism Panel Container */
        .kiosk-card {
            background: rgba(17, 24, 39, 0.7);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 16px;
            padding: 1.5rem;
            margin-bottom: 1rem;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
            transition: all 0.3s ease;
        }
        
        .kiosk-card:hover {
            border: 1px solid rgba(0, 242, 254, 0.3);
            box-shadow: 0 8px 32px 0 rgba(0, 242, 254, 0.15);
        }

        /* Title styling with Neon glow */
        .kiosk-title {
            font-size: 2.2rem;
            font-weight: 800;
            background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-align: center;
            margin-bottom: 1.5rem;
            text-transform: uppercase;
            letter-spacing: 2px;
            filter: drop-shadow(0px 2px 8px rgba(0, 242, 254, 0.3));
        }

        /* Terminal Console style for logs */
        .terminal-box {
            background-color: #060913;
            border-left: 4px solid #f43f5e;
            border-radius: 8px;
            font-family: 'Fira Code', 'Courier New', Courier, monospace;
            padding: 1rem;
            color: #38bdf8;
            max-height: 280px;
            overflow-y: auto;
            font-size: 0.85rem;
            line-height: 1.4;
            border: 1px solid rgba(244, 63, 94, 0.2);
        }

        /* Scrollbar customizing */
        .terminal-box::-webkit-scrollbar {
            width: 6px;
        }
        .terminal-box::-webkit-scrollbar-track {
            background: rgba(0,0,0,0.1);
        }
        .terminal-box::-webkit-scrollbar-thumb {
            background: rgba(255,255,255,0.2);
            border-radius: 3px;
        }

        /* Badge design */
        .badge {
            display: inline-block;
            padding: 0.2rem 0.6rem;
            font-size: 0.75rem;
            font-weight: bold;
            border-radius: 9999px;
            text-transform: uppercase;
        }
        .badge-success { background-color: rgba(16, 185, 129, 0.2); color: #10b981; border: 1px solid rgba(16, 185, 129, 0.4); }
        .badge-warning { background-color: rgba(245, 158, 11, 0.2); color: #f59e0b; border: 1px solid rgba(245, 158, 11, 0.4); }
        .badge-danger { background-color: rgba(239, 68, 68, 0.2); color: #ef4444; border: 1px solid rgba(239, 68, 68, 0.4); }
        .badge-info { background-color: rgba(59, 130, 246, 0.2); color: #3b82f6; border: 1px solid rgba(59, 130, 246, 0.4); }
    </style>
    """
    st.markdown(kiosk_css, unsafe_allow_html=True)
