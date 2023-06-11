import re

def remove_comments(file):
    with open(file, "r") as f:
        content = f.readlines()
    
    file_string = ' '.join(content)

    # Set comment style based on file extension
    if file.suffix in ['.py', '.java', '.c', '.cpp', '.cs']:
        # For Python, Java, C, C++, C# we look for comments that start with //
        # and /* */. We also look for Python-specific triple quote comments.
        no_comments = re.sub(r"(#).*?$|/\*.*?\*/|\'\'\'.*?\'\'\'", "", file_string, flags=re.DOTALL | re.MULTILINE)
    elif file.suffix in ['.js', '.ts']:
        # For JavaScript and TypeScript, we look for comments that start with //
        # and /* */
        no_comments = re.sub(r"//.*?$|/\*.*?\*/", "", file_string, flags=re.DOTALL | re.MULTILINE)
    elif file.suffix in ['.php']:
        # For PHP, we look for comments that start with //, /* */, and #
        no_comments = re.sub(r"//.*?$|/\*.*?\*/|#.*?$", "", file_string, flags=re.DOTALL | re.MULTILINE)
    elif file.suffix in ['.swift']:
        # For Swift, we look for comments that start with //, /* */, and ///
        no_comments = re.sub(r"//.*?$|/\*.*?\*/|///.*?$", "", file_string, flags=re.DOTALL | re.MULTILINE)
    else:
        # For all other files, we remove no comments.
        no_comments = file_string

    return no_comments
