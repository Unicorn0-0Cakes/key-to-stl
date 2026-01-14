"""Setup script for building Key to STL Desktop Application executable."""

from cx_Freeze import setup, Executable
import sys

# Dependencies are automatically detected, but some modules need help
build_exe_options = {
    "packages": [
        "tkinter",
        "requests",
        "PIL",
        "cv2",
        "numpy",
        "stl",
        "uuid",
        "hashlib",
        "pathlib",
        "json",
        "os"
    ],
    "include_files": [],
    "excludes": ["matplotlib", "scipy"],
}

# Base for GUI applications (hides console window)
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="KeyToSTL",
    version="1.0.0",
    description="Convert key photos to 3D printable STL files",
    author="Your Name",
    options={"build_exe": build_exe_options},
    executables=[
        Executable(
            "key_to_stl_app.py",
            base=base,
            target_name="KeyToSTL",
            icon=None  # Add your .ico file path here if you have one
        )
    ],
)
