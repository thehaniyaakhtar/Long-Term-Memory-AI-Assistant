from sentence_transformers import SentenceTransformer

from app.memory.extraction_service import extract_memories
from app.vector_store.qdrant import store_memory_vector
from memory.memory_service import create_memory
from app.memory.memory_decision import should_remember

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# receive user message ,coordinate with different components
def process_message(db, user_id, user_message):
    
    if not should_remember(user_message):
    return []

    extracted_memories = extract_memories(user_message)
    
    saved_memories = []
    
    for item in extracted_memories:
        memory_text = item["memory_text"]
        
        # each fact -> 384 numbers
        embedding = embedding_model.encode(
            memory_text
        ).tolist()
        
        # existing service saves text and metadata in PostgreSQL
        memory = create_memory(
            db=db,
            user_id = user_id,
            memory_text = memory_text,
            memory_type = item["memory_type"],
            importance_score = item["importance_score"]
        )
        
        try:
            store_memory_vector(
                memory_id = memory.id,
                embedding = embedding
            )
            
        except Exception:
            db.delete(memory)
            db.commit()
            raise
        
        saved_memories.append(memory)
    
    return saved_memories