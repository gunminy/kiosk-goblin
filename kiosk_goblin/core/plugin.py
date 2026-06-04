import os
import importlib
from abc import ABC, abstractmethod

class BasePlugin(ABC):
    """
    Abstract Base Class for all Kiosk Goblin plugins.
    """
    @property
    @abstractmethod
    def name(self) -> str:
        """Unique identifier name of the plugin."""
        pass

    @property
    @abstractmethod
    def title(self) -> str:
        """Display title of the plugin."""
        pass

    @abstractmethod
    def render(self, data_source, panel_config: dict):
        """
        Renders the plugin inside a Streamlit container.
        Args:
            data_source: The datasource interface providing required data.
            panel_config: Plugin-specific configuration from dashboard.yaml.
        """
        pass


def load_plugins() -> dict:
    """
    Dynamically loads all plugins in the `kiosk_goblin/plugins` directory.
    Looks for folders with __init__.py containing a class named `PluginClass` that inherits from BasePlugin.
    Returns:
        A dictionary mapping plugin names to their instantiated plugin objects.
    """
    plugins = {}
    plugins_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "plugins")
    
    if not os.path.exists(plugins_dir):
        return plugins

    for item in os.listdir(plugins_dir):
        item_path = os.path.join(plugins_dir, item)
        if os.path.isdir(item_path) and not item.startswith("__"):
            try:
                # Import the module
                module_name = f"kiosk_goblin.plugins.{item}"
                module = importlib.import_module(module_name)
                
                # Check for PluginClass definition
                if hasattr(module, "PluginClass"):
                    plugin_class = getattr(module, "PluginClass")
                    # Instantiate and register the plugin
                    plugin_instance = plugin_class()
                    if isinstance(plugin_instance, BasePlugin):
                        plugins[plugin_instance.name] = plugin_instance
                    else:
                        print(f"Warning: PluginClass in {module_name} does not inherit from BasePlugin.")
            except Exception as e:
                print(f"Error loading plugin {item}: {e}")
                
    return plugins
