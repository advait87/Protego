# Protego/win_flags.py

# Global constants for bulk checks
SECEDIT_EXPORT_COMMAND = 'secedit /export /cfg temp_export.inf /areas securitypolicy /quiet'

WIN_FLAGS = {
    # 1. Account Policies (secedit)
    "account_policy": {
        "MinimumPasswordLength": {
            "value": "unknown", 
            "target_value": "12",
            "check_type": "INF_PARSE",
            "section": "System Access"
        },
        "LockoutBadCount": {
            "value": "unknown",
            "target_value": "5",
            "check_type": "INF_PARSE",
            "section": "System Access"
        },
        "PasswordHistorySize": {
            "value": "unknown",
            "target_value": "24",
            "check_type": "INF_PARSE",
            "section": "System Access"
        },
    },

    # 4.b. System Services (sc.exe)
    "service_control": {
        "RemoteRegistry": {
            "value": "unknown",
            "target_value": "4", 
            "check_type": "SC_QUERY",
            "get_command": 'sc qc "RemoteRegistry"', 
            "set_command": 'sc config "RemoteRegistry" start= disabled',
        },
        "bthserv": {
            "value": "unknown",
            "target_value": "4",
            "check_type": "SC_QUERY",
            "get_command": 'sc qc "bthserv"',
            "set_command": 'sc config "bthserv" start= disabled',
        },
        "SharedAccess": {
            "value": "unknown",
            "target_value": "4",
            "check_type": "SC_QUERY",
            "get_command": 'sc qc "SharedAccess"',
            "set_command": 'sc config "SharedAccess" start= disabled',
        },
    },

    # 5. Windows Defender Firewall (netsh)
    "firewall": {
        "private_state": {
            "value": "unknown",
            "target_value": "ON",
            "check_type": "NETSH_FW",
            "get_command": 'netsh advfirewall show privateprofile state | findstr /I "State"',
            "set_command": 'netsh advfirewall set privateprofile state on',
        },
        "inbound_default": {
            "value": "unknown",
            "target_value": "BlockInboundDefault",
            "check_type": "NETSH_FW",
            "get_command": 'netsh advfirewall show allprofiles firewallpolicy | findstr /I "Inbound Default"',
            "set_command": 'netsh advfirewall set allprofiles firewallpolicy blockinbound,allowoutbound',
        }
    },

    # 3. Security Options - Rename Accounts (net user)
    "account_name": {
        "Administrator_Rename": {
            "value": "Administrator", 
            "target_value": "ProtegoAdmin",
            "check_type": "NET_USER",
            "get_command": 'net user Administrator', 
            "set_command": 'net user Administrator ProtegoAdmin',
        }
    }
}