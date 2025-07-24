from embeddings.embedder import get_embeddings
from mcp.message_dispatcher import MCPMessage

class RetrievalAgent:
    def __init__(self, dispatcher, vector_store):
        self.dispatcher = dispatcher
        self.vector_store = vector_store
        dispatcher.register_agent("retrieval_agent", self.handle)

    def handle(self, message: MCPMessage):
        trace_id = message.trace_id
        print(f"[RetrievalAgent] 🔍 Handling query. Trace ID: {trace_id}")

        query = message.payload.get("query")
        if not query:
            print(f"[RetrievalAgent]  Empty query received. Trace ID: {trace_id}")
            self._send_response(trace_id, "No query provided.", "")
            return

        try:
            # Step 1: Generate embedding for the query
            query_embedding = get_embeddings([query])[0]
            print(f"[RetrievalAgent]  Query embedding generated. Dimensions: {len(query_embedding)}")

            # Step 2: Retrieve top-k similar chunks
            top_chunks = self.vector_store.similarity_search(query_embedding, top_k=5)

            if not top_chunks:
                print(f"[RetrievalAgent]⚠️ No relevant chunks found. Trace ID: {trace_id}")
                retrieved_context = "No relevant information found."
            else:
                print(f"[RetrievalAgent]  Found {len(top_chunks)} relevant chunks. Trace ID: {trace_id}")
                retrieved_context = "\n".join(
                    chunk.get("text", "[No Text]") for chunk in top_chunks
                )

            # Step 3: Send retrieved context to LLM response agent
            self._send_response(trace_id, retrieved_context, query)

        except Exception as e:
            error_msg = f"[RetrievalAgent]  Retrieval error: {e}"
            print(error_msg)
            self._send_response(trace_id, error_msg, query)

    def _send_response(self, trace_id, context, query):
        response = MCPMessage(
            sender="retrieval_agent",
            receiver="llm_response_agent",
            type="RETRIEVAL_RESULT",
            trace_id=trace_id,
            payload={
                "retrieved_context": context,
                "query": query
            }
        )
        self.dispatcher.send_message(response)

# ✅ Exportable handler
def retrieval_agent_handler(dispatcher, vector_store):
    return RetrievalAgent(dispatcher, vector_store).handle
