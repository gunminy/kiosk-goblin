import streamlit as st

def glass_card(title: str, content_html: str, icon: str = None):
    """
    Renders a complete glassmorphism card with raw HTML content.
    """
    icon_html = f"<span style='margin-right: 0.5rem;'>{icon}</span>" if icon else ""
    html = f"""
    <div class="kiosk-card">
        <div style="font-weight: 700; font-size: 1.1rem; color: #94a3b8; margin-bottom: 0.8rem; display: flex; align-items: center;">
            {icon_html} {title}
        </div>
        <div>
            {content_html}
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

def metric_card(title: str, value: str, delta: str = None, color: str = "#00f2fe", icon: str = None):
    """
    Renders a premium visual metric card with an optional delta indicator.
    """
    delta_html = ""
    if delta:
        is_positive = not delta.startswith("-")
        delta_color = "#10b981" if is_positive else "#ef4444"
        delta_arrow = "▲" if is_positive else "▼"
        delta_html = f"""
        <div style="font-size: 0.85rem; color: {delta_color}; font-weight: 600; margin-top: 0.2rem;">
            {delta_arrow} {delta}
        </div>
        """
        
    icon_html = f"<span style='font-size: 1.2rem; margin-right: 0.5rem;'>{icon}</span>" if icon else ""
    
    html = f"""
    <div class="kiosk-card" style="border-left: 4px solid {color};">
        <div style="font-size: 0.85rem; font-weight: 600; color: #64748b; text-transform: uppercase; letter-spacing: 1px; display: flex; align-items: center;">
            {icon_html} {title}
        </div>
        <div style="font-size: 1.8rem; font-weight: 800; color: #f8fafc; margin-top: 0.4rem; font-family: 'Fira Code', monospace; text-shadow: 0 0 10px rgba({','.join(map(str, hex_to_rgb(color)))}, 0.25);">
            {value}
        </div>
        {delta_html}
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

def status_badge(text: str, badge_type: str = "info") -> str:
    """
    Returns an HTML string for a badge. Types: success, warning, danger, info.
    """
    return f'<span class="badge badge-{badge_type}">{text}</span>'

def hex_to_rgb(hex_str: str):
    """Convert hex string (e.g. #00f2fe) to RGB tuple."""
    hex_str = hex_str.lstrip('#')
    if len(hex_str) == 3:
        hex_str = ''.join(c*2 for c in hex_str)
    return tuple(int(hex_str[i:i+2], 16) for i in (0, 2, 4))
