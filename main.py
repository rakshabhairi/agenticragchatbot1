import streamlit as st
from mcp.message_dispatcher import MCPDispatcher, MCPMessage
from agents.ingestion_agent import ingestion_agent_handler
from agents.retrieval_agent import retrieval_agent_handler
from agents.llm_response_agent import llm_response_agent_handler
from vector_store.faiss_store import VectorStore
import parsers.pdf_parser as pdf
import parsers.pptx_parser as pptx
import parsers.docx_parser as docx
import parsers.csv_parser as csv
import parsers.txt_parser as txt
import uuid

# Initialize core components
vector_store = VectorStore(dim=1024)
dispatcher = MCPDispatcher()

# Register agents
dispatcher.register_agent("ingestion_agent", ingestion_agent_handler(dispatcher, vector_store))
dispatcher.register_agent("retrieval_agent", retrieval_agent_handler(dispatcher, vector_store))
dispatcher.register_agent("llm_response_agent", llm_response_agent_handler(dispatcher))

# Streamlit UI setup
st.set_page_config(page_title="Agentic RAG Chatbot", layout="wide")
st.title("Agentic RAG Chatbot")

# Session state
if "llm_response" not in st.session_state:
    st.session_state["llm_response"] = ""

if "uploaded_filename" not in st.session_state:
    st.session_state["uploaded_filename"] = None

# File upload
uploaded_file = st.file_uploader("Upload your file", type=["pdf", "pptx", "docx", "csv", "txt"])
user_query = st.text_input("Ask a question based on the uploaded document")

# Handle upload and ingestion
if uploaded_file:
    file_type = uploaded_file.name.split(".")[-1].lower()

    if file_type == "pdf":
        text_chunks = pdf.parse_pdf(uploaded_file)
    elif file_type == "pptx":
        text_chunks = pptx.parse_pptx(uploaded_file)
    elif file_type == "docx":
        text_chunks = docx.parse_docx(uploaded_file)
    elif file_type == "csv":
        text_chunks = csv.parse_csv(uploaded_file)
    elif file_type == "txt":
        text_chunks = txt.parse_txt(uploaded_file)
    else:
        st.error("Unsupported file format.")
        st.stop()

    trace_id = str(uuid.uuid4())
    ingest_msg = MCPMessage(
        sender="main",
        receiver="ingestion_agent",
        type="INGEST",
        trace_id=trace_id,
        payload={"chunks": text_chunks, "filename": uploaded_file.name}
    )
    dispatcher.send_message(ingest_msg)
    st.session_state["uploaded_filename"] = uploaded_file.name
    st.success(f"{uploaded_file.name} successfully ingested!")

# Handle user query
if user_query and st.session_state.get("uploaded_filename"):
    trace_id = str(uuid.uuid4())
    retrieval_msg = MCPMessage(
        sender="main",
        receiver="retrieval_agent",
        type="RETRIEVE",
        trace_id=trace_id,
        payload={"query": user_query}
    )
    dispatcher.send_message(retrieval_msg)

    st.subheader("📜 Response from LLM:")
    if st.session_state["llm_response"]:
        st.write(st.session_state["llm_response"])
    else:
        st.warning("No response generated for the query.")
