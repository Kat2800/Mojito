import os
import subprocess
import requests
import json
import random
from libs.mojstd import *

# Nome del file di configurazione
CONFIG_FILE = "updatlist.json"

def load_repositories():
    """
    Carica la lista dei repository dal file di configurazione.
    """
    try:
        with open(CONFIG_FILE, "r") as f:
            config = json.load(f)
        return config.get("repositories", [])
    except FileNotFoundError:
        ui_print("Config File Missing.", 1)
    except json.JSONDecodeError as e:
        ui_print("Config File Error.", 1)
    return []

def get_remote_hash(repo_url):
    """
    Ottieni l'hash più recente dal repository remoto.
    """
    try:
        # URL base del repository su GitHub
        repo_api_url = repo_url.replace("https://github.com/", "https://api.github.com/repos/")
        # Ottieni informazioni sul repository per determinare il branch di default
        repo_info = requests.get(repo_api_url)
        repo_info.raise_for_status()
        default_branch = repo_info.json().get("default_branch", "main")

        # Ottieni l'hash dell'ultimo commit del branch di default
        commits_api_url = f"{repo_api_url}/commits/{default_branch}"
        response = requests.get(commits_api_url)
        response.raise_for_status()

        commit_data = response.json()
        return commit_data.get("sha")
    except requests.exceptions.RequestException as e:
        ui_print("Hash Error.", 1)
        return None

def get_local_hash(local_dir):
    """
    Ottieni l'hash più recente dal repository locale.
    """
    try:
        result = subprocess.run(
            ["git", "-C", local_dir, "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        ui_print("Local Hash Error.", 1)
        return None

def update_repo(repo_url, repo_name, local_dir):
    """
    Aggiorna il repository locale per allinearlo al repository remoto.
    """
    try:
        # Ottieni il branch di default dal repository remoto
        repo_api_url = repo_url.replace("https://github.com/", "https://api.github.com/repos/")
        repo_info = requests.get(repo_api_url)
        repo_info.raise_for_status()
        default_branch = repo_info.json().get("default_branch", "main")

        if os.path.exists(local_dir):
            # Se la directory esiste, esegui un fetch e un reset
            subprocess.run(["git", "-C", local_dir, "fetch", "--all"], check=True)
            subprocess.run(["git", "-C", local_dir, "reset", "--hard", f"origin/{default_branch}"], check=True)
        else:
            # Altrimenti clona il repository
            subprocess.run(["git", "clone", repo_url, local_dir], check=True)

        ui_print(f"{repo_name} Updated!", 1)
    except subprocess.CalledProcessError as e:
        ui_print("Update Error.", 1)

def randomCheck():
    """
    Controllo casuale per simulazioni o test.
    """
    number = random.randint(1, 10)  
    return number in [3, 4, 5, 6]

def updateMain():
    """
    Controlla e installa gli aggiornamenti.
    """
    repositories = load_repositories()

    if not repositories:
        ui_print("Everything is\n    Updated!", 1)
        return

    for repo in repositories:
        repo_name = repo.get("name", "Repository sconosciuto")
        repo_url = repo.get("url")
        local_dir = repo.get("local_dir")

        if not repo_url or not local_dir:
            ui_print(f"Missing data: {repo_name}.", 1)
            continue

        ui_print(f"Checking update for\n    {repo_name}...")

        remote_hash = get_remote_hash(repo_url)
        if not remote_hash:
            ui_print(f"Remote hash error. {repo_name}", 1)
            continue

        local_hash = get_local_hash(local_dir)
        if local_hash != remote_hash:
            ui_print(f"Update available!\n {repo_name}.", 1)
            update_repo(repo_url, repo_name, local_dir)
        else:
            ui_print(f"{repo_name}\nAlready updated!", 1)
