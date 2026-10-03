from pydantic import BaseModel

class MemoryCreate(BaseModel):
    user_id: int
    memory_text: str
    memory_type: str
    importance_score: int
    
    