def generate_prompt(summary):
    if "file_content" in summary:
        return f"# File: {summary['filename']}:\n```python\n{summary['file_content']}\n```"

    sections = {
        "Variables": summary.get("variables", []),
        "Functions": summary.get("functions", []),
        "Classes": summary.get("classes", []),
        "Extra code": summary.get("extra_code", ""),
    }

    prompt = f"# File: {summary['filename']}:\n"  # Add "File: " prefix to the filename
    for section, items in sections.items():
        if items:  # Only append the section if it is not empty
            items_str = "\n".join(items) if isinstance(items, list) else items
            prompt += f"## {section}\n" + items_str + "\n"

    return prompt
