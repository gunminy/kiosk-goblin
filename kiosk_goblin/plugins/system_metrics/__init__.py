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
        accent_color = panel_config.get("accent_color", THEME_COLORS["success"])
        
        metrics = data_source.get_system_metrics()
        
        # Display Plugin Header
        st.markdown(f"""
        <div style="border-bottom: 2px solid {accent_color}; padding-bottom: 0.3rem; margin-bottom: 1rem;">
            <h3 style="margin: 0; color: #f8fafc; font-size: 1.2rem; font-weight: 700; letter-spacing: 0.5px;">
                ⚡ {self.title}
            </h3>
        </div>
        """, unsafe_allow_html=True)
        
        # CPU & RAM metrics
        col1, col2 = st.columns(2)
        with col1:
            metric_card("CPU Load", f"{metrics['cpu_usage']}%", color=THEME_COLORS["primary"], icon="💻")
        with col2:
            metric_card("RAM Load", f"{metrics['ram_usage']}%", color=THEME_COLORS["secondary"], icon="💾")

        # GPU metrics
        col3, col4 = st.columns(2)
        with col3:
            metric_card("GPU Load", f"{metrics['gpu_usage']}%", color=THEME_COLORS["purple"], icon="🎮")
        with col4:
            temp_color = THEME_COLORS["danger"] if metrics['gpu_temp'] > 80.0 else THEME_COLORS["warning"]
            metric_card("GPU Temp", f"{metrics['gpu_temp']}°C", color=temp_color, icon="🔥")

        # Visualizing with Plotly Horizontal bar chart (Comparison bar)
        resources = ['Disk', 'RAM', 'GPU VRAM', 'CPU']
        usages = [
            metrics['disk_usage'], 
            metrics['ram_usage'],
            round((metrics['gpu_memory_used_gb'] / metrics['gpu_memory_total_gb']) * 100.0, 1),
            metrics['cpu_usage']
        ]
        
        # Select bar color based on usage percent
        colors = []
        for usage in usages:
            if usage > 85.0:
                colors.append(THEME_COLORS["danger"])
            elif usage > 70.0:
                colors.append(THEME_COLORS["warning"])
            else:
                colors.append(THEME_COLORS["success"])
                
        fig = go.Figure(go.Bar(
            x=usages,
            y=resources,
            orientation='h',
            marker=dict(
                color=colors,
                line=dict(color='rgba(255,255,255,0.15)', width=1)
            ),
            text=[f"{v}%" for v in usages],
            textposition='auto',
            textfont=dict(color='#ffffff', size=10, family="monospace")
        ))
        
        fig.update_layout(
            xaxis=dict(range=[0, 100], showticklabels=True),
            yaxis=dict(autorange="reversed"),
            title=dict(
                text="Resource Occupancy (%)",
                font=dict(size=12, color="#94a3b8")
            )
        )
        
        apply_dark_theme(fig, height=180)
        # Tighten margins
        fig.update_layout(margin=dict(l=55, r=10, t=30, b=10))
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        
        # Additional metadata details
        st.markdown(f"""
        <div class="kiosk-card" style="padding: 0.8rem; font-size: 0.8rem; margin-top: 0.5rem; background: rgba(30, 41, 59, 0.4);">
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.3rem;">
                <span style="color: #64748b;">GPU VRAM:</span>
                <span style="color: #f8fafc; font-weight:600;">{metrics['gpu_memory_used_gb']}G / {metrics['gpu_memory_total_gb']}G</span>
            </div>
            <div style="display: flex; justify-content: space-between;">
                <span style="color: #64748b;">Disk Space:</span>
                <span style="color: #f8fafc; font-weight:600;">{metrics['disk_used_gb']}G / {metrics['disk_total_gb']}G</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

# Export class
PluginClass = SystemMetricsPlugin
