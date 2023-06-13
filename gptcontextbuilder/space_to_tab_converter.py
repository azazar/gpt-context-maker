def convert_spaces_to_tabs(line: str, space_count=8) -> str:
    """
    Replace consecutive spaces with a tab character in a string.

    :param line: A string where spaces should be replaced with tabs.
    :param space_count: Number of consecutive spaces to be replaced with a tab character.
    :return: The input string with spaces replaced with tabs.
    """
    spaces = " " * space_count
    return line.replace(spaces, "\t")


def convert_spaces_to_tabs_in_iterable(iterable, space_count=8):
    """
    Apply convert_spaces_to_tabs function to each element of an iterable.

    :param iterable: An iterable where spaces in each element should be replaced with tabs.
    :param space_count: Number of consecutive spaces to be replaced with a tab character in each element.
    :return: The iterable with spaces in each element replaced with tabs.
    """
    return [convert_spaces_to_tabs(i, space_count) for i in iterable]


def convert_spaces_to_tabs_python(code_string):
    lines = code_string.split('\n')  # Split the code into lines

    # Determine the number of spaces per indentation level
    indentation = ''
    for char in lines[0]:
        if char == ' ':
            indentation += ' '
        else:
            break
    if len(indentation) == 0:
        return code_string  # No spaces found, return the original code unchanged

    # Replace spaces with tabs
    converted_lines = []
    for line in lines:
        if line.startswith(indentation):
            # Replace spaces with tabs using the expandtabs() method
            converted_lines.append(line.replace(indentation, '\t'))
        else:
            converted_lines.append(line)  # Preserve lines without indentation

    # Join the lines back into a single string
    converted_code = '\n'.join(converted_lines)

    return converted_code
