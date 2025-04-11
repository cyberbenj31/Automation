import json
from netmiko import ConnectHandler

# Load loopback config from JSON file
with open("loopbacks.json", "r") as f:
    data = json.load(f)

# Router connection info (update IP/credentials)
router = {
    "device_type": "cisco_ios",
    "host": "208.8.8.11",
    "username": "admin",
    "password": "pass",
    "secret": "pass"
}

# Connect to router
conn = ConnectHandler(**router)
conn.enable()  # Enter privileged EXEC mode

# Loop over loopbacks and configure each one
for lb in data["loopbacks"]:
    print(f"\nConfiguring {lb['name']} with IP {lb['ip']}/32...")
    output = conn.send_config_set([
        f"interface {lb['name']}",                    # Enter loopback interface
        f"ip address {lb['ip']} 255.255.255.255",     # Set /32 IP address
        "no shutdown"                                 # Enable the interface
    ])
    print(output)  # Show command output from the router

# Disconnect from router
conn.disconnect()
