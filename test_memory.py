from app.database.database import SessionLocal
from app.database.models import Memory

# opens connection with PSQL to interact with database
db = SessionLocal()

try:
# creating a new memory
    new_memory = Memory(
        user_id = 1,
        memory_text = "User studies AIML",
        memory_type = "semantic",
        importance_score = 9
    )
    
    db.add(new_memory)
    # saving the memory
    
    db.commit()
    # permanently stored
    
    print("Memory saved successfully")
    
except Exception as e:
    db.rollback()
    print("Error:", e)
    # rollback if theres an incomplete database operation
    
finally:
    db.close()