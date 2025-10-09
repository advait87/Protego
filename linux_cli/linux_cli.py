##!/bin/python3
import argparse
import protego_utils as pu

parser = argparse.ArgumentParser()

subparsers = parser.add_subparsers()


get_parser = subparsers.add_parser("get")
get_parser.add_argument("--flag", "-f", type=str, required=True)
get_parser.set_defaults(func=pu.print_flag)

set_parser = subparsers.add_parser("set")
set_parser.add_argument("--flag", "-f", type=str, required=True)
set_parser.add_argument("--value", "-v", type=str, default="_")
set_parser.set_defaults(func=pu.set_flag)


lsconfig_parser = subparsers.add_parser("lsconfig")
lsconfig_parser.set_defaults(func=pu.lsconfig)








arguments = parser.parse_args()
arguments.func(arguments)
