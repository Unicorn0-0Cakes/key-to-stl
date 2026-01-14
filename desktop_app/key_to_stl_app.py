import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import requests
import json
import os
from pathlib import Path
from PIL import Image, ImageTk
import cv2
import numpy as np
from stl import mesh
import uuid
import hashlib

class KeygenLicenseManager:
    def __init__(self):
        self.account_id = "b7ebf59e-18f0-46b0-8a95-e97af6281bdd"
        self.api_key = "prod-27Xxxxxxxxxxxxxxxxxxxx"  # Replace with actual key
        self.policy_id = "e85d12e1-2785-4b5d-8c1d-992d63a2d606"
        self.base_url = "https://api.keygen.sh/v1/accounts/{}".format(self.account_id)
        self.license_file = Path.home() / ".key_to_stl_license"
        
    def validate_license(self, license_key):
        """Validate a license key with Keygen API"""
        try:
            headers = {
                "Accept": "application/vnd.api+json",
                "Content-Type": "application/vnd.api+json"
            }
            
            data = {
                "meta": {
                    "scope": {"fingerprint": self.get_machine_fingerprint()}
                }
            }
            
            response = requests.post(
                f"{self.base_url}/licenses/{license_key}/actions/validate",
                headers=headers,
                json=data,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("meta", {}).get("valid", False):
                    self.save_license(license_key)
                    return True, "License activated successfully!"
            
            return False, "Invalid license key"
        except Exception as e:
            return False, f"License validation error: {str(e)}"
    
    def get_machine_fingerprint(self):
        """Generate unique machine fingerprint"""
        machine_id = str(uuid.getnode())
        return hashlib.sha256(machine_id.encode()).hexdigest()
    
    def save_license(self, license_key):
        """Save license key locally"""
        try:
            with open(self.license_file, 'w') as f:
                f.write(license_key)
        except Exception as e:
            print(f"Error saving license: {e}")
    
    def load_license(self):
        """Load saved license key"""
        if self.license_file.exists():
            try:
                with open(self.license_file, 'r') as f:
                    return f.read().strip()
            except Exception as e:
                print(f"Error loading license: {e}")
        return None

class PhotoToSTLConverter:
    def __init__(self):
        self.image_path = None
        self.processed_image = None
        
    def load_image(self, file_path):
        """Load and validate image file"""
        try:
            self.image_path = file_path
            img = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
            if img is None:
                raise ValueError("Could not load image")
            self.processed_image = img
            return True, "Image loaded successfully"
        except Exception as e:
            return False, f"Error loading image: {str(e)}"
    
    def process_image(self, threshold=128, depth=5):
        """Process image to extract key profile"""
        if self.processed_image is None:
            return False, "No image loaded"
        
        try:
            # Apply threshold
            _, binary = cv2.threshold(self.processed_image, threshold, 255, cv2.THRESH_BINARY)
            
            # Find contours
            contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            if not contours:
                return False, "No key detected in image"
            
            # Get largest contour (assumed to be the key)
            main_contour = max(contours, key=cv2.contourArea)
            
            return True, "Image processed successfully"
        except Exception as e:
            return False, f"Processing error: {str(e)}"
    
    def generate_stl(self, output_path, depth=5):
        """Generate STL file from processed image"""
        if self.processed_image is None:
            return False, "No image to convert"
        
        try:
            h, w = self.processed_image.shape
            
            # Create simplified mesh
            vertices = []
            faces = []
            
            # Sample points from image
            step = 10
            for y in range(0, h, step):
                for x in range(0, w, step):
                    z = (self.processed_image[y, x] / 255.0) * depth
                    vertices.append([x, y, z])
                    vertices.append([x, y, 0])  # Bottom face
            
            # Create simple face structure
            vertices = np.array(vertices)
            num_vertices = len(vertices)
            
            # Create a simple mesh
            stl_mesh = mesh.Mesh(np.zeros(num_vertices // 3, dtype=mesh.Mesh.dtype))
            
            for i, vertex in enumerate(vertices[:num_vertices // 3]):
                stl_mesh.vectors[i] = vertices[i*3:(i+1)*3]
            
            stl_mesh.save(output_path)
            return True, f"STL file saved to {output_path}"
        except Exception as e:
            return False, f"STL generation error: {str(e)}"

class KeyToSTLApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Key to STL Converter")
        self.root.geometry("800x600")
        
        self.license_manager = KeygenLicenseManager()
        self.converter = PhotoToSTLConverter()
        
        # Check for existing license
        saved_license = self.license_manager.load_license()
        if saved_license:
            valid, msg = self.license_manager.validate_license(saved_license)
            if valid:
                self.show_main_app()
            else:
                self.show_license_screen()
        else:
            self.show_license_screen()
    
    def show_license_screen(self):
        """Display license activation screen"""
        for widget in self.root.winfo_children():
            widget.destroy()
        
        frame = ttk.Frame(self.root, padding="20")
        frame.pack(expand=True, fill="both")
        
        ttk.Label(frame, text="Key to STL Converter", font=("Arial", 24, "bold")).pack(pady=20)
        ttk.Label(frame, text="Enter your license key to activate", font=("Arial", 12)).pack(pady=10)
        
        self.license_entry = ttk.Entry(frame, width=50, font=("Arial", 11))
        self.license_entry.pack(pady=10)
        
        ttk.Button(frame, text="Activate License", command=self.activate_license).pack(pady=10)
        
        ttk.Label(frame, text="Don't have a license?", font=("Arial", 10)).pack(pady=20)
        ttk.Label(frame, text="Visit: https://yourwebsite.com/purchase", font=("Arial", 10)).pack()
    
    def activate_license(self):
        """Activate license key"""
        license_key = self.license_entry.get().strip()
        if not license_key:
            messagebox.showerror("Error", "Please enter a license key")
            return
        
        valid, msg = self.license_manager.validate_license(license_key)
        if valid:
            messagebox.showinfo("Success", msg)
            self.show_main_app()
        else:
            messagebox.showerror("Error", msg)
    
    def show_main_app(self):
        """Display main application interface"""
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Menu bar
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open Image", command=self.load_image)
        file_menu.add_command(label="Export STL", command=self.export_stl)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(expand=True, fill="both")
        
        # Title
        ttk.Label(main_frame, text="Key to STL Converter", font=("Arial", 18, "bold")).pack(pady=10)
        
        # Image display
        self.canvas = tk.Canvas(main_frame, width=600, height=400, bg="#f0f0f0")
        self.canvas.pack(pady=10)
        
        # Controls
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(pady=10)
        
        ttk.Button(control_frame, text="Load Image", command=self.load_image).pack(side="left", padx=5)
        ttk.Button(control_frame, text="Process", command=self.process_image).pack(side="left", padx=5)
        ttk.Button(control_frame, text="Export STL", command=self.export_stl).pack(side="left", padx=5)
        
        # Status
        self.status_label = ttk.Label(main_frame, text="Ready", font=("Arial", 10))
        self.status_label.pack(pady=10)
    
    def load_image(self):
        """Load image file"""
        file_path = filedialog.askopenfilename(
            title="Select Key Image",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")]
        )
        
        if file_path:
            success, msg = self.converter.load_image(file_path)
            if success:
                self.display_image(file_path)
                self.status_label.config(text=msg)
            else:
                messagebox.showerror("Error", msg)
    
    def display_image(self, file_path):
        """Display loaded image on canvas"""
        try:
            img = Image.open(file_path)
            img.thumbnail((600, 400))
            self.photo = ImageTk.PhotoImage(img)
            self.canvas.create_image(300, 200, image=self.photo)
        except Exception as e:
            print(f"Display error: {e}")
    
    def process_image(self):
        """Process loaded image"""
        success, msg = self.converter.process_image()
        if success:
            self.status_label.config(text=msg)
            messagebox.showinfo("Success", msg)
        else:
            messagebox.showerror("Error", msg)
    
    def export_stl(self):
        """Export STL file"""
        file_path = filedialog.asksaveasfilename(
            title="Save STL File",
            defaultextension=".stl",
            filetypes=[("STL files", "*.stl")]
        )
        
        if file_path:
            success, msg = self.converter.generate_stl(file_path)
            if success:
                self.status_label.config(text=msg)
                messagebox.showinfo("Success", msg)
            else:
                messagebox.showerror("Error", msg)

if __name__ == "__main__":
    root = tk.Tk()
    app = KeyToSTLApp(root)
    root.mainloop()
