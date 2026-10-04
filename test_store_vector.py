from sentence_transformers import SentenceTransformer

from app.vector_store.qdrant import (
    create_collection,
    store_memory_vector
)

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

create_collection()

text = "User studies AIML"

embedding = model.encode(text).tolist()

store_memory_vector(
    memory_id = 1,
    embedding = embedding
)