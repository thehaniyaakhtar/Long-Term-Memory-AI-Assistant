from app.database.database import SessionLocal 
from app.memory.memory_service import (
    create_memory,
    get_all_memories,
    get_memory,
    update_memory,
    delete_memory
)

db = SessionLocal()

try:
    memory = create_memory(
        db = db,
        user_id = 1,
        memory_text = "User likes ABC",
        memory_type = "semantic",
        importance_score = 8
    )
    
    print("Created")
    print(memory.id, memory.memory_text)
    
    memories = get_all_memories(db, user_id = 1)
    
    print("\n All memories:")
    for item in memories:
        print(item.id, item.memory_text)
        
        
    found = get_memory(
        db = db,
        memory_id = memory.id,
        user_id = 1
    )
    
    print("\nFound: ")
    print(found.id, found.memory_text)
    
    updated = update_memory(
        db = db,
        memory_id = memory.id,
        user_id = 1,
        importance_score = 10
    )
    
    print("\nUpdated: ")
    print(updated.id, updated.memory_text, updated.importance_score)
    
    deleted = delete_memory(
        db = db,
        memory_id = memory.id,
        user_id = 1
    )
    
    print("\nDeleted: ", deleted)
    
    
finally:
    db.close()