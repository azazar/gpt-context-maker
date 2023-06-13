import tiktoken


def count_tokens(file_content: str) -> int:
    # Uses tiktoken to count tokens in the provided file content
    enc = tiktoken.get_encoding("cl100k_base")
    tokens = enc.encode(file_content)
    return len(tokens)
