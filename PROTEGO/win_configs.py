# Protego/win_configs.py

strong_configs = {
    # 1. Account Policies 
    "account_policy": [
        "PasswordHistorySize", 
        "MaximumPasswordAge", 
        "MinimumPasswordLength", 
        "LockoutBadCount"
    ],
    # 4.b. System Services 
    "service_control": [
        "RemoteRegistry", 
        "bthserv", 
        "Browser",
        "SharedAccess"
    ],
    # 5. Firewall 
    "firewall": [
        "private_state", 
        "public_state",
        "inbound_default"
    ],
    # 3. Security Options (Rename)
    "account_name": [
        "Administrator_Rename"
    ]
}

medium_configs = {
    "account_policy": [
        "MinimumPasswordLength", 
        "LockoutBadCount"
    ],
    "service_control": [
        "RemoteRegistry"
    ],
    "firewall": [
        "private_state"
    ],
}

easy_configs = {
    "account_policy": [
        "MinimumPasswordLength"
    ]
}