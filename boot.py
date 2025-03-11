#
#
#    --- Mojito System Loader ---
#        (boot.py for friends)
# Mojito System Loader is a file that prepares everything necessary
# to make sure that Mojito has everything to work correctly at startup.
# In this file you can see how the system loader runs all the plugins that need to be run at boot and then runs the menu.

from libs.mojstd import *
import os
import glob
import time

show_image("images/logo.png", lambda: time.sleep(1) or True)
plugins = glob.glob('plugins/boot/*.py')
print("before plugin")
for file in plugins:
    os.system(f"sudo python {file}")


print("before menu.py")
os.system("sudo python menu.py")
print("after menu.py")
