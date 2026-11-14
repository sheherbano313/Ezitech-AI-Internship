
from pathlib import Path
import argparse
import contextlib
import io
import json
import sys

import faiss
from sentence_transformers import SentenceTransformer

BASE_DIR = Path(__file__).resolve().parent.parent

INDEX_PATH = BASE_DIR / "vector_store" / "faiss.index"
METADATA_PATH = BASE_DIR / "vector_store" / "metadata.json"


def load_resources():
    # Suppress model download and loading messages
    with contextlib.redirect_stdout(io.StringIO()), \
         contextlib.redirect_stderr(io.StringIO()):
        model = SentenceTransformer("all-MiniLM-L6-v2")

    index = faiss.read_index(str(INDEX_PATH))

    with open(METADATA_PATH, "r", encoding="utf-8") as file:
        metadata = json.load(file)

    return model, index, metadata


def search_tickets(query, model, index, metadata, top_k):
    with contextlib.redirect_stdout(io.StringIO()), \
         contextlib.redirect_stderr(io.StringIO()):
        embedding = model.encode(
            [query],
            show_progress_bar=False
        ).astype("float32")

    distances, indices = index.search(embedding, top_k)

    results = []

    for distance, idx in zip(distances[0], indices[0]):
        if idx < 0:
            continue

        ticket = metadata[idx]

        results.append({
            "ticket_id": ticket["id"],
            "category": ticket["category"],
            "subject": ticket["subject"],
            "body": ticket["body"],
            "suggested_reply": ticket["correct_reply"],
            "distance": round(float(distance), 4)
        })

    return {"query": query, "results": results}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", required=True)
    parser.add_argument("--top-k", type=int, default=3)
    args = parser.parse_args()

    if args.top_k < 1:
        print(json.dumps({"error": "top-k must be at least 1"}))
        return 1

    try:
        model, index, metadata = load_resources()

        output = search_tickets(
            args.query,
            model,
            index,
            metadata,
            min(args.top_k, index.ntotal)
        )

        print(json.dumps(output, ensure_ascii=False))
        return 0

    except Exception:
        print(json.dumps({
            "error": "Retrieval failed. Check the model, index and metadata."
        }))
        return 1


if __name__ == "__main__":
    sys.exit(main())
