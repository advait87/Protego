#!/usr/bin/env python3
# Shebang changed to be generic for Windows/Linux environments

import argparse
import sys
import os

# Adjust path for internal imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))

# Project Imports
try:
    from win_flags import win_flags
    from win_configs import strong_configs, medium_configs, easy_configs
    from windows_engine import WindowsEngine 
except ImportError as e:
    print(f"Critical Import Error: {e}. Check file names and structure.")
    sys.exit(1)


CONFIG_LEVELS = { 
    "easy": easy_configs, 
    "medium": medium_configs, 
    "strict": strong_configs 
}

def get_parameter_flag_data(parameter):
    """Retrieves the full flag data from win_flags."""
    for category in win_flags:
        if parameter in win_flags[category]:
            return win_flags[category][parameter]
    return None

def get_current_value(parameter):
    """Placeholder for fetching current live value, primarily for 'get' command."""
    # Note: For a true 'get' command in Windows, we would need to run the specific
    # get_command defined in win_flags here, similar to how check_compliance does.
    flag_data = get_parameter_flag_data(parameter)
    if flag_data:
        return flag_data.get('value', 'Value retrieval logic not fully implemented for this command.')
    return "Invalid flag"


def main():
    if sys.platform != "win32":
        # Check platform, though the Linux version handles Linux specifically.
        print("Error: This is the Windows Engine. Run the correct Protego version.")
        sys.exit(1)
        
    parser = argparse.ArgumentParser(
        prog="Protego",
        description="Protego: Windows System Hardening Tool (Annexure A Compliance)",
        epilog="Thanks for using Protego."
    )

    subparsers = parser.add_subparsers(dest='command', help='Available commands', required=True)

    # 1. GET Command
    subparser_get = subparsers.add_parser("get", help="Get the target definition/current value of a policy flag")
    subparser_get.add_argument("parameter", help="Policy name (e.g., MinimumPasswordLength)")

    # 2. CHECK Command
    subparsers.add_parser("check", help="Checks system compliance against the target policies.")

    # 3. HARDEN Command
    subparser_harden = subparsers.add_parser("harden", help="Applies hardening policies to the system.")
    subparser_harden.add_argument("--level", default="strict", choices=["easy", "medium", "strict"], 
                                   help="Hardening level to apply.")

    # 4. ROLLBACK Command
    subparsers.add_parser("rollback", help="Reverts system to the last known backup state.")


    args = parser.parse_args()

    print(f"Protego Windows Engine Initialized.")
    
    # Initialization for commands that need the Engine
    if args.command in ["harden", "check", "rollback"]:
        level = getattr(args, 'level', 'strict')
        target_config = CONFIG_LEVELS[level]
        engine = WindowsEngine(target_config, level) 
    
    # Execution Dispatch
    match args.command:
        case "get":
            # Display both current value and target value
            current_val = get_current_value(args.parameter)
            flag_data = get_parameter_flag_data(args.parameter)
            
            print(f"\nPolicy: {args.parameter}")
            print(f"  Current/Placeholder Value: {current_val}")
            if flag_data:
                print(f"  Target Value: {flag_data.get('target_value', 'N/A')}")
                print(f"  Check Type: {flag_data.get('check_type', 'N/A')}")
            else:
                print(f"Error: Parameter '{args.parameter}' not found.")
        
        case "check":
            engine.check_compliance() 

        case "harden":
            engine.harden_system()

        case "rollback":
            engine.rollback()
            
        case _:
            print("Invalid command.")

if __name__ == "__main__":
    main()