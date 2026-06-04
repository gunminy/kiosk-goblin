import os
import random
import streamlit as st
from PIL import Image, ImageDraw, ImageFont
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
        accent_color = panel_config.get("accent_color", THEME_COLORS["warning"])
        
        # Display Plugin Header
        st.markdown(f"""
        <div style="border-bottom: 2px solid {accent_color}; padding-bottom: 0.3rem; margin-bottom: 1rem;">
            <h3 style="margin: 0; color: #f8fafc; font-size: 1.2rem; font-weight: 700; letter-spacing: 0.5px;">
                👁️ {self.title}
            </h3>
        </div>
        """, unsafe_allow_html=True)

        # Dynamic simulation values for overlay
        latency = f"{random.randint(12, 16)}ms"
        confidence = f"{random.uniform(91.5, 96.8):.1f}%"
        objects_detected = random.randint(1, 3)

        # Top metric cards for inference status
        m_col1, m_col2, m_col3 = st.columns(3)
        with m_col1:
            metric_card("Latency", latency, color=THEME_COLORS["primary"], icon="⚡")
        with m_col2:
            metric_card("Confidence", confidence, color=THEME_COLORS["success"], icon="🎯")
        with m_col3:
            metric_card("Detections", str(objects_detected), color=accent_color, icon="📦")

        # Load the mock preview image
        base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        img_path = os.path.join(base_path, "assets", "mock_preview.png")

        # Fallback to empty dark image if assets missing
        if os.path.exists(img_path):
            try:
                img = Image.open(img_path)
            except Exception:
                img = Image.new("RGB", (640, 640), color="#090d16")
        else:
            img = Image.new("RGB", (640, 640), color="#090d16")

        # Resize image for fast streaming presentation if it is too big
        img = img.resize((640, 640))
        draw = ImageDraw.Draw(img)

        # Define dynamic box jitter to look like active inference
        jitter_x = random.randint(-3, 3)
        jitter_y = random.randint(-3, 3)

        # Draw Simulated Bounding Box 1 (Robot Arm Area)
        # Bounding box coordinates: [x0, y0, x1, y1]
        box_1 = [250 + jitter_x, 260 + jitter_y, 490 + jitter_x, 620 + jitter_y]
        draw.rectangle(box_1, outline=THEME_COLORS["primary"], width=3)
        
        # Label 1 background and text
        label_1 = f"Robot-Arm: {random.uniform(94.0, 97.5):.1f}%"
        draw.rectangle([box_1[0], box_1[1] - 22, box_1[0] + 160, box_1[1]], fill=THEME_COLORS["primary"])
        draw.text((box_1[0] + 5, box_1[1] - 18), label_1, fill="#0b0f19")

        # Draw Simulated Bounding Box 2 (PCB/Belt Area)
        if objects_detected >= 2:
            box_2 = [180 + jitter_y, 500 + jitter_x, 380 + jitter_y, 590 + jitter_x]
            draw.rectangle(box_2, outline=THEME_COLORS["warning"], width=3)
            label_2 = f"PCB-Component: {random.uniform(88.0, 92.5):.1f}%"
            draw.rectangle([box_2[0], box_2[1] - 22, box_2[0] + 185, box_2[1]], fill=THEME_COLORS["warning"])
            draw.text((box_2[0] + 5, box_2[1] - 18), label_2, fill="#0b0f19")

        # Draw Simulated Bounding Box 3 (Conveyor Belt or other target)
        if objects_detected >= 3:
            box_3 = [420 + jitter_x, 480 + jitter_y, 580 + jitter_x, 560 + jitter_y]
            draw.rectangle(box_3, outline=THEME_COLORS["purple"], width=3)
            label_3 = f"Conveyor-Belt: {random.uniform(85.0, 89.0):.1f}%"
            draw.rectangle([box_3[0], box_3[1] - 22, box_3[0] + 185, box_3[1]], fill=THEME_COLORS["purple"])
            draw.text((box_3[0] + 5, box_3[1] - 18), label_3, fill="#ffffff")

        # Render image
        st.image(img, use_column_width=True, caption="Inference Stream Overlaid with Class Boundaries")

# Export class
PluginClass = MediaPreviewPlugin
