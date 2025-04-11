import json
from netmiko import ConnectHandler

# Open and read the JSON file
file = open("loopbacks.json", "r")
data = json.load(file)
file.close()

# Extract each loopback manually
lb1 = data["loopbacks"][0]
lb2 = data["loopbacks"][1]
lb3 = data["loopbacks"][2]

# Define router credentials
router = {
    "device_type": "cisco_ios",
    "host": "208.8.8.11",     # Replace with your router's IP
    "username": "admin",
    "password": "pass",
    "secret": "pass"
}

# Connect to router
conn = ConnectHandler(**router)
conn.enable()  # Enter privileged EXEC mode

# Configure Loopback7
print("Configuring Loopback7")
conn.send_config_set([
    f"interface {lb1['name']}",                  # Enter interface config mode
    f"ip address {lb1['ip']} 255.255.255.255",   # Set IP /32
    "no shutdown"                                # Enable interface
])

# Configure Loopback8
print("Configuring Loopback8")
conn.send_config_set([
    f"interface {lb2['name']}",
    f"ip address {lb2['ip']} 255.255.255.255",
    "no shutdown"
])

# Configure Loopback9
print("Configuring Loopback9")
conn.send_config_set([
    f"interface {lb3['name']}",
    f"ip address {lb3['ip']} 255.255.255.255",
    "no shutdown"
])

# Disconnect
conn.disconnect()
