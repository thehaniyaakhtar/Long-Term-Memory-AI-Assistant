from app.database.database import SessionLocal
from app.database.models import Memory

db = SessionLocal()

try:
    memories = db.query(Memory).all()
    # getting every row from the memory table
    
    for memory in memories:
        print("Memory", memory.memory_text)
        print("Type", memory.memory_type)
        print("Importance", memory.importance_score)
        print("---------")
        # for each memory in the table, print the following
        
finally:
    db.close()
    # close the database
    
    
