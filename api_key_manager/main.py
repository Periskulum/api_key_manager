#!/usr/bin/env python3
"""
API Key Manager

A desktop application to securely store and manage API keys with quick copy-to-clipboard functionality.
"""

import sys
from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow
from core.config import config

def main():
    """Main entry point for the application."""
    app = QApplication(sys.argv)
    app.setApplicationName(config.get_app_name())
    app.setOrganizationName(config.get("organization", default="APIKeyManager"))
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
