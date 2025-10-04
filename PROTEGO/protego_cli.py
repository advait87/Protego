# Protego/protego_cli.py

import argparse
import sys
import os

# Adjust path for internal imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'engines'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))

# Project Imports
try:
    from win_flags import WIN_FLAGS
    from win_configs import strong_configs, medium_configs, easy_configs
    from win_engine import WinEngine 
except ImportError as e:
    print(f"Critical Import Error: {e}. Check file names and structure.")
    sys.exit(1)


CONFIG_LEVELS = { 
    "easy": easy_configs, 
    "medium": medium_configs, 
    "strict": strong_configs 
}

def get_parameter_flag_data(parameter):
    """Retrieves the full flag data from WIN_FLAGS."""
    for category in WIN_FLAGS:
        if parameter in WIN_FLAGS[category]:
            return WIN_FLAGS[category][parameter]
    return None

def main():
    if sys.platform != "win32":
        print("Error: Protego Windows Engine must run on Windows.")
        sys.exit(1)
        
    parser = argparse.ArgumentParser(
        prog="Protego",
        description="Protego: Windows System Hardening Tool (Annexure A Compliance)",
        epilog="Protecting your systems automatically."
    )

    subparsers = parser.add_subparsers(dest='command', help='Available commands', required=True)

    # 1. GET Command
    subparser_get = subparsers.add_parser("get", help="Get the target definition of a policy flag")
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
        engine = WinEngine(target_config, level) 
    
    # Execution Dispatch
    match args.command:
        case "get":
            flag_data = get_parameter_flag_data(args.parameter)
            if flag_data:
                print(f"\nPolicy: {args.parameter}")
                print(f"  Target Value: {flag_data.get('target_value', 'N/A')}")
                print(f"  Check Type: {flag_data.get('check_type', 'N/A')}")
                print(f"  Check Command Example: {flag_data.get('get_command', 'N/A')}")
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