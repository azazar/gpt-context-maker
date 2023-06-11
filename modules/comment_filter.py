def remove_comments(file):
    with open(file, "r") as f:
        content = f.readlines()

    no_comments = re.sub(r"(#|//).*?$|/\*.*?\*/|\'\'\'.*?\'\'\'", "", ' '.join(content), flags=re.DOTALL|re.MULTILINE)

    return no_comments
