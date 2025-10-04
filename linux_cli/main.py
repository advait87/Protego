#!/opt/homebrew/bin/python3
import argparse
import random
import subprocess
import flags from "./flags.py"

parser = argparse.ArgumentParser(
    prog="Protego",
    description="I protect you",
    epilog="Thanks for using protego"
)
# Maybe I'll add argument_default in this to add default behaviour for the CLI without any parameters


parser.add_argument('argument', choices=["get", "set", "help", "switch_config", "list_config"])



args = parser.parse_args()

match args.argument:

