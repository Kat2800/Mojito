from libs.mojstd import *
from libs.bootCheck import *
import os

def mon0():
        os.system("sudo iw wlan0 interface add mon0 type monitor")
        os.system("sudo airmon-ng start mon0")


mon0()
BootCheck() # Return True, so in case of plugin to start at boot it boot it
# execPlugins()

# returner() # uncomment for ask passowrd at boot
os.system("sudo python menu.py")
