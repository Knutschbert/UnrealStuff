import os
import json
import tkinter as tk
from tkinter import ttk, filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import random
from PIL import Image, ImageTk
from fmodel_oo import *

def image_histogram_equalization(image, number_bins=256):
    # from http://www.janeriksolem.net/histogram-equalization-with-python-and.html
    image = np.asarray(image)
    # get image histogram
    image_histogram, bins = np.histogram(image.flatten(), number_bins, density=True)
    cdf = image_histogram.cumsum() # cumulative distribution function
    cdf = (number_bins-1) * cdf / cdf[-1] # normalize

    # use linear interpolation of cdf to find new pixel values
    image_equalized = np.interp(image.flatten(), bins[:-1], cdf)

    return Image.fromarray(image_equalized.reshape(image.shape)), cdf

# Dummy functions to simulate script behavior
def first_function(filepath):
    pc = XeightMapProcessor(filepath)
    pc.Init()
    img1, img2 = pc.Extract_Heightmap()
    # img1 = Image.new('RGB', (1000, 1000), color='red')
    # img2 = Image.new('RGB', (1000, 1000), color='blue')
    params = {'param1': 'value1', 'param2': 'value2'}
    norm, cdf = image_histogram_equalization(img1)
    return  norm, img2, params

def second_function(filepath):
    pc = XeightMapProcessor(filepath)
    pc.Init()
    imgs = pc.Extract_Weightmaps()
    # imgs = [Image.new('RGB', (1000, 1000), color='green') for _ in range(20)]
    params = {'param3': 'value3', 'param4': 'value4'}
    return imgs, params

def debug_function(filepath):
    img1 = Image.new('RGB', (1000, 1000), color='yellow')
    img2 = Image.new('RGB', (1000, 1000), color='purple')
    params = {'debug_param1': 'debug_value1', 'debug_param2': 'debug_value2'}
    return img1, img2, params

# Setup GUI
root = tk.Tk()
root.title("Image Processing GUI")
root.geometry("1200x800")

# Notebook tabs
notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill='both')

# Main tab
main_tab = ttk.Frame(notebook)
notebook.add(main_tab, text="Main Tab")

# 2nd function preview tab
second_tab = ttk.Frame(notebook)


bottom = tk.Frame(second_tab, bg="white")
bottom.pack(fill='both', expand=True)
# BOTTOM-LEFT SECTION
canvas = tk.Canvas(bottom, bg="white")
canvas.pack(fill=tk.BOTH, expand=1, side=tk.LEFT)
left = tk.Frame(canvas)
#left.pack(fill=BOTH, expand=1)
canvas.create_window(0, 0, window=left, anchor='nw') ###
left_scroll = tk.Scrollbar(bottom, orient=tk.VERTICAL) ### left to bottom
left_scroll.pack(side=tk.LEFT, fill=tk.Y) ### side=RIGHT to side=LEFT
left_scroll.config(command=canvas.yview)
canvas.configure(yscrollcommand=left_scroll.set)
# Function to scroll canvas with the mouse wheel
def on_mouse_wheel(event):
    canvas.yview_scroll(int(-1*(event.delta/120)), "units")

# Bind the mouse wheel event to the canvas
canvas.bind_all("<MouseWheel>", on_mouse_wheel)
for root2, dirs, files in os.walk("C:\\", topdown=True):
    full = dirs + files
    for i in full:
        tk.Button(left, text=i, bg="white", anchor="w", relief=tk.SOLID, borderwidth=0).pack(fill=tk.BOTH)
    break
### update scrollregion of canvas
left.update()
canvas.configure(scrollregion=canvas.bbox('all'))
notebook.add(second_tab, text="Weightmaps Preview")

# Debug preview tab
debug_tab = ttk.Frame(notebook)
notebook.add(debug_tab, text="Debug Image Preview")

# Settings tab
settings_tab = ttk.Frame(notebook)
notebook.add(settings_tab, text="Settings")

# Main tab UI components
folder_path_var = tk.StringVar(value='H:/chivunpack/Output/Exports/TBL/Content/Maps')
selected_file_var = tk.StringVar()

def scan_for_json(folder):
    json_files = []
    for root, _, files in os.walk(folder):
        for file in files:
            if file.endswith('.json'):
                json_files.append(os.path.join(root, file))
    return json_files

def update_folder():
    folder = folder_path_var.get()
    json_files = scan_for_json(folder)
    shortnames = [os.path.relpath(f, folder) for f in json_files]
    dropdown_menu['values'] = shortnames
    if json_files:
        selected_file_var.set(shortnames[0])

def browse_folder():
    folder_selected = filedialog.askdirectory()
    folder_path_var.set(folder_selected)
    update_folder()

def process_files():
    folder = folder_path_var.get()
    filename = selected_file_var.get()
    filepath = os.path.join(folder, filename)
    
    img1, img2, params = first_function(filepath)
    update_image(canvas1, img1)
    update_image(canvas2, img2)
    update_labels(param_frame1, params)
    update_labels(param_frame2, params)

def update_image(canvas, img):
    img_resized = img.resize((500, 500))
    img_tk = ImageTk.PhotoImage(img_resized)
    canvas.create_image(0, 0, anchor='nw', image=img_tk)
    canvas.image = img_tk

def update_labels(frame, params):
    for widget in frame.winfo_children():
        widget.destroy()
    for key, value in params.items():
        label = ttk.Label(frame, text=f"{key}: {value}")
        label.pack(anchor='w')

# Function to process and display images using matplotlib
def process_second_function():
    folder = folder_path_var.get()
    filename = selected_file_var.get()
    filepath = os.path.join(folder, filename)
    
    imgs, params = second_function(filepath)
    random_imgs_count = random.randint(9, 12)  # Random number of images (2 to 6)

    # Clear previous matplotlib figures
    for widget in left.winfo_children():
        widget.destroy()
    num_cols = 2
    num_rows = int(len(imgs) / 2 + 0.5)
    # left.config(height=500*num_rows)
    # Display images in a grid using matplotlib and FigureCanvasTkAgg
    for idx, (name, img) in enumerate(imgs.items()):
        fig, ax = plt.subplots(figsize=(5, 5))
        ax.set_title(f'{name}')
        ax.grid()
        ax.imshow(img)
        ax.axis('off')
        
        canvas_agg = FigureCanvasTkAgg(fig, master=left)
        canvas_widget = canvas_agg.get_tk_widget()
        print(f'{idx}/{num_rows}, row={idx // num_cols}, column={idx % num_cols}')
        canvas_widget.grid(row=idx // num_cols, column=idx % num_cols, padx=2, pady=2)
        canvas_agg.draw()
    # Calculate total size of the canvas content
    num_rows = (random_imgs_count + num_cols - 1) // num_cols  # Round up division to get rows needed
    content_height = num_rows * 505  # 110 is the height of each image (plus padding)
    content_width = num_cols * 505   # 110 is the width of each image (plus padding)

    # Update canvas scroll region to fit all content
    canvas.config(scrollregion=(0, 0, content_width, content_height))


folder_frame = ttk.Frame(main_tab)
folder_frame.pack(anchor='w', padx=10, pady=5)
# Main tab layout
ttk.Label(folder_frame, text="Base Folder Directory:").pack(side=tk.LEFT)
entry = ttk.Entry(folder_frame, textvariable=folder_path_var, width=50)
entry.pack(side=tk.LEFT)
ttk.Button(folder_frame, text="Browse", command=browse_folder).pack(side=tk.LEFT)

json_frame = ttk.Frame(main_tab)
json_frame.pack(anchor='w', padx=10, pady=5)
ttk.Label(json_frame, text="Select JSON File:").pack(side=tk.LEFT)
dropdown_menu = ttk.Combobox(json_frame, textvariable=selected_file_var, width=50)
dropdown_menu.pack(side=tk.LEFT)

button_frame = ttk.Frame(json_frame)
button_frame.pack(anchor='w', padx=10, pady=5)
ttk.Button(button_frame, text="Start Processing", command=process_files).grid(row=0, column=0, padx=5)
ttk.Button(button_frame, text="Process Second Function", command=process_second_function).grid(row=0, column=2, padx=5)
ttk.Button(button_frame, text="Open Folder", command=lambda: os.startfile(folder_path_var.get())).grid(row=0, column=1, padx=5)

# Image display
canvas_frame = ttk.Frame(main_tab)
canvas_frame.pack(anchor='w', padx=10, pady=10)

canvas1 = tk.Canvas(canvas_frame, width=500, height=500)
canvas1.grid(row=0, column=0, padx=5)
param_frame1 = ttk.Frame(canvas_frame)
param_frame1.grid(row=1, column=0, padx=5)

canvas2 = tk.Canvas(canvas_frame, width=500, height=500)
canvas2.grid(row=0, column=1, padx=5)
param_frame2 = ttk.Frame(canvas_frame)
param_frame2.grid(row=1, column=1, padx=5)

# Settings handling
settings = {"setting1": "value1", "setting2": "value2"}
settings_path = "settings.json"

def load_settings():
    if os.path.exists(settings_path):
        with open(settings_path, 'r') as f:
            loaded_settings = json.load(f)
            for key, value in loaded_settings.items():
                ttk.Label(settings_tab, text=f"{key}: {value}").pack(anchor='w', padx=10)

def save_settings():
    with open(settings_path, 'w') as f:
        json.dump(settings, f)

load_settings()

tk.Button(settings_tab, text="Save Settings", command=save_settings).pack(anchor='w', padx=10, pady=5)

update_folder()
root.mainloop()
