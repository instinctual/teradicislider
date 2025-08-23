import tkinter as tk
from tkinter import messagebox
import subprocess
import os

class PCoIPImageQualityApp:
    def __init__(self, root, config_file="/etc/pcoip-agent/pcoip-agent.conf"):
        self.root = root
        self.config_file = config_file
        self.root.overrideredirect(True)  # Remove window title bar and decorations
        self.root.title("Teradici Quality")  # Title won't be visible
        
        # Set window to always stay on top
        self.root.attributes('-topmost', True)
        
        # Variables for dragging
        self.drag_start_x = 0
        self.drag_start_y = 0
        
        # Create a background frame for dragging
        self.drag_frame = tk.Frame(self.root, bg="gray", width=270, height=115)
        self.drag_frame.pack(fill="both", expand=True)
        self.drag_frame.pack_propagate(False)  # Prevent frame from resizing
        
        # Bind drag events to the background frame
        self.drag_frame.bind("<Button-1>", self.start_drag)
        self.drag_frame.bind("<B1-Motion>", self.on_drag)
        
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
            self.drag_frame,  # Place slider in drag_frame
            from_=0,
            to=100,
            orient=tk.HORIZONTAL,
            length=235,
            width=15,
            sliderlength=40,
            resolution=1,
            command=self.update_quality
        )
        self.slider.set(self.current_quality)
        self.slider.pack(pady=10)
        
        # Create a frame for buttons
        self.button_frame = tk.Frame(self.drag_frame, bg="gray")
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
        
    def start_drag(self, event):
        self.drag_start_x = event.x_root - self.root.winfo_x()
        self.drag_start_y = event.y_root - self.root.winfo_y()
    
    def on_drag(self, event):
        x = event.x_root - self.drag_start_x
        y = event.y_root - self.drag_start_y
        self.root.geometry(f"+{x}+{y}")
    
    def check_crudini(self):
        try:
            subprocess.run(["crudini", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
    
    def get_current_quality(self):
        try:
            result = subprocess.run(
                ["crudini", "--get", self.config_file, "", "pcoip.maximum_initial_image_quality"],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            return int(result.stdout.strip())
        except (subprocess.CalledProcessError, ValueError):
            return 85
    
    def update_quality(self, value):
        try:
            quality = int(value)
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
    root.geometry("270x115")
    root.mainloop()