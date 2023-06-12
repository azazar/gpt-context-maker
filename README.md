# GPT Context Maker

GPT Context Maker is a Python-based tool designed to generate a meaningful context for large projects, suitable for use with Open AI's ChatGPT model. It supports a variety of programming languages, including Python, PHP, and more.

The tool reads files from your project directory (excluding those specified in .gitignore), counts tokens in the context, removes comments to reduce the context size, and takes additional steps if necessary to ensure the context fits within the token limit.

## Installation

To install the GPT Context Maker, follow these steps:

1. Clone the repository:

    ```bash
    git clone https://github.com/azazar/gpt-context-maker.git
    ```

2. Navigate into the project directory:

    ```bash
    cd gpt-context-maker
    ```

3. Install the package:

    ```bash
    pip install .
    ```

This will install the `gpt-context-maker` command-line tool on your system.

## How to Use

You can use the GPT Context Maker with command line arguments. The tool accepts the following arguments:

- `--path`: The path to your project directory. If no path is provided, the current directory is used.
- `--copy`: An optional argument. If provided, the tool will copy the generated context to the clipboard.
- `--max-tokens`: The maximum number of tokens allowed in the context. If no value is provided, it will use the default value from the `.gptsettings.yml` or 4096 if the setting is not specified.
- `--exclude-dirs`: An optional argument that accepts a comma-separated list of directories to exclude from the context. If no value is provided, it will use the default value from the `.gptsettings.yml` or exclude none if the setting is not specified.
- `--include-keywords`: An optional argument that accepts a comma-separated list of keywords to filter included files. If no value is provided, it will use the default value from the `.gptsettings.yml` or include all files if the setting is not specified.

To run the tool, you can use the `gpt-context-maker` command with the desired arguments. For example:

```bash
gpt-context-maker --path /path/to/your/project --copy --max-tokens 4096 --exclude-dirs test,logs --include-keywords key1,key2
```

`test` and `logs` directories, generate a context, and copy the context to the clipboard. Only files that contain 'key1' or 'key2' in their names are included.

The context is also printed to the console, so if you prefer not to copy it to the clipboard, you can omit the `--copy` argument.

For example:

```bash
gpt-context-maker --path /path/to/your/project --max-tokens 4096 --exclude-dirs test,logs --include-keywords key1,key2
```

This will do the same as the previous command, but the context will not be copied to the clipboard.

## Settings

You can customize the behavior of the GPT Context Maker by creating a `.gptsettings.yml` file in your project directory. The file can include the following settings:

- `maxTokens`: The maximum number of tokens allowed in the context. Defaults to 4096 if not specified.
- `excludeDirs`: A list of directories to exclude from the context. Defaults to an empty list if not specified.

Here is an example of a `.gptsettings.yml` file:

```yaml
maxTokens: 4096
excludeDirs:
  - test
  - logs
```

This file specifies that the maximum number of tokens in the context is 4096 and that files in the `test` and `logs` directories should be excluded from the context.

## Contribution

Contributions are welcome! Feel free to submit a pull request.
