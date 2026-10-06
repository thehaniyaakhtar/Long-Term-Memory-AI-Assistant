from sentence_transformers import SentenceTransformer
from app.vector_store.qdrant import search_memory_vectors

model = SentenceTransformer("all-MiniLM-L6-v2")

query = "What am I studying?"

query_embedding = model.encode(query).tolist()

results = search_memory_vectors(
    query_embedding = query_embedding,
    limit = 5
)

for result in results:
    print("Memory ID:", result.payload["memory_id"])
    print("Similarity score:", result.score)
    print("----------------------")  