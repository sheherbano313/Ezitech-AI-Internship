cat > README.md <<'EOF'
# FreshCart RAG Support Drafting Workflow

## Overview
An n8n workflow that receives a customer support message, retrieves relevant historical tickets using FAISS, and generates a suggested reply using a local Qwen2.5 model through Ollama.

The workflow returns JSON. It does not automatically send messages to customers.

## Architecture
Webhook (n8n) → FastAPI retrieval API → FAISS search → Basic LLM Chain (Ollama Qwen2.5) → JSON response.

Error handling: n8n Error Trigger → FastAPI `/log-error` → `logs/errors.jsonl`.

## Technologies
- Python and FastAPI
- FAISS and Sentence Transformers
- n8n
- Ollama and Qwen2.5 (1.5B)
- Docker Desktop

## Project Structure
- `src/app.py`: FastAPI retrieval and error logging endpoints.
- `src/query_faiss.py`: FAISS retrieval logic.
- `vector_store/`: FAISS index and ticket metadata.
- `workflow/`: exported n8n workflow JSON files.
- `logs/errors.jsonl`: recorded workflow errors.
- `docs/`: project documentation.

## Setup

### Start the FastAPI service
Run in PowerShell:

```powershell
cd D:\Ezitech\freshcart-rag-workflow
& "D:\Ezitech\freshcart-rag-knowledge-base\.venv\Scripts\python.exe" -m uvicorn app:app --app-dir .\src --host 0.0.0.0 --port 8000