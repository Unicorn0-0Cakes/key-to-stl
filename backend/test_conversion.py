#!/usr/bin/env python3
"""
STANDALONE TEST SCRIPT - Key to STL Converter
No web server, no licensing - just pure image-to-STL conversion testing

Usage:
    python test_conversion.py path/to/key_image.jpg
"""

import sys
import cv2
import numpy as np
from stl import mesh
from pathlib import Path

def process_key_image(image_path):
    """Process a key image and generate STL file"""
    print(f"📸 Loading image: {image_path}")
    
    # Read image
    img = cv2.imread(str(image_path))
    if img is None:
        raise ValueError(f"Could not load image: {image_path}")
    
    print(f"✅ Image loaded: {img.shape[1]}x{img.shape[0]} pixels")
    
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Edge detection
    print("🔍 Detecting edges...")
    edges = cv2.Canny(blurred, 50, 150)
    
    # Find contours
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if not contours:
        raise ValueError("No key detected in image")
    
    # Get the largest contour (assumed to be the key)
    key_contour = max(contours, key=cv2.contourArea)
    print(f"✅ Key contour found: {len(key_contour)} points")
    
    # Generate 3D mesh from contour
    print("🏗️  Building 3D mesh...")
    vertices = []
    faces = []
    
    # Key thickness in mm
    thickness = 3.0
    
    # Bottom layer (z=0)
    for point in key_contour:
        x, y = point[0]
        vertices.append([float(x), float(y), 0.0])
    
    # Top layer (z=thickness)
    for point in key_contour:
        x, y = point[0]
        vertices.append([float(x), float(y), thickness])
    
    # Create side faces
    n = len(key_contour)
    for i in range(n):
        v1 = i
        v2 = (i + 1) % n
        v3 = i + n
        v4 = (i + 1) % n + n
        
        # Two triangles per side face
        faces.append([v1, v2, v3])
        faces.append([v2, v4, v3])
    
    # Bottom face (triangulate)
    for i in range(1, n-1):
        faces.append([0, i, i+1])
    
    # Top face (triangulate)
    for i in range(1, n-1):
        faces.append([n, n+i+1, n+i])
    
    # Create STL mesh
    vertices = np.array(vertices)
    faces = np.array(faces)
    
    key_mesh = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
    for i, face in enumerate(faces):
        for j in range(3):
            key_mesh.vectors[i][j] = vertices[face[j]]
    
    print(f"✅ Mesh created: {len(faces)} triangles")
    
    return key_mesh

def save_stl(key_mesh, output_path):
    """Save the mesh to an STL file"""
    print(f"💾 Saving STL to: {output_path}")
    key_mesh.save(str(output_path))
    file_size = Path(output_path).stat().st_size
    print(f"✅ STL file saved: {file_size:,} bytes")

def main():
    if len(sys.argv) < 2:
        print("Usage: python test_conversion.py <image_path>")
        print("Example: python test_conversion.py key_photo.jpg")
        sys.exit(1)
    
    image_path = sys.argv[1]
    
    print("="*60)
    print("🔑 KEY TO STL CONVERSION TEST")
    print("="*60)
    
    try:
        # Process the image
        key_mesh = process_key_image(image_path)
        
        # Generate output filename
        input_name = Path(image_path).stem
        output_path = f"{input_name}_key.stl"
        
        # Save the STL
        save_stl(key_mesh, output_path)
        
        print("\n" + "="*60)
        print("🎉 SUCCESS! Your key has been converted to STL")
        print(f"📁 Output file: {output_path}")
        print("="*60)
        print("\nYou can now:")
        print("  1. Open the STL in a 3D viewer (like MeshLab or Blender)")
        print("  2. Import it into your 3D printing slicer")
        print("  3. Print your key!")
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
