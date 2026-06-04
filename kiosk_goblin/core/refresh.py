import streamlit as st

def setup_auto_refresh(interval_seconds: int = 60):
    """
    Sets up automatic page reloading/refreshing.
    Uses `streamlit_autorefresh` if available; falls back to an HTML/JS-based refresh timer.
    """
    if interval_seconds <= 0:
        return
        
    try:
        from streamlit_autorefresh import st_autorefresh
        # st_autorefresh returns a counter but we just need it to trigger rerun
        st_autorefresh(interval=interval_seconds * 1000, key="kiosk_autorefresh")
    except ImportError:
        # Fallback to custom JS refresh if package is missing or fails
        js_refresh = f"""
        <iframe src="about:blank" style="display:none" name="refresh_iframe"></iframe>
        <script>
            if (window.parent) {{
                setTimeout(function() {{
                    window.parent.location.reload();
                }}, {interval_seconds * 1000});
            }}
        </script>
        """
        st.components.v1.html(js_refresh, height=0, width=0)
