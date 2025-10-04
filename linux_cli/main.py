#!/opt/homebrew/bin/python3
import argparse
import subprocess
import flags
import default_configs
# import flags from "./flags.py"
# import default_configs from "./default_configs.py"

parser = argparse.ArgumentParser(
    prog="Protego",
    description="I protect you",
    epilog="Thanks for using protego"
)


parser.add_argument('argument', choices=["get", "set", "help", "switch_config", "list_config"])

print(flags.flags)


args = parser.parse_args()


