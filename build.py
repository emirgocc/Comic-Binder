import PyInstaller.__main__
import os
import sys

# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Define the icon path with full Windows path
icon_path = os.path.abspath(os.path.join(current_dir, 'icon.ico'))

# Define PyInstaller arguments
args = [
    'cb_gui.py',  # Your main script
    '--name=ComicBinder',  # Name of your executable
    '--onefile',  # Create a single executable
    '--windowed',  # Don't show console window
    '--clean',  # Clean PyInstaller cache
    '--add-data=README.md;.',  # Include README
    '--add-data=LICENSE;.',  # Include LICENSE
    f'--icon={icon_path}',  # Add icon with full path, no quotes
    '--noconfirm',  # Replace existing build
]

# Run PyInstaller
PyInstaller.__main__.run(args) 