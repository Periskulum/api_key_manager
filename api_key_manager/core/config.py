"""
Configuration management for API Key Manager.
"""

import os
import json
from pathlib import Path

# Default configuration
DEFAULT_CONFIG = {
    # Application settings
    "app_name": "API Key Manager",
    "organization": "APIKeyManager",
    
    # UI settings
    "window": {
        "title": "API Key Manager",
        "min_width": 265,
        "min_height": 400,
        "start_maximized": False,
        "dark_mode": False,
    },
    
    # Build settings
    "build": {
        "executable_name": "API Key Manager",
        "icon_path": os.path.join("resources", "icons", "app_icon.ico"),
        "one_file": True,
    },
    
    # Storage settings
    "storage": {
        "service_name": "APIKeyManager",
        "index_key": "__key_index__",
    }
}

class Config:
    """Manage application configuration."""
    
    def __init__(self, config_path=None):
        """Initialize configuration.
        
        Args:
            config_path (str, optional): Path to the configuration file.
                If not provided, looks for config.json in the app directory.
        """
        self.config_data = DEFAULT_CONFIG.copy()
        
        # Determine config file path
        if config_path is None:
            app_dir = Path(__file__).resolve().parent.parent
            self.config_path = os.path.join(app_dir, "config.json")
        else:
            self.config_path = config_path
        
        # Load config file if it exists
        self.load_config()
    
    def load_config(self):
        """Load configuration from file."""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r") as f:
                    user_config = json.load(f)
                
                # Update default config with user settings (recursively)
                self._update_config(self.config_data, user_config)
                
                print(f"Configuration loaded from {self.config_path}")
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error loading configuration: {e}")
        else:
            # Create default config file if it doesn't exist
            self.save_config()
    
    def save_config(self):
        """Save current configuration to file."""
        try:
            with open(self.config_path, "w") as f:
                json.dump(self.config_data, f, indent=2)
            
            print(f"Configuration saved to {self.config_path}")
        except IOError as e:
            print(f"Error saving configuration: {e}")
    
    def _update_config(self, target, source):
        """Recursively update the target dictionary with values from source."""
        for key, value in source.items():
            if key in target and isinstance(target[key], dict) and isinstance(value, dict):
                self._update_config(target[key], value)
            else:
                target[key] = value
    
    def get(self, section, key=None, default=None):
        """Get a configuration value.
        
        Args:
            section (str): Configuration section.
            key (str, optional): Configuration key within section.
                If not provided, returns the entire section.
            default (any, optional): Default value if section/key not found.
        
        Returns:
            The configuration value or default if not found.
        """
        if section not in self.config_data:
            return default
        
        if key is None:
            return self.config_data[section]
        
        return self.config_data[section].get(key, default)
    
    def set(self, section, key, value):
        """Set a configuration value.
        
        Args:
            section (str): Configuration section.
            key (str): Configuration key within section.
            value: Value to set.
        """
        if section not in self.config_data:
            self.config_data[section] = {}
        
        self.config_data[section][key] = value
    
    def get_app_name(self):
        """Get the application name."""
        return self.config_data.get("app_name", "API Key Manager")
    
    def get_window_config(self):
        """Get window configuration."""
        return self.config_data.get("window", {})
    
    def get_build_config(self):
        """Get build configuration."""
        return self.config_data.get("build", {})
    
    def get_storage_config(self):
        """Get storage configuration."""
        return self.config_data.get("storage", {})

# Create a global configuration instance
config = Config()
