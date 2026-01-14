# Building Desktop App Releases

This guide explains how to build executable releases for the Key to STL desktop application.

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- PyInstaller (for creating executables)

## Installation

```bash
cd desktop_app
pip install -r requirements.txt
pip install pyinstaller
```

## Building Executables

### Windows (.exe)

```bash
pyinstaller --onefile --windowed --name="KeyToSTL" \
    --icon=icon.ico \
    --add-data="assets;assets" \
    key_to_stl_app.py
```

Output: `dist/KeyToSTL.exe`

### macOS (.app)

```bash
pyinstaller --onefile --windowed --name="KeyToSTL" \
    --icon=icon.icns \
    --add-data="assets:assets" \
    --osx-bundle-identifier="com.keytostl.app" \
    key_to_stl_app.py
```

To create DMG:
```bash
hdiutil create -volname "Key to STL" -srcfolder dist/KeyToSTL.app -ov -format UDZO KeyToSTL-macOS.dmg
```

Output: `KeyToSTL-macOS.dmg`

### Linux (AppImage)

```bash
pyinstaller --onefile --name="KeyToSTL" key_to_stl_app.py

# Convert to AppImage using appimagetool
wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage
chmod +x appimagetool-x86_64.AppImage

# Create AppDir structure
mkdir -p KeyToSTL.AppDir/usr/bin
cp dist/KeyToSTL KeyToSTL.AppDir/usr/bin/

# Create desktop file
cat > KeyToSTL.AppDir/KeyToSTL.desktop << EOF
[Desktop Entry]
Name=Key to STL
Exec=KeyToSTL
Icon=keytostl
Type=Application
Categories=Graphics;
EOF

# Build AppImage
./appimagetool-x86_64.AppImage KeyToSTL.AppDir KeyToSTL-Linux.AppImage
```

Output: `KeyToSTL-Linux.AppImage`

## Creating GitHub Release

1. **Tag your release:**
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```

2. **Go to GitHub Releases:**
   - Navigate to: https://github.com/Unicorn0-0Cakes/key-to-stl/releases/new
   - Select your tag (v1.0.0)
   - Title: "Key to STL v1.0.0"
   - Description:
     ```markdown
     ## 🚀 Key to STL v1.0.0
     
     Convert photos of physical keys into 3D printable STL files.
     
     ### ✨ Features
     - ✅ 7-Day Free Trial (License: A16OBC-078EAA-5D)
     - 🖼️ Photo to STL conversion
     - 🔒 Keygen license integration
     - ⚡ Fast processing (5-15 seconds)
     
     ### 💾 Downloads
     Choose your platform below:
     ```

3. **Upload your files:**
   - `KeyToSTL-Windows.exe`
   - `KeyToSTL-macOS.dmg`
   - `KeyToSTL-Linux.AppImage`

4. **Publish release**

## Trial License Information

**Built-in 7-Day Trial:**
- License Key: `A16OBC-078EAA-5D`
- Duration: 7 days from first activation
- No credit card required
- Full feature access

## Developer Testing

For development/testing, create a permanent license at:
https://app.keygen.sh/licenses/new

- Select "Premium License" policy (no expiration)
- Name it "Developer Test License"
- Use this key in your local testing

## Troubleshooting

### Missing Dependencies
If PyInstaller can't find modules:
```bash
pyinstaller --hidden-import=tkinter --hidden-import=PIL --hidden-import=cv2 --hidden-import=numpy --hidden-import=stl key_to_stl_app.py
```

### Icon Not Showing
Ensure you have icon files:
- Windows: `icon.ico`
- macOS: `icon.icns`
- Linux: `icon.png`

### Large File Size
To reduce executable size:
```bash
pyinstaller --onefile --windowed --strip --exclude-module matplotlib --exclude-module scipy key_to_stl_app.py
```

## Notes

- The landing page download links point to: `https://github.com/Unicorn0-0Cakes/key-to-stl/releases/latest/download/[filename]`
- This automatically serves the latest release
- Update version numbers in both the app code and release tags
- Test each platform build before publishing
