import requests
import ipaddress

# Function for counting first and last IP from range CIDR ip
def get_ip_range(cidr):
    network = ipaddress.IPv4Network(cidr, strict=False)
    first_ip = str(network.network_address + 1)  # IP pertama setelah network address
    last_ip = str(network.network_address + network.num_addresses - 2)  # Last IP Address
    return first_ip, last_ip

# Function for ask input from user
def get_user_input():
    cookies = input("Input Your Cookies: ")
    investigation_id = input("Input Investigation ID: ")
    session_id = input("Input Session ID: ")
    return cookies, investigation_id, session_id

# Function for running command XSOAR
def run_xsoar_command(cookies, investigation_id, session_id, first_ip, last_ip, ip_range_name):
    url = "https://XSOAR_URL/xsoar/entry"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Cookie": cookies,
    }
    data = {
        "id": "",
        "version": 0,
        "investigationId": investigation_id,
        "data": f"!checkpoint-address-range-add ip_address_first={first_ip} ip_address_last={last_ip} name=\"{ip_range_name}\" session_id={session_id} groups=\"Malicious IP From SOC Notification\""
    }

    response = requests.post(url, json=data, headers=headers, verify=False)
    if response.status_code == 200:
        print(f"Success adding IP range {ip_range_name}")
    else:
        print(f"Error detected: {response.status_code} - {response.text}")

# Function for read IP Address range from file
def process_ip_list(ip_file):
    with open(ip_file, "r") as file:
        ip_ranges = file.readlines()
    return [ip.strip() for ip in ip_ranges]

# Main function
def main():
    # Ask input from user
    cookies, investigation_id, session_id = get_user_input()

    # Read file ip ranges
    ip_file = "ip_ranges.txt"  # Change with your file name
    ip_ranges = process_ip_list(ip_file)

    # Loop by IP range and run command
    for ip_range in ip_ranges:
        print(f"Processing IP range: {ip_range}")
        first_ip, last_ip = get_ip_range(ip_range)
        ip_range_name = ip_range  # Name IP range
        run_xsoar_command(cookies, investigation_id, session_id, first_ip, last_ip, ip_range_name)

if __name__ == "__main__":
    main()

