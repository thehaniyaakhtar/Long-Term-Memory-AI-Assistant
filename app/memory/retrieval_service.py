from app.database.models import Memory


def retrieve_memories(
    db,
    user_id,
    query_embedding,
    limit=5
):
    from app.vector_store.qdrant import search_memory_vectors

    results = search_memory_vectors(
        query_embedding=query_embedding,
        limit=limit
    )

    memories = []

    for result in results:
        memory_id = result.payload["memory_id"]

        memory = db.query(Memory).filter(
            Memory.id == memory_id,
            Memory.user_id == user_id
        ).first()

        if memory:
            memories.append(memory)

    return memories