flags = {
        "filesystem": {
            "cramfs": {
                "value": "yes",
                "values": ["yes", "no", "unknown"],
                "get_command": "sudo modprobe| grep modprobe",
                "set_commands": {
                    "yes": "sudo apt update && sudo apt install cramfs",
                    "no": "sudo modprobe -r cramfs"
                },
                "recommended_value": "no"
            },
            "freevxfs": {
                "value": "unknown",
                "values": ["yes", "no", "unknown"],
                "get_command": "if [sudo modprobe | grep freevxfs]; then echo \"True\" else echo \"False\" fi",
                "set_commands": {
                    "yes": "sudo apt update && sudo apt install ",
                "recommended_value": "no"
                }
            }
        }
}

