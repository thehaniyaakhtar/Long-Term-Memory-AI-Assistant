from app.database.database import SessionLocal
from app.memory.memory_pipeline import process_message

db = SessionLocal()

try:
    
    messages = [
        "I am studying ML",
        "I am studying ML",
        "Hey, how are you"
    ]
    
    for message in messages:
        print("\n Message: ", message)
        
        memories = process_message(
            db = db,
            user_id = 1,
            user_message=message
        )
        
        if memories:
            for memory in memories:
                print(
                    "Saved: ",
                    memory.memory_text
                )
                
        else:
            print("No new memory saved.")
    
finally:
    db.close()
    