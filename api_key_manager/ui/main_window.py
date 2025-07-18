"""
Main window implementation for the API Key Manager application.
"""

import os
import sys
from PyQt6.QtWidgets import (
    QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, 
    QListWidget, QWidget, QInputDialog, QMessageBox, QLineEdit,
    QApplication
)
from PyQt6.QtCore import Qt, QDir
from PyQt6.QtGui import QIcon

from core.key_storage import KeyStorage
from core.config import config
from ui.dialogs import AddKeyDialog, EditKeyDialog

class MainWindow(QMainWindow):
    """Main window of the API Key Manager application."""
    
    def __init__(self):
        """Initialize the main window."""
        super().__init__()
        self.key_storage = KeyStorage()
        self.dark_mode = config.get("window", "dark_mode", False)
        self.init_ui()
        self.load_keys()
        
    def init_ui(self):
        """Initialize the user interface."""
        # Window settings
        window_config = config.get_window_config()
        self.setWindowTitle(window_config.get("title", "API Key Manager"))
        self.setMinimumSize(
            window_config.get("min_width", 500),
            window_config.get("min_height", 400)
        )
        
        # Set window icon with proper path handling for both direct execution and PyInstaller bundle
        build_config = config.get_build_config()
        icon_path = build_config.get("icon_path", os.path.join("resources", "icons", "app_icon.ico"))
        
        # List of possible icon paths to try
        icon_paths = [
            icon_path,                                              # Config specified path
            os.path.join("resources", "icons", "app_icon.ico"),     # Default relative path
            os.path.abspath(icon_path),                             # Absolute path from config
            os.path.abspath(os.path.join("resources", "icons", "app_icon.ico")), # Absolute default path
        ]
        
        # If running from a PyInstaller bundle
        if getattr(sys, 'frozen', False):
            # When running as a bundle, the path is different
            base_path = sys._MEIPASS if hasattr(sys, '_MEIPASS') else os.path.dirname(sys.executable)
            # Add PyInstaller paths
            icon_paths.extend([
                os.path.join(base_path, icon_path),                  # Config path relative to bundle
                os.path.join(base_path, "resources", "icons", "app_icon.ico"), # Default path relative to bundle
            ])
        
        # Try each path until we find a valid icon file
        icon_found = False
        for path in icon_paths:
            if os.path.exists(path):
                try:
                    self.setWindowIcon(QIcon(path))
                    print(f"Window icon set from: {path}")
                    icon_found = True
                    break
                except Exception as e:
                    print(f"Failed to set icon from {path}: {e}")
        
        if not icon_found:
            print("Warning: Could not set window icon, no valid icon file found")
        
        if window_config.get("start_maximized", False):
            self.showMaximized()
        
        # Central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # List widget for API keys
        self.key_list = QListWidget()
        self.key_list.itemClicked.connect(self.copy_key_to_clipboard)
        main_layout.addWidget(self.key_list)
        
        # Search bar
        search_layout = QHBoxLayout()
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search API keys...")
        self.search_box.textChanged.connect(self.filter_keys)
        search_layout.addWidget(self.search_box)
        main_layout.addLayout(search_layout)
        
        # Button layout
        button_layout = QHBoxLayout()
        
        # Dark mode toggle button
        self.dark_mode_button = QPushButton()
        self.dark_mode_button.setObjectName("dark_mode_button")
        self.dark_mode_button.setFixedSize(32, 32)
        self.dark_mode_button.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
            }
            QPushButton:hover {
                background-color: rgba(128, 128, 128, 0.2);
                border-radius: 4px;
            }
        """)
        self.dark_mode_button.clicked.connect(self.toggle_dark_mode)
        self.update_dark_mode_icon()
        button_layout.addWidget(self.dark_mode_button)
        
        # Add key button
        add_button = QPushButton("Add New Key")
        add_button.clicked.connect(self.add_key)
        button_layout.addWidget(add_button)
        
        # Edit key button
        edit_button = QPushButton("Edit Key")
        edit_button.clicked.connect(self.edit_key)
        button_layout.addWidget(edit_button)
        
        # Delete key button
        delete_button = QPushButton("Delete Key")
        delete_button.clicked.connect(self.delete_key)
        button_layout.addWidget(delete_button)
        
        main_layout.addLayout(button_layout)
        
        # Status bar
        self.statusBar().showMessage("Ready")
    
    def toggle_dark_mode(self):
        """Toggle between light and dark mode."""
        self.dark_mode = not self.dark_mode
        config.set("window", "dark_mode", self.dark_mode)
        config.save_config()
        self.update_dark_mode_icon()
        
    def update_dark_mode_icon(self):
        """Update the window and button icons based on dark mode state."""
        # Update application style
        if self.dark_mode:
            self.setStyleSheet("""
                QMainWindow {
                    background-color: #2b2b2b;
                }
                QListWidget {
                    background-color: #3b3b3b;
                    color: #ffffff;
                    border: 1px solid #555555;
                }
                QLineEdit {
                    background-color: #3b3b3b;
                    color: #ffffff;
                    border: 1px solid #555555;
                    padding: 5px;
                }
                QPushButton {
                    background-color: #444444;
                    color: #ffffff;
                    border: 1px solid #555555;
                    padding: 5px 10px;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: #555555;
                }
                QPushButton#dark_mode_button {
                    background: transparent;
                    border: none;
                }
                QPushButton#dark_mode_button:hover {
                    background-color: rgba(128, 128, 128, 0.2);
                }
                QStatusBar {
                    background-color: #2b2b2b;
                    color: #ffffff;
                }
            """)
        else:
            self.setStyleSheet("")

        build_config = config.get_build_config()
        base_icon = "app_icon_dark.ico" if self.dark_mode else "app_icon.ico"
        icon_path = os.path.join("resources", "icons", base_icon)
        
        # List of possible icon paths to try
        icon_paths = [
            icon_path,
            os.path.abspath(icon_path),
            os.path.abspath(os.path.join("resources", "icons", base_icon)),
        ]
        
        # If running from a PyInstaller bundle
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS if hasattr(sys, '_MEIPASS') else os.path.dirname(sys.executable)
            icon_paths.extend([
                os.path.join(base_path, icon_path),
                os.path.join(base_path, "resources", "icons", base_icon),
            ])
        
        # Try each path until we find a valid icon file
        icon_found = False
        for path in icon_paths:
            if os.path.exists(path):
                try:
                    icon = QIcon(path)
                    self.setWindowIcon(icon)
                    self.dark_mode_button.setIcon(icon)
                    self.dark_mode_button.setIconSize(self.dark_mode_button.size())
                    print(f"Icons set from: {path}")
                    icon_found = True
                    break
                except Exception as e:
                    print(f"Failed to set icons from {path}: {e}")
        
        if not icon_found:
            print("Warning: Could not set icons, no valid icon file found")
    
    def load_keys(self):
        """Load stored keys into the list widget."""
        self.key_list.clear()
        keys = self.key_storage.get_all_keys()
        for name in keys:
            self.key_list.addItem(name)
    
    def filter_keys(self, text):
        """Filter the key list based on search text."""
        for i in range(self.key_list.count()):
            item = self.key_list.item(i)
            if text.lower() in item.text().lower():
                item.setHidden(False)
            else:
                item.setHidden(True)
    
    def add_key(self):
        """Open dialog to add a new API key."""
        dialog = AddKeyDialog(self)
        if dialog.exec():
            name, key = dialog.get_key_data()
            if name and key:
                if self.key_storage.add_key(name, key):
                    self.load_keys()
                    self.statusBar().showMessage(f"Key '{name}' added successfully", 3000)
                else:
                    QMessageBox.warning(self, "Error", f"A key with name '{name}' already exists")
    
    def edit_key(self):
        """Edit the selected API key."""
        current_item = self.key_list.currentItem()
        if not current_item:
            QMessageBox.information(self, "Select Key", "Please select a key to edit")
            return
        
        name = current_item.text()
        key = self.key_storage.get_key(name)
        
        dialog = EditKeyDialog(name, key, self)
        if dialog.exec():
            new_name, new_key = dialog.get_key_data()
            if new_name and new_key:
                if name == new_name:
                    # Just updating the key
                    self.key_storage.update_key(name, new_key)
                    self.statusBar().showMessage(f"Key '{name}' updated successfully", 3000)
                else:
                    # Name change, need to delete old and add new
                    if self.key_storage.key_exists(new_name):
                        QMessageBox.warning(self, "Error", f"A key with name '{new_name}' already exists")
                        return
                    
                    self.key_storage.delete_key(name)
                    self.key_storage.add_key(new_name, new_key)
                    self.statusBar().showMessage(f"Key renamed to '{new_name}' and updated successfully", 3000)
                
                self.load_keys()
    
    def delete_key(self):
        """Delete the selected API key."""
        current_item = self.key_list.currentItem()
        if not current_item:
            QMessageBox.information(self, "Select Key", "Please select a key to delete")
            return
        
        name = current_item.text()
        reply = QMessageBox.question(
            self, "Confirm Delete", 
            f"Are you sure you want to delete the key '{name}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.key_storage.delete_key(name)
            self.load_keys()
            self.statusBar().showMessage(f"Key '{name}' deleted successfully", 3000)
    
    def copy_key_to_clipboard(self, item):
        """Copy the selected key to clipboard when clicked."""
        name = item.text()
        key = self.key_storage.get_key(name)
        
        clipboard = QApplication.instance().clipboard()
        clipboard.setText(key)
        
        self.statusBar().showMessage(f"Key '{name}' copied to clipboard", 3000)
