from modules import file_reader, code_summarizer, comment_filter, token_counter, context_reducer, prompt_generator

MAX_TOKENS = 2048

def generate_and_count_tokens(summary):
    prompt = prompt_generator.generate_prompt(summary)
    return prompt, token_counter.count_tokens(prompt)

def main(project_path="."):
    # Step 1: Read all files
    all_files = file_reader.read_all_code_files(project_path)
    all_files.reverse()  # As per the requirement, process files from least recent
    
    # Generate initial context with all files' contents
    context = []
    for file in all_files:
        with open(file, "r") as f:
            file_content = f.read()
        context.append({"filename": str(file), "file_content": file_content})

    # Check if context is within limits, if so, return early
    prompts, total_tokens = zip(*[generate_and_count_tokens(c) for c in context])
    if sum(total_tokens) <= MAX_TOKENS:
        return "\n".join(prompts)

    # Step 2: Remove comments
    for c in context:
        if "file_content" in c:
            c["file_content"] = comment_filter.remove_comments(file, c["file_content"])
        prompts, total_tokens = zip(*[generate_and_count_tokens(c) for c in context])
        if sum(total_tokens) <= MAX_TOKENS:
            return "\n".join(prompts)

    # Step 3: Summarize
    for c in context:
        if "file_content" in c:
            summary = code_summarizer.summarize(c["file_content"], c["filename"])
            c.update(summary)
        prompts, total_tokens = zip(*[generate_and_count_tokens(c) for c in context])
        if sum(total_tokens) <= MAX_TOKENS:
            return "\n".join(prompts)

    # Step 4: If context still doesn't fit, reduce context as a last resort
    if sum(total_tokens) > MAX_TOKENS:
        context = context_reducer.reduce_context(context)
    
    # Generate the final prompts
    prompts, total_tokens = zip(*[generate_and_count_tokens(c) for c in context])

    return "\n".join(prompts)

if __name__ == "__main__":
    import sys
    print(main(sys.argv[1] if len(sys.argv) > 1 else "."))
