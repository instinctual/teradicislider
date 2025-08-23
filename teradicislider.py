import tkinter as tk
from tkinter import messagebox
import subprocess
import os

class PCoIPImageQualityApp:
    def __init__(self, root, config_file="/etc/pcoip-agent/pcoip-agent.conf"):
        self.root = root
        self.config_file = config_file
        self.root.title("Teradici Quality")
        
        # Set window to always stay on top
        self.root.attributes('-topmost', True)
        
        # Check if crudini is installed
        if not self.check_crudini():
            messagebox.showerror("Error", "crudini is not installed. Please install it using 'sudo dnf install crudini'.")
            self.root.destroy()
            return
        
        # Check if config file exists
        if not os.path.exists(self.config_file):
            messagebox.showerror("Error", f"Configuration file {self.config_file} not found.")
            self.root.destroy()
            return
        
        # Get initial value
        self.current_quality = self.get_current_quality()
        
        # Create and configure the slider
        self.slider = tk.Scale(
            root,
            from_=0,
            to=100,
            orient=tk.HORIZONTAL,
            length=300,
            width=30,  # Increase track thickness for taller appearance
            sliderlength=60,  # Increase handle size
            resolution=1,
            command=self.update_quality
        )
        self.slider.set(self.current_quality)
        self.slider.pack(pady=10)
        
        # Create a frame for buttons
        self.button_frame = tk.Frame(root)
        self.button_frame.pack(pady=10)
        
        # Default button
        self.default_button = tk.Button(
            self.button_frame,
            text="Default",
            font=("Helvetica", 12),
            command=self.set_default_quality
        )
        self.default_button.pack(side=tk.LEFT, padx=5)
        
        # Exit button
        self.exit_button = tk.Button(
            self.button_frame,
            text="Exit",
            font=("Helvetica", 12),
            command=self.root.destroy
        )
        self.exit_button.pack(side=tk.LEFT, padx=5)
        
    def check_crudini(self):
        try:
            subprocess.run(["crudini", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
    
    def get_current_quality(self):
        try:
            # If your config file has a section header like [pcoip], replace '' with 'pcoip' below
            result = subprocess.run(
                ["crudini", "--get", self.config_file, "", "pcoip.maximum_initial_image_quality"],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            return int(result.stdout.strip())
        except (subprocess.CalledProcessError, ValueError):
            # Default to 85 if not found or invalid
            return 85
    
    def update_quality(self, value):
        try:
            quality = int(value)
            # If your config file has a section header like [pcoip], replace '' with 'pcoip' below
            subprocess.run(
                ["sudo", "crudini", "--set", self.config_file, "", "pcoip.maximum_initial_image_quality", str(quality)],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Failed to update quality: {e.stderr}")
    
    def set_default_quality(self):
        try:
            quality = 80
            # If your config file has a section header like [pcoip], replace '' with 'pcoip' below
            subprocess.run(
                ["sudo", "crudini", "--set", self.config_file, "", "pcoip.maximum_initial_image_quality", str(quality)],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            self.slider.set(quality)
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Failed to set default quality: {e.stderr}")
    
if __name__ == "__main__":
    root = tk.Tk()
    app = PCoIPImageQualityApp(root)
    root.geometry("330x135")  # Adjusted window size for larger slider
    root.mainloop()