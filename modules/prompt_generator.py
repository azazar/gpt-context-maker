def generate_prompt(summary):
    sections = {
        "Variables": summary["variables"],
        "Functions": summary["functions"],
        "Classes": summary["classes"],
        "Extra code": summary["extra_code"],
    }

    prompt = f"# File: {summary['filename']}:\n"  # Add "File: " prefix to the filename
    for section, items in sections.items():
        if items:  # Only append the section if it is not empty
            prompt += f"## {section}\n" + "\n".join(items) + "\n"

    return prompt
