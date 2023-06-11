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
