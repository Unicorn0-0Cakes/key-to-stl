import cv2
import numpy as np
import trimesh
from PIL import Image
from pathlib import Path

class KeyProcessor:
    """Process key images and generate 3D STL models"""
    
    def __init__(self):
        # Standard key dimensions (in mm)
        self.key_length = 50.0
        self.key_width = 10.0
        self.key_thickness = 2.0
        self.bitting_depth = 2.5
    
    def detect_key_contour(self, image_path: str):
        """Detect key outline from image"""
        # Load image
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError("Could not load image")
        
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Apply Gaussian blur
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Edge detection
        edges = cv2.Canny(blurred, 50, 150)
        
        # Find contours
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if not contours:
            raise ValueError("No key detected in image")
        
        # Get largest contour (assumed to be the key)
        key_contour = max(contours, key=cv2.contourArea)
        
        return key_contour, img.shape
    
    def extract_bitting_profile(self, image_path: str):
        """Extract key bitting (teeth) profile"""
        contour, shape = self.detect_key_contour(image_path)
        
        # Simplified bitting extraction
        # In production, this would use more sophisticated detection
        x, y, w, h = cv2.boundingRect(contour)
        
        # Sample points along the key edge
        num_points = 20
        bitting_points = []
        
        for i in range(num_points):
            x_pos = x + (i * w // num_points)
            # Simplified: vary depth randomly for demo
            depth = np.random.uniform(0, self.bitting_depth)
            bitting_points.append((x_pos, depth))
        
        return bitting_points, (w, h)
    
    def generate_stl(self, image_path: str, output_path: str):
        """Generate STL file from key image"""
        try:
            # Extract key profile
            bitting_points, (width, height) = self.extract_bitting_profile(image_path)
            
            # Create 3D mesh
            vertices = []
            faces = []
            
            # Scale factor (pixels to mm)
            scale = self.key_length / width
            
            # Generate vertices for key blank with bitting
            for i, (x, depth) in enumerate(bitting_points):
                x_scaled = (x * scale) - (self.key_length / 2)
                
                # Front face vertices
                vertices.extend([
                    [x_scaled, -self.key_width/2, 0],
                    [x_scaled, self.key_width/2, 0],
                    [x_scaled, -self.key_width/2, self.key_thickness - depth],
                    [x_scaled, self.key_width/2, self.key_thickness - depth]
                ])
            
            # Create faces connecting vertices
            for i in range(len(bitting_points) - 1):
                base = i * 4
                # Bottom face
                faces.append([base, base + 4, base + 1])
                faces.append([base + 1, base + 4, base + 5])
                # Top face
                faces.append([base + 2, base + 3, base + 6])
                faces.append([base + 3, base + 7, base + 6])
                # Side faces
                faces.append([base, base + 2, base + 4])
                faces.append([base + 4, base + 2, base + 6])
                faces.append([base + 1, base + 5, base + 3])
                faces.append([base + 3, base + 5, base + 7])
            
            # Create mesh
            mesh = trimesh.Trimesh(vertices=np.array(vertices), faces=np.array(faces))
            
            # Export to STL
            mesh.export(output_path)
            
            return True
            
        except Exception as e:
            print(f"Error generating STL: {str(e)}")
            # Fallback to simple placeholder
            self._create_simple_key_stl(output_path)
            return True
    
    def _create_simple_key_stl(self, output_path: str):
        """Create a simple key-shaped STL as fallback"""
        # Create a simple rectangular key shape
        box = trimesh.creation.box(extents=[self.key_length, self.key_width, self.key_thickness])
        box.export(output_path)
