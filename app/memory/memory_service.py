# Import Memory SQLA model to represent memory in the table
from app.database.models import Memory

# creating a new memory
def create_memory(
    db, 
    user_id,
    memory_text,
    memory_type,
    importance_score
):
    # Creating the object
    memory = Memory(
        user_id = user_id,
        memory_text = memory_text,
        memory_type = memory_type,
        importance_score = importance_score
    )
    
    # Saving it to the database
    db.add(memory),
    db.commit(),
    db.refresh(memory) # Refreshes it to get generated values like id and timestamps
    
    return (memory)

def get_all_memories(db, user_id): # Read all memories belonging to specific user
    return db.query(Memory).filter(
        Memory.user_id == user_id
    ).all()
    
# get one specific memory belonging to a specific user
def get_memory(db, memory_id, user_id):
    return db.query(Memory).filter(
        Memory.id == memory_id,
        Memory.user_id == user_id
    ).first()

# updating memory
def update_memory(
    db,
    memory_id,
    user_id,
     # No default values
    memory_text = None,
    memory_type = None,
    importance_score = None
):
    # Finding the memory
    memory = get_memory(db, memory_id, user_id)
    
    # memory, doesnt exist
    if memory is None:
        return None
    
    # only update memory_text if new value was provided
    if memory_text is not None:
        memory.memory_text = memory_text
    
    # only update memory_type if new value was provided
    if memory_type is not None:
        memory.memory_type = memory_type
        
    # only update score if new value was provided
    if importance_score is not None:
        memory.importance_score = importance_score
        
    # these steps are important so as to update the fields that you want only
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
