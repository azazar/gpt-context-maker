import os
from pathlib import Path
from pathspec import PathSpec
from pathspec.patterns import GitWildMatchPattern

DEFAULT_IGNORE_DIRS = {'__pycache__', '.venv', '.git', '.idea', '.vscode', 'node_modules', 'vendor'}
DEFAULT_IGNORE_FILES = {'*.o', '*.exe', '*.dll', '*.so', '*.dylib', '*.class', '*.jar', '*.war', '*.pyc', '*.pyo', '*.rbc', '*.beam', '*.wasm'}

def load_ignore_file_paths(ignore_file_paths):
    ignore_patterns = []
    for path in ignore_file_paths:
        if path.exists():
            with open(path, "r") as file:
                ignore_patterns += file.readlines()

    return [line.strip() for line in ignore_patterns]

def read_all_code_files(project_path=".", additional_ignore_dirs=None, include_keywords=None):
    # Combine the default and additional ignore directories
    ignore_dirs = DEFAULT_IGNORE_DIRS.union(additional_ignore_dirs if additional_ignore_dirs else {})

    ignore_file_paths = [Path(project_path) / name for name in [".gitignore", ".gptignore", "ignore_files.txt"]]
    ignore_patterns = load_ignore_file_paths(ignore_file_paths)
    spec = PathSpec.from_lines(GitWildMatchPattern, ignore_patterns)

    all_files = []
    for root, dirs, files in os.walk(project_path):
        dirs[:] = [d for d in dirs if d not in ignore_dirs]  # ignore directories in IGNORE_DIRS
        for file in files:
            file_path = Path(root) / file
            # Exclude files that match the ignore patterns or are in IGNORE_FILES
            if not any(file_path.match(pattern) for pattern in DEFAULT_IGNORE_FILES) and not spec.match_file(str(file_path)):
                # Include files with .md, .txt, .py, .php, .js, .ts, .java, .c, .cpp, .cs, .swift extensions
                if file_path.suffix in ['.py', '.php', '.js', '.ts', '.java', '.c', '.cpp', '.cs', '.swift', '.md', '.txt']:
                    if include_keywords is not None:
                        if any(keyword in str(file_path) for keyword in include_keywords):
                            all_files.append(file_path)
                    else:
                        all_files.append(file_path)

    return all_files
