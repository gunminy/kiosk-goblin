import streamlit as st

def inject_kiosk_theme():
    """
    Injects custom CSS to style the Streamlit app with a "Matrix terminal" theme.
    Uses pure black/deep green backgrounds, neon green text, and monospace fonts.
    Suppresses Streamlit's running status spinners to make refreshes seamless.
    Centering Plotly layouts removes asymmetrical margin gaps.
    """
    matrix_css = """
    <style>
        /* Hide Streamlit elements */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .stDeployButton {display:none;}
        
        /* Hide running spinners and top decoration lines to prevent refresh flickering */
        .stStatusWidget, [data-testid="stStatusWidget"] {display: none !important;}
        div[data-testid="stDecoration"] {display: none !important;}
        .stSpinner {display: none !important;}
        
        /* Center-align Plotly charts within containers to distribute margins evenly */
        .stPlotlyChart {
            display: flex !important;
            justify-content: center !important;
            width: 100% !important;
        }
        
        /* Disable scrollbars on the main body for standard kiosk layout */
        body {
            overflow: hidden;
            background-color: #000000;
            color: #00ff41;
            font-family: 'Fira Code', 'Courier New', Courier, monospace;
        }

        /* Adjust main container padding - reduced side padding to let charts bleed to edges */
        .block-container {
            padding-top: 0.8rem !important;
            padding-bottom: 0.8rem !important;
            padding-left: 0.8rem !important;
            padding-right: 0.8rem !important;
            max-width: 100% !important;
        }

        /* Matrix terminal card style */
        .kiosk-card {
            background: rgba(0, 15, 3, 0.4);
            border: 1px solid rgba(0, 255, 65, 0.2);
            border-radius: 4px;
            padding: 1.2rem;
            margin-bottom: 0.8rem;
            box-shadow: 0 0 10px rgba(0, 255, 65, 0.05);
            transition: all 0.2s ease;
        }
        
        .kiosk-card:hover {
            border: 1px solid rgba(0, 255, 65, 0.5);
            box-shadow: 0 0 15px rgba(0, 255, 65, 0.25);
        }

        /* Terminal Console style for logs */
        .terminal-box {
            background-color: #000000;
            border-left: 3px solid #00ff41;
            border-radius: 4px;
            font-family: 'Fira Code', 'Courier New', Courier, monospace;
            padding: 1rem;
            color: #00ff41;
            max-height: 280px;
            overflow-y: auto;
            font-size: 0.85rem;
            line-height: 1.4;
            border: 1px solid rgba(0, 255, 65, 0.2);
        }

        /* Scrollbar customizing */
        .terminal-box::-webkit-scrollbar {
            width: 5px;
        }
        .terminal-box::-webkit-scrollbar-track {
            background: rgba(0, 0, 0, 0.9);
        }
        .terminal-box::-webkit-scrollbar-thumb {
            background: rgba(0, 255, 65, 0.3);
            border-radius: 2px;
        }

        /* Monochrome green badges */
        .badge {
            display: inline-block;
            padding: 0.15rem 0.5rem;
            font-size: 0.7rem;
            font-weight: bold;
            border-radius: 2px;
            text-transform: uppercase;
        }
        .badge-success { background-color: rgba(0, 255, 65, 0.15); color: #00ff41; border: 1px solid rgba(0, 255, 65, 0.4); }
        .badge-warning { background-color: rgba(0, 150, 45, 0.15); color: #00cc33; border: 1px solid rgba(0, 150, 45, 0.4); }
        .badge-danger { background-color: rgba(255, 0, 0, 0.1); color: #ff3333; border: 1px solid rgba(255, 0, 0, 0.3); }
        .badge-info { background-color: rgba(0, 100, 20, 0.15); color: #009922; border: 1px solid rgba(0, 100, 20, 0.3); }
    </style>
    """
    st.markdown(matrix_css, unsafe_allow_html=True)
