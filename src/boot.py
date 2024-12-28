#
#
#    --- Mojito System Loader --- 
#
# Mojito System Loader is a file that prepares everything necessary 
# to make sure that Mojito has everything to work correctly at startup.
# In this file you can see how the system loader creates a network interface in virtual monitor, 
# checks for updates randomly and runs all the plugins that need to be run at boot and then runs the menu.


from libs.mojstd import *
from libs.bootCheck import *
from libs.updater import *
import os
import glob

def mon0():
        os.system("sudo iw wlan0 interface add mon0 type monitor")
        os.system("sudo airmon-ng start mon0")

if randomCheck():
    ui_print("Checking for\n   Updates...", 1)
        
else: 
    pass
mon0()        
plugins = glob.glob('plugins/boot/*.py')

for file in plugins:
    os.system(f"sudo python {file}")



os.system("sudo python menu.py")
