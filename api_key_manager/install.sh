#!/bin/bash

echo "==================================="
echo "API Key Manager - Installation"
echo "==================================="
echo

echo "Installing dependencies..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "Failed to install dependencies!"
    echo "Please make sure pip is installed and you have internet access."
    echo "On some systems, you may need to use pip3 instead of pip."
    read -p "Press Enter to exit..."
    exit 1
fi

echo
echo "Dependencies installed successfully!"
echo
echo "==================================="
echo "You can now:"
echo
echo "1. Run the application:"
echo "   python main.py"
echo
echo "2. Build the executable:"
echo "   python build_exe.py"
echo
echo "3. Configure the application in config.json"
echo "==================================="
echo

read -p "Press Enter to exit..."
