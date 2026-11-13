
from sentence_transformers import SentenceTransformer

# Load a pretrained sentence embedding model
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# Sample customer message
sentence = "My strawberries are rotten."

# Convert the sentence into numbers
embedding = model.encode(sentence)

# Display the result
print("Original sentence:", sentence)
print("Embedding shape:", embedding.shape)
print("First 10 values:", embedding[:10])
