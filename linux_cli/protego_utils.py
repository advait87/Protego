from all_flags import flags
import subprocess as sub
import pprint

def print_all_flags():
    for category in flags:
        print(category + ":")
        for flag in flags[category]:
            print(flags[category][flag])


def print_flag(args):
    [flag, category] = get_flag(args)
    if flag != 0:
        print(f"The flag {args.flag} is in category {category}")
        print(flag)
        return

    print(f"No flag named {args.flag}")
    return [0, 0]


def get_flag(args):
    for category in flags:
        for flag in flags[category]:
            print(flags[category], flag, args.flag)

            if flag == args.flag:
                return [flags[category][flag], category]
    return [0, 0]

def set_flag(args):
    [flag, category] = get_flag(args)
    print(args.value)
    if flag == 0:
        print(f"No flag named {args.flag}")
        return
    initial_value = flag["value"]
    value = args.value
    if value == "_":
        while True:
            value = input(f"({"/".join(flag["values"])})")
            if value != "":
                return

    if flag["value"] == value:
        print(f"The value of {args.flag} is already {value}")
        return
    if value not in flag["values"]:
        print(f"Invalid value for the parameter {args.flag}")
    try:
        sub.run(flag["set_commands"][value], shell=True)
        flag["value"] = value
        print(f"Successfully change {args.flag} from {initial_value} to {value}")
    except Exception as e:
        print("An error occurred while setting the parameter:")
        print(e)


def lsconfig(args):
    pprint.pprint(flags)






