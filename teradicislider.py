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
        
        # Define dark grey color
        self.dark_grey = "#333333"
        
        # Create a background frame for dragging
        self.drag_frame = tk.Frame(self.root, bg=self.dark_grey, width=270, height=115)
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
        
        # Create and configure the label
        self.label = tk.Label(
            self.drag_frame,
            text="Teradici Quality",
            font=("Helvetica", 10),  # Smaller font size
            bg=self.dark_grey,      # Match background
            fg="white"              # White text for contrast
        )
        self.label.pack(pady=(10, 0))  # Small padding above, none below
        
        # Create and configure the slider
        self.slider = tk.Scale(
            self.drag_frame,
            from_=0,
            to=100,
            orient=tk.HORIZONTAL,
            length=235,
            width=15,
            sliderlength=40,
            resolution=1,
            command=self.update_quality,
            bg=self.dark_grey,           # Background of slider
            troughcolor=self.dark_grey,  # Slider track color
            highlightthickness=0         # Remove border highlight
        )
        self.slider.set(self.current_quality)
        self.slider.pack(pady=(5, 10))  # Adjusted padding for label
        
        # Create a frame for buttons
        self.button_frame = tk.Frame(self.drag_frame, bg=self.dark_grey)
        self.button_frame.pack(pady=10)
        
        # Default button
        self.default_button = tk.Button(
            self.button_frame,
            text="Default",
            font=("Helvetica", 12),
            command=self.set_default_quality,
            bg=self.dark_grey,         # Button background
            fg="white",               # Text color for contrast
            activebackground="#555555",  # Slightly lighter grey when clicked
            highlightthickness=0      # Remove border highlight
        )
        self.default_button.pack(side=tk.LEFT, padx=5)
        
        # Exit button
        self.exit_button = tk.Button(
            self.button_frame,
            text="Exit",
            font=("Helvetica", 12),
            command=self.root.destroy,
            bg=self.dark_grey,         # Button background
            fg="white",               # Text color for contrast
            activebackground="#555555",  # Slightly lighter grey when clicked
            highlightthickness=0      # Remove border highlight
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
    root.geometry("270x135")  # Increased height to accommodate label
    root.mainloop()