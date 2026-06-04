import streamlit as st
import plotly.graph_objects as go
from kiosk_goblin.core.plugin import BasePlugin
from kiosk_goblin.ui.cards import metric_card
from kiosk_goblin.ui.charts import apply_dark_theme, THEME_COLORS

class MLTrainingPlugin(BasePlugin):
    @property
    def name(self) -> str:
        return "ml_training"

    @property
    def title(self) -> str:
        return "ML Training Pipeline"

    def render(self, data_source, panel_config: dict):
        accent_color = panel_config.get("accent_color", THEME_COLORS["primary"])
        chart_height = panel_config.get("chart_height", 220)
        
        status = data_source.get_ml_training_status()
        
        st.markdown(f"""
        <div style="border-bottom: 1px solid {accent_color}; padding-bottom: 0.3rem; margin-bottom: 1rem;">
            <h3 style="margin: 0; color: #00ff41; font-size: 1.1rem; font-weight: 700; letter-spacing: 0.5px; font-family: monospace; text-transform: uppercase;">
                {self.title}
            </h3>
        </div>
        """, unsafe_allow_html=True)
        
        m_col1, m_col2, m_col3 = st.columns(3)
        with m_col1:
            epoch_str = f"{status['epoch']}/{status['max_epochs']}"
            metric_card("Epoch Progress", epoch_str, color=accent_color)
        with m_col2:
            loss_val = f"{status['loss']:.4f}"
            delta_loss = f"{-0.024:.3f}" if status['epoch'] > 1 else None
            metric_card("Train Loss", loss_val, delta=delta_loss, color=THEME_COLORS["secondary"])
        with m_col3:
            acc_val = f"{status['val_accuracy'] * 100:.1f}%"
            delta_acc = f"{0.012 * 100:.1f}%" if status['epoch'] > 1 else None
            metric_card("Val Accuracy", acc_val, delta=delta_acc, color=THEME_COLORS["success"])

        history = status["history"]
        epochs = history["epochs"]
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=epochs, 
            y=history["loss"],
            mode='lines',
            name='Train Loss',
            line=dict(color=THEME_COLORS["primary"], width=2)
        ))
        fig.add_trace(go.Scatter(
            x=epochs, 
            y=history["val_loss"],
            mode='lines',
            name='Val Loss',
            line=dict(color=THEME_COLORS["secondary"], width=2, dash='dash')
        ))
        
        fig.add_trace(go.Scatter(
            x=epochs,
            y=history["val_accuracy"],
            mode='lines',
            name='Val Acc',
            line=dict(color=THEME_COLORS["success"], width=2)
        ))

        fig.update_layout(
            title=dict(
                text="Loss / Accuracy History",
                font=dict(size=11, color="#008f11")
            ),
            hovermode="x unified",
        )
        
        # Enable container width stretching to match the cards perfectly
        apply_dark_theme(fig, height=chart_height)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

        st.markdown(f"""
        <div class="kiosk-card" style="padding: 0.8rem; font-size: 0.8rem; margin-top: 0.5rem; background: rgba(0, 10, 2, 0.4); border-color: rgba(0, 255, 65, 0.1);">
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.3rem; font-family: monospace;">
                <span style="color: #008f11;">Learning Rate:</span>
                <span style="color: #00ff41; font-weight:600;">{status['learning_rate']:.2e}</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.3rem; font-family: monospace;">
                <span style="color: #008f11;">Time Elapsed:</span>
                <span style="color: #00ff41; font-weight:600;">{status['time_elapsed']}</span>
            </div>
            <div style="display: flex; justify-content: space-between; font-family: monospace;">
                <span style="color: #008f11;">Est. Remaining:</span>
                <span style="color: {accent_color}; font-weight:700;">{status['time_remaining']}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

# Export class
PluginClass = MLTrainingPlugin
