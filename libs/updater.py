import os
import subprocess

def get_local_commit_hash(repo_path):
    """Get the latest commit hash of the local Git repository."""
    if not os.path.isdir(os.path.join(repo_path, '.git')):
        raise ValueError(f"The directory {repo_path} is not a valid Git repository.")
    
    try:
        result = subprocess.run(
            ['git', '-C', repo_path, 'rev-parse', 'HEAD'],
            capture_output=True, text=True, check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Error while getting local commit hash for {repo_path}: {e.stderr}")

def get_remote_commit_hash(repo_url, branch="main"):
    """Get the latest commit hash of the remote Git repository."""
    try:
        result = subprocess.run(
            ['git', 'ls-remote', repo_url, branch],
            capture_output=True, text=True, check=True
        )
        return result.stdout.split()[0] if result.stdout else None
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Error while getting remote commit hash for {repo_url}: {e.stderr}")

def git_pull(repo_path):
    """Pull the latest changes from the remote repository."""

    try:
        subprocess.run(['git', '-C', repo_path, 'checkout', 'main'], capture_output=True, text=True, check=True)
        

        subprocess.run(['git', '-C', repo_path, 'stash'], capture_output=True, text=True, check=True)
        
    
        subprocess.run(['git', '-C', repo_path, 'pull'], capture_output=True, text=True, check=True)
    
        subprocess.run(['git', '-C', repo_path, 'stash', 'pop'], capture_output=True, text=True, check=True)
        
        print(f"Local repository at {repo_path} updated successfully.")
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Error while pulling the repository {repo_path}: {e.stderr}")

def update(file_path):
    """Check for updates and pull changes if necessary."""
    try:

        subprocess.run(
            ['git', 'config', '--global', '--add', 'safe.directory', '/home/kali/Mojito'],
            capture_output=True, text=True, check=True
        )
    except subprocess.CalledProcessError as e:
        print(f"Error while configuring Git safe directory: {e.stderr}")
    
    with open(file_path, 'r') as f:
        for line in f:
            repo_url, local_repo_path = line.strip().split(', ')
            try:
                local_hash = get_local_commit_hash(local_repo_path)
                remote_hash = get_remote_commit_hash(repo_url)

                if local_hash == remote_hash:
                    print(f"The repository {repo_url} is up to date.")
                else:
                    print(f"Updating {repo_url} (local repo: {local_repo_path})...")
                    git_pull(local_repo_path)

            except subprocess.CalledProcessError as e:
                print(f"Error executing a Git command for {repo_url}: {e.stderr}")
            except ValueError as ve:
                print(f"Error with repository path for {repo_url}: {ve}")
            except RuntimeError as re:
                print(f"Runtime error for {repo_url}: {re}")

