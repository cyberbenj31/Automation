import yaml
from netmiko import ConnectHandler

# Load the YAML file
file = open("loopbacks.yml", "r")
data = yaml.safe_load(file)
file.close()

# Extract each loopback manually
lb1 = data["loopbacks"][0]
lb2 = data["loopbacks"][1]
lb3 = data["loopbacks"][2]

# Device login info
router = {
    "device_type": "cisco_ios",
    "host": "208.8.8.11",     # Replace with actual router IP
    "username": "admin",
    "password": "pass",
    "secret": "pass"
}

# Connect to router
conn = ConnectHandler(**router)
conn.enable()  # Enter enable/privileged mode

# Configure Loopback4
print("Configuring Loopback4")
conn.send_config_set([
    f"interface {lb1['name']}",              # Go to interface Loopback1
    f"ip address {lb1['ip']} 255.255.255.255",  # Assign IP address
    "no shutdown"                            # Enable the interface
])

# Configure Loopback5
print("Configuring Loopback5")
conn.send_config_set([
    f"interface {lb2['name']}",
    f"ip address {lb2['ip']} 255.255.255.255",
    "no shutdown"
])

# Configure Loopback6
print("Configuring Loopback6")
conn.send_config_set([
    f"interface {lb3['name']}",
    f"ip address {lb3['ip']} 255.255.255.255",
    "no shutdown"
])

# Disconnect from router
conn.disconnect()
