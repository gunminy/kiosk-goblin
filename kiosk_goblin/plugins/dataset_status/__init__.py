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
        chart_height = panel_config.get("chart_height", 180)
        
        status = data_source.get_dataset_status()
        
        # Display Plugin Header
        st.markdown(f"""
        <div style="border-bottom: 2px solid {accent_color}; padding-bottom: 0.3rem; margin-bottom: 1rem;">
            <h3 style="margin: 0; color: #f8fafc; font-size: 1.2rem; font-weight: 700; letter-spacing: 0.5px;">
                📊 {self.title}
            </h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Display summary cards
        metric_card("Total Dataset", f"{status['total_images']:,}", color=accent_color, icon="🖼️")
        
        col1, col2 = st.columns(2)
        with col1:
            metric_card("Labeled", f"{status['labeled_ratio']}%", color=THEME_COLORS["success"], icon="✅")
        with col2:
            metric_card("Added Today", f"+{status['recent_adds_today']}", color=THEME_COLORS["primary"], icon="📈")

        # Class Distribution Donut Chart
        dist = status["class_distribution"]
        labels = list(dist.keys())
        values = list(dist.values())
        
        # Cyberpunk colors mapping
        pie_colors = [
            THEME_COLORS["primary"],
            THEME_COLORS["purple"],
            THEME_COLORS["success"],
            THEME_COLORS["warning"],
            THEME_COLORS["danger"]
        ]
        
        fig = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hole=.5,
            marker=dict(colors=pie_colors),
            textinfo='label+percent',
            textposition='inside',
            insidetextorientation='radial',
            showlegend=False
        )])
        
        fig.update_layout(
            title=dict(
                text="Class Distribution",
                font=dict(size=12, color="#94a3b8")
            )
        )
        
        apply_dark_theme(fig, height=chart_height)
        # Tweak padding for pie chart
        fig.update_layout(margin=dict(l=0, r=0, t=25, b=0))
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

# Export class
PluginClass = DatasetStatusPlugin
