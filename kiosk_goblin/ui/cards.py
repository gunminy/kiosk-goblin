import streamlit as st

def glass_card(title: str, content_html: str, icon: str = None):
    """
    Renders a terminal style card without icons, in a single HTML block to prevent Streamlit parsing errors.
    """
    html = f'<div class="kiosk-card"><div style="font-family:monospace;font-weight:700;font-size:1.0rem;color:#00ff41;margin-bottom:0.6rem;border-bottom:1px solid rgba(0,255,65,0.1);padding-bottom:0.3rem;">{title}</div><div>{content_html}</div></div>'
    st.markdown(html, unsafe_allow_html=True)

def metric_card(title: str, value: str, delta: str = None, color: str = "#00ff41", icon: str = None):
    """
    Renders a terminal metric card with matrix-green typography. Condensed html string avoids code-block leaks.
    """
    delta_html = ""
    if delta:
        is_positive = not delta.startswith("-")
        delta_color = "#00ff41" if is_positive else "#ff3333"
        delta_arrow = "+" if is_positive else ""
        delta_html = f'<div style="font-size:0.8rem;color:{delta_color};font-weight:600;margin-top:0.2rem;font-family:monospace;">{delta_arrow}{delta}</div>'
        
    html = f'<div class="kiosk-card" style="border-left:3px solid {color};border-radius:2px;"><div style="font-size:0.75rem;font-weight:600;color:#008f11;text-transform:uppercase;letter-spacing:1px;font-family:monospace;">{title}</div><div style="font-size:1.6rem;font-weight:800;color:#00ff41;margin-top:0.3rem;font-family:monospace;text-shadow:0 0 5px rgba(0,255,65,0.4);">{value}</div>{delta_html}</div>'
    st.markdown(html, unsafe_allow_html=True)

def status_badge(text: str, badge_type: str = "info") -> str:
    """
    Returns an HTML string for a badge.
    """
    return f'<span class="badge badge-{badge_type}">{text}</span>'
