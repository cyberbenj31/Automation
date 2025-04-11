import yaml
from netmiko import ConnectHandler

# Load YAML file
with open("loopbacks.yml", "r") as file:
    data = yaml.safe_load(file)

# Router connection info
router = {
    "device_type": "cisco_ios",
    "host": "208.8.8.11",  # Replace with your router's IP
    "username": "admin",
    "password": "pass",
    "secret": "pass"
}

# Connect to router
conn = ConnectHandler(**router)
conn.enable()

# Configure each loopback
for lb in data["loopbacks"]:
    print(f"\nConfiguring {lb['name']} with IP {lb['ip']}/32...")
    output = conn.send_config_set([
        f"interface {lb['name']}",
        f"ip address {lb['ip']} 255.255.255.255",
        "no shutdown"
    ])
    print(output)  # Print router response

# Disconnect
conn.disconnect()
