def create_prompt_from_context(context):
    if any(key in context for key in ['variables', 'functions', 'classes', 'extra_code']):
        sections = {
            "Variables": context.get("variables", []),
            "Functions": context.get("functions", []),
            "Classes": context.get("classes", []),
            "Extra code": context.get("extra_code", ""),
        }

        prompt = f"## File {context['filename']}\n"  # Add "File " prefix to the filename
        for section, items in sections.items():
            if items:  # Only append the section if it is not empty
                items_str = "\n".join(items) if isinstance(items, list) else items
                prompt += f"### {section}\n" + items_str + "\n"

        return prompt

    if "reduced_content" in context:
        return f"## File {context['filename']}\n```\n{context['reduced_content']}\n```"

    return f"## File {context['filename']}\n```\n{context['file_content']}\n```"