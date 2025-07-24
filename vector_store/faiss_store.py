import faiss
import numpy as np

class Chunk:
    def __init__(self, text, metadata=None):
        self.page_content = text
        self.metadata = metadata

class VectorStore:
    def __init__(self, dim):
        self.dim = dim
        self.index = faiss.IndexFlatL2(dim)
        self.documents = []  # Store Chunk objects

    def add_documents(self, chunks, metadata=None):
        vectors = [chunk['embedding'] for chunk in chunks]
        texts = [chunk['text'] for chunk in chunks]
        vectors_np = np.array(vectors).astype('float32')

        self.index.add(vectors_np)

        for text in texts:
            self.documents.append(Chunk(text, metadata))

    def search(self, query_embedding, top_k=5):
        query_np = np.array([query_embedding]).astype('float32')
        distances, indices = self.index.search(query_np, top_k)

        results = []
        for i in indices[0]:
            if i < len(self.documents):
                results.append(self.documents[i])
        return results
