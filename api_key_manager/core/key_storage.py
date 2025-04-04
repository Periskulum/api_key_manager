"""
Secure storage for API keys using the system keyring.
"""

import keyring
import json
import os
from core.config import config

class KeyStorage:
    """Handle secure API key storage using the system keyring."""
    
    def __init__(self):
        """Initialize the key storage."""
        # Get storage configuration
        storage_config = config.get_storage_config()
        
        # Service name for keyring entries (used as a prefix for all stored keys)
        self.SERVICE_NAME = storage_config.get("service_name", "APIKeyManager")
        # Special key name for the index of all stored keys
        self.INDEX_KEY = storage_config.get("index_key", "__key_index__")
        
        self.ensure_index_exists()
    
    
    def ensure_index_exists(self):
        """Ensure the key index exists in the keyring."""
        index = self.get_key_index()
        if index is None:
            self.set_key_index([])
    
    def get_key_index(self):
        """Get the index of all stored key names."""
        index_json = keyring.get_password(self.SERVICE_NAME, self.INDEX_KEY)
        if index_json:
            try:
                return json.loads(index_json)
            except json.JSONDecodeError:
                return []
        return []
    
    def set_key_index(self, names):
        """Set the index of all stored key names."""
        keyring.set_password(self.SERVICE_NAME, self.INDEX_KEY, json.dumps(names))
    
    def get_all_keys(self):
        """Get all stored key names."""
        return self.get_key_index()
    
    def get_key(self, name):
        """Get a specific API key by name."""
        return keyring.get_password(self.SERVICE_NAME, name)
    
    def add_key(self, name, key):
        """Add a new API key.
        
        Returns:
            bool: True if key was added, False if the key name already exists
        """
        # Check if key already exists
        if self.key_exists(name):
            return False
        
        # Add to index
        index = self.get_key_index()
        index.append(name)
        self.set_key_index(index)
        
        # Store key
        keyring.set_password(self.SERVICE_NAME, name, key)
        return True
    
    def update_key(self, name, new_key):
        """Update an existing API key's value."""
        if not self.key_exists(name):
            return False
        
        keyring.set_password(self.SERVICE_NAME, name, new_key)
        return True
    
    def delete_key(self, name):
        """Delete an API key."""
        if not self.key_exists(name):
            return False
        
        # Remove from index
        index = self.get_key_index()
        index.remove(name)
        self.set_key_index(index)
        
        # Delete from keyring
        keyring.delete_password(self.SERVICE_NAME, name)
        return True
    
    def key_exists(self, name):
        """Check if a key with the given name exists."""
        return name in self.get_key_index()
