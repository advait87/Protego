# Protego/engines/win_engine.py

import subprocess
import os
import re
import datetime
import sys

# Ensure project structure is accessible
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from win_flags import WIN_FLAGS, SECEDIT_EXPORT_COMMAND
from utils.rollback import backup_windows_state, rollback_windows_state
from utils.reporting import create_compliance_report

class WinEngine:
    def __init__(self, target_config, level="strict"):
        self.target_config = target_config 
        self.level = level
        self.results = []
        self.backup_path = None
        self.INF_FILENAME = "protego_harden.inf"

    def __run_cli(self, command, verbose=True):
        """Helper to execute Windows CLI commands and returns success/output."""
        try:
            # Setting encoding='utf-8' here helps capture output reliably
            result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True, encoding='utf-8',
                                    creationflags=subprocess.CREATE_NO_WINDOW)
            return True, result.stdout.strip()
        except subprocess.CalledProcessError as e:
            if verbose:
                # Use stderr for error details
                print(f"[ERROR] Command failed: {command[:40]}... Error: {e.stderr[:50]}...")
            return False, e.stderr.strip()
        except FileNotFoundError:
            return False, "Command not found."

    # --- MAIN ENGINE COMMANDS (CHECK and HARDEN) ---

    def check_compliance(self):
        """Checks current state against target policies."""
        self.results = []
        temp_export_inf = "temp_export.inf"
        
        print("-> Executing Windows Compliance Check...")
        self.__run_cli(SECEDIT_EXPORT_COMMAND, verbose=False) 
        
        for category, policies in self.target_config.items():
            for policy_name in policies:
                flag_data = WIN_FLAGS.get(category, {}).get(policy_name)
                if not flag_data: continue

                status = 'NON-COMPLIANT'
                current_value = "N/A"
                target_value = flag_data['target_value']
                
                # --- LIVE VALUE CHECKING LOGIC ---
                if flag_data.get('check_type') == "INF_PARSE":
                    try:
                        # Note: INF export is often ANSI/UTF-8, but we handle the content carefully
                        with open(temp_export_inf, 'r') as f:
                            for line in f:
                                if line.strip().startswith(policy_name):
                                    current_value = line.split('=')[-1].strip()
                                    break
                    except FileNotFoundError:
                        current_value = "INF File Missing"
                        
                elif flag_data.get('check_type') == "SC_QUERY":
                    success, output = self.__run_cli(flag_data["get_command"], verbose=False)
                    if success:
                        match = re.search(r'START_TYPE\s+:\s+(\d+)', output)
                        if match: current_value = match.group(1) 
                
                elif flag_data.get('check_type') == "NETSH_FW":
                    success, output = self.__run_cli(flag_data["get_command"], verbose=False)
                    if success:
                        if str(target_value).upper() in output.upper():
                            current_value = target_value
                        else:
                            current_value = "INCORRECT SETTING"

                if str(current_value).upper() == str(target_value).upper():
                    status = 'COMPLIANT'

                self.results.append({
                    'policy': policy_name,
                    'status': status,
                    'current': current_value,
                    'target': target_value
                })
        
        if os.path.exists(temp_export_inf): os.remove(temp_export_inf)
        
        create_compliance_report(self.results, "CHECK", f"Protego_Compliance_{self.level}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.txt", self.level)
        return self.results

    def harden_system(self):
        """Applies all policies defined in the target config."""
        print("\n-> 1. Backing up system state...")
        self.backup_path = backup_windows_state()
        if not self.backup_path:
             print("Hardening aborted due to critical backup failure.")
             return
        self.results = []
        
        print("\n-> 2. Applying Hardening Policies...")
        self._configure_services()
        self._apply_secedit_policies()
        self._configure_firewall()
        self._perform_other_actions()
        
        print("\n-> 3. Verifying final compliance state...")
        self.check_compliance() 
        
        create_compliance_report(self.results, "HARDEN", f"Protego_Remediation_{self.level}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.txt", self.level)

    def rollback(self):
        """Reverts to the last backed-up state."""
        if not self.backup_path:
            latest_backup = sorted([f for f in os.listdir("backups") if f.endswith('.inf')], reverse=True)
            if latest_backup:
                self.backup_path = os.path.join("backups", latest_backup[0])
            
        if self.backup_path:
            rollback_windows_state(self.backup_path)
        else:
            print("No previous backup found to rollback.")

    # --- REMEDIATION METHODS ---
    
    def _apply_secedit_policies(self):
        """Generates INF file and executes secedit /configure."""
        print("   - Configuring Account/Local/Security Options via secedit...")
        
        inf_path = os.path.join(os.getcwd(), self.INF_FILENAME)
        temp_sdb_path = os.path.join(os.getcwd(), 'temp.sdb')
        
        # --- CRITICAL FIX: INF FILE GENERATION (UTF-16 encoding, no quotes) ---
        # secedit requires UTF-16, and numeric values in System Access should NOT be quoted.
        try:
            with open(inf_path, 'w', encoding='utf-16') as f:
                
                # 1. System Access Section (Account Policies)
                account_policies = self.target_config.get("account_policy", [])
                if account_policies:
                    f.write("[System Access]\n")
                    
                    for policy_name in account_policies:
                        flag_data = WIN_FLAGS.get("account_policy", {}).get(policy_name)
                        if flag_data:
                             # Write PolicyName = Value (Value is raw number, no quotes)
                             f.write(f"{policy_name} = {flag_data['target_value']}\n")
                             
        except IOError as e:
            print(f"     -> FATAL ERROR: Could not write INF file: {e}")
            return
            
        # --- SECEDIT EXECUTION ---
        success, output = self.__run_cli(
            f'secedit /configure /cfg "{inf_path}" /db "{temp_sdb_path}" /overwrite /quiet',
            verbose=False
        )
        
        print(f"     -> SECEDIT execution status: {'Success' if success else 'Failure'}")
        if not success:
            print(f"     -> FAILED COMMAND: secedit /configure /cfg \"{inf_path}\" /db \"{temp_sdb_path}\" /overwrite /quiet")
            print("     -> SECEDIT ERROR DETAIL (FULL OUTPUT):")
            # The 'output' variable contains the error stream (stderr/stdout merged)
            print(output) 

        # --- Cleanup ---
        if os.path.exists(inf_path): 
            os.remove(inf_path)
        if os.path.exists(temp_sdb_path):
             os.remove(temp_sdb_path)


    def _configure_services(self):
        """Disables/enables services using sc.exe."""
        print("   - Disabling System Services (4.b)...")
        for service_name in self.target_config.get("service_control", []):
            flag_data = WIN_FLAGS.get("service_control", {}).get(service_name)
            if flag_data and flag_data.get('set_command'):
                success, _ = self.__run_cli(flag_data['set_command'], verbose=False)
                print(f"     -> {service_name}: {'Disabled' if success else 'Failed'}")

    def _configure_firewall(self):
        """Configures firewall profiles using netsh."""
        print("   - Configuring Windows Firewall (5)...")
        for policy_name in self.target_config.get("firewall", []):
            flag_data = WIN_FLAGS.get("firewall", {}).get(policy_name)
            if flag_data and flag_data.get('set_command'):
                self.__run_cli(flag_data['set_command'], verbose=False)
        
        print("     -> Firewall profile settings applied.")

    def _perform_other_actions(self):
        """Handles unique actions like renaming accounts (net user)."""
        print("   - Performing Other Account Actions...")
        flag_data = WIN_FLAGS.get("account_name", {}).get("Administrator_Rename")
        if flag_data and flag_data.get('set_command'):
            success, _ = self.__run_cli(flag_data['set_command'], verbose=False)
            print(f"     -> Rename Admin: {'Success' if success else 'Failure'}")