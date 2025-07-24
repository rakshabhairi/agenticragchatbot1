import sys
import os
import time

# Add project root directory to sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
print("Python PATH:", sys.path)
print("Working dir:", os.getcwd())

from mcp.message_dispatcher import MCPDispatcher, MCPMessage
from agents.ingestion_agent import IngestionAgent
from agents.retrieval_agent import RetrievalAgent
from agents.llm_response_agent import LLMResponseAgent
from vector_store.faiss_store import VectorStore
import parsers.pdf_parser as pdf
import parsers.pptx_parser as pptx
import parsers.docx_parser as docx
import parsers.csv_parser as csv
import parsers.txt_parser as txt
import streamlit as st

# Initialize Dispatcher and VectorStore
dispatcher = MCPDispatcher()
vector_store = VectorStore(dim=384)
parsers_dict = {
    "pdf": pdf.parse_pdf,
    "pptx": pptx.parse_pptx,
    "docx": docx.parse_docx,
    "csv": csv.parse_csv,
    "txt": txt.parse_txt
}

# Register agents
IngestionAgent(dispatcher, vector_store, parsers_dict)
RetrievalAgent(dispatcher, vector_store)
LLMResponseAgent(dispatcher)

# Load custom CSS
with open("styles/custom_style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Header Section
st.markdown("""
<div class="app-header">
    <h1 class="app-title"> ⧉ Agentic RAG System  </h1>
    <p class="app-subtitle"></p>
</div>
""", unsafe_allow_html=True)

# Upload Section
st.markdown("""
<div class="card">
    <div class="card-header">
        <svg class="card-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path>
        </svg>
        <h2 class="card-title">Document Upload</h2>
    </div>
    <p class="card-description">Upload your document to begin intelligent analysis and querying</p>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader("Choose a file", type=["pdf", "pptx", "docx", "csv", "txt"])

if uploaded_file:
    file_type = uploaded_file.name.split(".")[-1]
    temp_path = f"temp_upload.{file_type}"

    with st.spinner("Processing document..."):
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        ingestion_msg = MCPMessage(
            sender="UI",
            receiver="IngestionAgent",
            type="DOCUMENT_UPLOAD",
            trace_id="trace-001",
            payload={"file_path": temp_path, "file_type": file_type}
        )
        dispatcher.send_message(ingestion_msg)

    st.success(f"✅ Document '{uploaded_file.name}' successfully processed and indexed")

st.markdown("</div>", unsafe_allow_html=True)

# Query Section
st.markdown("""
<div class="card">
    <div class="card-header">
        <svg class="card-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"></path>
        </svg>
        <h2 class="card-title">Ask a Question</h2>
    </div>
    <p class="card-description">Enter your question about the uploaded document</p>
</div>
""", unsafe_allow_html=True)

query = st.text_input("Your question", placeholder="What would you like to know about the document?")

if query:
    if not uploaded_file:
        st.warning("Please upload a document before asking a question.")
    else:
        loading_placeholder = st.empty()
        loading_html = open("styles/loading_animation.html").read()
        loading_placeholder.markdown(loading_html, unsafe_allow_html=True)

        time.sleep(3)

        loading_placeholder.empty()

        retrieval_msg = MCPMessage(
            sender="UI",
            receiver="RetrievalAgent",
            type="QUERY_REQUEST",
            trace_id="trace-002",
            payload={"query": query}
        )
        dispatcher.send_message(retrieval_msg)

# Display response
if "llm_response" in st.session_state:
    st.markdown("### Agentic Analysis")
    st.markdown(f"""
    <div style="background-color: #ffffff; padding: 1rem; border-radius: 8px; border: 1px solid #e2e8f0; color: black; font-size: 1rem; line-height: 1.6; overflow: visible; white-space: pre-wrap;">
    {st.session_state["llm_response"]}
    </div>
    """, unsafe_allow_html=True)

# System Status
with st.expander("🔧 System Information"):
    st.markdown("""
    **System Status:**
    - Vector Store: Active (384 dimensions)
    - Supported Formats: PDF, PPTX, DOCX, CSV, TXT
    - Agents: Ingestion, Retrieval, LLM Response
    - Message Dispatcher: Running
    """)

# Footer
with open("styles/footer.html") as f:
    st.markdown(f.read(), unsafe_allow_html=True)
