import calendar
from datetime import datetime
import streamlit as st
from kiosk_goblin.core.plugin import BasePlugin
from kiosk_goblin.ui.charts import THEME_COLORS

class DateTimeWeatherPlugin(BasePlugin):
    @property
    def name(self) -> str:
        return "datetime_weather"

    @property
    def title(self) -> str:
        return "System Time & Local Environment"

    def render(self, data_source, panel_config: dict):
        accent_color = panel_config.get("accent_color", THEME_COLORS["primary"])
        
        # Display Plugin Header
        st.markdown(f"""
        <div style="border-bottom: 1px solid {accent_color}; padding-bottom: 0.3rem; margin-bottom: 0.8rem;">
            <h3 style="margin: 0; color: #00ff41; font-size: 1.1rem; font-weight: 700; letter-spacing: 0.5px; font-family: monospace; text-transform: uppercase;">
                {self.title}
            </h3>
        </div>
        """, unsafe_allow_html=True)

        now = datetime.now()
        weather = data_source.get_weather_status()
        tasks = data_source.get_today_tasks()

        col1, col2 = st.columns([7, 5])
        
        with col1:
            clock_html = """
            <style>
                body {
                    margin: 0;
                    padding: 0;
                    background-color: transparent;
                    color: #00ff41;
                    font-family: 'Fira Code', 'Courier New', Courier, monospace;
                    overflow: hidden;
                }
                .kiosk-card-inner {
                    background: rgba(0, 15, 3, 0.4);
                    border: 1px solid rgba(0, 255, 65, 0.2);
                    border-radius: 4px;
                    padding: 1.0rem;
                    box-shadow: 0 0 10px rgba(0, 255, 65, 0.05);
                }
            </style>
            <div class="kiosk-card-inner">
                <div style="font-size: 0.75rem; color: #008f11; text-transform: uppercase;">System Chronometer</div>
                <div id="matrix-clock" style="font-size: 2.2rem; font-weight: 800; color: #00ff41; text-shadow: 0 0 8px rgba(0, 255, 65, 0.5); line-height: 1.2; margin-top: 0.2rem;">
                    --:--:--
                </div>
                <div id="matrix-date" style="font-size: 0.9rem; font-weight: 600; color: #00cc33; margin-top: 0.2rem;">
                    YYYY-MM-DD
                </div>
            </div>
            
            <script>
                function updateMatrixClock() {
                    const now = new Date();
                    const hrs = String(now.getHours()).padStart(2, '0');
                    const mins = String(now.getMinutes()).padStart(2, '0');
                    const secs = String(now.getSeconds()).padStart(2, '0');
                    
                    const days = ['SUNDAY', 'MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY'];
                    const year = now.getFullYear();
                    const month = String(now.getMonth() + 1).padStart(2, '0');
                    const date = String(now.getDate()).padStart(2, '0');
                    const dayName = days[now.getDay()];
                    
                    const clockEl = document.getElementById('matrix-clock');
                    const dateEl = document.getElementById('matrix-date');
                    if (clockEl) clockEl.textContent = hrs + ':' + mins + ':' + secs;
                    if (dateEl) dateEl.textContent = year + '-' + month + '-' + date + '  ' + dayName;
                }
                updateMatrixClock();
                setInterval(updateMatrixClock, 1000);
            </script>
            """
            st.components.v1.html(clock_html, height=130)
            
            st.markdown(f"""
            <div class="kiosk-card" style="padding: 0.8rem 1.0rem; border-color: rgba(0, 255, 65, 0.1); background: rgba(0, 10, 2, 0.3); margin-bottom: 0;">
                <div style="font-size: 0.75rem; color: #008f11; text-transform: uppercase; font-family: monospace; margin-bottom: 0.3rem;">Atmospheric Feed</div>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.4rem; font-family: monospace; font-size: 0.8rem;">
                    <div><span style="color: #008f11;">LOC:</span> <span style="color: #00ff41; font-weight: 600;">{weather['location']}</span></div>
                    <div><span style="color: #008f11;">TEMP:</span> <span style="color: #00ff41; font-weight: 600;">{weather['temp']}°C</span></div>
                    <div><span style="color: #008f11;">SKY:</span> <span style="color: #00ff41; font-weight: 600;">{weather['condition']}</span></div>
                    <div><span style="color: #008f11;">HUMI:</span> <span style="color: #00ff41; font-weight: 600;">{weather['humidity']}%</span></div>
                    <div><span style="color: #008f11;">WIND:</span> <span style="color: #00ff41;">{weather['wind_speed']}</span></div>
                    <div><span style="color: #008f11;">AQI:</span> <span style="color: #00ff41;">{weather['air_quality']}</span></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            # Build Calendar
            year = now.year
            month = now.month
            today = now.day
            
            cal = calendar.TextCalendar(calendar.SUNDAY)
            cal_str = cal.formatmonth(year, month)
            
            lines = cal_str.split('\n')
            formatted_lines = []
            
            formatted_lines.append(f"<div style='color: #00ff41; font-weight: 700; text-align: center;'>{lines[0].strip().upper()}</div>")
            formatted_lines.append(f"<div style='color: #008f11;'>{lines[1]}</div>")
            
            for line in lines[2:]:
                if not line.strip():
                    continue
                padded_line = line.ljust(20)
                chunks = [padded_line[i:i+3] for i in range(0, len(padded_line), 3)]
                
                new_chunks = []
                for chunk in chunks:
                    day_str = chunk.strip()
                    if day_str and day_str.isdigit() and int(day_str) == today:
                        if len(day_str) == 1:
                            new_chunks.append(f"<span style='color: #00ff41; font-weight: 900; background: rgba(0,255,65,0.25); border: 1px solid #00ff41; padding: 0 2px;'>{day_str}</span>")
                        else:
                            new_chunks.append(f"<span style='color: #00ff41; font-weight: 900; background: rgba(0,255,65,0.25); border: 1px solid #00ff41; padding: 0 1px;'>{day_str}</span>")
                    else:
                        new_chunks.append(f"<span style='color: #008f11;'>{chunk}</span>")
                formatted_lines.append("".join(new_chunks))
                
            cal_html = "<br>".join(formatted_lines)
            
            # Build Daily Tasks List (Bigger font and spacing)
            tasks_lines = []
            for t in tasks:
                t_time = t["time"]
                t_name = t["task"]
                t_status = t["status"]
                
                if t_status == "SUCCESS":
                    status_html = '<span style="color:#00ff41;">[DONE]</span>'
                elif t_status == "ACTIVE":
                    status_html = '<span class="blink-text" style="color:#00ff41; font-weight:bold;">[RUN]</span>'
                else:
                    status_html = '<span style="color:#005500;">[WAIT]</span>'
                
                line = f'<div style="margin-bottom:0.4rem;display:flex;justify-content:space-between;font-size:0.75rem;line-height:1.3;"><span style="color:#008f11;font-weight:bold;margin-right:0.3rem;">{t_time}</span><span style="color:#00cc33;flex-grow:1;text-align:left;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;margin-right:0.3rem;">{t_name}</span>{status_html}</div>'
                tasks_lines.append(line)
            tasks_html = "".join(tasks_lines)

            # Condensed Flexbox layout: Left = Calendar, Right = Schedules, with vertical split line
            # Increased line heights and font sizes to eliminate empty space
            style_block = "<style>@keyframes taskBlink {0% { opacity: 1; } 50% { opacity: 0.4; } 100% { opacity: 1; }} .blink-text {animation: taskBlink 1.5s infinite;}</style>"
            
            card_html = f'{style_block}<div class="kiosk-card" style="padding:1.1rem 1.0rem;border-color:rgba(0,255,65,0.15);background:rgba(0,10,2,0.3);height:100%;"><div style="display:flex;justify-content:space-between;align-items:center;gap:0.8rem;height:100%;"><div style="font-family:monospace;font-size:0.82rem;line-height:1.6;white-space:pre;width:46%;">{cal_html}</div><div style="border-left:1px dashed rgba(0,255,65,0.2);height:175px;margin:0 0.1rem;align-self:center;"></div><div style="font-family:monospace;width:50%;align-self:center;"><div style="color:#00ff41;font-weight:700;margin-bottom:0.8rem;font-size:0.8rem;letter-spacing:0.5px;text-align:center;">[ SCHEDULES ]</div>{tasks_html}</div></div></div>'

            st.markdown(card_html, unsafe_allow_html=True)

# Export class
PluginClass = DateTimeWeatherPlugin
