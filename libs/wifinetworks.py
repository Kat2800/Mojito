
from wifi import Cell
import json
from functools import lru_cache

# Initialize WiFi adapter

INTERFACE = json.load(open("/home/kali/Mojito/settings/settings.json", "r"))["interface"]

class wifi_info():
    def __init__(self, INTERFACE):
        self.adapter = Cell.all(INTERFACE)

    #clear chache
    #@lru_cache(maxsize=128)
    def info(self):
        
        wifi_data = []

        for cell in self.adapter:
            bssid = cell.address
            
            if not any(entry['bssid'] == bssid for entry in wifi_data):
                ssid = cell.ssid
                signal = cell.signal
                mode = cell.mode
                chan = cell.channel
                rate = cell.quality
                security = cell.encryption_type
            

                #take the info for each ''for'' and store them into thefinaldict        
                thefinaldict = {
                "bssid" : bssid,
                "ssid"  : ssid,
                #"mode"  : mode,
                "chan"  : chan,
                #"rate"  : rate,
                #"signal" : signal,
                #"security" : security
            }    
            
            #store all the info collected in thefinaldict              
            wifi_data.append(thefinaldict)
            #print(thefinaldict) enable this by removing # for debugging
            
        with open("wifiinfo.json", mode="w") as a:
            json.dump(wifi_data, a, indent=2)
   
    def main(self):
        self.info()

