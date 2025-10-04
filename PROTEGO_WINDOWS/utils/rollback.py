# PROTEGO_WINDOWS/utils/rollback.py

import subprocess
import os
import datetime
import shutil

BACKUP_DIR = os.path.join(os.getcwd(), "backups")
INF_FILENAME = "security_backup.inf"

def get_timestamped_path(filename):
    """Generates a unique, timestamped path for the backup file."""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    return os.path.join(BACKUP_DIR, f"{timestamp}_{filename}")

def backup_windows_state():
    """Exports current system state for rollback using secedit and reg export."""
    os.makedirs(BACKUP_DIR, exist_ok=True)
    inf_path = get_timestamped_path(INF_FILENAME)
    
    try:
        subprocess.run(f'secedit /export /cfg "{inf_path}" /areas securitypolicy /quiet', 
                       shell=True, check=True, creationflags=subprocess.CREATE_NO_WINDOW)
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Failed to export secedit settings. Run as Administrator. {e}")
        return None

    reg_path = get_timestamped_path("system_registry_backup.reg")
    try:
        # CRITICAL FIX: Use a raw string (r"") to prevent Python from interpreting \H and \S as escape sequences.
        subprocess.run(r'reg export HKLM\Software\Microsoft\Windows\CurrentVersion\Policies\System "{reg_path}" /y'.format(reg_path=reg_path), 
                       shell=True, check=True, creationflags=subprocess.CREATE_NO_WINDOW)
    except subprocess.CalledProcessError:
        print("[WARNING] Failed to export critical registry keys.")

    print(f"Backup created at: {os.path.basename(inf_path)}")
    return inf_path

def rollback_windows_state(backup_inf_path):
    """Applies the previous security database backup."""
    if not os.path.exists(backup_inf_path):
        print(f"[ERROR] Backup file not found: {backup_inf_path}")
        return

    print("Attempting full system configuration rollback...")
    
    temp_sdb = os.path.join(os.getcwd(), "rollback_temp.sdb")
    try:
        subprocess.run(f'secedit /configure /cfg "{backup_inf_path}" /db "{temp_sdb}" /overwrite /quiet', 
                       shell=True, check=True, creationflags=subprocess.CREATE_NO_WINDOW)
        print("Security Policies (secedit) rolled back successfully.")
        
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Rollback failed during secedit execution. {e.stderr}")
        return
    finally:
        if os.path.exists(temp_sdb):
            os.remove(temp_sdb)

    print("\nRollback complete. System reboot is recommended to fully apply all settings.")