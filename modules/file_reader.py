import os
from pathlib import Path
from pathspec import PathSpec
from pathspec.patterns import GitWildMatchPattern

IGNORE_DIRS = {'__pycache__'}

def read_gitignore(gitignore_path):
    gitignore = []
    if gitignore_path.exists():
        with open(gitignore_path, "r") as file:
            gitignore = file.readlines()

    return [line.strip() for line in gitignore]

def read_all_code_files(project_path="."):
    gitignore = read_gitignore(Path(project_path) / ".gitignore")
    spec = PathSpec.from_lines(GitWildMatchPattern, gitignore)

    all_files = []
    for root, dirs, files in os.walk(project_path):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]  # ignore directories in IGNORE_DIRS
        for file in files:
            file_path = Path(root) / file
            if not spec.match_file(str(file_path)):
                all_files.append(file_path)

    return all_files
