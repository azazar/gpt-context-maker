# GPT Context Maker

GPT Context Maker is a Python-based tool that intelligently generates a context from a provided project. It's designed for compatibility with Open AI's ChatGPT model, suitable for large software projects across various programming languages, including Python, PHP, and more.

The tool generates a context by analyzing your project files, prioritizing recent changes, removing comments, and taking additional steps as necessary to ensure the context fits within a predefined token limit.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/azazar/gpt-context-maker.git
    ```

2. Navigate into the cloned directory:

    ```bash
    cd gpt-context-maker
    ```

3. Install the package using pip:

    ```bash
    pip install .
    ```

## Usage

The GPT Context Maker can be used either through command-line arguments or by creating a `.gptsettings.yml` configuration file in your project directory.

Here are the available command-line arguments:

- `--path` (Optional): Path to your project directory. Defaults to the current directory if not specified.
- `--copy` (Optional): If included, the tool will copy the generated context to the clipboard.
- `--max-tokens` (Optional): The maximum number of tokens allowed in the context. Defaults to 3072 if not specified.
- `--exclude-dirs` (Optional): A comma-separated list of directories to exclude from the context.
- `--include-keywords` (Optional): A comma-separated list of keywords to filter included files.
- `--prompt` (Optional): Text to prepend to the generated context.

Example of a command-line usage:

```bash
gpt-context-maker --path /path/to/your/project --copy --max-tokens 4096 --exclude-dirs test,logs --include-keywords key1,key2 --prompt "Fix this function"
```

The above command instructs the tool to generate a context from the project located at `/path/to/your/project`, excluding files from `test` and `logs` directories. It will filter files to include only those that contain 'key1' or 'key2' in their names, prepend the context with "Fix this function" and copy the resulting context to the clipboard.

### Usage with Visual Studio Code

You can integrate GPT Context Maker with Visual Studio Code using tasks and keybindings for a more seamless experience. Here's how to set it up:

1. Open your user `tasks.json` file in Visual Studio Code. If it does not exist, you will need to create it. You can access it by opening the command palette `Ctrl+Shift+P`, and type `Tasks: Open User Tasks`.

2. Add the following task configurations to the `tasks.json` file:

```json
{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "Generate GPT Context from current workspace with filtering",
            "type": "shell",
            "command": "gpt-context-maker",
            "args": [
                "--path",
                "${workspaceFolder}",
                "--prompt",
                "${input:inputPrompt}",
                "--include-keywords",
                "${input:includeKeywords}",
                "--copy"
            ],
            "problemMatcher": [],
            "group": {
                "kind": "none",
            },
            "presentation": {
                "revealProblems": "onProblem"
            }
        },
        {
            "label": "Generate GPT Context from current workspace",
            "type": "shell",
            "command": "gpt-context-maker",
            "args": [
                "--path",
                "${workspaceFolder}",
                "--copy"
            ],
           

 "problemMatcher": [],
            "group": {
                "kind": "none",
            },
            "presentation": {
                "revealProblems": "onProblem"
            }
        }
    ],
    "inputs": [
        {
            "id": "inputPrompt",
            "type": "promptString",
            "description": "Provide a prompt."
        },
        {
            "id": "includeKeywords",
            "type": "promptString",
            "description": "Comma-separated list of keywords to include.",
            "default": ""
        }
    ]
}
```

3. Update your user keybindings file (`keybindings.json`). You can access it by opening the command palette `Ctrl+Shift+P`, and type `Preferences: Open Keyboard Shortcuts (JSON)`.

```json
[
    {
        "key": "ctrl+shift+g",
        "command": "workbench.action.tasks.runTask",
        "args": "Generate GPT Context from current workspace with filtering"
    },
    {
        "key": "alt+g",
        "command": "workbench.action.tasks.runTask",
        "args": "Generate GPT Context from current workspace"
    }
]
```

With these settings, you can generate a context for your current workspace with filtering by pressing `Ctrl+Shift+G` and without filtering by pressing `Alt+G`. You will be prompted to input a prompt and keywords when using the `Ctrl+Shift+G` shortcut.

### Troubleshooting

If you encounter any problems while running the tasks, check the 'Problems' tab in VSCode for any error messages. If the issue persists, ensure that the `gpt-context-maker` command is correctly installed and accessible in your PATH.

## Settings

If you prefer not to use command-line arguments, you can create a `.gptsettings.yml` file in your project directory with the same configuration options:

```yaml
copy: false
max-tokens: 4096
exclude-dirs: "test,logs"
include-keywords: "main,py"
prompt: |
  Here are project files for the context. Wait for instructions.
```

Please note that any command-line arguments will override the respective settings from the `.gptsettings.yml` file.

## Contribution

Your contributions are most welcome! Here are the steps to contribute:

1. Fork this repository.
2. Create a new branch in your forked repository.
3. Make changes in your new branch.
4. Create a pull request.

Ensure that your code adheres to the existing style for consistency.

## Output

The output of the GPT Context Maker is a summarized context of your code, suitable for input into the OpenAI GPT-3 model. The context is generated by intelligently summarizing and filtering your codebase while prioritizing recent changes. If the `--copy` argument is used or `copy: true` is set in the `.gptsettings.yml` file, this context is also copied to your clipboard.

If you have any issues or suggestions, please open an issue in this repository. Happy coding!