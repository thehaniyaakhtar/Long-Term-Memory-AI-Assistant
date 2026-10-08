from sentence_transformers import SentenceTransformer

from app.memory.extraction_service import extract_memories
from app.memory.memory_service import create_memory
from app.memory.memory_decision import should_remember
from app.memory.duplicate_service import find_similar_memory
from app.vector_store.qdrant import store_memory_vector


embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


def process_message(db, user_id, user_message):

    # 1. Decide whether the message is worth remembering
    if not should_remember(user_message):
        return []

    # 2. Extract individual memories
    extracted_memories = extract_memories(
        user_message
    )

    saved_memories = []

    # 3. Process each extracted memory
    for item in extracted_memories:

        memory_text = item["memory_text"]

        # 4. Check whether a similar memory already exists
        existing_memory = find_similar_memory(
            db=db,
            user_id=user_id,
            memory_text=memory_text
        )

        if existing_memory:
            print(
                "Duplicate memory skipped:",
                memory_text
            )
            continue

        # 5. Create embedding
        embedding = embedding_model.encode(
            memory_text
        ).tolist()

        # 6. Save memory in PostgreSQL
        memory = create_memory(
            db=db,
            user_id=user_id,
            memory_text=memory_text,
            memory_type=item["memory_type"],
            importance_score=item["importance_score"]
        )

        # 7. Save vector in Qdrant
        try:
            store_memory_vector(
                memory_id=memory.id,
                embedding=embedding
            )

        except Exception:
            db.delete(memory)
            db.commit()
            raise

        saved_memories.append(memory)

    return saved_memories