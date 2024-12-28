import os
import subprocess
import requests
import json
import random
try:
    import mojstd
except ImportError:
    try:
        import libs.mojstd
    except ImportError:
         ui_print("Mojstd not found", 1)

# Configuration file name
CONFIG_FILE = "updatlist.json"

def load_repositories():
    """
    Load the list of repositories from the configuration file.
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
    Get the most recent hash from the remote repository.
    """
    try:
        # Base URL of the repository on GitHub
        repo_api_url = repo_url.replace("https://github.com/", "https://api.github.com/repos/")
        # Get repository information to determine the default branch
        repo_info = requests.get(repo_api_url)
        repo_info.raise_for_status()
        default_branch = repo_info.json().get("default_branch", "main")

        # Get the hash of the latest commit from the default branch
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
    Get the most recent hash from the local repository.
    """
    try:
        result = subprocess.run(
            ["sudo", "git", "-C", local_dir, "rev-parse", "HEAD"],
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
    Aggiorna la directory del repository locale per allinearla al repository remoto.
    """
    try:
        # Ottieni informazioni sul ramo predefinito
        repo_api_url = repo_url.replace("https://github.com/", "https://api.github.com/repos/")
        repo_info = requests.get(repo_api_url)
        repo_info.raise_for_status()
        default_branch = repo_info.json().get("default_branch", "main")

        # Controlla se la directory esiste
        src_dir = os.path.join(local_dir, "src")
        if os.path.exists(local_dir):
            # Aggiorna il repository
            subprocess.run(["sudo", "git", "-C", local_dir, "fetch", "--all"], check=True)
            subprocess.run(["sudo", "git", "-C", local_dir, "reset", "--hard", f"origin/{default_branch}"], check=True)
        else:
            # Clona il repository se non esiste
            subprocess.run(["sudo", "git", "clone", repo_url, local_dir], check=True)

        # Controlla che la directory src/ sia aggiornata
        if not os.path.exists(src_dir):
            ui_print(f"Directory 'src/' non trovata in {repo_name}.", 1)
        else:
            ui_print(f"Tutti i file e le directory in 'src/' sono aggiornati per {repo_name}.", 0)

        ui_print(f"{repo_name} Updated!", 1)
    except subprocess.CalledProcessError as e:
        ui_print(f"Update Error: {e}", 1)


def randomCheck():
    """
    Random check for simulations or testing.
    """
    number = random.randint(1, 10)  
    return number in [3, 4, 5, 6]

def updateMain():
    """
    Check and install updates.
    """
    repositories = load_repositories()

    if not repositories:
        ui_print("Everything is\n    Updated!", 1)
        return

    for repo in repositories:
        repo_name = repo.get("name", "Unknown Repository")
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
