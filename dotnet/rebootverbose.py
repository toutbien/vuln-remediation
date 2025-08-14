import subprocess
import time
from datetime import datetime

def execute_reboot_commands(server_list, command_template, delay_seconds=30):
    """Execute reboot commands with delays between each server."""
    
    print(f"Starting reboot process at {datetime.now()}")
    print(f"Total servers: {len(server_list)}\n")
    
    for i, server in enumerate(server_list, 1):
        # Replace with actual server name
        command = command_template.replace("\\ServerName", f"\\\\{server}")
        
        print(f"[{i}/{len(server_list)}] Executing: {command}")
        
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"\\\\{server} rebooted")
            else:
                print(f"✗ {server} - Failed: {result.stderr.strip()}")
                
        except Exception as e:
            print(f"✗ {server} - Error: {str(e)}")
        
        # Wait before next server (except for the last one)
        if i < len(server_list):
            print(f"Waiting {delay_seconds} seconds...\n")
            time.sleep(delay_seconds)
    
    print(f"\nAll done at {datetime.now()}")

# The server list
servers = ["bark0929", "bark0930", "bark0931", "bark1001", "bark1002"]

# The command template  
template = "shutdown /r /m \\ServerName /t 0 /f"

# Execute with 40-second delays
execute_reboot_commands(servers, template, delay_seconds=40)
