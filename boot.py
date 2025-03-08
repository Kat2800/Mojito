#
#
#    --- Mojito System Loader --- 
#
# Mojito System Loader is a file that prepares everything necessary 
# to make sure that Mojito has everything to work correctly at startup.
# In this file you can see how the system loader creates a network interface in virtual monitor, 
# checks for updates randomly and runs all the plugins that need to be run at boot and then runs the menu.

from menu import *
menu()
