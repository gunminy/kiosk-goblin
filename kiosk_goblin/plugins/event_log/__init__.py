import streamlit as st
from kiosk_goblin.core.plugin import BasePlugin
from kiosk_goblin.ui.cards import status_badge
from kiosk_goblin.ui.charts import THEME_COLORS

class EventLogPlugin(BasePlugin):
    @property
    def name(self) -> str:
        return "event_log"

    @property
    def title(self) -> str:
        return "System Events & Logs"

    def render(self, data_source, panel_config: dict):
        accent_color = panel_config.get("accent_color", THEME_COLORS["primary"])
        log_height = panel_config.get("height", 150)
        
        logs = data_source.get_event_logs()
        
        # Display Plugin Header without emoji
        st.markdown(f"""
        <div style="border-bottom: 1px solid {accent_color}; padding-bottom: 0.3rem; margin-bottom: 1rem;">
            <h3 style="margin: 0; color: #00ff41; font-size: 1.1rem; font-weight: 700; letter-spacing: 0.5px; font-family: monospace; text-transform: uppercase;">
                {self.title}
            </h3>
        </div>
        """, unsafe_allow_html=True)

        # Count log states
        info_cnt = sum(1 for log in logs if log["level"] == "INFO")
        warn_cnt = sum(1 for log in logs if log["level"] == "WARN")
        err_cnt = sum(1 for log in logs if log["level"] == "ERROR")

        # Summary line
        badge_summary_html = f"""
        <div style="display: flex; gap: 1.0rem; margin-bottom: 0.8rem; font-size: 0.8rem; font-family: monospace;">
            <div>INFO: <span style="font-weight: 700; color: #00ff41;">{info_cnt}</span></div>
            <div>WARN: <span style="font-weight: 700; color: #00cc33;">{warn_cnt}</span></div>
            <div>ERROR: <span style="font-weight: 700; color: #ff3333;">{err_cnt}</span></div>
        </div>
        """
        st.markdown(badge_summary_html, unsafe_allow_html=True)

        # Build Terminal Output HTML
        terminal_lines = []
        for log in logs:
            level = log["level"]
            timestamp = log["timestamp"]
            message = log["message"]
            
            badge_type = "info"
            if level == "INFO":
                badge_type = "success"
                txt_color = "#00ff41" # Bright green
            elif level == "WARN":
                badge_type = "warning"
                txt_color = "#00aa22" # Mid green
            elif level == "ERROR":
                badge_type = "danger"
                txt_color = "#ff3333" # Dim red
                
            badge_html = status_badge(level, badge_type)
            line = f"""
            <div style="margin-bottom: 0.4rem; font-family: monospace; line-height: 1.4; font-size: 0.8rem;">
                <span style="color: #005500;">[{timestamp}]</span> 
                {badge_html} 
                <span style="color: {txt_color}; margin-left: 0.3rem;">{message}</span>
            </div>
            """
            terminal_lines.append(line)

        # Combine lines and inject
        logs_html = "".join(terminal_lines)
        terminal_html = f"""
        <div class="terminal-box" style="height: {log_height}px; border-left-color: {accent_color};">
            {logs_html}
        </div>
        """
        st.markdown(terminal_html, unsafe_allow_html=True)

# Export class
PluginClass = EventLogPlugin
