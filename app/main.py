from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.memory.memory_service import create_memory
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