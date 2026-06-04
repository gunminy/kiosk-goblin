import streamlit as st
import plotly.graph_objects as go
from kiosk_goblin.core.plugin import BasePlugin
from kiosk_goblin.ui.cards import metric_card
from kiosk_goblin.ui.charts import apply_dark_theme, THEME_COLORS

class SystemMetricsPlugin(BasePlugin):
    @property
    def name(self) -> str:
        return "system_metrics"

    @property
    def title(self) -> str:
        return "System Resources"

    def render(self, data_source, panel_config: dict):
        accent_color = panel_config.get("accent_color", THEME_COLORS["primary"])
        
        metrics = data_source.get_system_metrics()
        
        st.markdown(f"""
        <div style="border-bottom: 1px solid {accent_color}; padding-bottom: 0.3rem; margin-bottom: 1rem;">
            <h3 style="margin: 0; color: #00ff41; font-size: 1.1rem; font-weight: 700; letter-spacing: 0.5px; font-family: monospace; text-transform: uppercase;">
                {self.title}
            </h3>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            metric_card("CPU Load", f"{metrics['cpu_usage']}%", color=THEME_COLORS["primary"])
        with col2:
            metric_card("RAM Load", f"{metrics['ram_usage']}%", color=THEME_COLORS["secondary"])

        col3, col4 = st.columns(2)
        with col3:
            metric_card("GPU Load", f"{metrics['gpu_usage']}%", color=THEME_COLORS["orange"])
        with col4:
            metric_card("GPU Temp", f"{metrics['gpu_temp']}°C", color=THEME_COLORS["primary"])

        resources = ['Disk', 'RAM', 'GPU VRAM', 'CPU']
        usages = [
            metrics['disk_usage'], 
            metrics['ram_usage'],
            round((metrics['gpu_memory_used_gb'] / metrics['gpu_memory_total_gb']) * 100.0, 1),
            metrics['cpu_usage']
        ]
        
        colors = []
        for usage in usages:
            if usage > 85.0:
                colors.append("#00ff66")
            elif usage > 70.0:
                colors.append("#00dd33")
            else:
                colors.append("#008f11")
                
        fig = go.Figure(go.Bar(
            x=usages,
            y=resources,
            orientation='h',
            marker=dict(
                color=colors,
                line=dict(color='rgba(0, 255, 65, 0.3)', width=1)
            ),
            text=[f"{v}%" for v in usages],
            textposition='auto',
            textfont=dict(color='#000000', size=10, family="monospace")
        ))
        
        fig.update_layout(
            xaxis=dict(range=[0, 100], showticklabels=True),
            yaxis=dict(autorange="reversed"),
            title=dict(
                text="Resource Occupancy (%)",
                font=dict(size=11, color="#008f11")
            )
        )
        
        # Enable container-width stretching for responsive width alignment
        apply_dark_theme(fig, height=180)
        fig.update_layout(margin=dict(l=55, r=10, t=30, b=10))
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        
        st.markdown(f"""
        <div class="kiosk-card" style="padding: 0.8rem; font-size: 0.8rem; margin-top: 0.5rem; background: rgba(0, 10, 2, 0.4); border-color: rgba(0, 255, 65, 0.1);">
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.3rem; font-family: monospace;">
                <span style="color: #008f11;">GPU VRAM:</span>
                <span style="color: #00ff41; font-weight:600;">{metrics['gpu_memory_used_gb']}G / {metrics['gpu_memory_total_gb']}G</span>
            </div>
            <div style="display: flex; justify-content: space-between; font-family: monospace;">
                <span style="color: #008f11;">Disk Space:</span>
                <span style="color: #00ff41; font-weight:600;">{metrics['disk_used_gb']}G / {metrics['disk_total_gb']}G</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

# Export class
PluginClass = SystemMetricsPlugin
