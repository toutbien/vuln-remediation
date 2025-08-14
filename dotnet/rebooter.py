import subprocess
import time
from datetime import datetime

def create_and_execute_reboot_commands(server_list, command_template, delay_seconds=30):
    """
    Create and execute reboot commands from server list with delays.
    
    Args:
        server_list: List of server names
        command_template: Command template with \\ServerName placeholder
        delay_seconds: Delay between executions (default 30 seconds)
    """
    
    print(f"Starting reboot process at {datetime.now()}")
    print(f"Total servers: {len(server_list)}")
    print(f"Delay between reboots: {delay_seconds} seconds\n")
    
    for i, server in enumerate(server_list, 1):
        # Replace placeholder with actual server name
        command = command_template.replace("\\ServerName", f"\\\\{server}")
        
        print(f"[{i}/{len(server_list)}] Executing: {command}")
        
        try:
            # Execute the command
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"✓ Command successful for {server}")
            else:
                print(f"✗ Command failed for {server}: {result.stderr.strip()}")
                
        except Exception as e:
            print(f"✗ Error executing command for {server}: {str(e)}")
        
        # Wait before next command (except for the last server)
        if i < len(server_list):
            print(f"Waiting {delay_seconds} seconds before next server...\n")
            time.sleep(delay_seconds)
    
    print(f"Reboot process completed at {datetime.now()}")

def preview_commands(server_list, command_template):
    """Preview the commands that will be executed without running them."""
    print("Commands that will be executed:")
    print("-" * 50)
    for i, server in enumerate(server_list, 1):
        command = command_template.replace("\\ServerName", f"\\\\{server}")
        print(f"{i}. {command}")
    print("-" * 50)

# Add Server list here ("name1", "name2") etc
servers = ["bark0929", "bark0930", "bark0931", "bark1001", "bark1002"]

#CLI to verify
template = "shutdown /r /m \\ServerName /t 0 /f"

# Preview the commands 
preview_commands(servers, template)

# Ask for confirmation before executing
response = input(f"\nExecute these commands with 30-second delays? (yes/no): ").lower().strip()

if response == 'yes' or response == 'y':
    create_and_execute_reboot_commands(servers, template, delay_seconds=30)
else:
    print("Operation cancelled.")
