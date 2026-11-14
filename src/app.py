
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from query_faiss import load_resources, search_tickets
import json
from datetime import datetime, timezone
from pathlib import Path

resources = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Loading FreshCart RAG resources...")

    try:
        model, index, metadata = load_resources()
        resources["model"] = model
        resources["index"] = index
        resources["metadata"] = metadata

        print(f"Loaded {len(metadata)} support tickets.")

    except Exception as exc:
        raise RuntimeError("Failed to load RAG resources.") from exc

    yield

    resources.clear()


app = FastAPI(
    title="FreshCart RAG API",
    description="Retrieves relevant support tickets for customer complaints.",
    version="1.0.0",
    lifespan=lifespan
)


class RetrievalRequest(BaseModel):
    ticket_body: str = Field(min_length=3)
    top_k: int = Field(default=3, ge=1, le=10)

class ErrorLogRequest(BaseModel):
    workflow_name: str = "FreshCart RAG Workflow"
    node_name: str = "Unknown"
    error_message: str = Field(min_length=1)
    execution_id: str | None = None

@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/retrieve")
def retrieve(request: RetrievalRequest):
    if not resources:
        raise HTTPException(status_code=503, detail="RAG resources are not ready.")

    try:
        result = search_tickets(
            request.ticket_body,
            resources["model"],
            resources["index"],
            resources["metadata"],
            min(request.top_k, resources["index"].ntotal)
        )

        return {
            "success": True,
            **result
        }

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Ticket retrieval failed."
        )

@app.post("/log-error")
def log_error(request: ErrorLogRequest):
    log_dir = Path(__file__).resolve().parent.parent / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)

    log_file = log_dir / "errors.jsonl"

    error_data = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        **request.model_dump()
    }

    with log_file.open("a", encoding="utf-8") as file:
        file.write(json.dumps(error_data) + "\n")

    return {
        "success": True,
        "message": "Error logged successfully"
    }