from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.memory.memory_service import (
    create_memory,
    get_all_memories,
    get_memory,
    update_memory,
    delete_memory
)
from app.memory.schemas import MemoryCreate

app = FastAPI(
    title = "Long Term Memory AI Assistant"
)

def get_db():
    db = SessionLocal()
    
    try: 
        yield db
    finally:
        db.close()
        
        
@app.get("/")
def home():
    return{
        "message": "Long-Term Memory AI Assistant is running"
    }
    
    
@app.post("/memories")

def create_new_memory(
    memory: MemoryCreate,
    db: Session = Depends(get_db)
):
    
    new_memory = create_memory(
     db = db,
     user_id = memory.user_id,
     memory_text = memory.memory_text,
     memory_type = memory.memory_type,
     importance_score = memory.importance_score   
    )
    
    return {
        "id": new_memory.id,
        "memory_text": new_memory.memory_text,
        "memory_type": new_memory.memory_type,
        "importance_score": new_memory.importance_score
    }

@app.get("/memories/{user_id}")
def get_memories(
    user_id: int,
    db: Session = Depends(get_db)
):
    memories = get_all_memories(
        db = db,
        user_id = user_id
    )
    
    return [
        {
            "id": memory.id,
            "memory_text": memory.memory_text,
            "memory_type": memory.memory_type,
            "importance_score": memory.importance_score
        }
        for memory in memories
    ]
    
@app.get("/memory/{memory_id}")
def get_single_memory(
    memory_id: int,
    user_id: int,
    db: Session = Depends(get_db)
):
    memory = get_memory(
        db=db,
        memory_id=memory_id,
        user_id=user_id
    )

    if memory is None:
        return {"error": "Memory not found"}

    return {
        "id": memory.id,
        "memory_text": memory.memory_text,
        "memory_type": memory.memory_type,
        "importance_score": memory.importance_score
    }


@app.put("/memory/{memory_id}")
def update_single_memory(
    memory_id: int,
    user_id: int,
    memory: MemoryUpdate,
    db: Session = Depends(get_db)
):
    updated_memory = update_memory(
        db=db,
        memory_id=memory_id,
        user_id=user_id,
        memory_text=memory.memory_text,
        memory_type=memory.memory_type,
        importance_score=memory.importance_score
    )

    if updated_memory is None:
        return {"error": "Memory not found"}

    return {
        "id": updated_memory.id,
        "memory_text": updated_memory.memory_text,
        "memory_type": updated_memory.memory_type,
        "importance_score": updated_memory.importance_score
    }


@app.delete("/memory/{memory_id}")
def delete_single_memory(
    memory_id: int,
    user_id: int,
    db: Session = Depends(get_db)
):
    deleted = delete_memory(
        db=db,
        memory_id=memory_id,
        user_id=user_id
    )

    if not deleted:
        return {"error": "Memory not found"}

    return {
        "message": "Memory deleted successfully"
    }