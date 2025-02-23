#
#
#    --- Mojito System Loader --- 
#
# Mojito System Loader is a file that prepares everything necessary 
# to make sure that Mojito has everything to work correctly at startup.
# In this file you can see how the system loader creates a network interface in virtual monitor, 
# checks for updates randomly and runs all the plugins that need to be run at boot and then runs the menu.

from libs.mojstd import *
from libs.updater import *
import os
import glob
import time
clear()
show_image("images/logo.png", exit_event=lambda: time.sleep(1) or True)
plugins = glob.glob('plugins/boot/*.py')

for file in plugins:
    os.system(f"sudo python {file}")



os.system("sudo python menu.py")
