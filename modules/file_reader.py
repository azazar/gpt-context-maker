import os
from pathlib import Path
from pathspec import PathSpec
from pathspec.patterns import GitWildMatchPattern

IGNORE_DIRS = {'__pycache__', '.venv', '.git', '.idea', '.vscode', 'node_modules', 'vendor'}
IGNORE_FILES = {'*.o', '*.exe', '*.dll', '*.so', '*.dylib', '*.class', '*.jar', '*.war', '*.pyc', '*.pyo', '*.rbc', '*.beam', '*.wasm'}

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
            # Exclude files that match the gitignore pattern or are in IGNORE_FILES
            if not any(file_path.match(pattern) for pattern in IGNORE_FILES) and not spec.match_file(str(file_path)):
                # Include files with .md, .txt, .py, .php, .js, .ts, .java, .c, .cpp, .cs, .swift extensions
                if file_path.suffix in ['.py', '.php', '.js', '.ts', '.java', '.c', '.cpp', '.cs', '.swift', '.md', '.txt']:
                    all_files.append(file_path)

    return all_files
