import os
import shutil
import tkinter as tk
from tkinterdnd2 import DND_FILES, TkinterDnD
from pathlib import Path

def create_symlink(src, dest):
    # Create the destination directory if it doesn't exist
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    
    # Create a symlink for the file or directory
    if os.path.exists(dest):
        os.remove(dest)
    os.symlink(src, dest)

def handle_drop(event):
    # Get the path of the dropped file or folder
    dropped_path = event.data
    dropped_path = dropped_path.strip('{}')  # Clean up the path format
    
    # Get the relative path
    relative_path = os.path.relpath(dropped_path)
    
    # Define the output directory name
    output_dir = "Filtered"
    
    # Create the new destination path
    new_dest = os.path.join(output_dir, relative_path)
    
    # Create the symlink
    create_symlink(dropped_path, new_dest)
    
    # Notify the user
    status_label.config(text=f'Symlink created at: {new_dest}')

# Set up the main window
root = TkinterDnD.Tk()
root.title('Drop File/Folder Here')
root.geometry('400x300')

# Set up the drop area
drop_area = tk.Label(root, text='Drop your file or folder here', width=50, height=10, relief='ridge')
drop_area.pack(pady=20)

# Set up the status label
status_label = tk.Label(root, text='Waiting for file', wraplength=300)
status_label.pack(pady=10)

# Bind the drop event
drop_area.drop_target_register(DND_FILES)
drop_area.dnd_bind('<<Drop>>', handle_drop)

# Run the application
root.mainloop()
