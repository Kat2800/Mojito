import curses
import os
import subprocess
import time
import textwrap
import json

moggy_faces = {
    "happy": [
        r" /\_/\  ",
        r"( ^.^ ) ",
        r" > ^ <  ",
        "\n\n\n"
    ],
    "sad": [
        r" /\_/\  ",
        r"( T_T ) ",
        r" > ^ <  ",
        "\n\n\n"
    ],
    "thinking": [
        r" /\_/\  ",
        r"( o_O ) ",
        r" > ^ <  ",
        "\n\n\n"
    ],
    "chill": [
        r" /\_/\  ",
        r"( o.o ) ",
        r" > ^ <  ",
        "\n\n\n"
    ],
    "angry": [
        r" /\_/\  ",
        r"( >_< ) ",
        r" > ^ <  ",
        "\n\n\n"
    ],
    "irritated": [
        r" /\_/\  ",
        r"( -.- ) ",
        r" > ^ <  ",
        "\n\n\n"
    ],
    "cool": [
        r" /\_/\  ",
        r"( ⌐■_■ ) ",
        r" > ^ <  ",
        "\n\n\n"
    ]
}

def moggy(message, mood="chill", stdscr=None):
    cat = moggy_faces.get(mood, moggy_faces["chill"])
    wrapped_message = textwrap.fill(message, width=50)
    msg_lines = wrapped_message.split("\n")
    max_cat_width = max(len(line) for line in cat)

    if stdscr:
        stdscr.erase()
        for i, line in enumerate(cat):
            stdscr.addstr(i, 0, line)
        for i, line in enumerate(msg_lines):
            stdscr.addstr(i + 1, max_cat_width + 2, line)
        stdscr.refresh()
    else:
        os.system("clear")
        for i in range(max(len(cat), len(msg_lines))):
            cat_part = cat[i] if i < len(cat) else " " * max_cat_width
            msg_part = msg_lines[i] if i < len(msg_lines) else ""
            print(f"{cat_part}  {msg_part}")

def menu(stdscr):
    curses.curs_set(0)
    options = ["wlan0", "wlan1", "other"]
    selected = 0

    while True:
        stdscr.clear()
        moggy("Select your interface:", "thinking", stdscr)

        for i, option in enumerate(options):
            if i == selected:
                stdscr.addstr(i + 5, 0, f"> {option}", curses.A_REVERSE)
            else:
                stdscr.addstr(i + 5, 0, f"  {option}")

        key = stdscr.getch()
        if key == curses.KEY_UP and selected > 0:
            selected -= 1
        elif key == curses.KEY_DOWN and selected < len(options) - 1:
            selected += 1
        elif key == 10:
            break

    return options[selected]
PROFILE_FILE = "myprofile.json"
def set_bluetooth_name(name="Mojito"):
    try:
        subprocess.run(["sudo", "hciconfig", "hci0", "name", name], check=True)
        with open("/etc/bluetooth/main.conf", "r+") as file:
            content = file.read()
            if "Name =" not in content:
                file.write(f"\nName = {name}\n")
        subprocess.run(["sudo", "systemctl", "restart", "bluetooth"], check=True)
    except Exception as e:
        print(e)
set_bluetooth_name()
def get_bluetooth_mac():
    try:
        result = subprocess.run(["hciconfig"], capture_output=True, text=True)
        for line in result.stdout.split("\n"):
            if "BD Address" in line:
                return line.split()[2].strip()
    except Exception as e:
        print(f"Errore nel recuperare il MAC Bluetooth: {e}")
    return "Unknown"
def load_or_create_profile():
    if os.path.exists(PROFILE_FILE):
        try:
            with open(PROFILE_FILE, "r") as file:
                profile_data = json.load(file)
                return profile_data
        except (json.JSONDecodeError, FileNotFoundError):
            pass
    
    mac_address = get_bluetooth_mac()
    moggy('Let\'s get started! What do you want to be called, little "hacker"? Write your nickname!', "cool")
    nickname = input("> ")
    
    profile_data = {
        "nickname": nickname,
        "mac_address": mac_address,
        "achievements": []
    }
    with open(PROFILE_FILE, "w") as file:
        json.dump(profile_data, file, indent=4)
    
    moggy(f"Nice to meet you, {nickname}", "happy")
    time.sleep(3)
    return profile_data
    
moggy("Hi! My name is Moggy, I will help you to set up Mojito! I am here to guide you step by step.", "happy")
time.sleep(3)

profile_data = load_or_create_profile()
selected_option = curses.wrapper(menu)
interface = selected_option if selected_option != "other" else input("Write the name of your interface (E.g. wlan2): ")

os.system(f"sudo ifconfig {interface} up")
with open("settings/settings.json", "w") as settings:
    settings_data = {"interface": interface}
    json.dump(settings_data, settings, indent=2)
moggy("Write your WiFi name (E.g. HomeWiFi): ")
ssid = input("> ")
moggy("Write your WiFi password (E.g. H3ll0!): ")
password = input("> ")

try:
    result = subprocess.run(["nmcli", "dev", "wifi", "connect", ssid, "password", password], capture_output=True, text=True, shell=True)
    if "successfully activated" in result.stdout.lower():
        moggy("Connected!", "happy")
        time.sleep(2)
        moggy("Cool password...", "cool")
        time.sleep(2)
    else:
        moggy("Can't connect to selected WiFi", "sad")
        
except Exception as e:
    moggy(f"Error: {e}", "angry")

os.system("sudo systemctl enable ssh")
os.system("sudo systemctl start ssh")

def drivers(stdscr):
    curses.curs_set(0)
    options = ["Morrownr's drivers", "Realtek drivers", "Skip for now"]
    selected = 0

    while True:
        stdscr.clear()
        moggy("Which drivers do you want to install? (REALTEK ANTENNA ONLY)", "thinking", stdscr)

        for i, option in enumerate(options):
            if i == selected:
                stdscr.addstr(i + 5, 0, f"> {option}", curses.A_REVERSE)
            else:
                stdscr.addstr(i + 5, 0, f"  {option}")

        key = stdscr.getch()
        if key == curses.KEY_UP and selected > 0:
            selected -= 1
        elif key == curses.KEY_DOWN and selected < len(options) - 1:
            selected += 1
        elif key == 10:
            break
    return options[selected]

selected_option1 = curses.wrapper(drivers)
driver = selected_option1 if selected_option1 != "Skip for now" else None

if driver == "Realtek":
    os.system("""
    sudo apt update
    sudo apt install realtek-rtl88xxau-dkms -y
    sudo apt install dkms -y
    sudo apt upgrade -y
    sudo reboot
    """)
elif driver == "Morrownr":
    os.system("""
    git clone https://github.com/morrownr/88x2bu-20210702.git && cd 88x2bu-20210702
    sudo bash install-driver.sh
    sudo reboot
    """)
else:
    moggy("Skipping driver installation...")


moggy("Write your time zone (E.g Europe/Amsterdam)", "chill")
timezone = input("> ")
os.system(f"sudo timedatectl set-timezone {timezone}")
moggy("I will install everything for you, in the meantime you can go and have a coffee or your favorite energy drink", "cool")
time.sleep(3)
os.system("""
sudo apt update
sudo apt-get install libbluetooth-dev -y
sudo apt install python3-spidev python3-RPi.gpio -y
sudo pip install git+https://github.com/pybluez/pybluez
""")
os.system("""
git clone https://github.com/kovmir/l2flood && cd l2flood && make && sudo make install
""")

os.system('sudo sed -i "s/#dtparam=spi=on/dtparam=spi=on/" "/boot/config.txt"')
moggy("-- Almost finished! --", "happy")

os.system("""
sudo cp mojito.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable mojito.service
sudo systemctl start mojito.service
sudo hostnamectl set-hostname Mojito
sudo reboot
""")
