# STILL UNDER DEVELOPMENT 
### Ehy! We are working hard on this project! So please if you can help us! 🫰
## No release and ISO or IMG file will be made before version 1.0. Using the code now may have bugs or incomplete pieces. 💿❌ If you want to install it without a iso file, go to "How to setup and install" section.

# The Mojito Project by BlacKat

## Why is called "Mojito" like the cocktail? 🍸
This project is called "Mojito" beacuse while the developers were coding this project, they were drinking Mojitos (maked by @rickyfili10)
![Mojito](https://github.com/user-attachments/assets/b10b95f5-7286-47bb-a8e1-64bc07b0ffd4)

# What's that? 🤔
Mojito is swiss army knife for ethical hacking (educational purposes only) and penetration testing, it runs on a raspberry pi 0 w/wh that use a wavseshare 1.44 inch lcd HAT display. It has a collection of hacking tools and it is based on Kali Linux. 

# DISCLAIMER ⚠️
### Mojito is for educational purposes only. 
The authors take NO responsibility and liability for how you use any of the tools/source code/any files provided. The authors and anyone affiliated with will not be liable for any losses and/or damages in connection or other type of damages with use of ANY Tools provided with Mojito. DO NOT use Mojito if you don't have the permission to do that. <br>
We, the authors and developers of Mojito, do not guarantee that the tools inside it will work completely bug-free and we do not guarantee the safety of being anonymous/undetected when performing an attack on a device or service.

## USE IT AT YOUR OWN RISK. 

# REQUIREMENTS 📃
  - Wavseshare 1.44 inch lcd HAT display 
  - Raspberry pi 0 w/wh 
  - 16 GB sd card (You need much less, but you might need 16 GB for additional packages)
  - An external usb antenna that support packet injection and monitor mode. We recommend RTL8812BU or RTL8822BU Chipsets
  - An USB to Micro USB adapter
# HOW TO SETUP AND INSTALL MOJITO? 
## First version is not been released yet! You can see the code in the "src" folder 
1. Flash and setup kali linux for raspberry pi 0 wh  <br>{<br>
    You can get kali linux official image from: [Download Kali Linux](https://kali.download/arm-images/kali-2024.4/kali-linux-2024.4-raspberry-pi-zero-w-armel.img.xz)  <br>
    You can flash the image on the sd card using Balena Etcher. You can get it from: [Download Balena Etcher](https://etcher.balena.io) <br>
}<br>
3. Put a wpa_supplicant.conf with your wifi information inside the sd card and create a file called "ssh" with nothing inside. <br>{<br>
    Don't know how to write a wpa_supplican file? No problem! [Wpa supplicant file example](https://github.com/asparatu/raspberrypi-wpa-supplicant.conf/blob/master/wpa_supplicant.conf)<br>
}<br>
### ⚠️ REMEMBER: THE PASSWORD WILL BE ALWAYS "kali" ⚠️
4. Connect to USB port, and if you have it connect the antenna on the second port, Then wait... (The first boot is slow, don't worry it's normal!). Then, connect to it using ssh, for example:
```
ssh kali@192.168.1.xxx
```
You can see Mojito ip form your WiFi-Router.
If it doesn't seem to appear, try connecting it to an HDMI and plugging a keyboard into it to try connecting to the wifi manually.<br>

```
sudo iwconfig wlan0 up
sudo nmcli device wifi connect "{your wifi SSID}" password "{your wifi password}"
sudo enable ssh
sudo start ssh
```
5. Install and setup requisites with the commands below
## ⚠️ IF YOU HAVE ALREADY AN EXTERNAL ANTENNA THAT SUPPORT PACKET INJECTION WITH A RECOMMEND CHIPSETS BY US, INSTALL THIS ⚠️
### Else skip to Clone the Mojito repostory and enter in it 
## Method 1 (Credit to morrownr on github)
 ```
git clone https://github.com/morrownr/88x2bu-20210702.git && cd 88x2bu-20210702
 ```
 ```
sudo bash install-driver.sh
sudo reboot
 ```
### ⚠️ BE CAREFUL NOT TO BLACKLIST INSTALLED DRIVERS ⚠️
## Method 2
 ```
sudo apt update
sudo apt install realtek-rtl88xxau-dkms -y
sudo apt install dkms
sudo apt upgrade
sudo reboot
```
## Clone the Mojito repostory and enter in it 
 ```
  git clone https://github.com/rickyfili10/Mojito.git && cd Mojito/src
 ```
## Install the requisites 📃
 ```
    sudo apt update
    sudo apt-get install libbluetooth-dev
    sudo apt install python3-spidev python3-RPi.gpio
    sudo pip install git+https://github.com/pybluez/pybluez 
```
   ### <br>Set the time zone 
```
    sudo timedatectl set-timezone {your local time zone} -- EXAMPLE FOR ITALY: "sudo timedatectl set-timezone Europe/Rome"
```
  ### Install l2flood ⛓️‍💥
```
  git clone https://github.com/kovmir/l2flood
  cd l2flood
  make # Use `make serial` to build upstream l2ping.
  sudo make install
```
   ### Enabling SPi
```
sudo sed -i "s/#dtparam=spi=on/dtparam=spi=on/" "/boot/config.txt"
```   
  ### Execute Mojito at boot and set his hostname
```
  sudo cp mojito.service /etc/systemd/system/
```
```
 sudo systemctl daemon-reload
```
```
  sudo systemctl enable mojito.service
```
```
  sudo systemctl start mojito.service
```
```
  sudo hostnamectl set-hostname Mojito
```
```
  sudo reboot
```

## After a while it should display the Mojito menu! 🎉
## Remember: This is not the first version of mojito! You're using the "uncomplete" code of Mojito, it might not work and many function could not work as well
# SIMBOLS LIST: 
   - NB! = No Battery Found! <br> 
   - Plug = pluged to a power source 🔌<br>
   - N% = battery level ( not tested ) 🔋<br>
# TO DO ✔️
  [<br>
  ❌ Not implemented yet <br>
  ✔️ Implemented <br>
  ]
   - ✔️ Add wifi deauth
   - ❌ Add wifi sniff
   - ❌ Add wifi fakeAP
   - ✔️ 4 Way Handshake capture
   - ✔️ Add wifi fakeAP (Rick Roll)
   - ✔️ Fix I/O errors
   - ❌ Add Apple sideload
   - ❌ Add Apple Jailbreaker 
   - ❌ Add android rooter -> Bootloader unlocker, vbmeta flasher and sudo binary flasher (like Magisk)
   - ❌ Mojito official wiki
   - ❌ Fix Settings app
   - ❌ bluetooth spam
   - ❌ Fix all the exit buttons
   - ✔️ Plugin and app support

### Under Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International (CC BY-NC-ND 4.0) Licence 📄
  What you cannot do: ❌<br>
   - Use for non-commercial purposes 💸❌<br>
   - You cannot Create Derivative Works, but the authors permict that if you respect that: the work will be ALWAYS open source and free, and the authors will be mentionated and if the authors dosn't like what you did, you must remove it from the internet (but you can have a copy that only you can use) 📄<br>
   - Impose additional restrictions 🟰<br>
What you can do: ✔️<br> 
   - Share 🔗<br>
   - Use Mojito for educational purposes
   - Use Mojito for penetration testing (with permission)


Screen drivers based on https://github.com/Kudesnick/1.44inch-LCD-HAT-Code 💻<br>
Antenna drivers created by https://github.com/morrownr/88x2bu-20210702.git 📡<br>
⚠️ The rest of the credits will be implemented shortly ⚠️
## --- By BlacKat team. ツ ---
## Please follow us and drop a star! ⭐
