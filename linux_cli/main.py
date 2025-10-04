#!/opt/homebrew/bin/python3
# Change the above line, I think we can do which python3 on the target system and add the path above

import argparse
import subprocess
import flags
import default_configs

parser = argparse.ArgumentParser(
    prog="Protego",
    description="I protect you",
    epilog="Thanks for using protego"
)

subparsers = parser.add_subparsers(dest='command', help='Available commands', required=True)

subparser_get = subparsers.add_parser("get", help="Get the current value of a parameter")
subparser_get.add_argument("parameter")




args = parser.parse_args()

def get_parameter(parameter):
    for category in flags.flags:
        if parameter in flags.flags[category]:
            return flags.flags[category][parameter]["value"]
    return "Invalid flag"

if args.command == "get":
    print(args)
match args.command:
    case "get":
        print(get_parameter(args.parameter))
    case _:
        print("Invalid command")


