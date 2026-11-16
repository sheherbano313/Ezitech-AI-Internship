
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
- The cloned project repository and its included vector store files


## Setup and Deployment

### 1. Clone the repository

Clone the project and open its root directory:

```powershell
git clone https://github.com/sheherbano313/Ezitech-AI-Internship.git
cd Ezitech-AI-Internship
```

Run the remaining commands from this repository root directory.

### 2. Create the Python environment

Python 3.12 is recommended.

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install fastapi "uvicorn[standard]" pydantic faiss-cpu sentence-transformers
```

The virtual environment is created inside the cloned repository. No external virtual environment or personal computer path is required.

### 3. Start the FastAPI service

From the repository root, run:

```powershell
python -m uvicorn app:app --app-dir src --host 0.0.0.0 --port 8000
```

Keep this terminal running while using the workflow.

Check the API health endpoint:

`http://localhost:8000/health`

The first startup may download the `all-MiniLM-L6-v2` embedding model. An internet connection is required for the initial download.

### 4. Start Ollama

Install and start Ollama on the machine that runs the workflow services.

Check whether the required model is available:

```powershell
ollama list
```

If it is not installed, run:

```powershell
ollama pull qwen2.5:1.5b
```

Keep Ollama running while using the workflow.

### 5. Start and connect n8n

Start Docker Desktop and ensure the n8n container is running.

Open n8n:

`http://localhost:5678`

**Important network requirement:** The FastAPI service and Ollama must run on the same machine as n8n, or they must be reachable by n8n through a valid hostname or network address. The services must not be isolated from the n8n container.

When n8n runs inside Docker on the same Windows machine as FastAPI and Ollama, use:

- FastAPI: `http://host.docker.internal:8000`
- Ollama: `http://host.docker.internal:11434`

When n8n runs directly on the same machine outside Docker, use:

- FastAPI: `http://localhost:8000`
- Ollama: `http://localhost:11434`

If n8n, FastAPI, or Ollama run on separate machines, replace these addresses with the appropriate reachable hostnames or IP addresses. Configure the services and firewall to permit access only from trusted networks. Do not expose Ollama or the API publicly without appropriate security controls.

### 6. Import and configure the workflow

The exported workflow files are located in:

`workflow/`

Import the required JSON workflow into n8n.

Configure the Ollama connection with the reachable Ollama address and confirm that the HTTP Request node uses the reachable FastAPI address followed by:

`/retrieve`

The main workflow is named **FreshCart RAG Workflow**.

### 7. Test the workflow

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

In test mode, activate the workflow again before sending another test request.

For production-mode requests, use:

`http://localhost:5678/webhook/freshcart-support`

The workflow must be published or active for production-mode requests.


## Error Handling

A separate n8n error workflow uses an Error Trigger and sends error details to the FastAPI `/log-error` endpoint.

Errors are recorded locally in:

`logs/errors.jsonl`

This provides a basic record of workflow failures for troubleshooting.

## API Endpoints

The FastAPI service provides:

- `GET /health` - Health check.
- `POST /retrieve` - Retrieves relevant historical support tickets.
- `POST /log-error` - Records workflow errors.

The retrieval endpoint accepts a customer message and a `top_k` value to control the number of retrieved results.

## Evaluation

Ten functional test cases were performed:

1. Damaged strawberries - PASS
2. Late delivery - PASS
3. Refund for cancelled order - PASS
4. Spoiled milk / food safety - FAIL
5. Angry customer complaint - FAIL
6. Vague customer query - FAIL
7. Wrong items delivered - FAIL
8. Duplicate payment - FAIL
9. Out-of-scope question - FAIL
10. The tests identified areas for improvement, including retrieval relevance, unsupported assumptions, refund promises, out-of-scope detection, and graceful error handling.

Detailed test inputs, outputs, results, and observations are documented in the evaluation report.

## Limitations


## Limitations

 **Retrieval gaps:** The knowledge base contains only 20 historical support tickets and does not adequately cover food-safety issues. As a result, relevant food-safety tickets may not be retrieved, leading to incomplete or unreliable responses.

 **No out-of-scope detection:** The workflow does not check whether a customer's question is related to FreshCart services. Unrelated questions may be passed to the AI with irrelevant support tickets, causing incorrect responses.

 **Model over-commitment:** The local Qwen2.5 1.5B model may make assumptions or promise a resolution when the customer's input is unclear or insufficient. The workflow has no clarification loop to ask for missing details before generating a reply.


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
## Screen Recording

[Watch the FreshCart RAG Workflow demonstration]https://github.com/sheherbano313/Ezitech-AI-Internship/blob/master/video.mp4
