
# FreshCart RAG Support Drafting Workflow

## Overview

FreshCart RAG Support Drafting is an n8n-based customer support assistant. It receives a customer message, retrieves relevant historical support tickets using FAISS, and generates a suggested reply using the local Qwen2.5 model through Ollama.

The workflow returns a JSON response. It does not automatically send messages to customers or perform refunds, cancellations, or order changes.

## Architecture

Customer Message
→ n8n Webhook
→ FastAPI Retrieval API
→ FAISS Similarity Search
→ Basic LLM Chain (Ollama Qwen2.5)
→ JSON Response

Error handling:
n8n Error Trigger → FastAPI `/log-error` → `logs/errors.jsonl`

## Technologies

- Python 3.12
- FastAPI
- FAISS
- Sentence Transformers
- n8n
- Ollama
- Qwen2.5 (1.5B)
- Docker Desktop

## Project Structure

- `src/app.py` - FastAPI retrieval and error logging endpoints.
- `src/query_faiss.py` - FAISS retrieval logic.
- `vector_store/` - FAISS index and ticket metadata.
- `workflow/` - Exported n8n workflow JSON files.
- `logs/errors.jsonl` - Recorded workflow errors.
- `docs/` - Project documentation.

## Prerequisites

Install or configure the following before running the project:

- Python 3.12
- Docker Desktop
- n8n (version 2.x)
- Ollama
- Qwen2.5 1.5B model
- The project files and knowledge-base virtual environment

## Setup and Deployment

### 1. Start the FastAPI service

Open PowerShell and run:

```powershell
cd D:\Ezitech\freshcart-rag-workflow

& "D:\Ezitech\freshcart-rag-knowledge-base\.venv\Scripts\python.exe" -m uvicorn app:app --app-dir .\src --host 0.0.0.0 --port 8000
```

Keep this terminal running while using the workflow.

### 2. Start Ollama

Ensure Ollama is running on the Windows host.

Check that the model is available:

```powershell
ollama list
```

If the model is not installed, download it:

```powershell
ollama pull qwen2.5:1.5b
```

### 3. Start n8n

Start Docker Desktop and ensure the n8n container is running.

Open n8n in your browser:

`http://localhost:5678`

The workflow uses these host addresses from inside Docker:

- FastAPI: `http://host.docker.internal:8000`
- Ollama: `http://host.docker.internal:11434`

The `host.docker.internal` hostname allows the n8n container to communicate with services running on the Windows host.

### 4. Configure the n8n workflow

The exported workflow files are located in:

`workflow/`

Import the required JSON exports into n8n when setting up a fresh instance.

Configure the Ollama model connection to use:

`http://host.docker.internal:11434`

Check the HTTP Request node and confirm that its retrieval URL is:

`http://host.docker.internal:8000/retrieve`

The main workflow is named **FreshCart RAG Workflow**.

### 5. Test the workflow

For test mode:

1. Open the FreshCart RAG Workflow in n8n.
2. Click **Execute Workflow**.
3. Wait for the test webhook listener.
4. Send a POST request to:

`http://localhost:5678/webhook-test/freshcart-support`

Example PowerShell request:

```powershell
Invoke-RestMethod -Method POST -Uri "http://localhost:5678/webhook-test/freshcart-support" -ContentType "application/json" -Body '{"ticket_body":"My grocery delivery is late. Please help.","top_k":3}' | ConvertTo-Json -Depth 10
```

In test mode, the webhook accepts one request after each activation. Click Execute Workflow again before another test.

For production-mode webhook requests, use:

`http://localhost:5678/webhook/freshcart-support`

The workflow must be published or active for production-mode requests.

## API Endpoints

The FastAPI service provides:

- `GET /health` - Health check.
- `POST /retrieve` - Retrieves relevant historical support tickets.
- `POST /log-error` - Records workflow errors.

The retrieval endpoint accepts a customer message and a `top_k` value to control the number of retrieved results.

## Error Handling

A separate n8n error workflow uses an Error Trigger and sends error details to the FastAPI `/log-error` endpoint.

Errors are recorded locally in:

`logs/errors.jsonl`

This provides a basic record of workflow failures for troubleshooting.

## Evaluation

Ten functional test cases were performed:

1. Damaged strawberries - PASS
2. Late delivery - PASS
3. Refund for cancelled order - PASS
4. Spoiled milk / food safety - PASS with improvements needed
5. Angry customer complaint - FAIL
6. Vague customer query - FAIL
7. Wrong items delivered - PASS with improvements needed
8. Duplicate payment - FAIL
9. Out-of-scope question - FAIL
10. Empty customer message - PASS with improvements needed

The tests identified areas for improvement, including retrieval relevance, unsupported assumptions, refund promises, out-of-scope detection, and graceful error handling.

Detailed test inputs, outputs, results, and observations are documented in the evaluation report.

## Limitations

- The knowledge base contains a limited sample of 20 historical support tickets.
- Retrieval uses FAISS similarity search and returns up to three tickets by default.
- Retrieval may return partially relevant or irrelevant tickets.
- The local Qwen2.5 1.5B model may generate incorrect assumptions or imperfect responses.
- The system does not connect to live order, inventory, delivery, or payment systems.
- It cannot actually issue refunds, replace products, cancel orders, or verify transactions.
- Generated replies require human review before being sent to customers.
- Customer-name placeholders may require manual editing.
- Empty or invalid input can cause workflow errors; graceful customer-facing validation should be improved.
- Out-of-scope questions are not yet reliably detected.
- The current implementation is a local prototype, not a production-ready customer support deployment.
- Authentication, production-grade privacy controls, and comprehensive monitoring are not implemented.
- Error logs are stored locally.

## Future Improvements

- Improve retrieval quality and relevance.
- Add out-of-scope query detection.
- Strengthen prompt instructions to prevent unsupported assumptions and promises.
- Add graceful input validation and error responses.
- Replace customer-name placeholders with appropriate greetings.
- Add human review and approval before sending replies.
- Integrate secure order and payment verification systems.
- Add a user-friendly frontend.

## Project Status

This project demonstrates a local RAG-based customer support drafting workflow using FastAPI, FAISS, n8n, and Ollama. It is intended as an informational prototype and requires further testing and improvements before real-world deployment.

