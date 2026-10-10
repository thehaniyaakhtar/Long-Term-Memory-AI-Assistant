from fastapi import FastAPI, Depends
# SQLA session is used to communicate with the database
from sqlalchemy.orm import Session

# SessionLocal creates db sessions
from app.database.database import SessionLocal

# Databse operations for memories
from app.memory.memory_service import (
    create_memory,
    get_all_memories,
    get_memory,
    update_memory,
    delete_memory
)
# Pydantic schemas, used to validate incoming API data
from app.memory.schemas import MemoryCreate, MemoryUpdate


from fastapi import UploadFile, File, HTTPException
from pydantic import BaseModel

from app.agent.chat_graph import chat_graph
from app.memory.file_processing import (
    extract_file_text,
    save_file_memories
)

from pathlib import Path
from fastapi.staticfiles import StaticFiles

# Creating the application via object that defines API
app = FastAPI(
    title = "Long Term Memory AI Assistant"
)

# Function that creates a database session for each API request
def get_db():
    db = SessionLocal()
    
    try: 
        # Function that creates a database session for each API request
        yield db
    finally:
        # Close application after request
        db.close()
        
        
@app.get("/")
def home():
    return{
        "message": "Long-Term Memory AI Assistant is running"
    }
    
# CREATING MEMORY
# POST to create new data
# /memories is the URL endpoint
@app.post("/memories")

def create_new_memory(
    # FastAPI receives JSON fromm the request, validates it using MemoryCreate schema
    memory: MemoryCreate,
    
    # "give this function a database session"
    db: Session = Depends(get_db)
):
    
    # Call service function to insert memory into the database
    new_memory = create_memory(
     db = db,
     user_id = memory.user_id,
     memory_text = memory.memory_text,
     memory_type = memory.memory_type,
     importance_score = memory.importance_score   
    )
    
    # return newly created memory as JSON
    return {
        "id": new_memory.id,
        "memory_text": new_memory.memory_text,
        "memory_type": new_memory.memory_type,
        "importance_score": new_memory.importance_score
    }


# GET ALL MEMORIES FOR A USER


@app.get("/memories/{user_id}")
def get_memories(
    user_id: int,
    db: Session = Depends(get_db)
):
    # memories ask the server to find all memories
    memories = get_all_memories(
        db = db,
        user_id = user_id
    )
    
    # converting database objects into JSON dictionaries
    return [
        {
            "id": memory.id,
            "memory_text": memory.memory_text,
            "memory_type": memory.memory_type,
            "importance_score": memory.importance_score
        }
        for memory in memories
    ]
  
# for user_id, 
# find one memory using memory and user id  
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

    # if nothing was found, return error
    if memory is None:
        return {"error": "Memory not found"}

    # return memory as JSON
    return {
        "id": memory.id,
        "memory_text": memory.memory_text,
        "memory_type": memory.memory_type,
        "importance_score": memory.importance_score
    }


# Updating memory
@app.put("/memory/{memory_id}")
def update_single_memory(
    memory_id: int,
    user_id: int,
    memory: MemoryUpdate,
    db: Session = Depends(get_db)
):
    # Send updated informationn to the service layer
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


class ChatRequest(BaseModel):
    user_id: int
    question: str


@app.post("/chat")
def chat(request: ChatRequest):
    result = chat_graph.invoke({
        "user_id": request.user_id,
        "question": request.question,
        "memories": [],
        "compressed_context": "",
        "answer": ""
    })

    return {
        "question": request.question,
        "memories_used": result["memories"],
        "answer": result["answer"]
    }


@app.post("/files/{user_id}")
async def upload_file(
    user_id: int,
    file: UploadFile = File(...)
):
    filename = file.filename or ""

    if not filename.lower().endswith((".txt", ".pdf")):
        raise HTTPException(
            status_code=400,
            detail="Only TXT and PDF files are supported."
        )

    file_bytes = await file.read()

    try:
        text = extract_file_text(filename, file_bytes)

        saved = save_file_memories(
            user_id=user_id,
            filename=filename,
            file_text=text
        )

        return {
            "filename": filename,
            "chunks_saved": len(saved),
            "memories": saved
        }

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail="File processing failed. Check the server logs."
        ) from error

    finally:
        await file.close()

app.mount(
    "/ui",
    StaticFiles(
        directory=Path(__file__).parent / "static",
        html=True
    ),
    name="ui"
)