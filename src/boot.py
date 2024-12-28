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
    updateMain()
else: 
    pass
        
plugins = glob.glob('plugins/boot/*.py')

for file in plugins:
    os.system(f"sudo python {file}")
        
mon0()


os.system("sudo python menu.py")
