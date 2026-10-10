
from sentence_transformers import SentenceTransformer

from app.database.database import SessionLocal
from app.memory.retrieval_service import retrieve_memories


embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


def retrieve_relevant_memories(user_id, question):
    # Convert the question into a vector.
    query_embedding = embedding_model.encode(
        question
    ).tolist()

    db = SessionLocal()

    try:
        # Search for memories similar to the question.
        memories = retrieve_memories(
            db=db,
            user_id=user_id,
            query_embedding=query_embedding,
            limit=5
        )

        # Return only the useful details.
        return [
            {
                "id": memory.id,
                "memory_text": memory.memory_text,
                "memory_type": memory.memory_type,
                "importance_score": memory.importance_score
            }
            for memory in memories
        ]

    finally:
        db.close()
