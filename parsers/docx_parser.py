import docx

def parse_docx(file_bytes):
    doc = docx.Document(file_bytes)
    text = "\n".join([para.text for para in doc.paragraphs])
    chunks = text.split("\n\n")
    return [{"text": chunk.strip()} for chunk in chunks if chunk.strip()]
