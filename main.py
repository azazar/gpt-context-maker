import argparse
import pyperclip
from modules import file_reader, code_summarizer, comment_filter, token_counter, context_reducer, prompt_generator, space_to_tab_converter

MAX_TOKENS = 4096

def generate_and_count_tokens(summary):
    prompt = prompt_generator.generate_prompt(summary)
    return prompt, token_counter.count_tokens(prompt)

def main(project_path=".", copy_to_clipboard=False, max_tokens=MAX_TOKENS, exclude_dirs=None):
    # Step 1: Read all files
    all_files = file_reader.read_all_code_files(project_path, exclude_dirs)
    all_files.reverse()  # As per the requirement, process files from least recent

    # Generate initial context with all files' contents
    context = []
    for file in all_files:
        with open(file, "r") as f:
            file_content = f.read().splitlines()
            # Replace every 8 spaces with a tab character in each line
            file_content = "\n".join(space_to_tab_converter.convert_spaces_to_tabs_in_iterable(file_content))
        context.append({"filename": str(file), "file_content": file_content})

    # Check if context is within limits, if so, return early
    prompts, total_tokens = zip(*[generate_and_count_tokens(c) for c in context])
    if sum(total_tokens) <= max_tokens:
        result = "\n".join(prompts)
        if copy_to_clipboard:
            pyperclip.copy(result)
        return result

    # Step 2: Remove comments
    for c in context:
        if "file_content" in c:
            c["file_content"] = comment_filter.remove_comments(file, c["file_content"])
        prompts, total_tokens = zip(*[generate_and_count_tokens(c) for c in context])
        if sum(total_tokens) <= max_tokens:
            result = "\n".join(prompts)
            if copy_to_clipboard:
                pyperclip.copy(result)
            return result

    # Step 3: Summarize
    for c in context:
        if "file_content" in c:
            summary = code_summarizer.summarize(c["file_content"], c["filename"])
            c.update(summary)
        prompts, total_tokens = zip(*[generate_and_count_tokens(c) for c in context])
        if sum(total_tokens) <= max_tokens:
            result = "\n".join(prompts)
            if copy_to_clipboard:
                pyperclip.copy(result)
            return result

    # Step 4: If context still doesn't fit, reduce context as a last resort
    if sum(total_tokens) > max_tokens:
        context = context_reducer.reduce_context(context)

    # Generate the final prompts
    prompts, total_tokens = zip(*[generate_and_count_tokens(c) for c in context])
    result = "\n".join(prompts)

    if copy_to_clipboard:
        pyperclip.copy(result)
    
    return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate a GPT Context from a project.')
    parser.add_argument('--path', default='.', help='Path to the project.')
    parser.add_argument('--copy', action='store_true', help='Copy the output to clipboard.')
    parser.add_argument('--max-tokens', type=int, default=MAX_TOKENS, help='Max tokens for the context.')
    parser.add_argument('--exclude-dirs', default='', help='Comma-separated list of directories to exclude.')
    args = parser.parse_args()

    # convert the comma-separated string into a set
    exclude_dirs = set(args.exclude_dirs.split(',')) if args.exclude_dirs else None

    print(main(args.path, args.copy, args.max_tokens, exclude_dirs))
