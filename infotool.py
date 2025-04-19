import sys
import requests
import json
import socket

def get_ip_address(url):
    try:
        ip_address = socket.gethostbyname(url)
        return ip_address
    except socket.gaierror:
        return None

def get_location_info(ip_address):
    try:
        response = requests.get(f"https://ipinfo.io/{ip_address}/json")
        return response.json()
    except requests.RequestException:
        return None

def main():
    if len(sys.argv) != 2:
        print("Usage: python infotool.py <websiteurl>")
        sys.exit(1)

    website_url = sys.argv[1]
    ip_address = get_ip_address(website_url)

    if ip_address is None:
        print(f"Could not resolve IP address for {website_url}")
        sys.exit(1)

    location_info = get_location_info(ip_address)

    if location_info is None:
        print(f"Could not retrieve location information for IP address {ip_address}")
        sys.exit(1)

    print(json.dumps(location_info, indent=4))

if __name__ == "__main__":
    main()
