from app.database.database import SessionLocal
from app.database.models import Memory

db = SessionLocal()

try:
    memories = db.query(Memory).all()
    
    for memory in memories:
        print("Memory", memory.memory_text)
        print("Type", memory.memory_type)
        print("Importance", memory.importance_score)
        print("---------")
        
finally:
    db.close()
