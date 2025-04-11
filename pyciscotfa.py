from netmiko import ConnectHandler

# Open and read the .tf file
file = open("loopbacks.tf", "r")
lines = file.readlines()
file.close()

# Create empty lists to store names and IPs
names = []
ips = []

# Go through each line to find name and ip
for line in lines:
    line = line.strip()
    if line.startswith("name"):
        name = line.split("=")[1].strip().strip('"')
        names.append(name)
    elif line.startswith("ip"):
        ip = line.split("=")[1].strip().strip('"')
        ips.append(ip)

# Define Cisco router connection info
router = {
    "device_type": "cisco_ios",
    "host": "208.8.8.11",  # Replace with your router IP
    "username": "admin",
    "password": "pass",
    "secret": "pass"
}

# Connect to the router using SSH
conn = ConnectHandler(**router)
conn.enable()  # Enter privileged EXEC mode

# Send configuration commands for each loopback
for i in range(len(names)):
    name = names[i]
    ip = ips[i]

    # Print what we're doing
    print(f"Configuring {name} with IP {ip}/32")

    # Send Cisco config commands
    conn.send_config_set([
        f"interface {name}",                     # Enter loopback interface config
        f"ip address {ip} 255.255.255.255",      # Assign IP with /32 mask
        "no shutdown"                            # Ensure interface is enabled
    ])

# Close the connection
conn.disconnect()
