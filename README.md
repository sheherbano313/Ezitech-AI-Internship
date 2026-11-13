# FreshCart AI Support – RAG Knowledge Base

## 1. Project Overview

This project builds a Retrieval-Augmented Generation (RAG) knowledge base for FreshCart Grocers' customer support system.

It uses Sentence Transformers to convert customer support tickets into numerical embeddings and FAISS to retrieve semantically similar tickets.

The retrieved tickets and their suggested replies can later provide relevant context to an AI model for drafting customer support responses.

## 2. Features

- Sample dataset containing 20 customer support tickets.
- Data cleaning and preprocessing.
- Text embeddings using Sentence Transformers.
- FAISS vector index creation and storage.
- Metadata storage in JSON format.
- Semantic similarity search for relevant support tickets.

## 3. Technologies Used

- Python 3.12
- Pandas
- NumPy
- Sentence Transformers
- FAISS (faiss-cpu)
- Jupyter Notebook

## 4. Project Structure

```text
freshcart-rag-knowledge-base/
│
├── data/
│   ├── raw/
│   │   └── support_tickets.csv
│   └── processed/
│       └── cleaned_support_tickets.csv
│
├── Notebook/
│   ├── data_exploration.ipynb
│   └── embedding_generation.ipynb
│
├── src/
│   ├── generate_data.py
│   ├── data_cleaning.py
│   ├── test_embedding.py
│   └── build_faiss_index.py
│
├── vector_store/
│   ├── faiss.index
│   └── metadata.json
│
├── logs/
├── .gitignore
└── README.md
```

## 5. Dataset

The project uses a synthetic sample dataset of 20 customer support tickets.

Each ticket contains:

- `id`: Unique ticket identifier
- `subject`: Ticket subject
- `body`: Customer's message
- `correct_reply`: Suggested support response
- `category`: Ticket category

The dataset covers these categories:

- Organic Produce Quality
- Delivery Delays
- Refunds and Returns
- Missing or Damaged Items
- Order Cancellation
- Payment Issues
- General Store Policies

**Note:** The dataset and suggested replies are illustrative sample data, not official FreshCart policies or verified customer records.

## 6. Installation and Setup

### Step 1: Clone the repository

```bash
git clone https://github.com/sheherbano313/Ezitech-AI-Internship.git
cd Ezitech-AI-Internship
```

### Step 2: Create a virtual environment

```bash
python -m venv .venv
```

Activate it:

**Windows (Git Bash):**

```bash
source .venv/Scripts/activate
```

**Windows (Command Prompt):**

```bash
.venv\Scripts\activate
```

### Step 3: Install dependencies

```bash
pip install pandas numpy sentence-transformers faiss-cpu jupyter
```

## 7. How to Run

Run the following command from the project root directory:

```bash
python src/build_faiss_index.py
```

The script will:

1. Load the cleaned support ticket CSV file.
2. Validate the required dataset columns.
3. Clean missing text values.
4. Combine ticket subjects and message bodies.
5. Generate embeddings using `all-MiniLM-L6-v2`.
6. Create a FAISS index.
7. Save the index and ticket metadata locally.

### Expected Output

```text
FAISS index created successfully!
Total tickets: 20
Embedding dimensions: 384
Index saved at: vector_store/faiss.index
Metadata saved at: vector_store/metadata.json
```

The first execution may download the Sentence Transformer model if it is not already cached.

## 8. Vector Store

The generated vector store contains:

- `faiss.index`: FAISS index containing the ticket embeddings.
- `metadata.json`: Corresponding ticket information, including IDs, subjects, bodies, categories, and suggested replies.

The embeddings have 384 dimensions.

## 9. Similarity Search

The FAISS index can retrieve support tickets that are semantically similar to a customer query.

For example:

**Query:** My strawberries arrived rotten and damaged.

The system retrieves relevant organic produce quality tickets based on embedding similarity.

Lower L2 distance indicates greater similarity.

## 10. Limitations

- The dataset contains synthetic sample tickets.
- Suggested replies are illustrative and should not be treated as official company policies.
- This task implements the retrieval knowledge base, not the complete automated response-generation workflow.

## 11. Author

**Sheher Bano**

AI Intern – Ezitech

GitHub: https://github.com/sheherbano313