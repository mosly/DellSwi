from netmiko import ConnectHandler

user_device = input("Please enter IP address for Dell Switch: ")

device = {
    'device_type': 'dell_os6',
    'ip': user_device,
    'username': 'admin',
    'password': 'Enter Password here',
    'port': 22,
}

try:
    net_connect = ConnectHandler(**device)
    print("Connected to", device['ip'])
    
    # Get list of down ports
    output = net_connect.send_command("show interfaces status", expect_string="Port")
    down_ports = [line.split()[0] for line in output.splitlines() if "Down" in line]

    # Shut down each down portd
    for port in down_ports:
        config_commands = ["interface " + port, "shutdown", "exit"]
        output = net_connect.send_config_set(config_commands)
        print(output)

    net_connect.disconnect()
    print("Disconnected from", device['ip'])

except Exception as e:
    print("Exception occurred:", str(e))