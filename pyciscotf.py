import re
from netmiko import ConnectHandler

def parse_loopbacks_from_tf(tf_file):
    with open(tf_file, "r") as f:
        content = f.read()

    blocks = re.findall(r'resource\s+"cisco_loopback"\s+".*?"\s+{(.*?)}', content, re.DOTALL)
    
    loopbacks = []
    for block in blocks:
        name = re.search(r'name\s*=\s*"([^"]+)"', block).group(1)
        ip = re.search(r'ip\s*=\s*"([^"]+)"', block).group(1)
        loopbacks.append({"name": name, "ip": ip})
    
    return loopbacks

def configure_router(loopbacks, router):
    conn = ConnectHandler(**router)
    conn.enable()

    for lb in loopbacks:
        cmds = [
            f"interface {lb['name']}",
            f"ip address {lb['ip']} 255.255.255.255",
            "no shutdown"
        ]
        print(f"Sending config for {lb['name']}")
        conn.send_config_set(cmds)
    
    conn.disconnect()

if __name__ == "__main__":
    tf_file_path = "loopbacks.tf"

    # Update these to your router's connection info
    router_info = {
        "device_type": "cisco_ios",
        "host": "208.8.8.11",
        "username": "admin",
        "password": "pass",
        "secret": "cisco"
    }

    loopbacks = parse_loopbacks_from_tf(tf_file_path)
    configure_router(loopbacks, router_info)
