import curses
import os
import subprocess

def menu(stdscr):
    curses.curs_set(0)  # Nasconde il cursore
    stdscr.clear()
    stdscr.refresh()
    options = ["wlan0", "wlan1", "other"]
    selected = 0

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, "--- Mojito Setup Helper ---\n")
        stdscr.addstr(1, 0, "--- Select your interface ---\n")

        for i, option in enumerate(options):
            if i == selected:
                stdscr.addstr(i + 2, 0, f"> {option}\n", curses.A_REVERSE)
            else:
                stdscr.addstr(i + 2, 0, f"  {option}\n")

        key = stdscr.getch()

        if key == curses.KEY_UP and selected > 0:
            selected -= 1
        elif key == curses.KEY_DOWN and selected < len(options) - 1:
            selected += 1
        elif key == 10:  # Invio
            break

    return options[selected]

if __name__ == "__main__":
    selected_option = curses.wrapper(menu)
    interface = None

    if selected_option == "wlan0":
        interface = "wlan0"
    elif selected_option == "wlan1":
        interface = "wlan1"
    elif selected_option == "other":
        interface = input("Write the name of your interface (E.g. wlan2): ")
    
    if interface is None:
        print("Error: No interface selected.")
        exit(1)

    os.system(f"sudo ifconfig {interface} up")

    ssid = input("Write your WiFi name (E.g. HomeWiFi): ")
    password = input("Write your WiFi password (E.g. H3ll0!): ")
    
    try:
        result = subprocess.run(
            ["nmcli", "dev", "wifi", "connect", ssid, "password", password],
            capture_output=True,
            text=True
        )
        
        if "successfully activated" in result.stdout.lower():
            print("-- Connected!")
        else:
            print("-- Can't connect to selected WiFi")
            print(result.stderr)
    except Exception as e:
        print(f"Error: {e}")

    os.system("sudo systemctl enable ssh")
    os.system("sudo systemctl start ssh")

def drivers(stdscr):
    curses.curs_set(0)  # Nasconde il cursore
    stdscr.clear()
    stdscr.refresh()

    options = ["Morrownr's drivers", "Realtek drivers", "Skip for now"]
    selected = 0

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, "Which drivers do you want to install? (REALTEK ANTENNA ONLY)\n")
        
        for i, option in enumerate(options):
            if i == selected:
                stdscr.addstr(i + 1, 0, f"> {option}\n", curses.A_REVERSE)
            else:
                stdscr.addstr(i + 1, 0, f"  {option}\n")

        key = stdscr.getch()

        if key == curses.KEY_UP and selected > 0:
            selected -= 1
        elif key == curses.KEY_DOWN and selected < len(options) - 1:
            selected += 1
        elif key == 10:
            break

    return options[selected]

selected_option1 = curses.wrapper(drivers)
driver = None

if selected_option1 == "Morrownr's drivers":
    driver = "Morrownr"
elif selected_option1 == "Realtek drivers":
    driver = "Realtek"

if driver == "Realtek":
    os.system("""
    sudo apt update
    sudo apt install realtek-rtl88xxau-dkms -y
    sudo apt install dkms
    sudo apt upgrade
    sudo reboot
    """)
elif driver == "Morrownr":
    os.system("""
    git clone https://github.com/morrownr/88x2bu-20210702.git && cd 88x2bu-20210702
    sudo bash install-driver.sh
    sudo reboot
    """)
else:
    print("Skipping driver installation...")


timezone = input("Write your time zone (E.g Europe/Amsterdam): ")
os.system(f"sudo timedatectl set-timezone {timezone}")
os.system("""
sudo apt update
sudo apt-get install libbluetooth-dev
sudo apt install python3-spidev python3-RPi.gpio
sudo pip install git+https://github.com/pybluez/pybluez
""")
os.system("""
git clone https://github.com/kovmir/l2flood && cd l2flood && make && sudo make install
""")

os.system('sudo sed -i "s/#dtparam=spi=on/dtparam=spi=on/" "/boot/config.txt"')
print("-- Almost finished! --")

os.system("""
sudo cp mojito.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable mojito.service
sudo systemctl start mojito.service
sudo hostnamectl set-hostname Mojito
sudo reboot
""")
