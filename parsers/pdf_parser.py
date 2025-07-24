import fitz  # PyMuPDF

def parse_pdf(uploaded_file):
    # Read the PDF as bytes
    file_bytes = uploaded_file.read()

    # Open the document from bytes
    doc = fitz.open(stream=file_bytes, filetype="pdf")

    text = ""
    for page in doc:
        text += page.get_text()

    return [text]  # Return list of one big chunk (or chunk it further if needed)
