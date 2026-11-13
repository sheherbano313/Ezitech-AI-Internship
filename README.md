# FreshCart AI Support – RAG Knowledge Base

## Project Overview

This project builds a Retrieval-Augmented Generation (RAG) knowledge base for FreshCart Grocers' customer support system.

It uses Sentence Transformers to convert customer support tickets into numerical embeddings and FAISS to retrieve semantically similar tickets.

The retrieved tickets and their suggested replies can later provide context to an AI model for drafting customer support responses.

## Features

- Sample customer support dataset containing 20 tickets.
- Data cleaning using Pandas.
- Text embeddings using Sentence Transformers.
- Vector indexing and similarity search using FAISS.
- Metadata storage using JSON.
- Retrieval of relevant tickets and their suggested replies.

## Technologies Used

- Python
- Pandas
- NumPy
- Sentence Transformers
- FAISS
- JSON
- Jupyter Notebook

## Project Structure

```text
freshcart-rag-knowledge-base/
│
├── data/
│   ├── raw/
│   │   ├── support_tickets.csv
│   │   └── code.ipynb
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
│   └── test_embedding.py
│
├── vector_store/
│   ├── faiss.index
│   └── metadata.json
│
├── docs/
├── logs/
├── tests/
└── README.md
```

## Installation

Install the required libraries:

```bash
pip install pandas numpy sentence-transformers faiss-cpu jupyter
```

## How to Run

1. Clone or download this repository.
2. Open the project folder in VS Code.
3. Install the required libraries.
4. Launch Jupyter Notebook:

```bash
jupyter notebook
```

5. Open `Notebook/embedding_generation.ipynb`.
6. Run the notebook cells in order to generate embeddings, build the FAISS index, save metadata, and test retrieval.

## How It Works

1. Prepare and clean the customer support dataset.
2. Load the cleaned dataset into a Pandas DataFrame.
3. Combine ticket subjects and customer messages.
4. Generate embeddings using `all-MiniLM-L6-v2`.
5. Convert embeddings into NumPy float32 format.
6. Build a FAISS index using L2 distance.
7. Save the FAISS index and ticket metadata.
8. Convert a new customer query into an embedding.
9. Retrieve the three most similar support tickets.

## Retrieval Example

Example customer query:

"My strawberries arrived rotten and damaged."

The system retrieves relevant tickets, including:

- Mold on strawberries
- Damaged organic apples
- Wilted spinach

The retrieved tickets provide relevant information and suggested replies for future AI response generation.

## Dataset Note

The dataset contains 20 synthetic sample customer support tickets created for project development and testing.

The sample replies are illustrative examples and are not official or approved FreshCart Grocers policies.

## Current Status

Core RAG knowledge base and similarity retrieval have been implemented and tested using Jupyter Notebook.

The next stage is integrating the retrieval system with an AI response drafting workflow using n8n.

## Author

Sheher Bano

Project: FreshCart AI Support Drafting Pipeline