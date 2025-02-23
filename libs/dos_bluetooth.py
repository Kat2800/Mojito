
import subprocess
from functools import lru_cache

mac_addrs = set()
current_mac = None

@lru_cache(maxsize=236)
class dos:

    def __init__(self):
        self.result = subprocess.run(["sudo", "btmgmt", "find"], stdout=subprocess.PIPE)

    def scan_mac_addrs(self):
        output = self.result.stdout.decode('utf-8')

        # Trova i MAC address nell'output
        for line in output.splitlines():
            parts = line.split()

            if "dev_found" in line.lower():  # Il MAC address è prima di "type"
                current_mac = parts[2]  # Il MAC address è la seconda parola
                # Verifica che sia un MAC address valido
                if len(current_mac.split(":")) == 6:
                    mac_addrs.add(current_mac)  # Aggiungi solo il MAC address

            elif "name" in line.lower() and current_mac:
                name = line.split(maxsplit=1)[1]
                mac_addrs.discard(current_mac)  # Rimuove il MAC senza nome
                mac_addrs.add(f"{current_mac} {name}")  # Aggiunge MAC + nome
                current_mac = None

        # Stampa i MAC address trovati
        print(*mac_addrs)

    def main(self):
        self.scan_mac_addrs()

dos().main()
