# GPT Context Maker

The GPT Context Maker, created by Mikhail Yevchenko, is a Python-based tool built to generate compact and useful context for ChatGPT from large-scale projects. It supports an array of programming languages, including Python and PHP, and its main goal is to aid in generating efficient and relevant prompts for OpenAI's ChatGPT model.

The tool operates by scanning files from your project directory (excluding those stated in .gitignore), counting tokens within the context, and removing comments to trim down the context size. If necessary, it takes further steps to ensure the context stays within the model's token limit.

## Steps to Operation

1. **Reading all files from directory tree:** The tool parses your project's complete directory tree, ignoring files as per the .gitignore file.

2. **Token counting in context:** Post file reading, the tool counts all tokens within the context using the `tiktoken` library. This count is essential for controlling the size of the context.

3. **Comment removal:** Comments from the source code are eliminated to further downsize the context.

4. **Context size reduction:** If the context exceeds the model's token limit, the tool implements additional actions to decrease its size, such as shortening lengthy summaries and giving priority to essential code segments.

5. **Final context generation:** When the context is within the token limit, the tool generates the final context, which includes the source code or summaries for larger files.

## Installation

Clone the GitHub repository and install the necessary Python packages for GPT Context Maker installation:

```bash
git clone https://github.com/azazar/gpt-context-maker.git
cd gpt-context-maker
pip install -r requirements.txt
```

## Usage

Run the `main.py` file with your project directory as the argument to use the GPT Context Maker:

```bash
python main.py /path/to/your/project
```

The generated context is printed to the standard output.

You can optionally add the `--copy` flag to copy the output to your clipboard:

```bash
python main.py /path/to/your/project --copy
```

## Credits

- **Mikhail Yevchenko:** Project lead, responsible for designing the prompts and managing the project's development.
- **OpenAI's GPT-4 Assistant:** Contributed to the initial step-by-step guide, proposed algorithms, constructed the Python project structure, and implemented the project's code.

## License

This project is licensed under the MIT License. For more information, please refer to the `LICENSE` file in the project's root directory.