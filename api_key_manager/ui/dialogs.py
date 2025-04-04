"""
Dialog classes for the API Key Manager application.
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QPushButton, QDialogButtonBox, QCheckBox
)
from PyQt6.QtCore import Qt

class KeyDialog(QDialog):
    """Base dialog for adding/editing API keys."""
    
    def __init__(self, title, parent=None):
        """Initialize the key dialog."""
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setMinimumWidth(400)
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface."""
        layout = QVBoxLayout(self)
        
        # Name field
        name_layout = QHBoxLayout()
        name_label = QLabel("Name:")
        name_layout.addWidget(name_label)
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Enter a name for this API key")
        name_layout.addWidget(self.name_edit)
        layout.addLayout(name_layout)
        
        # Key field
        key_layout = QHBoxLayout()
        key_label = QLabel("Key:")
        key_layout.addWidget(key_label)
        self.key_edit = QLineEdit()
        self.key_edit.setPlaceholderText("Enter the API key")
        self.key_edit.setEchoMode(QLineEdit.EchoMode.Password)
        key_layout.addWidget(self.key_edit)
        layout.addLayout(key_layout)
        
        # Show key checkbox
        show_key_layout = QHBoxLayout()
        self.show_key_checkbox = QCheckBox("Show Key")
        self.show_key_checkbox.toggled.connect(self.toggle_key_visibility)
        show_key_layout.addWidget(self.show_key_checkbox)
        show_key_layout.addStretch()
        layout.addLayout(show_key_layout)
        
        # Buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
    
    def toggle_key_visibility(self, checked):
        """Toggle between showing and hiding the API key."""
        if checked:
            self.key_edit.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.key_edit.setEchoMode(QLineEdit.EchoMode.Password)
    
    def get_key_data(self):
        """Return the name and key data."""
        return self.name_edit.text().strip(), self.key_edit.text().strip()


class AddKeyDialog(KeyDialog):
    """Dialog for adding a new API key."""
    
    def __init__(self, parent=None):
        """Initialize the add key dialog."""
        super().__init__("Add New API Key", parent)


class EditKeyDialog(KeyDialog):
    """Dialog for editing an existing API key."""
    
    def __init__(self, name, key, parent=None):
        """Initialize the edit key dialog."""
        super().__init__("Edit API Key", parent)
        self.name_edit.setText(name)
        self.key_edit.setText(key)
