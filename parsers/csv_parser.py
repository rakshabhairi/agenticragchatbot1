import pandas as pd
from io import BytesIO

def parse_csv(file_bytes):
    df = pd.read_csv(BytesIO(file_bytes))
    text = df.to_string(index=False)
    chunks = text.split("\n\n")
    return [{"text": chunk.strip()} for chunk in chunks if chunk.strip()]
