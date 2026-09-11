# Repo Inventory

A simple Python command-line tool that scans a folder for Git repositories and prints useful information about each one.

## What It Shows

- Repo name
- Current branch
- Git status
- Repo size
- Last updated date
- Total repo count

## Usage

Run from the project folder:

```bash
python3 repo_inventory.py ~/Home/code
```
Or run from anywhere using the full script path:

```bash
python3 ~/Home/code/repo-inventory/repo_inventory.py ~/Home/code
```
if no folder is provided, it defaults to:
 ```
~/repos
```
Why I Built This

I built this as a beginner Python and Git practice project to learn how to:

scan folders with Python
run Git commands from Python
format terminal output
use Git and GitHub for version control
