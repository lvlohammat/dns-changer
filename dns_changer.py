import os
import subprocess
import json

dns_file = 'dns_servers.json'
favorites_file = 'favorites.json'
RED = "\033[31m"
GREEN = "\033[32m"
ORANGE = "\033[33m"
RESET = "\033[0m"
support_info = {
    "Bitcoin": "your-bitcoin-address",
    "Ethereum": "your-ethereum-address",
    "Litecoin": "your-litecoin-address"
}

def load_dns_servers():
    if os.path.exists(dns_file):
        with open(dns_file, 'r') as file:
            return json.load(file)
    else:
        return {
            "Shecan.ir": ["178.22.122.100", "185.51.200.2"],
            "Begzar.ir": ["185.55.225.25", "185.55.226.26"],
            "403.online": ["10.202.10.202", "10.202.10.102"],
            "Radar.game": ["10.202.10.10", "10.202.10.11"],
            "electrotm.org": ["78.157.42.100", "78.157.42.101"],
            "Google": ["8.8.8.8", "8.8.4.4"],
            "Control D": ["76.76.2.0", "76.76.10.0"],
            "Quad9": ["9.9.9.9", "149.112.112.112"],
            "OpenDNS Home": ["208.67.222.222", "208.67.220.220"],
            "Cloudflare": ["1.1.1.1", "1.0.0.1"],
            "AdGuard DNS": ["94.140.14.14", "94.140.15.15"],
            "CleanBrowsing": ["185.228.168.9", "185.228.169.9"],
            "Alternate DNS": ["76.76.19.19", "76.223.122.150"]
        }

def load_favorites():
    if os.path.exists(favorites_file):
        with open(favorites_file, 'r') as file:
            return json.load(file)
    else:
        return []

def save_favorites(favorites):
    with open(favorites_file, 'w') as file:
        json.dump(favorites, file, indent=4)

def save_dns_servers(dns_servers):
    with open(dns_file, 'w') as file:
        json.dump(dns_servers, file, indent=4)

def get_active_connection():
    result = subprocess.run(["nmcli", "-t", "-f", "DEVICE,STATE", "device", "status"], capture_output=True, text=True)
    lines = result.stdout.strip().split('\n')
    for line in lines:
        device, state = line.split(':')
        if state == "connected":
            return device
    return None

def set_dns(connection_name, dns, dns_servers, lang):
    os.system(f'sudo resolvectl dns {connection_name} ""')
    for server in dns_servers[dns]:
        os.system(f'sudo resolvectl dns {connection_name} {server}')
    if lang == "fa":
        print(GREEN + f"DNS با موفقیت به {dns} تغییر یافت!" + RESET)
    else:
        print(GREEN + f"DNS successfully changed to {dns}!" + RESET)

def clear_dns(connection_name, lang):
    os.system(f'sudo resolvectl dns {connection_name} ""')
    if lang == "fa":
        print(RED + "تنظیمات DNS پاک شد!" + RESET)
    else:
        print(RED + "DNS settings cleared!" + RESET)

def add_dns(dns_servers, lang):
    if lang == "fa":
        name = input("نام DNS جدید را وارد کنید: ")
        servers = input("آدرس‌های DNS جدید را با کاما جدا کنید (به عنوان مثال: 1.1.1.1, 1.0.0.1): ").split(',')
        dns_servers[name] = [server.strip() for server in servers]
        save_dns_servers(dns_servers)
        print(GREEN + f"DNS جدید {name} با موفقیت اضافه شد!" + RESET)
    else:
        name = input("Enter the name of the new DNS: ")
        servers = input("Enter the new DNS addresses separated by commas (e.g., 1.1.1.1, 1.0.0.1): ").split(',')
        dns_servers[name] = [server.strip() for server in servers]
        save_dns_servers(dns_servers)
        print(GREEN + f"New DNS {name} added successfully!" + RESET)

def add_to_favorites(favorites, dns, lang):
    if dns not in favorites:
        favorites.append(dns)
        save_favorites(favorites)
        if lang == "fa":
            print(GREEN + f"{dns} به موارد علاقه اضافه شد!" + RESET)
        else:
            print(GREEN + f"{dns} added to favorites!" + RESET)
    else:
        if lang == "fa":
            print(RED + f"{dns} قبلاً در موارد علاقه بوده است!" + RESET)
        else:
            print(RED + f"{dns} is already in favorites!" + RESET)

def show_favorites(favorites, dns_servers, lang):
    if lang == "fa":
        print("موارد علاقه:")
    else:
        print("Favorites:")
    for idx, name in enumerate(favorites):
        print(f"{idx + 1}. {name} - {', '.join(dns_servers[name])}")

def ping_dns(dns_server):
    result = subprocess.run(["ping", "-c", "1", dns_server], capture_output=True, text=True)
    if result.returncode == 0:
        return float(result.stdout.split('time=')[1].split(' ms')[0])
    return float('inf')

def sort_dns_by_ping(dns_servers):
    dns_pings = {}
    for name, servers in dns_servers.items():
        pings = [ping_dns(server) for server in servers]
        dns_pings[name] = min(pings)
    sorted_dns = sorted(dns_pings, key=dns_pings.get)
    return {name: dns_servers[name] for name in sorted_dns}

def show_support_info(support_info, lang):
    if lang == "fa":
        print("حمایت از سازنده برنامه:")
    else:
        print("Support the developer:")
    for currency, address in support_info.items():
        print(f"{ORANGE}{currency}: {address}{RESET}")

def display_sorted_dns(dns_servers, lang, connection_name):
    while True:
        if lang == "fa":
            print(GREEN + "DNS ها بر اساس پینگ مرتب شدند!" + RESET)
            print("لیست DNS ها:")
            for idx, name in enumerate(dns_servers):
                print(f"{idx + 1}. {name}")
            print("0. بازگشت")
            choice = input("یک DNS را انتخاب کنید یا 0 را برای بازگشت وارد کنید: ")
        else:
            print(GREEN + "DNS sorted by ping!" + RESET)
            print("DNS list:")
            for idx, name in enumerate(dns_servers):
                print(f"{idx + 1}. {name}")
            print("0. Back")
            choice = input("Select a DNS or enter 0 to go back: ")

        if choice == "0":
            return
        elif choice.isdigit() and 1 <= int(choice) <= len(dns_servers):
            set_dns(connection_name, list(dns_servers.keys())[int(choice) - 1], dns_servers, lang)
        else:
            if lang == "fa":
                print(RED + "انتخاب نامعتبر است، دوباره امتحان کنید." + RESET)
            else:
                print(RED + "Invalid selection, please try again." + RESET)

def main():
    dns_servers = load_dns_servers()
    favorites = load_favorites()
    connection_name = get_active_connection()

    if connection_name is None:
        print(RED + "اتصال شبکه فعالی پیدا نشد." + RESET)
        exit(1)

    print("Choose your language:")
    print("1. English")
    print("2. فارسی")
    lang_choice = input("Select your language (1 or 2): ")

    if lang_choice == "2":
        lang = "fa"
    else:
        lang = "en"

    while True:
        if lang == "fa":
            print("\nمنوی DNS:")
            print("1. تغییر DNS")
            print("2. پاک کردن DNS")
            print("3. افزودن DNS جدید")
            print("4. افزودن به موارد علاقه")
            print("5. نمایش موارد علاقه")
            print("6. مرتب‌سازی DNS ها بر اساس پینگ")
            print("7. حمایت از سازنده برنامه")
            print("8. خروج")
            choice = input("انتخاب شما: ")
        else:
            print("\nDNS Menu:")
            print("1. Change DNS")
            print("2. Clear DNS")
            print("3. Add New DNS")
            print("4. Add to Favorites")
            print("5. Show Favorites")
            print("6. Sort DNS by Ping")
            print("7. Support the Developer")
            print("8. Exit")
            choice = input("Your choice: ")

        if choice == "1":
            if lang == "fa":
                print("لیست DNS ها:")
                for idx, name in enumerate(dns_servers):
                    print(f"{idx + 1}. {name}")
                dns_choice = input("یک DNS را انتخاب کنید: ")
            else:
                print("DNS list:")
                for idx, name in enumerate(dns_servers):
                    print(f"{idx + 1}. {name}")
                dns_choice = input("Select a DNS: ")
            if dns_choice.isdigit() and 1 <= int(dns_choice) <= len(dns_servers):
                set_dns(connection_name, list(dns_servers.keys())[int(dns_choice) - 1], dns_servers, lang)
            else:
                if lang == "fa":
                    print(RED + "انتخاب نامعتبر است، دوباره امتحان کنید." + RESET)
                else:
                    print(RED + "Invalid selection, please try again." + RESET)
        elif choice == "2":
            clear_dns(connection_name, lang)
        elif choice == "3":
            add_dns(dns_servers, lang)
        elif choice == "4":
            if lang == "fa":
                print("لیست DNS ها:")
                for idx, name in enumerate(dns_servers):
                    print(f"{idx + 1}. {name}")
                dns_choice = input("یک DNS را انتخاب کنید: ")
            else:
                print("DNS list:")
                for idx, name in enumerate(dns_servers):
                    print(f"{idx + 1}. {name}")
                dns_choice = input("Select a DNS: ")
            if dns_choice.isdigit() and 1 <= int(dns_choice) <= len(dns_servers):
                add_to_favorites(favorites, list(dns_servers.keys())[int(dns_choice) - 1], lang)
            else:
                if lang == "fa":
                    print(RED + "انتخاب نامعتبر است، دوباره امتحان کنید." + RESET)
                else:
                    print(RED + "Invalid selection, please try again." + RESET)
        elif choice == "5":
            show_favorites(favorites, dns_servers, lang)
        elif choice == "6":
            if lang == "fa":
                print(ORANGE + "در حال مرتب‌سازی DNS ها بر اساس پینگ..." + RESET)
            else:
                print(ORANGE + "Sorting DNS by ping..." + RESET)
            sorted_dns_servers = sort_dns_by_ping(dns_servers)
            display_sorted_dns(sorted_dns_servers, lang, connection_name)
        elif choice == "7":
            show_support_info(support_info, lang)
        elif choice == "8":
            break
        else:
            if lang == "fa":
                print(RED + "انتخاب نامعتبر است، دوباره امتحان کنید." + RESET)
            else:
                print(RED + "Invalid selection, please try again." + RESET)

if __name__ == "__main__":
    main()
