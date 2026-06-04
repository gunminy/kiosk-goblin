import streamlit as st
from kiosk_goblin.core.config import DashboardConfig

def render_layout(config: DashboardConfig, plugins: dict, data_source):
    """
    Renders the layout grid based on the DashboardConfig and invokes
    the associated plugins to render within their layout cells.
    """
    if not config.layout:
        st.warning("No layout configuration found. Please check dashboard.yaml.")
        return

    # Render row by row
    for row_idx, row_item in enumerate(config.layout):
        row_data = row_item.get("row", [])
        if not row_data:
            continue
            
        # Parse columns widths
        cols_widths = []
        for panel in row_data:
            width = panel.get("width", 12)  # default is full width
            cols_widths.append(width)
            
        # Create columns in Streamlit
        if len(cols_widths) == 1:
            # Single column row
            panel = row_data[0]
            plugin_name = panel.get("plugin")
            panel_config = config.get_panel_config(plugin_name)
            
            _render_panel(plugin_name, plugins, data_source, panel_config)
        else:
            # Multi-column row
            cols = st.columns(cols_widths)
            for col_idx, panel in enumerate(row_data):
                plugin_name = panel.get("plugin")
                panel_config = config.get_panel_config(plugin_name)
                
                with cols[col_idx]:
                    _render_panel(plugin_name, plugins, data_source, panel_config)

def _render_panel(plugin_name: str, plugins: dict, data_source, panel_config: dict):
    """Renders an individual plugin panel with error fallback."""
    if not plugin_name:
        st.error("Invalid panel definition: 'plugin' name missing.")
        return

    if plugin_name in plugins:
        try:
            plugins[plugin_name].render(data_source, panel_config)
        except Exception as e:
            st.error(f"Error rendering plugin '{plugin_name}': {e}")
    else:
        st.warning(f"Plugin '{plugin_name}' not loaded or does not exist.")
