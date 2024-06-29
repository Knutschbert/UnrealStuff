import os
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox
import json
import glob
import threading

# Default paths
default_project_path = "M:\\chivmodding_i\\SDK\\ArgonSDK\\TBL.uproject"
default_dump_directory = "F:\\CAS_output_2_10\\Filtered"
default_log_path = "I:\\chivmodding\\ArgonSDK-Clean\\AssetGenerator.log"

# Asset class whitelist
asset_class_whitelist = ["Texture2D", "Material", "StaticMesh", "Blueprint"]

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("UE4 Command Runner")
        self.refreshAssets = False

        self.create_widgets()
        self.pack_widgets()
        self.update_idletasks()  # Update "requested size" from geometry manager
        self.geometry(f'{self.winfo_reqwidth()}x{self.winfo_reqheight()}')  # Set the window size

    def create_widgets(self):
        # Frames for better layout management
        self.frame = tk.Frame(self)
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Project Path
        tk.Label(self.frame, text="Project Path:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.project_path_var = tk.StringVar(value=default_project_path)
        tk.Entry(self.frame, textvariable=self.project_path_var, width=60).grid(row=0, column=1, padx=10, pady=5)
        chk = tk.Checkbutton(self.frame, text="Refresh Assets", variable=self.refreshAssets).grid(row=2, column=3, sticky="w", padx=10, pady=5)

        # Dump Directory
        tk.Label(self.frame, text="Dump Directory:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.dump_directory_var = tk.StringVar(value=default_dump_directory)
        tk.Entry(self.frame, textvariable=self.dump_directory_var, width=60).grid(row=1, column=1, padx=10, pady=5)

        # Log Path
        tk.Label(self.frame, text="Log Path:").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.log_path_var = tk.StringVar(value=default_log_path)
        tk.Entry(self.frame, textvariable=self.log_path_var, width=60).grid(row=2, column=1, padx=10, pady=5)

        # Asset Class Whitelist
        tk.Label(self.frame, text="Asset Class Whitelist:").grid(row=3, column=0, sticky="w", padx=10, pady=5)
        self.asset_vars = {}
        last_box_row = self.create_asset_checkboxes()

        # Run button
        tk.Button(self.frame, text="Run Command", command=self.run_command).grid(row=9, column=1, pady=10)

        # Output frames for logs
        self.output_normal_frame = tk.Frame(self)
        self.output_normal_frame.pack(fill=tk.BOTH, expand=True)
        tk.Label(self.output_normal_frame, text="Normal Logs:").pack(anchor='w', padx=10, pady=5)
        self.output_normal_text = tk.Text(self.output_normal_frame, wrap=tk.WORD, height=10, width=80)
        self.output_normal_text.pack(fill=tk.BOTH, expand=True)
        self.output_normal_text.config(state=tk.DISABLED)  # Disable editing

        self.output_error_frame = tk.Frame(self)
        self.output_error_frame.pack(fill=tk.BOTH, expand=True)
        tk.Label(self.output_error_frame, text="Error Logs:").pack(anchor='w', padx=10, pady=5)
        self.output_error_text = tk.Text(self.output_error_frame, wrap=tk.WORD, height=10, width=80)
        self.output_error_text.pack(fill=tk.BOTH, expand=True)
        self.output_error_text.config(state=tk.DISABLED)  # Disable editing

        self.output_warning_frame = tk.Frame(self)
        self.output_warning_frame.pack(fill=tk.BOTH, expand=True)
        tk.Label(self.output_warning_frame, text="Warning Logs:").pack(anchor='w', padx=10, pady=5)
        self.output_warning_text = tk.Text(self.output_warning_frame, wrap=tk.WORD, height=10, width=80)
        self.output_warning_text.pack(fill=tk.BOTH, expand=True)
        self.output_warning_text.config(state=tk.DISABLED)  # Disable editing

    def pack_widgets(self):
        # Configure grid weights
        self.frame.grid_rowconfigure(0, weight=0)
        for i in range(1, 4):
            self.frame.grid_rowconfigure(i, weight=0)  # Row weights for fixed size
        self.frame.grid_rowconfigure(4, weight=1)  # Make the last row (logs) stretch
        self.frame.grid_columnconfigure(1, weight=1)  # Column weight for input fields to stretch

    def create_asset_checkboxes(self):
        # Function to create checkboxes for asset classes
        max_rows = 5
        current_row = 4
        current_column = 1

        # Iterate through dump directory to find available types from JSON files
        dump_directory = self.dump_directory_var.get()
        available_types = self.get_available_types(dump_directory)

        for i, asset in enumerate(available_types):
            var = tk.BooleanVar()
            chk = tk.Checkbutton(self.frame, text=asset, variable=var)
            chk.grid(row=current_row, column=current_column, sticky="w", padx=10, pady=2)

            self.asset_vars[asset] = var

            # Move to next row if max rows reached
            current_row += 1
            if current_row - 4 >= max_rows:
                current_row = 4
                current_column += 1
        return current_row

    def get_available_types(self, dump_directory):
        available_types = set()

        try:
            json_files = glob.glob(os.path.join(dump_directory, '**/*.json'), recursive=True)

            # Function to process each JSON file and extract asset classes
            def process_json_file(file_path):
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    asset_class = data.get("AssetClass")
                    if asset_class:
                        available_types.add(asset_class)

            # Create threads to process JSON files concurrently
            threads = []
            for file_path in json_files:
                thread = threading.Thread(target=process_json_file, args=(file_path,))
                thread.start()
                threads.append(thread)

            # Wait for all threads to complete
            for thread in threads:
                thread.join()

        except Exception as e:
            messagebox.showerror("Error", f"Error reading JSON files: {str(e)}")
        available_types = set()

        try:
            # Use glob to recursively search for JSON files in subdirectories
            json_files = glob.glob(os.path.join(dump_directory, '**/*.json'), recursive=True)
            
            for file_path in json_files:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    asset_class = data.get("AssetClass")
                    if asset_class:
                        available_types.add(asset_class)

        except Exception as e:
            messagebox.showerror("Error", f"Error reading JSON files: {str(e)}")

        return sorted(available_types)

    def run_command(self):
        project_path = self.project_path_var.get()
        dump_directory = self.dump_directory_var.get()
        log_path = self.log_path_var.get()

        selected_asset_classes = [asset for asset, var in self.asset_vars.items() if var.get()]
        if not selected_asset_classes:
            messagebox.showerror("Error", "Please select at least one asset class.")
            return

        asset_class_whitelist_str = ", ".join(selected_asset_classes)
        
        command = [
            "UE4Editor-Cmd.exe",
            project_path,
            "-run=AssetGenerator",
            f"-DumpDirectory={dump_directory}",
            f"-AssetClassWhitelist={asset_class_whitelist_str}",
            self.refreshAssets and "-NoRefresh" or "",
            f"-abslog={log_path}",
            "-stdout",
            "-unattended",
            "-NoLogTimes"
        ]

         # Clear previous logs
        self.clear_logs()

        # Create a thread to run the command and read output
        output_thread = threading.Thread(target=self.execute_command, args=(command,))
        output_thread.start()

        # try:
        #     process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        #     stdout, stderr = process.communicate()

        #     # Clear previous logs
        #     self.output_error_text.config(state=tk.NORMAL)
        #     self.output_warning_text.config(state=tk.NORMAL)
        #     self.output_normal_text.config(state=tk.NORMAL)
        #     self.output_error_text.delete(1.0, tk.END)
        #     self.output_warning_text.delete(1.0, tk.END)
        #     self.output_normal_text.delete(1.0, tk.END)

        #     # Display logs in respective windows
        #     self.display_logs(stdout, stderr)

        #     # Scroll to the end of logs
        #     self.output_error_text.see(tk.END)
        #     self.output_warning_text.see(tk.END)
        #     self.output_normal_text.see(tk.END)

        #     self.output_error_text.config(state=tk.DISABLED)
        #     self.output_warning_text.config(state=tk.DISABLED)
        #     self.output_normal_text.config(state=tk.DISABLED)

        # except Exception as e:
        #     messagebox.showerror("Error", f"Error running command: {str(e)}")

    def display_log(self, line, text_widget):
        text_widget.config(state=tk.NORMAL)
        text_widget.insert(tk.END, line + "\n")
        text_widget.see(tk.END)
        text_widget.config(state=tk.DISABLED)

    def execute_command(self, command):
        try:
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            # Read stdout and stderr in real-time
            for line in process.stdout:
                self.display_log(line, self.output_normal_text)
                if "Error:" in line:
                    self.display_log(line, self.output_error_text)
                elif "Warning:" in line:
                    self.display_log(line, self.output_warning_text)
            
            for line in process.stderr:
                self.display_log(line, self.output_error_text)

            process.communicate()  # Wait for process to complete

        except Exception as e:
            messagebox.showerror("Error", f"Error running command: {str(e)}")
                
    def clear_logs(self):
        self.output_normal_text.config(state=tk.NORMAL)
        self.output_normal_text.delete(1.0, tk.END)
        self.output_normal_text.config(state=tk.DISABLED)

        self.output_error_text.config(state=tk.NORMAL)
        self.output_error_text.delete(1.0, tk.END)
        self.output_error_text.config(state=tk.DISABLED)

        self.output_warning_text.config(state=tk.NORMAL)
        self.output_warning_text.delete(1.0, tk.END)
        self.output_warning_text.config(state=tk.DISABLED)
        
    def display_logs(self, stdout, stderr):
        stdout_lines = stdout.split('\n')
        stderr_lines = stderr.split('\n')

        # Display Normal Logs
        normal_logs = [line for line in stdout_lines if "Error:" not in line and "Warning:" not in line]
        if normal_logs:
            self.output_normal_text.config(state=tk.NORMAL)
            self.output_normal_text.insert(tk.END, "\n".join(normal_logs) + "\n")
            self.output_normal_text.config(state=tk.DISABLED)

        # Display Error Logs
        error_logs = [line for line in stderr_lines if "Error:" in line]
        if error_logs:
            self.output_error_text.config(state=tk.NORMAL)
            self.output_error_text.insert(tk.END, "\n".join(error_logs) + "\n")
            self.output_error_text.config(state=tk.DISABLED)

        # Display Warning Logs
        warning_logs = [line for line in stdout_lines if "LogAutomationTest" not in line and "Warning:" in line]
        if warning_logs:
            self.output_warning_text.config(state=tk.NORMAL)
            self.output_warning_text.insert(tk.END, "\n".join(warning_logs) + "\n")
            self.output_warning_text.config(state=tk.DISABLED)

if __name__ == "__main__":
    app = Application()
    app.mainloop()