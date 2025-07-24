def parse_txt(file_bytes):
    text = file_bytes.decode("utf-8")
    chunks = text.split("\n\n")
    return [{"text": chunk.strip()} for chunk in chunks if chunk.strip()]
