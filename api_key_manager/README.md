# API Key Manager

A desktop application to securely store API keys and quickly copy them to the clipboard.

## Features

- Securely store API keys using your system's credential manager
- Display only key names in the UI for enhanced security
- Copy keys to clipboard with a single click
- Add, edit, and delete API keys
- Search functionality to quickly find keys
- Cross-platform support (Windows, macOS, Linux)

## Getting Started

### Prerequisites

- Python 3.7+
- pip (Python package manager)

### Running with Python

The application can run directly with Python after installing the required dependencies:

1. Clone or download this repository
2. Navigate to the api_key_manager directory:
   ```bash
   cd api_key_manager
   ```
3. Install dependencies using one of the following methods:

   **Option A: Using installation scripts**
   - On Windows: Double-click `install.bat` or run it from command prompt
   - On Linux/macOS:
     ```bash
     chmod +x install.sh
     ./install.sh
     ```

   **Option B: Manual installation**
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   python main.py
   ```

### Building a Standalone Executable

You can create a standalone executable that runs without requiring Python to be installed:

1. Navigate to the api_key_manager directory:
   ```bash
   cd api_key_manager
   ```
2. Install dependencies (if not done already):
   ```bash
   pip install -r requirements.txt
   ```
3. Run the build script:
   ```bash
   python build_exe.py
   ```
4. Once completed, find the executable in the `dist` folder
   - Windows: `dist/API Key Manager.exe`
   - macOS: `dist/API Key Manager.app`
   - Linux: `dist/API Key Manager`

The standalone executable includes all necessary dependencies and can be moved to any location on your system.

## Configuration

The application can be customized through the `config.json` file located in the application directory. The following settings can be configured:

```json
{
  "app_name": "API Key Manager",         // Application name
  "organization": "APIKeyManager",       // Organization name for system storage

  "window": {
    "title": "API Key Manager",          // Window title
    "min_width": 265,                    // Minimum window width
    "min_height": 400,                   // Minimum window height
    "start_maximized": false             // Whether to start maximized
  },

  "build": {
    "executable_name": "API Key Manager", // Name of the executable
    "icon_path": "resources/icons/app_icon.ico", // Path to application icon
    "one_file": true                     // Whether to build as a single file
  },

  "storage": {
    "service_name": "APIKeyManager",     // Service name for keyring storage
    "index_key": "__key_index__"         // Key name for the index of stored keys
  }
}
```

## Usage

1. Start the application
2. To add a new key:
   - Click the "Add New Key" button
   - Enter a name for the API key and the key value
   - Click OK to save
3. To copy a key to clipboard:
   - Click on the key name in the list
   - A confirmation message will appear in the status bar
4. To edit a key:
   - Select the key from the list
   - Click the "Edit Key" button
   - Update the name and/or key value
   - Click OK to save
5. To delete a key:
   - Select the key from the list
   - Click the "Delete Key" button
   - Confirm deletion when prompted

## Security

This application uses the system's secure credential storage:
- Windows: Windows Credential Locker
- macOS: Keychain
- Linux: Secret Service API/libsecret

API keys are never stored in plain text on disk. The application only displays key names in the UI, not the actual key values, to prevent shoulder surfing.

## License

MIT License
