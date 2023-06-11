from modules import (
    file_reader, 
    token_counter, 
    comment_filter, 
    code_summarizer, 
    context_reducer, 
    prompt_generator
)

MAX_TOKENS = 2048  # Define a limit for tokens

def main(project_path="."):
    # Step 1: Read files
    code_files = file_reader.read_all_code_files(project_path)

    # Step 2: Summarize or store file contents
    summaries = []
    for file_path in code_files:
        try:
            with open(file_path, "r") as f:
                file_content = f.read()
        except UnicodeDecodeError:
            print(f"Warning: File {file_path} couldn't be read due to encoding issues. Skipping this file.")
            continue

        token_count = token_counter.count_tokens(file_content)
        if token_count > MAX_TOKENS:
            file_content = comment_filter.remove_comments(file_content)
            token_count = token_counter.count_tokens(file_content)  # Count tokens again after removing comments

            # Summarize the file if token count is still too large
            if token_count > MAX_TOKENS:
                summary = code_summarizer.summarize(file_content, str(file_path))
                summaries.append(summary)
        else:
            summaries.append({"filename": str(file_path), "file_content": file_content})

    # Step 3: Reduce context size if needed
    total_token_count = sum(token_counter.count_tokens(s.get("file_content", "") + ''.join(s.values())) for s in summaries)
    if total_token_count > MAX_TOKENS:
        summaries = context_reducer.reduce_context(summaries)

    # Step 4: Generate full GPT prompts
    prompts = [
        prompt_generator.generate_prompt(summary) 
        if 'file_content' not in summary 
        else f"# File: {summary['filename']}:\n```python\n{summary['file_content']}\n```" 
        for summary in summaries
    ]

    return '\n'.join(prompts)


if __name__ == "__main__":
    print(main())
