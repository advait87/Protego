import tkinter as tk
from tkinter import ttk, scrolledtext
import ttkbootstrap as bs
from ttkbootstrap.scrolled import ScrolledFrame
from ttkbootstrap.tooltip import ToolTip
import platform
import datetime
import random

# --- DATA SIMULATION ---
# In a real application, these functions would execute system commands
# (e.g., PowerShell, regedit, sysctl, auditctl) to get actual values.

def get_simulated_current_value(options):
    """Returns a random value from the options to simulate a real system check."""
    return random.choice(options) if options else "N/A"

# --- Annexure 'A' for Windows OS (Sample Parameters) ---
WINDOWS_PARAMS = {
    "Account Policies - Password Policy": {
        "Enforce password history": {
            "description": "Number of previous passwords to remember.",
            "ideal": "24",
            "options": ["0", "5", "10", "24"],
            "presets": {"Low": "5", "Moderate": "10", "High": "24"}
        },
        "Maximum password age": {
            "description": "Maximum number of days a password can be used.",
            "ideal": "60",
            "options": ["90", "60", "30"],
            "presets": {"Low": "90", "Moderate": "60", "High": "30"}
        },
        "Minimum password length": {
            "description": "Minimum number of characters in a password.",
            "ideal": "14",
            "options": ["8", "12", "14"],
            "presets": {"Low": "8", "Moderate": "12", "High": "14"}
        },
    },
    "Account Policies - Account Lockout Policy": {
        "Account lockout threshold": {
            "description": "Invalid logon attempts before account lockout.",
            "ideal": "5",
            "options": ["10", "5", "3"],
            "presets": {"Low": "10", "Moderate": "5", "High": "3"}
        },
        "Account lockout duration": {
            "description": "Minutes the account stays locked out.",
            "ideal": "15",
            "options": ["30", "15", "5"],
            "presets": {"Low": "30", "Moderate": "15", "High": "15"}
        },
    },
    "Advanced Audit Policy Configuration": {
        "Audit Credential Validation": {
            "description": "Audits events related to credential validation.",
            "ideal": "Success and Failure",
            "options": ["No Auditing", "Success", "Success and Failure"],
            "presets": {"Low": "Success", "Moderate": "Success and Failure", "High": "Success and Failure"}
        }
    }
}

# --- Annexure 'B' for Linux OS (Sample Parameters) ---
LINUX_PARAMS = {
    "Filesystem Configuration": {
        "Disable unused filesystems": {
            "description": "Ensure mounting of cramfs, freevxfs is disabled.",
            "ideal": "Disabled",
            "options": ["Enabled", "Disabled"],
            "presets": {"Low": "Enabled", "Moderate": "Disabled", "High": "Disabled"}
        },
        "Set nodev option for /tmp partition": {
            "description": "Prevents character/block special devices on /tmp.",
            "ideal": "Enabled",
            "options": ["Disabled", "Enabled"],
            "presets": {"Low": "Disabled", "Moderate": "Enabled", "High": "Enabled"}
        }
    },
    "Secure Boot Settings": {
        "Ensure password is set for GRUB Legacy": {
            "description": "Protects boot loader from unauthorized modification.",
            "ideal": "Enabled",
            "options": ["Disabled", "Enabled"],
            "presets": {"Low": "Disabled", "Moderate": "Enabled", "High": "Enabled"}
        }
    },
    "System Accounting (Auditd)": {
        "Ensure auditd is installed": {
            "description": "Enables system event logging and auditing.",
            "ideal": "Installed",
            "options": ["Not Installed", "Installed"],
            "presets": {"Low": "Not Installed", "Moderate": "Installed", "High": "Installed"}
        },
        "Ensure events that modify date/time are collected": {
            "description": "Logs changes to system time (adjtimex, settimeofday).",
            "ideal": "Enabled",
            "options": ["Disabled", "Enabled"],
            "presets": {"Low": "Disabled", "Moderate": "Enabled", "High": "Enabled"}
        }
    }
}


class SecurityHardeningApp(bs.Window):
    def __init__(self):
        super().__init__(themename="cyborg", title="Automated Security Hardening Tool")
        self.geometry("1200x800")
        self.minsize(1000, 700)
        self.parameter_widgets = []

        self.os_type = platform.system()
        # self.os_type = "Linux" # Uncomment to force Linux mode for testing
        # self.os_type = "Windows" # Uncomment to force Windows mode for testing
        
        if self.os_type == "Windows":
            self.params = WINDOWS_PARAMS
        else: # For Linux, macOS, etc.
            self.os_type = "Linux" # Standardize for display
            self.params = LINUX_PARAMS

        self.title(f"Automated Security Hardening Tool - [{self.os_type.upper()}]")
        self.create_widgets()

    def create_widgets(self):
        main_pane = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        main_pane.pack(fill=tk.BOTH, expand=True)

        # --- Left Sidebar ---
        sidebar = ttk.Frame(main_pane, width=200)
        main_pane.add(sidebar, weight=1)

        logo_font = ("Helvetica", 20, "bold")
        logo_label = ttk.Label(sidebar, text="Hardening Tool", font=logo_font, anchor="center")
        logo_label.pack(pady=20, padx=10)

        btn_dashboard = bs.Button(sidebar, text="Dashboard", bootstyle="success", command=self.on_dashboard_click)
        btn_dashboard.pack(fill="x", pady=5, padx=10)
        
        btn_rollback = bs.Button(sidebar, text="History/Rollback", bootstyle="secondary")
        btn_rollback.pack(fill="x", pady=5, padx=10)
        
        # --- Right Content Area ---
        content_area = ttk.PanedWindow(main_pane, orient=tk.VERTICAL)
        main_pane.add(content_area, weight=5)

        # --- Top Frame for Controls ---
        top_frame = ttk.Frame(content_area, height=400)
        content_area.add(top_frame, weight=3)

        top_frame.columnconfigure(0, weight=1)
        top_frame.rowconfigure(1, weight=1)

        controls_header = ttk.Frame(top_frame)
        controls_header.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 0))
        
        # --- Preset buttons ---
        presets_label = ttk.Label(controls_header, text="Apply Security Level:", font=("Helvetica", 12, "bold"))
        presets_label.pack(side="left", padx=(0, 20))

        btn_low = bs.Button(controls_header, text="Low Security", bootstyle="warning", command=lambda: self.apply_preset("Low"))
        btn_low.pack(side="left", padx=5)
        
        btn_moderate = bs.Button(controls_header, text="Moderate Security", bootstyle="info", command=lambda: self.apply_preset("Moderate"))
        btn_moderate.pack(side="left", padx=5)
        
        btn_high = bs.Button(controls_header, text="High Security", bootstyle="danger", command=lambda: self.apply_preset("High"))
        btn_high.pack(side="left", padx=5)

        os_label = ttk.Label(controls_header, text=f"Detected OS: {self.os_type}", font=("Helvetica", 12, "bold"), bootstyle="info")
        os_label.pack(side="right", padx=10)

        # --- Parameter Display Area ---
        self.scrolled_frame = ScrolledFrame(top_frame, autohide=True)
        self.scrolled_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        self.populate_parameters()
        
        # --- Main Action Buttons ---
        action_frame = ttk.Frame(top_frame)
        action_frame.grid(row=2, column=0, pady=10)

        btn_analyze = bs.Button(action_frame, text="Analyze System", bootstyle="primary-outline", command=self.analyze_system)
        btn_analyze.pack(side="left", padx=10)

        btn_apply = bs.Button(action_frame, text="Apply All Changes", bootstyle="success", command=self.apply_all_configurations)
        btn_apply.pack(side="left", padx=10)

        # --- Bottom Frame for Console ---
        console_frame = ttk.Frame(content_area, height=200)
        content_area.add(console_frame, weight=1)
        
        console_header_frame = ttk.Frame(console_frame)
        console_header_frame.pack(fill='x', padx=10, pady=(5,0))

        console_label = ttk.Label(console_header_frame, text="Execution Log", font=("Helvetica", 12, "bold"))
        console_label.pack(side="left", anchor="nw")

        clear_log_btn = bs.Button(console_header_frame, text="Clear Log", bootstyle="danger-outline", command=self.clear_log)
        clear_log_btn.pack(side="right")

        self.console = scrolledtext.ScrolledText(
            console_frame, wrap=tk.WORD, state='disabled',
            bg="#2A2A2A", fg="#FFFFFF", font=("Consolas", 10)
        )
        self.console.pack(expand=True, fill="both", padx=10, pady=(0, 10))

        self.log_message(f"OS Detected: {self.os_type}. Parameters loaded.")
        self.log_message("Click 'Analyze System' to fetch current values.")

    def populate_parameters(self):
        # --- REFACTORED FOR GRID LAYOUT AND TOOLTIPS ---
        for widget in self.scrolled_frame.winfo_children():
            widget.destroy()
        self.parameter_widgets.clear()

        # Configure columns for a true grid
        header_labels = ["Parameter", "Current Value", "Ideal Value", "Set New Value"]
        weights = [4, 2, 2, 3]
        for i, (label, weight) in enumerate(zip(header_labels, weights)):
            self.scrolled_frame.columnconfigure(i, weight=weight)
            lbl = ttk.Label(self.scrolled_frame, text=label, font=("Helvetica", 10, "bold"))
            lbl.grid(row=0, column=i, sticky='w', padx=5)

        # Separator for a cleaner table look
        ttk.Separator(self.scrolled_frame, orient='horizontal').grid(row=1, column=0, columnspan=len(header_labels), sticky='ew', pady=5)

        row_index = 2
        for category, params in self.params.items():
            cat_label = ttk.Label(self.scrolled_frame, text=category, font=("Helvetica", 12, "bold", "underline"), bootstyle="info")
            cat_label.grid(row=row_index, column=0, columnspan=len(header_labels), sticky='w', pady=(15, 5), padx=5)
            row_index += 1
            
            for name, details in params.items():
                # --- Parameter Name with Tooltip ---
                name_frame = ttk.Frame(self.scrolled_frame)
                name_frame.grid(row=row_index, column=0, sticky='w', padx=5, pady=4)
                
                name_label = ttk.Label(name_frame, text=name, font=("Helvetica", 10, "bold"))
                name_label.pack(side="left", anchor='w')
                
                # --- NEW: Question mark icon with hover tooltip ---
                q_mark_label = ttk.Label(name_frame, text=" (?)", font=("Helvetica", 9, "bold"), bootstyle="success")
                q_mark_label.pack(side="left", anchor='w', padx=(2,0))
                ToolTip(q_mark_label, text=details['description'], bootstyle="info-inverse", wraplength=300)

                # --- Other Columns ---
                current_val_label = ttk.Label(self.scrolled_frame, text="-", font=("Helvetica", 10))
                current_val_label.grid(row=row_index, column=1, sticky='w', padx=5, pady=4)

                ideal_val_label = ttk.Label(self.scrolled_frame, text=details['ideal'], font=("Helvetica", 10), bootstyle="success")
                ideal_val_label.grid(row=row_index, column=2, sticky='w', padx=5, pady=4)

                combo = bs.Combobox(self.scrolled_frame, values=details['options'], state="readonly")
                combo.grid(row=row_index, column=3, sticky='ew', padx=(5, 30), pady=4)
                if details['options']: combo.set(details['options'][0])

                widget_info = {
                    "name": name, "details": details,
                    "labels": {"current": current_val_label},
                    "control": combo
                }
                self.parameter_widgets.append(widget_info)
                row_index += 1

    def analyze_system(self):
        self.log_message("Starting system analysis...")
        for widget_info in self.parameter_widgets:
            current_value = get_simulated_current_value(widget_info['details']['options'])
            widget_info['labels']['current'].config(text=current_value)
            
            if current_value in widget_info['control']['values']:
                widget_info['control'].set(current_value)
            
            self.log_message(f"  Checked '{widget_info['name']}': Current value is '{current_value}'")
        self.log_message("System analysis complete.")

    def apply_preset(self, level):
        self.log_message(f"Applying '{level} Security' preset values...")
        for widget_info in self.parameter_widgets:
            preset_value = widget_info['details']['presets'].get(level)
            if preset_value and preset_value in widget_info['control']['values']:
                widget_info['control'].set(preset_value)
        self.log_message(f"Preset '{level}' loaded. Click 'Apply All Changes' to enforce.")

    def _apply_single_setting(self, widget_info):
        """Helper function to apply configuration for a single parameter."""
        new_value = widget_info['control'].get()
        current_value = widget_info['labels']['current'].cget("text")
        name = widget_info['name']

        if new_value != current_value:
            # In a real app, this is where you'd run the command to change the setting
            self.log_message(f"  SUCCESS: Changed '{name}' from '{current_value}' to '{new_value}'", "success")
            # Update the 'current value' label to reflect the change
            widget_info['labels']['current'].config(text=new_value)
        else:
            self.log_message(f"  INFO: No change needed for '{name}'. Value is already '{new_value}'.", "info")
    
    def apply_all_configurations(self):
        """Applies all changed configurations."""
        self.log_message("Applying all selected configurations...", "warning")
        for widget_info in self.parameter_widgets:
            self._apply_single_setting(widget_info)
        self.log_message("All configurations applied.", "success")
        
    def on_dashboard_click(self):
        self.log_message("Dashboard selected.")

    def clear_log(self):
        """Clears all text from the console log."""
        self.console.config(state='normal')
        self.console.delete('1.0', tk.END)
        self.console.config(state='disabled')
        self.log_message("Log cleared by user.")

    def log_message(self, message, style=""):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        formatted_message = f"[{timestamp}] {message}\n"
        
        self.console.config(state='normal')
        self.console.insert(tk.END, formatted_message)
        self.console.see(tk.END)
        self.console.config(state='disabled')

if __name__ == "__main__":
    app = SecurityHardeningApp()
    app.mainloop()

