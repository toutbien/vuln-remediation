def create_reboot_commands(server_list, command_template):
    """Simple function to create reboot commands from server list."""
    commands = []
    for server in server_list:
        command = command_template.replace("\\ServerName", f"\\\\{server}")
        commands.append(command)
    return commands

# Your server list
servers = ["bark0929", "bark0930", "bark0931", "bark1001", "bark1002"]

# Your command template
template = "shutdown /r /m \\ServerName /t 0 /f"

# Generate commands
reboot_commands = create_reboot_commands(servers, template)

# Print or save commands
for cmd in reboot_commands:
    print(cmd)
