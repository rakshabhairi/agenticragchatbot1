import cohere
from typing import List

# Initialize Cohere client ( Avoid hardcoding keys in production)
co = cohere.Client("2xTRZVraYBDx8GILR5d8CuTtwvyWnsiHayzM1TH5")  #  Replace with your secure key management

def get_embeddings(
    texts: List[str],
    model: str = "embed-english-v3.0",
    input_type: str = "search_document"
) -> List[List[float]]:
    """
    Generate embeddings for a list of texts using Cohere.

    Args:
        texts (List[str]): List of input text strings.
        model (str): Cohere embedding model to use.
        input_type (str): Type of input ('search_document' or 'search_query').

    Returns:
        List[List[float]]: List of embeddings (one per text).
    """
    if not texts:
        print("[Embedder] No texts provided for embedding.")
        return []

    try:
        print(f"[Embedder] Generating embeddings for {len(texts)} texts...")
        response = co.embed(
            texts=texts,
            model=model,
            input_type=input_type
        )
        print("[Embedder]  Embeddings generated successfully.")
        return response.embeddings

    except Exception as e:
        print(f"[Embedder]  Error generating embeddings: {e}")
        return [[] for _ in texts]  # Return empty embeddings for consistency
