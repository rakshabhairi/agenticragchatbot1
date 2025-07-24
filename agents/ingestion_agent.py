from mcp.message_dispatcher import MCPMessage
from vector_store.faiss_store import VectorStore


class IngestionAgent:
    def __init__(self, dispatcher, vector_store: VectorStore, parsers: dict = None):
        self.dispatcher = dispatcher
        self.vector_store = vector_store
        self.parsers = parsers or {}

    def handle(self, message: MCPMessage):
        print(f"[IngestionAgent] Received message with trace_id: {message.trace_id}")

        chunks = message.payload.get("chunks")
        filename = message.payload.get("filename")

        if not chunks:
            print("[IngestionAgent] No chunks provided.")
            return

        # Store the chunks in the vector store
        try:
            self.vector_store.add_documents(chunks, metadata={"source": filename})
            print(f"[IngestionAgent] Stored {len(chunks)} chunks from {filename} into vector store.")
        except Exception as e:
            print(f"[IngestionAgent] Error while storing chunks: {e}")


# ✅ This is the function MCPDispatcher will call
def ingestion_agent_handler(dispatcher, vector_store):
    agent = IngestionAgent(dispatcher, vector_store)
    return agent.handle
