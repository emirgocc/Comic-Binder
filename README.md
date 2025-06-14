# Comic Binder

<div align="center">
  <img src="icon.png" alt="Comic Binder Logo" width="128" height="128">
  <br>
  <p><em>A user-friendly GUI application for merging multiple comic book archives (CBZ/CBR) into a single CBZ file with a custom cover image.</em></p>
</div>

---

## 🗂️ Why Comic Binder?

If you're a digital comic collector, you've probably found yourself juggling scattered `.cbz` or `.cbr` files — separate issues, tie-ins, minis, or collected events split across folders. **Comic Binder** helps you organize your collection more like a bookshelf:

- 📚 Group a miniseries into a single digital volume.
- 🧩 Merge event tie-ins in the proper reading order.
- 🖼️ Add a proper cover image so your archive looks like a real collected edition.

**In short:** Comic Binder helps you treat your digital comics like a curated library, not a pile of files.

---

## Features

- 🖼️ Merge multiple CBZ/CBR files into a single CBZ archive
- 🎨 Add custom cover image to your comic book
- 📱 Modern and intuitive user interface
- 🔄 Drag and drop support for adding files
- ⬆️⬇️ Easy file reordering with up/down buttons
- 🗑️ Quick file removal from the list
- 🎯 Automatic file sorting and validation
- 🛡️ Error handling for corrupted files

## Requirements

- Python 3.6 or higher
- Required Python packages:
  - `Pillow` (PIL)
  - `tkinterdnd2`
  - `rarfile`
  - `unrar` (system dependency for RAR support)

## Installation

### Option 1: Using the Executable (Windows)

1. Download the latest `ComicBinder.exe` from the [Releases](https://github.com/emirgocc/Comic-Binder/releases/) page
2. Run the executable directly - no installation required

### Option 2: Building from Source

1. Clone the repository:
```bash
git clone https://github.com/emirgocc/comic-binder.git
cd comic-binder
```

2. Install the required Python packages:
```bash
pip install -r requirements.txt
```

3. Install system dependencies:

For Windows:
- Download and install UnRAR from [RARLab](https://www.rarlab.com/rar_add.htm)

For Linux:
```bash
sudo apt-get install unrar  # Debian/Ubuntu
sudo yum install unrar      # CentOS/RHEL
```

For macOS:
```bash
brew install unrar
```

4. Build the executable:
```bash
python build.py
```

The executable will be created in the `dist` folder.

## Usage

1. Run the application:
   - Double-click `ComicBinder.exe` (Windows)
   - Or run `python cb_gui.py` (from source)

2. Add your comic files:
   - Click the "+ Add Files" button
   - Or drag and drop CBZ/CBR files into the application

3. Select a cover image:
   - Click "Select Cover Image"
   - Choose a JPG/PNG image file

4. Reorder files if needed:
   - Use the up/down arrows to change file order
   - Remove files using the "×" button

5. Create the merged CBZ:
   - Click "Merge as CBZ"
   - Choose the output location and filename
   - Wait for the process to complete

## Supported File Formats

- Input:
  - CBZ (Comic Book ZIP)
  - CBR (Comic Book RAR)
- Output:
  - CBZ (Comic Book ZIP)
- Cover Image:
  - JPG/JPEG
  - PNG

## Error Handling

The application includes robust error handling:
- Skips corrupted files during processing
- Validates image files before adding
- Provides clear error messages
- Cleans up temporary files automatically

## Building from Source

To build the executable from source:

1. Install all requirements:
```bash
pip install -r requirements.txt
```

2. Run the build script:
```bash
python build.py
```

3. Find the executable in the `dist` folder

Note: Building requires PyInstaller and all dependencies to be installed.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thanks to all contributors and users
- Built with Python and Tkinter
- Uses [tkinterdnd2](https://github.com/pmgagne/tkinterdnd2) for drag and drop support 