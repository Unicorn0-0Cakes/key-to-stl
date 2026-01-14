# Key to STL Desktop Application

A Python desktop application for converting key photographs into 3D printable STL files with Keygen license management.

## Features

- 🔑 **Photo to STL Conversion**: Upload a key photo and convert it to a 3D printable STL file
- 🔐 **Keygen License Integration**: Secure license validation and management
- 🖥️ **User-Friendly GUI**: Built with tkinter for cross-platform compatibility
- 📸 **Image Processing**: Advanced OpenCV processing for accurate key profiles
- 💾 **Local License Storage**: License keys are saved locally for convenience

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Operating System: Windows, macOS, or Linux

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Unicorn0-0Cakes/key-to-stl.git
cd key-to-stl/desktop_app
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure API Key

Open `key_to_stl_app.py` and replace the placeholder API key:

```python
self.api_key = "prod-27Xxxxxxxxxxxxxxxxxxxx"  # Replace with actual key
```

## Usage

### Running the Application

```bash
python key_to_stl_app.py
```

### First Launch - License Activation

1. When you first run the application, you'll see the license activation screen
2. Enter your license key (obtained from your purchase)
3. Click "Activate License"
4. If valid, you'll be taken to the main application

### Converting a Key to STL

1. **Load Image**: Click "Load Image" or use File → Open Image
2. Select a clear photo of your key
3. **Process**: Click "Process" to extract the key profile
4. **Export**: Click "Export STL" or use File → Export STL
5. Choose your save location and filename
6. Your STL file is ready for 3D printing!

## Building an Executable

### Using PyInstaller (Recommended)

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name="KeyToSTL" key_to_stl_app.py
```

The executable will be in the `dist/` folder.

### Using cx_Freeze

```bash
pip install cx_Freeze
python setup.py build
```

## License Management

### How Licensing Works

- Each license key is validated against Keygen servers
- Machine fingerprinting ensures licenses are tied to specific devices
- License keys are stored locally in `~/.key_to_stl_license`
- Licenses are validated on startup

### Obtaining a License

Visit [your website] to purchase a license key.

### Trial Licenses

Trial licenses are available through the Keygen policy configuration.

## Troubleshooting

### "Invalid license key" Error

- Verify your license key is correct
- Check your internet connection
- Ensure the license hasn't expired

### "Could not load image" Error

- Make sure the image file is a supported format (JPG, PNG, BMP)
- Check that the file isn't corrupted

### "No key detected in image" Error

- Ensure the key is clearly visible in the photo
- Try adjusting the lighting and contrast
- Use a plain background

### OpenCV Installation Issues

If you have trouble installing opencv-python, try:

```bash
pip install opencv-python-headless
```

## Development

### Project Structure

```
desktop_app/
├── key_to_stl_app.py      # Main application
├── requirements.txt        # Dependencies
└── README.md              # This file
```

### Key Classes

- **KeygenLicenseManager**: Handles license validation and storage
- **PhotoToSTLConverter**: Processes images and generates STL files
- **KeyToSTLApp**: Main GUI application

## API Configuration

### Keygen Account Details

- **Account ID**: `b7ebf59e-18f0-46b0-8a95-e97af6281bdd`
- **Policy ID**: `e85d12e1-2785-4b5d-8c1d-992d63a2d606`

Replace the API key in the source code with your production key from Keygen.

## Support

For issues or questions:
- GitHub Issues: [https://github.com/Unicorn0-0Cakes/key-to-stl/issues](https://github.com/Unicorn0-0Cakes/key-to-stl/issues)
- Email: support@yourwebsite.com

## License

This software is protected by copyright and requires a valid license key to operate.

## Acknowledgments

- Keygen.sh for license management
- OpenCV for image processing
- numpy-stl for STL generation
