import os
import yaml
from dotenv import load_dotenv

# Load environmental variables
load_dotenv()

class DashboardConfig:
    """
    Configuration manager for the Kiosk Goblin dashboard.
    Loads settings from the YAML file specified by the KIOSK_CONFIG_PATH environment variable.
    """
    def __init__(self, config_path: str = None):
        if not config_path:
            config_path = os.getenv("KIOSK_CONFIG_PATH", "examples/dashboard.yaml")
        
        self.config_path = config_path
        self.title = "Kiosk Goblin"
        self.refresh_interval = 60
        self.theme = "cyberpunk-dark"
        self.layout = []
        self.datasource = {"type": "mock"}
        self.panel_settings = {}
        
        self.load_config()

    def load_config(self):
        """Loads configuration from YAML file."""
        if not os.path.exists(self.config_path):
            # If the file does not exist, we log a warning or use defaults.
            print(f"Warning: Configuration file {self.config_path} not found. Using defaults.")
            return

        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
                if data:
                    self.title = data.get("title", self.title)
                    # Environment variable takes priority if defined
                    self.refresh_interval = int(os.getenv("KIOSK_REFRESH_INTERVAL", data.get("refresh_interval", self.refresh_interval)))
                    self.theme = data.get("theme", self.theme)
                    self.layout = data.get("layout", self.layout)
                    self.datasource = data.get("datasource", self.datasource)
                    self.panel_settings = data.get("panels", self.panel_settings)
        except Exception as e:
            print(f"Error loading configuration from {self.config_path}: {e}")
            raise e
            
    def get_panel_config(self, plugin_name: str) -> dict:
        """Returns specific configurations for a given plugin."""
        return self.panel_settings.get(plugin_name, {})
