# GPT Context Maker

The GPT Context Maker is a Python-based tool designed to generate a concise and meaningful ChatGPT context for large projects. It supports projects written in various programming languages including Python, PHP and others. The purpose of the tool is to assist you in creating concise and effective prompts for OpenAI's ChatGPT model.

The tool works by reading files from your project directory (excluding those mentioned in .gitignore), counting the tokens in the context, removing comments to reduce the context size and taking further actions if necessary to ensure the context fits within the model's token limit.

## How It Works - Step by Step Guide

1. **Read all files from directory tree:** The tool scans the entire directory tree of your project, ignoring files that are mentioned in the .gitignore file.

2. **Count tokens in context:** After reading the files, the tool counts all the tokens in the context using the `tiktoken` library. This count is used to manage the size of the context.

3. **Remove comments:** To further reduce the context size, the tool removes all comments from the source code.

4. **Reduce context size:** If the context is still too large to fit within the model's token limit, the tool will take additional actions to reduce its size. This includes truncating long summaries and prioritizing the inclusion of important code segments.

5. **Generate the final context:** Once the context is within the token limit, the tool generates the final context which includes the source code of each file or summaries for larger files.

## Installation

To install the GPT Context Maker, clone the repository from GitHub and install the required Python packages:

```bash
git clone https://github.com/azazar/gpt-context-maker.git
cd gpt-context-maker
pip install -r requirements.txt
```

## Usage

To use the GPT Context Maker, run the `main.py` file with your project directory as the argument:

```bash
python main.py /path/to/your/project
```

This will print the generated context to the standard output.

## Credits

- **Azazar:** Project lead, responsible for engineering the prompts and overseeing the project development.
- **OpenAI's GPT-4 Assistant:** Developed the initial step-by-step guide, proposed algorithms, created the Python project structure, and implemented the project's code.

## License

This project is released under the MIT License. For more details, see the `LICENSE` file in the project's root directory.