import ast
from netmiko import ConnectHandler

# Read the .tf file (as plain text)
with open("loopbacks1.tf", "r") as file:
    lines = file.readlines()

# Extract the loopback list (manually without regex)
loopbacks_line = ""
for line in lines:
    if "loopbacks" in line or "[" in line or "]" in line or "{" in line or "}" in line or "=" in line or "," in line:
        loopbacks_line += line.strip().replace("loopbacks =", "")

# Convert to Python list using ast.literal_eval (safe eval)
loopbacks = ast.literal_eval(loopbacks_line)

# Router SSH details
router = {
    "device_type": "cisco_ios",
    "host": "208.8.8.11",  # Change this
    "username": "admin",
    "password": "pass",
    "secret": "pass"
}

# Connect and enter enable mode
conn = ConnectHandler(**router)
conn.enable()

# Configure each loopback
for lb in loopbacks:
    print(f"\nConfiguring {lb['name']} with IP {lb['ip']}/32...")
    output = conn.send_config_set([
        f"interface {lb['name']}",
        f"ip address {lb['ip']} 255.255.255.255",
        "no shutdown"
    ])
    print(output)

# Disconnect SSH
conn.disconnect()
