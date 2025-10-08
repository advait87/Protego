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
            if flag == args.flag:
                return [flags[category][flag], category]
    print(f"No flag named {args.flag}")

def set_flag(args):
    [flag, category] = get_flag(args)
    initial_value = flag["value"]
    if flag == 0:
        return
    if flag["value"] == args.value:
        print(f"The value of {args.flag} is already {args.value}")
        return
    try:
        sub.run(flag["set_commands"][args.value], shell=True)
        flag["value"] = args.value
        print(f"Successfully change {args.flag} from {initial_value} to {args.value}")
    except Exception as e:
        print("An error occurred while setting the parameter:")
        print(e)


def lsconfig(args):
    pprint.pprint(flags)






