import argparse
import pyperclip
import yaml
import os
from modules import file_reader, code_summarizer, comment_filter, token_counter, context_reducer, prompt_generator, space_to_tab_converter

MAX_TOKENS = 3072
DEFAULT_REQUIREMENTS = """
# Output Requirements
1. Before generating code, specify the filename.
2. Replace in-code triple backticks with "~~~" to avoid Markdown conflict.
3. For file modifications, provide diff-style patch code in a format that can be used with the patch utility (include a patch command example) unless you generate a whole file. For file renaming, provide a bash script.
4. Keep replies brief and avoid explanations due to size limits. Use code to provide clear explanations.
5. Keep explanation outside of generated code. It's supposed to be added into the project without modifications.
6. All requirements and guidelines must be followed.

# Critical Guidelines
1. **Maintainability**: Code should be clear, modular, and well-documented. Follow industry-standard style guides. Use meaningful names for variables and methods.
2. **Testability**: Write the code in easily testable units with robust error handling. Specify the test framework and required coverage level.
3. **Performance**: Code should be efficient, optimized, and minimize unnecessary calculations. Include specific performance benchmarks if necessary.
4. **Security**: Anticipate and address common security issues, validate and sanitize user input. Provide examples of potential security risks if needed.
5. **Quality**: Ensure adherence to SOLID, KISS, and YAGNI principles in the generated code.
""".strip()

def generate_prmompt_and_count_tokens(context, prepend_text=""):
    prompts = [prompt_generator.create_prompt_from_context(summary) for summary in context]
    prompt = (prepend_text.strip() + "\n\n" + "\n".join(prompts)).strip()
    return prompt, token_counter.count_tokens(prompt)

def load_settings(project_path):
    default_settings = {
        'copy': False,
        'max-tokens': MAX_TOKENS,
        'exclude-dirs': '',
        'include-keywords': '',
        'prompt': '',
        'requirements': DEFAULT_REQUIREMENTS,
    }
    settings_path = os.path.join(project_path, '.gptsettings.yml')
    if os.path.isfile(settings_path):
        with open(settings_path, 'r') as f:
            loaded_settings = yaml.safe_load(f)
            default_settings.update(loaded_settings)
    return default_settings

def main(project_path=".", max_tokens=MAX_TOKENS, exclude_dirs=None, include_keywords=None, prepend_text=""):
    # Step 1: Read all files
    all_files = file_reader.read_all_code_files(project_path, exclude_dirs, include_keywords)
    
    # Sort files by modification time, from oldest to newest
    all_files.sort(key=os.path.getmtime)
    
    # Generate initial context with all files' contents
    context = []
    for file in all_files:
        with open(file, "r") as f:
            file_content = f.read().splitlines()
            if file.suffix == '.py':
                reduced_content = space_to_tab_converter.convert_spaces_to_tabs_python("\n".join(file_content))
            else:
                reduced_content = "\n".join(space_to_tab_converter.convert_spaces_to_tabs_in_iterable(file_content))
            context.append({"filename": os.path.relpath(str(file), project_path), "file_content": "\n".join(file_content), "reduced_content": reduced_content})

    # Check if context is within limits, if so, return early
    prompt, total_tokens = generate_prmompt_and_count_tokens(context, prepend_text)
    if total_tokens <= max_tokens:
        return prompt, total_tokens

    # Step 2: Remove comments
    for c in context:
        if "reduced_content" in c:
            c["reduced_content"] = comment_filter.remove_comments(file, c["reduced_content"])

            prompt, total_tokens = generate_prmompt_and_count_tokens(context, prepend_text)
            if total_tokens <= max_tokens:
                return prompt, total_tokens

    # Step 3: Summarize
    for c in context:
        if "reduced_content" in c:
            summary = code_summarizer.summarize(c["file_content"], c["filename"])
            c.update(summary)
            c.pop('reduced_content')

            prompt, total_tokens = generate_prmompt_and_count_tokens(context, prepend_text)
            if total_tokens <= max_tokens:
                return prompt, total_tokens

    # Step 4: If context still doesn't fit, reduce context as a last resort
    if total_tokens > max_tokens:
        context = context_reducer.reduce_context(context, max_tokens)

    # Generate the final prompts
    prompt, total_tokens = generate_prmompt_and_count_tokens(context, prepend_text)

    return prompt, total_tokens


def main_cli():
    parser = argparse.ArgumentParser(description='Generate a GPT Context from a project.')
    parser.add_argument('--path', default=None, help='Path to the project.')
    parser.add_argument('--copy', action='store_true', help='Copy the output to clipboard.')
    parser.add_argument('--max-tokens', type=int, default=None, help='Max tokens for the context.')
    parser.add_argument('--exclude-dirs', default=None, help='Comma-separated list of directories to exclude.')
    parser.add_argument('--include-keywords', default=None, help='Comma-separated list of keywords to filter included files.')
    parser.add_argument('--prompt', default=None, help='Text to prepend to the generated context.')
    parser.add_argument('--requirements', default=None, help='Text to append to the generated context.')
    args = parser.parse_args()

    path = args.path if args.path else '.'
    settings = load_settings(path)

    settings['copy'] = args.copy if args.copy else settings['copy']
    settings['max-tokens'] = args.max_tokens if args.max_tokens else settings['max-tokens']
    settings['exclude-dirs'] = args.exclude_dirs if args.exclude_dirs else settings['exclude-dirs']
    settings['include-keywords'] = args.include_keywords if args.include_keywords else settings['include-keywords']
    settings['prompt'] = args.prompt if args.prompt else settings['prompt']
    settings['requirements'] = args.requirements if args.requirements else settings['requirements']

    exclude_dirs = set(settings['exclude-dirs'].split(',')) if settings['exclude-dirs'] else None
    include_keywords = set(settings['include-keywords'].split(',')) if settings['include-keywords'] else None
    
    prompt = []
    
    if 'prompt' in settings and len(settings['prompt']) > 0:
        prompt.append(settings['prompt'].strip())

    if 'requirements' in settings and len(settings['requirements']) > 0:
        prompt.append(settings['requirements'].strip())

    result, tokens = main(path, settings['max-tokens'], exclude_dirs, include_keywords, "\n\n".join(prompt).strip())

    print("Total Tokens: ", tokens)

    if settings['copy']:
        pyperclip.copy(result)
    else:
        print(result)


if __name__ == "__main__":
    main_cli()
