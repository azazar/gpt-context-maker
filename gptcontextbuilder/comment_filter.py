import re
import tokenize
import io


def remove_comments_python(source_code):
    try:
        io_obj = io.StringIO(source_code)
        out = ""
        prev_toktype = tokenize.INDENT
        last_lineno = -1
        last_col = 0

        for tok in tokenize.generate_tokens(io_obj.readline):
            token_type = tok[0]
            token_string = tok[1]
            start_line, start_col = tok[2]
            end_line, end_col = tok[3]

            if start_line > last_lineno:
                last_col = 0
            if start_col > last_col:
                out += (" " * (start_col - last_col))

            if token_type == tokenize.COMMENT:
                pass
            elif token_type == tokenize.STRING:
                if prev_toktype != tokenize.INDENT:
                    if prev_toktype != tokenize.NEWLINE:
                        out += token_string
            else:
                out += token_string
            prev_toktype = token_type
            last_col = end_col
            last_lineno = end_line

        return out
    except:  # noqa: E722
        # fallback to regexp if tokenization fails due to syntax errors
        regex = r"(^[ \t]*#.*?$|[ \t]+#[^'\"]+$)"
        no_comments = re.sub(regex, "", source_code, flags=re.MULTILINE)
        return no_comments


def remove_comments(file, content):
    file_string = ''.join(content)

    if file.suffix == '.py':
        no_comments = remove_comments_python(file_string)
    elif file.suffix in ['.java', '.c', '.cpp', '.cs']:
        no_comments = re.sub(r"//.*?$|/\*.*?\*/", " ", file_string, flags=re.DOTALL | re.MULTILINE)
    elif file.suffix in ['.js', '.ts']:
        no_comments = re.sub(r"//.*?$|/\*.*?\*/", " ", file_string, flags=re.DOTALL | re.MULTILINE)
    elif file.suffix in ['.php']:
        no_comments = re.sub(r"//.*?$|/\*.*?\*/|#.*?$", " ", file_string, flags=re.DOTALL | re.MULTILINE)
    elif file.suffix in ['.swift']:
        no_comments = re.sub(r"//.*?$|/\*.*?\*/|///.*?$", " ", file_string, flags=re.DOTALL | re.MULTILINE)
    else:
        no_comments = file_string

    return no_comments.strip()
