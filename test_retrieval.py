from sentence_transformers import SentenceTransformer

from app.database.database import SessionLocal
from app.memory.retrieval_service import retrieve_memories


model = SentenceTransformer("all-MiniLM-L6-v2")

query = "What am I studying?"

query_embedding = model.encode(query).tolist()

db = SessionLocal()

try:
    memories = retrieve_memories(
        db=db,
        user_id=1,
        query_embedding=query_embedding,
        limit=5
    )

    for memory in memories:
        print("Memory:", memory.memory_text)
        print("Type:", memory.memory_type)
        print("Importance:", memory.importance_score)
        print("----------------------")

finally:
    db.close()