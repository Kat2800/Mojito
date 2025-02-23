import RPi.GPIO as GPIO
from PIL import Image, ImageDraw, ImageFont
import sys
import time
import os
import hashlib
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # THIS IS FOR IMPORT THE SCREEN DRIVERS WITH import LCD_1in44
import LCD_1in44
import json  
# Pin setup
KEY_UP_PIN = 6
KEY_DOWN_PIN = 19
KEY_LEFT_PIN = 5
KEY_RIGHT_PIN = 26
KEY_PRESS_PIN = 13
KEY1_PIN = 21
KEY2_PIN = 20
KEY3_PIN = 16

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(KEY_UP_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(KEY_DOWN_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(KEY_LEFT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(KEY_RIGHT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(KEY_PRESS_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(KEY1_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(KEY2_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(KEY3_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)



# Initialize display
# Assume that LCD_1in44 is correctly imported and configured
disp = LCD_1in44.LCD()
Lcd_ScanDir = LCD_1in44.SCAN_DIR_DFT
disp.LCD_Init(Lcd_ScanDir)
disp.LCD_Clear()

# Create blank image for drawing
width = 128
height = 128
image = Image.new('RGB', (width, height))
draw = ImageDraw.Draw(image)
font = ImageFont.load_default()



def system_info():
    try:
        # Apri il file info.json
        with open('setting/info.json', 'r') as f:
            info = json.load(f)

        # Crea il messaggio da mostrare (modifica in base ai contenuti del file JSON)
        system_info_message = (
            f"System Info:\n"
            f"Version: {info.get('version', 'N/A')}\n"
            f"Setting version: {info.get('settings', 'N/A')}\n"
            f"Authors: {info.get('author', '@rickyfili10, @Lif28')}\n"
        )
        show_message(system_info_message, 5)  # Mostra le informazioni per 5 secondi

    except FileNotFoundError:
        show_message("info.json not found!", 3)  # Messaggio di errore se il file non esiste
    except json.JSONDecodeError:
        show_message("Error reading info.json", 3)  # Messaggio di errore se il file è corrotto
def generate_key_from_password(password: str) -> bytes:
    """Genera una chiave AES a partire dalla password."""
    return hashlib.sha256(password.encode()).digest()

def encrypt_message(message: str, key: bytes) -> bytes:
    """Cripta un messaggio usando una chiave e restituisce il testo cifrato."""
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_message = padder.update(message.encode()) + padder.finalize()
    encrypted_message = encryptor.update(padded_message) + encryptor.finalize()
    return iv + encrypted_message

def write_encrypted_message_to_file(file_path: str, message: str, key: bytes):
    """Cripta un messaggio e lo scrive in un file."""

    encrypted_message = encrypt_message(message, key)
    with open(file_path, 'wb') as file:
        file.write(encrypted_message)
def decrypt_message(encrypted_message: bytes, key: bytes) -> str:
    """Decifra un messaggio usando una chiave e restituisce il testo in chiaro."""
    iv = encrypted_message[:16]
    encrypted_message = encrypted_message[16:]
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_message = decryptor.update(encrypted_message) + decryptor.finalize()
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    try:
        message = unpadder.update(padded_message) + unpadder.finalize()
        return message.decode()
    except ValueError:
        pass
def setPsk():
    # Definisci il messaggio da criptare e la chiave per la cifratura
    original_message = "mojito"
    show_message("Create the new password:", 3)
    password = get_keyboard_input()  # Password per generare la chiave AES
    key = generate_key_from_password(password)

    # Scrivi il messaggio criptato nel file psk.txt
    write_encrypted_message_to_file("psk.txt", original_message, key)
    show_message("Password Saved.", 3)
def read_encrypted_message_from_file(file_path: str) -> bytes:
    """Legge un messaggio criptato da un file."""
    with open(file_path, 'rb') as file:
        return file.read()
def returner():
    psk_try = 0
    max_tries = 4
    if os.path.exists("psk.txt"):
        encrypted_message = read_encrypted_message_from_file("psk.txt")

        while psk_try < max_tries:
            show_message("Password Required.", 1)
            user_password = get_keyboard_input()
            user_key = generate_key_from_password(user_password)

            try:
                decrypted_message = decrypt_message(encrypted_message, user_key)

                if decrypted_message == "mojito":
                    show_message("Login in...", 1)
                    break

                else:
                    show_message("Wrong password", 1)
                    psk_try += 1
            except ValueError as e:
                show_message(str(e))
                psk_try += 1


    else:
        setPsk()




def draw_menu(selected_index):
    draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
    menu_options = ["Wifi", "SSH", "Password", "Info", "Exit"]
    for i, option in enumerate(menu_options):
        y = i * 20
        if i == selected_index:
            text_size = draw.textbbox((0, 0), option, font=font)
            text_width = text_size[2] - text_size[0]
            text_height = text_size[3] - text_size[1]
            draw.rectangle((0, y, width, y + text_height), fill=(0, 255, 0))
            draw.text((1, y), option, font=font, fill=(0, 0, 0))
        else:
            draw.text((1, y), option, font=font, fill=(255, 255, 255))
    disp.LCD_ShowImage(image, 0, 0)

def draw_sub_menu(selected_index):
    sub_menu_options = ["Connect WiFi", "Disconnect WiFi", "My WiFi", "Exit"]
    draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
    for i, option in enumerate(sub_menu_options):
        y = i * 20
        if i == selected_index:
            text_size = draw.textbbox((0, 0), option, font=font)
            text_width = text_size[2] - text_size[0]
            text_height = text_size[3] - text_size[1]
            draw.rectangle((0, y, width, y + text_height), fill=(0, 255, 0))
            draw.text((1, y), option, font=font, fill=(0, 0, 0))
        else:
            draw.text((1, y), option, font=font, fill=(255, 255, 255))
    disp.LCD_ShowImage(image, 0, 0)

def show_message(message, duration=2):
    draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
    draw.text((10, 50), message, font=font, fill=(255, 255, 255))
    disp.LCD_ShowImage(image, 0, 0)
    time.sleep(duration)
    disp.LCD_Clear()

def draw_keyboard(selected_key_index, input_text, mode="alpha", caps_lock=False):
    if mode == "alpha":
        keys = [
            '1', '2', '3', '4', '5', '6', '7', '8', '9', '0',
            'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p',
            'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';',
            'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/',
            ' ', 'DEL', '⏎', "!#1", "CAPS"
        ]
    else:  # special characters mode
        keys = [
            '!', '"', '£', '$', '%', '&', '/', '(', ')', '=',
            '?', '^', '@', '#', '_', '-', '+', '{', '}', '\\',
            '[', ']', '*', ':', ';', "'", '<', '>', '|', '~',
            ' ', 'DEL', '⏎', "ABC", "CAPS"
        ]

    if caps_lock:
        keys = [key.upper() if key.isalpha() else key for key in keys]

    key_width = 12
    key_height = 12
    cols = 10

    # Clear previous image
    draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))

    # Draw the current input text
    draw.text((0, 0), input_text, font=font, fill=(255, 255, 255))

    # Draw the keyboard
    for i, key in enumerate(keys):
        col = i % cols
        row = i // cols
        x = col * key_width
        y = (row + 1) * key_height  # Start drawing from second row
        if i == selected_key_index:
            draw.rectangle((x, y, x + key_width, y + key_height), fill=(0, 255, 0))  # Highlight selected key
            draw.text((x + 2, y + 2), key, font=font, fill=(0, 0, 0))
        else:
            draw.rectangle((x, y, x + key_width, y + key_height), outline=(255, 255, 255))
            draw.text((x + 2, y + 2), key, font=font, fill=(255, 255, 255))

    # Display the updated image
    disp.LCD_ShowImage(image, 0, 0)

def get_keyboard_input():
    alpha_keys = [
        '1', '2', '3', '4', '5', '6', '7', '8', '9', '0',
        'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p',
        'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';',
        'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/',
        ' ', 'DEL', '⏎', "!#1", "CAPS"
    ]
    special_keys = [
        '!', '"', '£', '$', '%', '&', '/', '(', ')', '=',
        '?', '^', '@', '#', '_', '-', '+', '{', '}', '\\',
        '[', ']', '*', ':', ';', "'", '<', '>', '|', '~',
        ' ', 'DEL', '⏎', "ABC", "CAPS"
    ]

    input_text = ""
    selected_key_index = 0
    mode = "alpha"
    caps_lock = False

    draw_keyboard(selected_key_index, input_text, mode, caps_lock)

    while True:
        if GPIO.input(KEY_UP_PIN) == 0:
            selected_key_index = (selected_key_index - 10) % len(alpha_keys)
            draw_keyboard(selected_key_index, input_text, mode, caps_lock)
            time.sleep(0.3)
        if GPIO.input(KEY_DOWN_PIN) == 0:
            selected_key_index = (selected_key_index + 10) % len(alpha_keys)
            draw_keyboard(selected_key_index, input_text, mode, caps_lock)
            time.sleep(0.3)
        if GPIO.input(KEY_LEFT_PIN) == 0:
            selected_key_index = (selected_key_index - 1) % len(alpha_keys)
            draw_keyboard(selected_key_index, input_text, mode, caps_lock)
            time.sleep(0.3)
        if GPIO.input(KEY_RIGHT_PIN) == 0:
            selected_key_index = (selected_key_index + 1) % len(alpha_keys)
            draw_keyboard(selected_key_index, input_text, mode, caps_lock)
            time.sleep(0.3)

        # Verifica dell'input dei tasti speciali
        if GPIO.input(KEY1_PIN) == 0:  # Se KEY1 (P21) è premuto, cancella l'ultimo carattere
            input_text = input_text[:-1]
            draw_keyboard(selected_key_index, input_text, mode, caps_lock)
            time.sleep(0.3)
        
        if GPIO.input(KEY2_PIN) == 0:  # Se KEY2 (P20) è premuto, aggiungi uno spazio
            input_text += ' '
            draw_keyboard(selected_key_index, input_text, mode, caps_lock)
            time.sleep(0.3)

        if GPIO.input(KEY3_PIN) == 0:  # Se KEY3 (P16) è premuto, conferma l'input
            return input_text

        # Gestione dell'input del pulsante di selezione (KEY_PRESS_PIN)
        if GPIO.input(KEY_PRESS_PIN) == 0:
            key = alpha_keys[selected_key_index] if mode == "alpha" else special_keys[selected_key_index]
            if key == "DEL":
                input_text = input_text[:-1]
            elif key == "⏎":
                return input_text
            elif key == "!#1":
                mode = "special" if mode == "alpha" else "alpha"
            elif key == "CAPS":
                caps_lock = not caps_lock
            elif key == "ABC":
                mode = "alpha" if mode == "special" else "special"
            else:
                input_text += key.upper() if caps_lock else key

            draw_keyboard(selected_key_index, input_text, mode, caps_lock)
            time.sleep(0.3)

while True:
    selected_index = 0
    draw_menu(selected_index)

    while True:
        if GPIO.input(KEY_UP_PIN) == 0:
            selected_index = (selected_index - 1) % 4
            draw_menu(selected_index)
            time.sleep(0.3)
        if GPIO.input(KEY_DOWN_PIN) == 0:
            selected_index = (selected_index + 1) % 4
            draw_menu(selected_index)
            time.sleep(0.3)
        if GPIO.input(KEY_PRESS_PIN) == 0:
            selected_option = ["Wifi", "SSH", "Password", "Exit"][selected_index]
            show_message(f"Selected: {selected_option}", 1)

            if selected_option == "Wifi":
                sub_selected_index = 0
                while True:
                    draw_sub_menu(sub_selected_index)
                    if GPIO.input(KEY_UP_PIN) == 0:
                        sub_selected_index = (sub_selected_index - 1) % 4
                        draw_sub_menu(sub_selected_index)
                        time.sleep(0.3)
                    if GPIO.input(KEY_DOWN_PIN) == 0:
                        sub_selected_index = (sub_selected_index + 1) % 4
                        draw_sub_menu(sub_selected_index)
                        time.sleep(0.3)
                    if GPIO.input(KEY_PRESS_PIN) == 0:
                        sub_selected_option = ["Connect WiFi", "Disconnect WiFi", "My WiFi", "Exit"][sub_selected_index]
                        show_message(f"Selected: {sub_selected_option}", 1)

                        if sub_selected_option == "Connect WiFi":
                            show_message("Insert WiFi name:", 3)
                            wifiName = get_keyboard_input()
                            show_message("Insert Password\nEnter for Null", 3)
                            wifiPassword = get_keyboard_input()
                            os.system("sudo ifconfig wlan0 up")
                            os.system(f"sudo nmcli device wifi connect {wifiName} password '{wifiPassword}'")
                            getWifiName = os.popen("nmcli -t -f active,ssid dev wifi | grep '^yes' | cut -d':' -f2").read().strip()
                            show_message(f"Connected to:\n{getWifiName}", 3)
                        elif sub_selected_option == "Disconnect WiFi":
                            show_message("Type 'yes' to\ndisconnect", 3)
                            yes = get_keyboard_input()
                            if yes == 'yes':
                                os.system("sudo nmcli device disconnect wlan0")
                                show_message("Disconnected", 3)
                            else:
                                show_message("Stopped", 3)
                        elif sub_selected_option == "My WiFi":
                            getWifiName = os.popen("nmcli -t -f active,ssid dev wifi | grep '^yes' | cut -d':' -f2").read().strip()
                            show_message(f"Connected to:\n{getWifiName}", 3)
                        elif sub_selected_index == "Exit":
                            break
            if selected_option == "SSH":
                sub_selected_index = 0
                while True:
                    draw_sub_menu(sub_selected_index)
                    if GPIO.input(KEY_UP_PIN) == 0:
                        sub_selected_index = (sub_selected_index - 1) % 4
                        draw_sub_menu(sub_selected_index)
                        time.sleep(0.3)
                    if GPIO.input(KEY_DOWN_PIN) == 0:
                        sub_selected_index = (sub_selected_index + 1) % 4
                        draw_sub_menu(sub_selected_index)
                        time.sleep(0.3)
                    if GPIO.input(KEY_PRESS_PIN) == 0:
                        sub_selected_option = ["Enable SSH", "Disable SSH", "Exit"][sub_selected_index]
                        show_message(f"Selected: {sub_selected_option}", 1)

                        if sub_selected_option == "Enable SSH":
                            returner()
                            os.system("sudo systemctl enable ssh")
                            show_message("SSH Enabled.", 3)
                        if sub_selected_index == "Disbale SSH":
                            returner()
                            os.system("SSH Disable", 3)
                            show_message("SSH Disabled", 3)
                        elif sub_selected_option == "Exit":
                            break
            if selected_option == "Password":
                returner()
                setPsk()
            elif selected_option == "Exit":
                os.system("sudo python /home/kali/mojito/src/menu.py")  # Exit the main menu
            if selected_option == "Info":
                system_info()

