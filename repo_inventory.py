from pathlib import Path
import subprocess
import shutil
from datetime import datetime
import argparse

def get_args():
    parser = argparse.ArgumentParser(description="Scan a folder and show Git repo information.")
    parser.add_argument(
        "path",
        nargs="?",
        default=DEFAULT_REPOS_DIR,
        help="Folder to scan for Git repositories. Defaults to ~/repos."
    )
    return parser.parse_args()

DEFAULT_REPOS_DIR = Path.home() / "repos"


def run_git_command(repo_path, command):
    try:
        result = subprocess.run(
            ["git", "-C", str(repo_path), *command],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            return result.stdout.strip()
        return None
    except subprocess.TimeoutExpired:
        return None


def is_git_repo(path):
    return (path / ".git").exists()


def get_repo_size(path):
    total_size = 0

    for item in path.rglob("*"):
        try:
            if item.is_file():
                total_size += item.stat().st_size
        except OSError:
            pass

    size_mb = total_size / (1024 * 1024)
    return f"{size_mb:.1f} MB"


def get_last_updated(path):
    try:
        modified_time = path.stat().st_mtime
        return datetime.fromtimestamp(modified_time).strftime("%Y-%m-%d %H:%M")
    except OSError:
        return "Unknown"


def get_repo_info(repo_path):
    status_output = run_git_command(repo_path, ["status", "--short"])
    branch = run_git_command(repo_path, ["branch", "--show-current"])
    remote = run_git_command(repo_path, ["remote", "get-url", "origin"])

    if status_output:
        status = "Uncommitted changes"
    else:
        status = "Clean"

    return {
        "name": repo_path.name,
        "last_updated": get_last_updated(repo_path),
        "status": status,
        "branch": branch or "Unknown",
        "size": get_repo_size(repo_path),
        "remote": remote or "No remote"
    }


def find_repos(repos_dir):
    repos = []

    if not repos_dir.exists():
        print(f"Could not find repos folder: {repos_dir}")
        return repos

    for item in repos_dir.iterdir():
        if item.is_dir() and is_git_repo(item):
            repos.append(get_repo_info(item))

    return sorted(repos, key=lambda repo: repo["name"].lower())


def print_repos(repos, repos_dir):
    if not repos:
        print("No Git repos found.")
        return

    divider = "-" * 80

    print()
    print(f"Repos found in {repos_dir}")
    print(divider)
    print(f"{'Repo':<20} {'Branch':<12} {'Status':<22} {'Size':<10} {'Updated':<16}")
    print(divider)
    

    for repo in repos:
        print(f"{repo['name']:<20} {repo['branch']:<12} {repo['status']:<22} {repo['size']:<10} {repo['last_updated']:<16}")
        print(divider)
        print(f"Total repos: {len(repos)}")

def main():
    args = get_args()
    repos_dir = Path(args.path).expanduser()
    repos = find_repos(repos_dir)
    print_repos(repos, repos_dir)


if __name__ == "__main__":
    main()