from pydantic import BaseModel

class MemoryCreate(BaseModel):
    user_id: int
    memory_text: str
    memory_type: str
    importance_score: int
    
class MemoryUpdate(BaseModel):
    memory_text: str | None = None
    memory_type: str | None = None
    importance_score: int | None = None