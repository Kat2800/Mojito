import RPi.GPIO as GPIO
from PIL import Image, ImageDraw, ImageFont
import LCD_1in44
import time
import os
import subprocess
import psutil
import json
# Network settings
BROADCAST_IP = '<broadcast>'
PORT = 12345  # Port


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
disp = LCD_1in44.LCD()
Lcd_ScanDir = LCD_1in44.SCAN_DIR_DFT
disp.LCD_Init(Lcd_ScanDir)
disp.LCD_Clear()

def list_files_in_directory(directory):
    """List all files in the specified directory without extensions."""
    return [os.path.splitext(f)[0] for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

def draw_file_menu(files, selected_index):
    """Draw the file menu on the display in a grid format."""
    draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))

    # Definire dimensioni della griglia
    num_cols = 3  # Numero di colonne
    num_rows = 4  # Numero di righe
    item_width = width // num_cols
    item_height = 20  # Altezza dell'elemento, puoi modificarlo se necessario

    for i, file in enumerate(files):
        col = i % num_cols
        row = i // num_cols
        x = col * item_width
        y = row * item_height

        if i == selected_index:
            text_size = draw.textbbox((0, 0), file, font=font)
            text_width = text_size[2] - text_size[0]
            text_height = text_size[3] - text_size[1]
            draw.rectangle((x, y, x + item_width, y + item_height), fill=(0, 255, 0))  # Evidenziare lo sfondo
            draw.text((x + 1, y + 1), file, font=font, fill=(0, 0, 0))  # Testo in nero
        else:
            draw.text((x + 1, y + 1), file, font=font, fill=(255, 255, 255))  # Testo in bianco

    disp.LCD_ShowImage(image, 0, 0)

def execute_file(directory, file_base):
    """Execute the file based on its base name by searching its extension."""
    file_extensions = ['.py', '.sh', '.moj']  # Definisci le estensioni supportate
    for ext in file_extensions:
        file_path = os.path.join(directory, file_base + ext)
        if os.path.exists(file_path):
            if ext == '.py':
                subprocess.run(['sudo', 'python3', file_path])
            elif ext == '.sh':
                subprocess.run(['sudo', 'bash', file_path])
            elif ext == ".moj":
                subprocess.run(['sudo', './', file_path])
            return
    # Se il file non ha una delle estensioni supportate
    ui_print(f"Unsupported file: {file_base}")

def show_file_menu():
    directory = "app/"  # Modifica questo percorso con il percorso corretto
    files = list_files_in_directory(directory)
    selected_index = 0
    num_cols = 3  # Numero di colonne
    num_rows = 4  # Numero di righe

    def draw_file_menu(files, selected_index, num_cols, num_rows):
        num_items = len(files)

        # Calcola le dimensioni delle celle
        cell_width = width // num_cols
        cell_height = height // num_rows

        draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))

        for i, file in enumerate(files):
            y = (i // num_cols) * cell_height
            x = (i % num_cols) * cell_width
            if i == selected_index:
                draw.rectangle((x, y, x + cell_width, y + cell_height), fill=(0, 255, 0))  # Evidenzia
                draw.text((x + 2, y + 2), file, font=font, fill=(0, 0, 0))  # Testo in nero
            else:
                draw.text((x + 2, y + 2), file, font=font, fill=(255, 255, 255))  # Testo in bianco

        disp.LCD_ShowImage(image, 0, 0)

    draw_file_menu(files, selected_index, num_cols, num_rows)

    while True:
        if GPIO.input(KEY_UP_PIN) == 0:
            selected_index = (selected_index - num_cols) % len(files)
            draw_file_menu(files, selected_index, num_cols, num_rows)
            time.sleep(0.3)
        if GPIO.input(KEY_DOWN_PIN) == 0:
            selected_index = (selected_index + num_cols) % len(files)
            draw_file_menu(files, selected_index, num_cols, num_rows)
            time.sleep(0.3)
        if GPIO.input(KEY_LEFT_PIN) == 0:
            selected_index = (selected_index - 1) % len(files)
            draw_file_menu(files, selected_index, num_cols, num_rows)
            time.sleep(0.3)
        if GPIO.input(KEY_RIGHT_PIN) == 0:
            selected_index = (selected_index + 1) % len(files)
            draw_file_menu(files, selected_index, num_cols, num_rows)
            time.sleep(0.3)
        if GPIO.input(KEY_PRESS_PIN) == 0:
            selected_file = files[selected_index]
            ui_print(f"Selected: {selected_file}", 1)
            # Esegui l'azione sul file selezionato
            execute_file(directory, selected_file)  # Passa solo il nome base del file
            break
        if GPIO.input(KEY1_PIN) == 0:
            break
        if GPIO.input(KEY2_PIN) == 0:
            break
        if GPIO.input(KEY3_PIN) == 0:
            break

# Create blank image for drawing
width = 128
height = 128
image = Image.new('RGB', (width, height))

# Get drawing object to draw on image
draw = ImageDraw.Draw(image)
font = ImageFont.load_default()

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
def getinput(): 
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

def YesNo(selected_key_index, mode="alpha"):
    # Impostazioni per il disegno della schermata
    width, height = 320, 240  # Risoluzione dello schermo (adatta questa dimensione al tuo schermo)
    
    # Clear previous image
    draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))

    # Crea i tasti "Yes" e "No"
    button_width = 100
    button_height = 50
    center_x = width // 2
    center_y = height // 2

    # Posizioni dei tasti "Yes" e "No" (disposti orizzontalmente)
    yes_x = center_x - button_width - 20  # "Yes" si sposterà a sinistra
    no_x = center_x + 20  # "No" sarà a destra del centro
    button_y = center_y - button_height // 2  # Verticalmente centrato

    # Disegna i tasti con il cursore selezionato
    if selected_key_index == 0:
        draw.rectangle((yes_x, button_y, yes_x + button_width, button_y + button_height), fill=(0, 255, 0))  # Tasto Yes selezionato
        draw.text((yes_x + 20, button_y + 15), "Yes", font=font, fill=(0, 0, 0))
        draw.rectangle((no_x, button_y, no_x + button_width, button_y + button_height), outline=(255, 255, 255))  # Tasto No non selezionato
        draw.text((no_x + 20, button_y + 15), "No", font=font, fill=(255, 255, 255))
    else:
        draw.rectangle((yes_x, button_y, yes_x + button_width, button_y + button_height), outline=(255, 255, 255))  # Tasto Yes non selezionato
        draw.text((yes_x + 20, button_y + 15), "Yes", font=font, fill=(255, 255, 255))
        draw.rectangle((no_x, button_y, no_x + button_width, button_y + button_height), fill=(0, 255, 0))  # Tasto No selezionato
        draw.text((no_x + 20, button_y + 15), "No", font=font, fill=(0, 0, 0))

    # Display the updated image
    disp.LCD_ShowImage(image, 0, 0)
def getYesNo():
    selected_key_index = 0  # Inizialmente selezionato "Yes"
    while True:
        draw_keyboard(selected_key_index)

        # Navigazione tra i tasti (cambia selezione tra "Yes" e "No")
        if GPIO.input(KEY_LEFT_PIN) == 0:  # Se l'utente preme il tasto sinistro, seleziona "Yes"
            selected_key_index = 0
            time.sleep(0.3)
        if GPIO.input(KEY_RIGHT_PIN) == 0:  # Se l'utente preme il tasto destro, seleziona "No"
            selected_key_index = 1
            time.sleep(0.3)

        # Conferma la selezione
        if GPIO.input(KEY_PRESS_PIN) == 0:  # Quando l'utente preme il tasto di conferma
            if selected_key_index == 0:
                return "Yes"
            elif selected_key_index == 1:
                return "No"
            time.sleep(0.3)

# Menu options
#menu_options = ["Networks","Bluetooth", "Settings", "Reboot", "Shutdown"]
#selected_index = 0

def show_image(image_path, exit_event=None):
    image = Image.open(image_path)
    image = image.resize((128, 128))  # Resize the image to fit the display if necessary

    disp.LCD_Clear()  # Clear the display
    disp.LCD_ShowImage(image, 0, 0)  # Show the image on the display

    # Wait for exit event (e.g., button press or timeout)
    while True:
        if exit_event is not None and exit_event():
            break  # Exit the loop if exit event occurs
        time.sleep(0.1)  # Adjust sleep time as needed

    disp.LCD_Clear()  # Clear the display after exit

def get_battery_level():
    battery = psutil.sensors_battery()
    if battery is None:
        return None, None  # Nessuna batteria rilevata
    percent = battery.percent
    is_plugged = battery.power_plugged
    return percent, is_plugged

"""def draw_menu(selected_index):
    # Clear previous image

    # Clear screen
    draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))

    # Aggiungi l'orario in alto a destra
    current_time = time.strftime("%H:%M")  # Formato 24h HH:MM
    draw.text((width - 40, 0), current_time, font=font, fill=(255, 255, 255))  # Orario in alto a destra

    # Ottieni il livello della batteria
    battery_level, plugged_in = get_battery_level()

    # Visualizza messaggio sul livello della batteria o "NB!" a sinistra
    if battery_level is None:
        draw.text((5, 0), "NB!", font=font, fill=(255, 0, 0))  # Messaggio di errore a sinistra
    else:
        if plugged_in:
            draw.text((5, 0), "PLUG", font=font, fill=(255, 255, 255))  # Messaggio "PLUG" a sinistra
        else:
            draw.text((5, 0), f"{battery_level}%", font=font, fill=(255, 255, 255))  # Livello della batteria a sinistra

    # Imposta il numero massimo di opzioni visibili
    max_visible_options = 6
    # Calcola l'offset di scorrimento in base all'opzione selezionata
    scroll_offset = max(0, min(selected_index - max_visible_options + 1, len(menu_options) - max_visible_options))

    # Ottieni le opzioni visibili nella finestra di visualizzazione
    visible_options = menu_options[scroll_offset:scroll_offset + max_visible_options]

    # Disegna le opzioni del menu con scorrimento
    menu_offset = 16  # Offset per iniziare a disegnare il menu più in basso
    for i, option in enumerate(visible_options):
        y = (i * 20) + menu_offset  # Spaziatura tra le opzioni con l'offset

        # Evidenzia l'opzione selezionata
        if scroll_offset + i == selected_index:
            text_size = draw.textbbox((0, 0), option, font=font)
            text_width = text_size[2] - text_size[0]
            text_height = text_size[3] - text_size[1]
            draw.rectangle((0, y, width, y + text_height), fill=(50, 205, 50))  # Evidenzia sfondo
            draw.text((1, y), option, font=font, fill=(0, 0, 0))  # Testo in nero
        else:
            draw.text((1, y), option, font=font, fill=(255, 255, 255))  # Testo in bianco

    # Display the updated image
    disp.LCD_ShowImage(image, 0, 0)"""



def ui_print(message, duration=2):
    draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))  # Clear previous image
    draw.text((10, 50), message, font=font, fill=(255, 255, 255))
    disp.LCD_ShowImage(image, 0, 0)
    if duration != "unclear":
        time.sleep(duration)
        disp.LCD_Clear()
def screen_clear():
    disp.LCD_Clear()
def bk(): # Back Keys
    if GPIO.input(KEY1_PIN) == 0:
        return True
    if GPIO.input(KEY2_PIN) == 0:
        return True
    if GPIO.input(KEY3_PIN) == 0:
        return True
    
def draw_sub_menu(selected_index, menu_options):
    # Clear previous image

    # Clear screen
    draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))

    # Aggiungi l'orario in alto a destra
    current_time = time.strftime("%H:%M")  # Formato 24h HH:MM
    draw.text((width - 40, 0), current_time, font=font, fill=(255, 255, 255))  # Orario in alto a destra

    # Ottieni il livello della batteria
    battery_level, plugged_in = get_battery_level()

    # Visualizza messaggio sul livello della batteria o "NB!" a sinistra
    if battery_level is None:
        draw.text((5, 0), "NB!", font=font, fill=(255, 0, 0))  # Messaggio di errore a sinistra
    else:
        if plugged_in:
            draw.text((5, 0), "PLUG", font=font, fill=(255, 255, 255))  # Messaggio "PLUG" a sinistra
        else:
            draw.text((5, 0), f"{battery_level}%", font=font, fill=(255, 255, 255))  # Livello della batteria a sinistra

    # Imposta il numero massimo di opzioni visibili
    max_visible_options = 6
    # Calcola l'offset di scorrimento in base all'opzione selezionata
    scroll_offset = max(0, min(selected_index - max_visible_options + 1, len(menu_options) - max_visible_options))

    # Ottieni le opzioni visibili nella finestra di visualizzazione
    visible_options = menu_options[scroll_offset:scroll_offset + max_visible_options]

    # Disegna le opzioni del menu con scorrimento
    menu_offset = 16  # Offset per iniziare a disegnare il menu più in basso
    for i, option in enumerate(visible_options):
        y = (i * 20) + menu_offset  # Spaziatura tra le opzioni con l'offset

        # Evidenzia l'opzione selezionata
        if scroll_offset + i == selected_index:
            text_size = draw.textbbox((0, 0), option, font=font)
            text_width = text_size[2] - text_size[0]
            text_height = text_size[3] - text_size[1]
            draw.rectangle((0, y, width, y + text_height), fill=(50, 205, 50))  # Evidenzia sfondo
            draw.text((1, y), option, font=font, fill=(0, 0, 0))  # Testo in nero
        else:
            draw.text((1, y), option, font=font, fill=(255, 255, 255))  # Testo in bianco

    # Display the updated image
    disp.LCD_ShowImage(image, 0, 0)


def mc(menu_options): # Menu Configuration, don't confuse this with Mc Donald.
    # Clear previous image

    # Clear screen
    draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))

    # Aggiungi l'orario in alto a destra
    current_time = time.strftime("%H:%M")  # Formato 24h HH:MM
    draw.text((width - 40, 0), current_time, font=font, fill=(255, 255, 255))  # Orario in alto a destra

    # Ottieni il livello della batteria
    battery_level, plugged_in = get_battery_level()

    # Visualizza messaggio sul livello della batteria o "NB!" a sinistra
    if battery_level is None:
        draw.text((5, 0), "NB!", font=font, fill=(255, 0, 0))  # Messaggio di errore a sinistra
    else:
        if plugged_in:
            draw.text((5, 0), "PLUG", font=font, fill=(255, 255, 255))  # Messaggio "PLUG" a sinistra
        else:
            draw.text((5, 0), f"{battery_level}%", font=font, fill=(255, 255, 255))  # Livello della batteria a sinistra

    # Imposta il numero massimo di opzioni visibili
    max_visible_options = 6
    # Calcola l'offset di scorrimento in base all'opzione selezionata
    scroll_offset = max(0, min(selected_index - max_visible_options + 1, len(menu_options) - max_visible_options))

    # Ottieni le opzioni visibili nella finestra di visualizzazione
    visible_options = menu_options[scroll_offset:scroll_offset + max_visible_options]

    # Disegna le opzioni del menu con scorrimento
    menu_offset = 16  # Offset per iniziare a disegnare il menu più in basso
    for i, option in enumerate(visible_options):
        y = (i * 20) + menu_offset  # Spaziatura tra le opzioni con l'offset

        # Evidenzia l'opzione selezionata
        if scroll_offset + i == selected_index:
            text_size = draw.textbbox((0, 0), option, font=font)
            text_width = text_size[2] - text_size[0]
            text_height = text_size[3] - text_size[1]
            draw.rectangle((0, y, width, y + text_height), fill=(read_theme_color()))  # Evidenzia sfondo
            draw.text((1, y), option, font=font, fill=(0, 0, 0))  # Testo in nero
        else:
            draw.text((1, y), option, font=font, fill=(255, 255, 255))  # Testo in bianco

    # Display the updated image
    disp.LCD_ShowImage(image, 0, 0)




def list(menu_options):
    # Clear previous image

    # Clear screen
    draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))

    max_visible_options = 7
    # Calcola l'offset di scorrimento in base all'opzione selezionata
    scroll_offset = max(0, min(selected_index - max_visible_options + 1, len(menu_options) - max_visible_options))

    # Ottieni le opzioni visibili nella finestra di visualizzazione
    visible_options = menu_options[scroll_offset:scroll_offset + max_visible_options]

    # Disegna le opzioni del menu con scorrimento
    menu_offset = 16  # Offset per iniziare a disegnare il menu più in basso
    for i, option in enumerate(visible_options):
        y = (i * 20) + menu_offset  # Spaziatura tra le opzioni con l'offset

        # Evidenzia l'opzione selezionata
        if scroll_offset + i == selected_index:
            text_size = draw.textbbox((0, 0), option, font=font)
            text_width = text_size[2] - text_size[0]
            text_height = text_size[3] - text_size[1]
            draw.rectangle((0, y, width, y + text_height), fill=(read_theme_color()))  # Evidenzia sfondo
            draw.text((1, y), option, font=font, fill=(0, 0, 0))  # Testo in nero
        else:
            draw.text((1, y), option, font=font, fill=(255, 255, 255))  # Testo in bianco

    # Display the updated image
    disp.LCD_ShowImage(image, 0, 0)
