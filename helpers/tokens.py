import tiktoken

enc = tiktoken.get_encoding("cl100k_base")

def count_tokens(text):
    tokens = enc.encode(text)
    return len(tokens)