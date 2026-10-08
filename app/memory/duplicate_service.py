from app.database.models import Memory

def find_similar_memory(
    db,
    user_id,
    memory_text,
    threshold = 0.85
):
    from sentence_transformers import SentenceTransformer
    from app.vector_store.qdrant import search_memory_vectors
    
    model = SentenceTransformer("all-MiniLM-L6-v2")
    
    # Convert the memory into an embedding
    embedding = model.emcode(
        memory_text
    ).tolist()
    
    results = search_memory_vectors(
        query_embedding = embedding,
        limit = 5
    )
    
    for result in results:
        if result.score < threshold:
            continue
        
        memory_id = result.payload["memory_id"]
        
        memory = db.query(Memory).filter(
            Memory.id == memory_id,
            Memory.user_id == user_id
        ).first()
        
        if memory:
            return memory
        
    return None
    