from modules import file_reader, code_summarizer, comment_filter, token_counter, context_reducer, prompt_generator

MAX_TOKENS = 2048

def main(project_path="."):
    # Step 1: Read all files
    all_files = file_reader.read_all_code_files(project_path)
    
    # Step 2: Generate a summary for each file
    summaries = []
    for file in all_files:
        with open(file, "r") as f:
            file_content = f.read()

        # If file_content fits in context, append file content, otherwise append summary
        if token_counter.count_tokens(file_content) <= MAX_TOKENS:
            summaries.append({"filename": str(file), "file_content": file_content})
        else:
            # Step 3: Remove comments
            no_comments = comment_filter.remove_comments(file_content)
            
            # Step 4: Summarize the code
            summary = code_summarizer.summarize(no_comments, str(file))
            summaries.append(summary)

    # Step 5: Reduce the context if necessary
    if sum(token_counter.count_tokens(s.get("file_content", "") + ''.join(s.values())) for s in summaries) > MAX_TOKENS:
        summaries = context_reducer.reduce_context(summaries)
    
    # Step 6: Generate the final prompts
    prompts = [prompt_generator.generate_prompt(summary) if 'file_content' not in summary else f"# File: {summary['filename']}:\n```python\n{summary['file_content']}\n```" for summary in summaries]
    
    return "\n".join(prompts)

if __name__ == "__main__":
    import sys
    print(main(sys.argv[1] if len(sys.argv) > 1 else "."))
