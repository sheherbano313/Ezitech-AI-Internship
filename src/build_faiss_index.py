
from pathlib import Path
import pandas as pd
import numpy as np
import json
import logging
import faiss
from sentence_transformers import SentenceTransformer


# 1. Project paths
BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "data" / "processed" / "cleaned_support_tickets.csv"
VECTOR_DIR = BASE_DIR / "vector_store"
INDEX_PATH = VECTOR_DIR / "faiss.index"
METADATA_PATH = VECTOR_DIR / "metadata.json"
LOG_DIR = BASE_DIR / "logs"
LOG_PATH = LOG_DIR / "build_index.log"


# 2. Create required directories
VECTOR_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)


# 3. Configure error logging
logging.basicConfig(
    filename=LOG_PATH,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def build_faiss_index():
    try:
        # 4. Load cleaned dataset
        if not DATA_PATH.exists():
            raise FileNotFoundError(f"Dataset not found: {DATA_PATH}")

        df = pd.read_csv(DATA_PATH)

        required_columns = [
            "id", "subject", "body", "correct_reply", "category"
        ]

        missing_columns = [
            col for col in required_columns if col not in df.columns
        ]

        if missing_columns:
            raise ValueError(
                f"Missing required columns: {missing_columns}"
            )

        if df.empty:
            raise ValueError("Dataset is empty.")

        # 5. Handle missing values
        for col in required_columns:
            df[col] = df[col].fillna("")

        # Remove records without searchable text
        df = df[
            (df["subject"].str.strip() != "") |
            (df["body"].str.strip() != "")
        ].copy()

        if df.empty:
            raise ValueError("No usable ticket text found.")

        # 6. Combine subject and body
        df["combined_text"] = (
            df["subject"].str.strip() + ". " +
            df["body"].str.strip()
        )

        # 7. Load Sentence Transformer model
        logging.info("Loading Sentence Transformer model.")

        model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2"
        )

        # 8. Generate embeddings
        embeddings = model.encode(
            df["combined_text"].tolist(),
            show_progress_bar=True
        )

        embeddings = np.asarray(embeddings, dtype=np.float32)

        # 9. Build FAISS index
        dimension = embeddings.shape[1]

        index = faiss.IndexFlatL2(dimension)
        index.add(embeddings)

        # 10. Save FAISS index
        faiss.write_index(index, str(INDEX_PATH))

        # 11. Save metadata
        metadata = df[
            ["id", "subject", "body", "category", "correct_reply"]
        ].to_dict(orient="records")

        with open(METADATA_PATH, "w", encoding="utf-8") as file:
            json.dump(metadata, file, indent=4, ensure_ascii=False)

        logging.info(
            "FAISS index built successfully with %s vectors.",
            index.ntotal
        )

        print("FAISS index created successfully!")
        print("Total tickets:", index.ntotal)
        print("Embedding dimensions:", dimension)
        print("Index saved at:", INDEX_PATH)
        print("Metadata saved at:", METADATA_PATH)

    except Exception as error:
        logging.exception("Failed to build FAISS index: %s", error)
        print("Error:", error)


if __name__ == "__main__":
    build_faiss_index()
