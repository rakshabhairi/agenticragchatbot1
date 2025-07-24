
# Agentic RAG Chatbot  [agentic-rag-chatbot.com](https://agentic-rag-chatbot.up.railway.app/)


## Overview

This project is a Retrieval-Augmented Generation (RAG) chatbot built using a multi-agent architecture. It answers user questions based on the content of uploaded documents in different formats. Each agent in the system has a specific role and communicates using a custom message format called Model Context Protocol (MCP).

The chatbot supports multiple file types like PDF, PPTX, DOCX, CSV, and TXT/Markdown, and uses a language model to provide answers with relevant context.


## Key Features

* **Document Upload and Parsing**
  Supports PDF, PPTX, DOCX, CSV, and TXT/Markdown formats.

* **Agent-Based Design**

  * **IngestionAgent**: Parses and chunks documents.
  * **RetrievalAgent**: Handles embedding and semantic search.
  * **LLMResponseAgent**: Builds final prompt and generates answers.

* **Model Context Protocol (MCP)**
  Used for communication between agents with structured message objects.

* **Semantic Search with FAISS**
  Embedding-based retrieval using FAISS and sentence-transformers.

* **Streamlit UI**
  Clean interface for uploading documents and interacting with the chatbot.

* **Multi-Turn QA Support**
  Handles follow-up questions using the retrieved document context.


## Folder Structure

```
agentic_rag_chatbot/
├── agents/
│   ├── ingestion_agent.py
│   ├── retrieval_agent.py
│   ├── llm_response_agent.py
|
├── embeddings/
│   └── embedder.py
├── parsers/
│   ├── pdf_parser.py
│   ├── pptx_parser.py
│   ├── docx_parser.py
│   ├── csv_parser.py
│   └── txt_parser.py
├── vector_store/
│   └── faiss_store.py
├── mcp/
│   └── message_dispatcher.py
|   └── __init__.py
├── ui/
│   └── streamlit_app.py
├── utils/
│   └── chunking.py
├── main.py
├── README.md
└── requirements.txt
```

---

## System Flow

1. User uploads a document through the UI.
2. The **IngestionAgent** parses and processes the document content into chunks and stores them in FAISS.
3. When a user asks a question, the **RetrievalAgent** performs semantic search to fetch relevant chunks.
4. The **LLMResponseAgent** formats a query using both context and question and calls the LLM API.
5. The response is returned and shown to the user, along with the source context.

All agents exchange information using MCP messages to keep the architecture modular and traceable.

---

## MCP Format Example

```json
{
  "sender": "RetrievalAgent",
  "receiver": "LLMResponseAgent",
  "type": "RETRIEVAL_RESULT",
  "trace_id": "rag-457",
  "payload": {
    "retrieved_context": ["context chunk 1", "context chunk 2"],
    "query": "What KPIs were tracked in Q1?"
  }
}
```

---

## Technologies Used

* Python 3.11+
* Streamlit (UI)
* Cohere API (LLM - `command-r-plus`)
* FAISS (Vector Search)
* Sentence Transformers (`all-MiniLM-L6-v2`)
* python-pptx, python-docx, PyMuPDF, pandas

---

## Getting Started

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/agentic_rag_chatbot.git
   cd agentic_rag_chatbot
   ```

2. **Create a virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Add your Cohere API key**
   Open `agents/llm_response_agent.py` and set your key:

   ```python
   co = cohere.Client("YOUR_COHERE_API_KEY")
   ```

5. **Run the app**

   ```bash
   streamlit run ui/streamlit_app.py
   ```

---

## Video Explanation

[Watch the walkthrough (Demo + Architecture + Code)](https://vimeo.com/1098989359?share=copy)

* 1 min: Application Demo
* 2 min: System Architecture and Flow
* 2 min: Code Walkthrough

---

## Challenges Faced

* Handling parsing inconsistencies across different document types
* Managing MCP message flow clearly across agents
* Embedding large documents efficiently
* Supporting multi-turn conversation context
* Resolving dependency compatibility issues in Python 3.11+

---

## Future Scope

* Add Excel and Markdown support
* Include other LLMs like OpenAI, Mistral, Claude
* Switch to FastAPI + Docker deployment
* Use message brokers like Kafka/RabbitMQ for better async handling
* Add user-based session and chat history
* Highlight document chunks used in answers

---

# agenticragchatbotmain
 d64bb8d4b57e009b748a347856a112972c9343a8
