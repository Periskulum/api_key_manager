"""
Script to build a standalone executable for the API Key Manager.
"""

import os
import subprocess
import sys
import platform
import shutil
import importlib.util
from core.config import config

def ensure_pyinstaller_installed():
    """Check if PyInstaller is installed, install if not."""
    if importlib.util.find_spec("PyInstaller") is None:
        print("PyInstaller not found. Installing...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
            print("PyInstaller installed successfully!")
        except subprocess.CalledProcessError as e:
            print(f"Failed to install PyInstaller: {e}", file=sys.stderr)
            return False
    return True

def main():
    """Build the executable using PyInstaller."""
    # Ensure PyInstaller is installed
    if not ensure_pyinstaller_installed():
        print("Cannot proceed without PyInstaller. Exiting.", file=sys.stderr)
        return 1
    
    # Get build configuration
    build_config = config.get_build_config()
    
    # Determine icon path
    icon_option = []
    icon_path = build_config.get("icon_path")
    
    # Validate icon path
    if icon_path and os.path.exists(icon_path):
        abs_icon_path = os.path.abspath(icon_path)
        icon_option = ["--icon", abs_icon_path]
        print(f"Using icon: {abs_icon_path}")
    # Default platform-specific icon if configured path doesn't exist
    elif not icon_path:
        if platform.system() == "Windows":
            default_icon = os.path.join("resources", "icons", "app_icon.ico")
            if os.path.exists(default_icon):
                abs_icon_path = os.path.abspath(default_icon)
                icon_option = ["--icon", abs_icon_path]
                print(f"Using default Windows icon: {abs_icon_path}")
        elif platform.system() == "Darwin":  # macOS
            default_icon = os.path.join("resources", "icons", "app_icon.icns")
            if os.path.exists(default_icon):
                abs_icon_path = os.path.abspath(default_icon)
                icon_option = ["--icon", abs_icon_path]
                print(f"Using default macOS icon: {abs_icon_path}")
    
    # Determine if one-file mode should be used
    one_file_option = ["--onefile"] if build_config.get("one_file", True) else ["--onedir"]
    
    # Prepare data files to include
    data_files = [
        ("config.json", "."),
        ("resources", "resources")
    ]
    
    data_options = []
    for src, dst in data_files:
        data_options.extend(["--add-data", f"{src}{os.pathsep}{dst}"])
    
    # Determine if one-file mode should be used
    one_file_option = ["--onefile"] if build_config.get("one_file", True) else ["--onedir"]
    
    # PyInstaller command with all options
    executable_name = build_config.get("executable_name", "API Key Manager")
    pyinstaller_cmd = [
        sys.executable, "-m", "PyInstaller",
        f"--name={executable_name}",
        "--windowed",
        *one_file_option,
        *icon_option,
        "--clean",
        "--distpath=./dist",
        "--workpath=./build",
        *data_options,
        "main.py"
    ]
    
    print("Running PyInstaller with the following command:")
    print(" ".join(pyinstaller_cmd))
    
    # Run PyInstaller
    try:
        subprocess.run(pyinstaller_cmd, check=True)
        print("Build completed successfully!")
        
        # Show output location
        output_dir = os.path.abspath("dist")
        executable_name = build_config.get("executable_name", "API Key Manager")
        if platform.system() == "Windows":
            output_file = os.path.join(output_dir, f"{executable_name}.exe")
        elif platform.system() == "Darwin":
            output_file = os.path.join(output_dir, f"{executable_name}.app")
        else:
            output_file = os.path.join(output_dir, executable_name)
            
        print(f"Executable created at: {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Build failed: {e}", file=sys.stderr)
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
