import os
import subprocess
import requests
import json
import random
from libs.mojstd import *
# list of to-update check
CONFIG_FILE = "updatlist.json"

def load_repositories():
    """
    Load repo list
    """
    try:
        with open(CONFIG_FILE, "r") as f:
            config = json.load(f)
        return config.get("repositories", [])
    except FileNotFoundError:
        print(f"{CONFIG_FILE} not found. ")
    except json.JSONDecodeError as e:
        print(f"Error during reading {CONFIG_FILE}: {e}")
    return []

def get_remote_hash(repo_url):
    """
    See the most recent hash
    """
    api_url = repo_url.replace("https://github.com/", "https://api.github.com/repos/") + "/commits/main"
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        commit_data = response.json()
        return commit_data["sha"]
    except Exception as e:
        print(f"Error during chatching remote hash {repo_url}: {e}")
        ui_print("Hash Error.", 1)
        return None

def get_local_hash(local_dir):
    """
    See the most recent local hash
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
        print(f"Error during chatching local hash: {local_dir}. Maybe not a Git repostory?")
        ui_print("Local Hash Error.", 1)
        return None

def update_repo(repo_url, repo_name, local_dir):
    """
    Update the local repo
    """
    try:
        if os.path.exists(local_dir):
            # Se la directory esiste, esegui un pull
            subprocess.run(["git", "-C", local_dir, "fetch", "--all"], check=True)
            subprocess.run(["git", "-C", local_dir, "reset", "--hard", "origin/main"], check=True)
        else:
            # Altrimenti, clona il repository
            subprocess.run(["git", "clone", repo_url, local_dir], check=True)
        print(f"Repository {repo_name} updated!")
        ui_print(f"{repo_name} Updated!", 1)
    except subprocess.CalledProcessError as e:
        print(f"Error while updating {repo_url}: {e}")
        ui_print("Update Error.", 1)
import random

def randomCheck():
    number = random.randint(1, 10)  
    if number in [3, 4, 5, 6]:
        return True
    else:
        return False



def updateMain():
    """
    Check and install updates
    """
    print("Loading configuration...")
    repositories = load_repositories()

    if not repositories:
        print("No repo to update!")
        ui_print("Everything is\n    Updated!", 1)
        return

    for repo in repositories:
        repo_name = repo.get("name", "repository sconosciuto")
        repo_url = repo.get("url")
        local_dir = repo.get("local_dir")

        if not repo_url or not local_dir:
            print(f"Missing data: {repo_name}. Skipping...")
            ui_print(f"Missing data: {repo_name}.", 1)
            continue

        print(f"Checking update for {repo_name}...")
        ui_print(f"Checking update for\n    {repo_name}...")

        remote_hash = get_remote_hash(repo_url)
        if not remote_hash:
            print(f"Can't see remote hash: {repo_name}. Skipping...")
            ui_print(f"Remote hash error. {repo_name}", 1)
            continue

        local_hash = get_local_hash(local_dir)
        if local_hash != remote_hash:
            print(f"Update avabile! {repo_name}. ")
            ui_print(f"Update avabile!\n {repo_name}.", 1)
            update_repo(repo_url, repo_name, local_dir)
        else:
            print(f"{repo_name} alredy updated!")
            ui_print(f"{repo_name}\nAlredy updated!", 1)


