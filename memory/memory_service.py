from app.database.models import Memory

def create_memory(
    db, 
    user_id,
    memory_text,
    memory_type,
    importance_score
):
    memory = Memory(
        user_id = user_id,
        memory_text = memory_text,
        memory_type = memory_type,
        importance_score = importance_score
    )
    
    db.add(memory),
    db.commit(),
    db.refresh(memory)
    
    return (memory)

def get_all_memories(db, user_id):
    return db.query(Memory).filter(
        Memory.user_id == user_id
    ).all()
    

def get_memory(db, memory_id, user_id):
    return db.query(Memory).filter(
        Memory.id == memory_id,
        Memory.user_id == user_id
    ).first()
    
def update_memory(
    db,
    memory_id,
    user_id,
    memory_text = None,
    memory_type = None,
    importance_score = None
):
    memory = get_memory(db, memory_id, user_id)
    
    if memory is None:
        return None
    
    if memory_text is not None:
        memory.memory_text = memory_text
    
    if memory_type is not None:
        memory.memory_type = memory_type
        
    if importance_score is not None:
        memory.importance_score = importance_score
        
    db.commit()
    db.refresh(memory)
    
    return memory

def delete_memory(db, memory_id, user_id):
    memory = get_memory(db, memory_id, user_id)
    
    if memory is None:
        return False
    
    db.delete(memory)
    db.commit()
    
    return True
