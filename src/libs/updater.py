import os
import subprocess

def get_local_commit_hash(repo_path):
    if not os.path.isdir(os.path.join(repo_path, '.git')):
        raise ValueError(f"The directory {repo_path} is not a valid Git repository.")
    
    result = subprocess.run(
        ['sudo', 'git', '-C', repo_path, 'rev-parse', 'HEAD'],
        capture_output=True, text=True, check=True
    )
    return result.stdout.strip()

def get_remote_commit_hash(repo_url, branch="main"):
    result = subprocess.run(
        ['sudo', 'git', 'ls-remote', repo_url, branch],
        capture_output=True, text=True, check=True
    )
    return result.stdout.split()[0]

def git_pull(repo_path, remote_url):
    result = subprocess.run(
        ['sudo', 'git', '-C', repo_path, 'pull', remote_url],
        capture_output=True, text=True, check=True
    )
    print(f"Local repository updated successfully:\n{result.stdout}")

def update(file_path):
    with open(file_path, 'r') as f:
        for line in f:
            repo_url, local_repo_path = line.strip().split(', ')
            try:
                local_hash = get_local_commit_hash(local_repo_path)
                remote_hash = get_remote_commit_hash(repo_url)

                if local_hash == remote_hash:
                    print(f"The repositories for {repo_url} are identical (the last commits match).")
                else:
                    print(f"The repositories for {repo_url} are different (the last commits do not match).")
                    print(f"Performing git pull to update the local repository at {local_repo_path}...")
                    git_pull(local_repo_path, repo_url)

            except subprocess.CalledProcessError as e:
                print(f"Error executing a Git command for {repo_url}: {e}")
            except ValueError as ve:
                print(f"Error with repository path for {repo_url}: {ve}")

# Path to the file containing repository URLs and paths
repos_file_path = '/home/kali/Mojito/src/repos.txt'

update(repos_file_path)
