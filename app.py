import os
import streamlit as st

# Set Streamlit Page Configuration first
st.set_page_config(
    page_title="Kiosk Goblin",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Core Framework imports
from kiosk_goblin.core.config import DashboardConfig
from kiosk_goblin.core.plugin import load_plugins
from kiosk_goblin.core.layout import render_layout
from kiosk_goblin.core.refresh import setup_auto_refresh
from kiosk_goblin.ui.theme import inject_kiosk_theme

# Datasource imports
from kiosk_goblin.datasources.mock_source import MockDataSource
from kiosk_goblin.datasources.json_source import JSONDataSource

@st.fragment
def render_dashboard_fragment(config, plugins, data_source):
    """
    Renders the grid layout within a isolated fragment container.
    Refreshes inside this fragment every second, preventing full-page DOM rebuilding.
    """
    # 5. Set periodic screen update loops (Auto refresh) inside the fragment
    setup_auto_refresh(config.refresh_interval)
    
    # 6. Render rows and columns visual layout
    render_layout(config, plugins, data_source)

def main():
    # 1. Inject custom dark theme stylesheet designed for vertical kiosk aspect ratios
    inject_kiosk_theme()
    
    # 2. Load layout configurations
    try:
        config = DashboardConfig()
    except Exception as e:
        st.error(f"Failed to load configurations: {e}")
        return

    # 3. Setup dynamic datasource selection
    ds_type = config.datasource.get("type", "mock").lower()
    if ds_type == "json":
        data_source = JSONDataSource()
    else:
        # Default fallback is stateful mock datasource
        data_source = MockDataSource()

    # 4. Dynamically discover and load plugin instances
    plugins = load_plugins()

    # Invoke the fragment container for flicker-free rendering loops
    render_dashboard_fragment(config, plugins, data_source)

    # 7. Fullscreen toggle guide text (Rendered static outside the loop)
    st.markdown(
        """
        <div style="position: fixed; bottom: 8px; right: 15px; font-size: 0.7rem; color: #005500; z-index: 999999; font-family: monospace; opacity: 0.6; pointer-events: none;">
            💡 Press <b>F11</b> to toggle Fullscreen/Windowed mode
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
