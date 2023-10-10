import paramiko
from netmiko import ConnectHandler
import ipaddress

# Define the old network
old_network = ipaddress.IPv4Network('OLD NETWORK RANGE')

# Define the SSH credentials and connection parameters for your VMs
ssh_credentials = {
    "username": "YOUR_SSH_CREDENTIALS",
    "password": "YOUR_SSH_CREDENTIALS",
}

# Iterate through old IP addresses
for ip in old_network.hosts():
    try:
        # Attempt to SSH into the VM
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(str(ip), **ssh_credentials)

        # If SSH is successful, update the IP address and set it as the default gateway
        new_ip = str(ip)
        config_commands = [
            f"interface eth0",
            f"ip address {new_ip} netmask {old_network.netmask}",
            f"ip route add default via {new_ip}",  # Set the new IP as the default gateway
        ]

        # SSH into the VM and apply the new IP address and default gateway configuration
        device = {
            "device_type": "linux",
            "ip": str(ip),
            **ssh_credentials,
        }
        net_connect = ConnectHandler(**device)
        net_connect.send_config_set(config_commands)
        net_connect.save_config()
        net_connect.disconnect()

        print(f"VM at {ip} updated to IP: {new_ip}, Default Gateway: {new_ip}")

    except (paramiko.AuthenticationException, paramiko.SSHException, ConnectionError):
        print(f"Failed to connect to VM at {ip}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

    # Close the SSH client for each VM
    ssh_client.close()