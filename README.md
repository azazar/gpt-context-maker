# GPT Context Maker

GPT Context Maker is a Python-based tool designed to generate a meaningful context for large projects, suitable for use with Open AI's ChatGPT model. It supports a variety of programming languages, including Python, PHP, and more.

The tool reads files from your project directory (excluding those specified in .gitignore), counts tokens in the context, removes comments to reduce the context size, and takes additional steps if necessary to ensure the context fits within the token limit.

## How to Use

You can use the GPT Context Maker with command line arguments. The tool accepts the following arguments:

- `--path`: The path to your project directory. If no path is provided, the current directory is used.
- `--copy`: An optional argument. If provided, the tool will copy the generated context to the clipboard.
- `--max-tokens`: The maximum number of tokens allowed in the context. The default value is 4096.
- `--exclude-dirs`: An optional argument that accepts a comma-separated list of directories to exclude from the context. Default is none.

To run the tool, execute the `main.py` script with the desired arguments. For example:

```bash
python main.py --path /path/to/your/project --copy --max-tokens 4096 --exclude-dirs test,logs
```

This command will read the files from the specified path, excluding files in the 'test' and 'logs' directories, generate a context that fits within 4096 tokens, and copy the generated context to the clipboard.

## Installation

To install the GPT Context Maker, clone the repository and install the required Python packages:

```bash
git clone https://github.com/azazar/gpt-context-maker.git
cd gpt-context-maker
pip install -r requirements.txt
```

## Credits

This tool was developed by Mikhail Yevchenko and OpenAI's GPT-4 Assistant, which proposed algorithms, created the project structure, and implemented the project's code.

## License

This project is licensed under the terms of the MIT License. See the `LICENSE` file for more information.