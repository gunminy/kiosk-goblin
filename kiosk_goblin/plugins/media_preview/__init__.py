import os
import random
import streamlit as st
from PIL import Image, ImageDraw
from kiosk_goblin.core.plugin import BasePlugin
from kiosk_goblin.ui.cards import metric_card
from kiosk_goblin.ui.charts import THEME_COLORS

class MediaPreviewPlugin(BasePlugin):
    @property
    def name(self) -> str:
        return "media_preview"

    @property
    def title(self) -> str:
        return "Model Inference Live Stream"

    def render(self, data_source, panel_config: dict):
        accent_color = panel_config.get("accent_color", THEME_COLORS["primary"])
        
        # Display Plugin Header without emoji
        st.markdown(f"""
        <div style="border-bottom: 1px solid {accent_color}; padding-bottom: 0.3rem; margin-bottom: 1rem;">
            <h3 style="margin: 0; color: #00ff41; font-size: 1.1rem; font-weight: 700; letter-spacing: 0.5px; font-family: monospace; text-transform: uppercase;">
                {self.title}
            </h3>
        </div>
        """, unsafe_allow_html=True)

        # Dynamic simulation values
        latency = f"{random.randint(12, 16)}ms"
        confidence = f"{random.uniform(91.5, 96.8):.1f}%"
        objects_detected = random.randint(1, 3)

        # Top metric cards (no icons)
        m_col1, m_col2, m_col3 = st.columns(3)
        with m_col1:
            metric_card("Latency", latency, color=THEME_COLORS["primary"])
        with m_col2:
            metric_card("Confidence", confidence, color=THEME_COLORS["secondary"])
        with m_col3:
            metric_card("Detections", str(objects_detected), color=THEME_COLORS["success"])

        # Dynamically generate a Matrix Digital Widescreen Scanner Grid (640x300 to reduce vertical space)
        img = Image.new("RGB", (640, 300), color="#000000")
        draw = ImageDraw.Draw(img)

        # Draw grid lines (monochrome dark green overlay)
        grid_color = (0, 35, 8)
        grid_size = 40
        for x in range(0, 640, grid_size):
            draw.line([(x, 0), (x, 300)], fill=grid_color, width=1)
        for y in range(0, 300, grid_size):
            draw.line([(0, y), (640, y)], fill=grid_color, width=1)

        # Draw scanner circular radar effect in the background
        draw.ellipse([120, -50, 520, 350], outline=(0, 50, 12), width=1)
        draw.ellipse([220, 50, 420, 250], outline=(0, 50, 12), width=1)

        # Add jitter
        jitter_x = random.randint(-2, 2)
        jitter_y = random.randint(-2, 2)

        # RGB colors
        c_primary = (0, 255, 65)
        c_secondary = (0, 204, 51)
        c_dark = (0, 143, 17)

        # Draw Simulated Bounding Box 1 (Robot Arm) scaled for 640x300
        box_1 = [220 + jitter_x, 80 + jitter_y, 450 + jitter_x, 240 + jitter_y]
        draw.rectangle(box_1, outline=c_primary, width=2)
        label_1 = f"Robot-Arm: {random.uniform(94.0, 97.5):.1f}%"
        draw.rectangle([box_1[0], box_1[1] - 18, box_1[0] + 150, box_1[1]], fill=c_primary)
        draw.text((box_1[0] + 4, box_1[1] - 15), label_1, fill=(0, 0, 0))

        # Draw Simulated Bounding Box 2 (PCB)
        if objects_detected >= 2:
            box_2 = [80 + jitter_y, 160 + jitter_x, 240 + jitter_y, 250 + jitter_x]
            draw.rectangle(box_2, outline=c_secondary, width=2)
            label_2 = f"PCB-Comp: {random.uniform(88.0, 92.5):.1f}%"
            draw.rectangle([box_2[0], box_2[1] - 18, box_2[0] + 145, box_2[1]], fill=c_secondary)
            draw.text((box_2[0] + 4, box_2[1] - 15), label_2, fill=(0, 0, 0))

        # Draw Simulated Bounding Box 3 (Conveyor)
        if objects_detected >= 3:
            box_3 = [450 + jitter_x, 140 + jitter_y, 590 + jitter_x, 220 + jitter_y]
            draw.rectangle(box_3, outline=c_dark, width=2)
            label_3 = f"Conveyor: {random.uniform(85.0, 89.0):.1f}%"
            draw.rectangle([box_3[0], box_3[1] - 18, box_3[0] + 135, box_3[1]], fill=c_dark)
            draw.text((box_3[0] + 4, box_3[1] - 15), label_3, fill=(0, 0, 0))

        # Scale image smoothly onto the container
        st.image(img, use_container_width=True, caption="Grid Scanner Overlaid with Real-time Inference Coordinates")

# Export class
PluginClass = MediaPreviewPlugin
