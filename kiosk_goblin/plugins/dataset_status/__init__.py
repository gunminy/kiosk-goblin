import streamlit as st
import plotly.graph_objects as go
from kiosk_goblin.core.plugin import BasePlugin
from kiosk_goblin.ui.cards import metric_card
from kiosk_goblin.ui.charts import apply_dark_theme, THEME_COLORS

class DatasetStatusPlugin(BasePlugin):
    @property
    def name(self) -> str:
        return "dataset_status"

    @property
    def title(self) -> str:
        return "Dataset Status"

    def render(self, data_source, panel_config: dict):
        accent_color = panel_config.get("accent_color", THEME_COLORS["purple"])
        # Increased default height to 240px to prevent the donut shape from being squished vertically
        chart_height = 240
        
        status = data_source.get_dataset_status()
        
        st.markdown(f"""
        <div style="border-bottom: 1px solid {accent_color}; padding-bottom: 0.3rem; margin-bottom: 1rem;">
            <h3 style="margin: 0; color: #00ff41; font-size: 1.1rem; font-weight: 700; letter-spacing: 0.5px; font-family: monospace; text-transform: uppercase;">
                {self.title}
            </h3>
        </div>
        """, unsafe_allow_html=True)
        
        metric_card("Total Dataset", f"{status['total_images']:,}", color=accent_color)
        
        col1, col2 = st.columns(2)
        with col1:
            metric_card("Labeled", f"{status['labeled_ratio']}%", color=THEME_COLORS["success"])
        with col2:
            metric_card("Added Today", f"+{status['recent_adds_today']}", color=THEME_COLORS["primary"])

        dist = status["class_distribution"]
        labels = list(dist.keys())
        values = list(dist.values())
        
        pie_colors = [
            "#00ff41",
            "#00dd33",
            "#00aa22",
            "#008811",
            "#005500"
        ]
        
        fig = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hole=.6,
            marker=dict(colors=pie_colors, line=dict(color='#000000', width=1.5)),
            textinfo='label+percent',
            textposition='inside',
            insidetextorientation='horizontal',  # Keep text upright
            showlegend=False,  # Disable legend to maximize rendering space
            domain=dict(x=[0, 1], y=[0, 1])
        )])
        
        fig.update_layout(
            margin=dict(l=5, r=5, t=5, b=5),
        )
        
        apply_dark_theme(fig, height=chart_height)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

# Export class
PluginClass = DatasetStatusPlugin
