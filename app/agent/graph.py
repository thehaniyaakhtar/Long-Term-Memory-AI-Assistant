
from typing import TypedDict

from langgraph.graph import StateGraph, START, END
from sentence_transformers import SentenceTransformer

from app.memory.memory_decision import should_remember
from app.memory.extraction_service import extract_memories
from app.memory.duplicate_service import find_similar_memory
from app.memory.memory_service import create_memory
from app.database.database import SessionLocal
from app.vector_store.qdrant import store_memory_vector


class AgentState(TypedDict):
    user_message: str
    user_id: int
    should_remember: bool
    extracted_memories: list
    new_memories: list
    duplicate_memories: list
    saved_memories: list


embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


def decide_memory(state: AgentState):
    result = should_remember(state["user_message"])
    return {"should_remember": result}


def extract_memory(state: AgentState):
    memories = extract_memories(state["user_message"])
    return {"extracted_memories": memories}


def memory_decision_router(state: AgentState):
    if state["should_remember"]:
        return "extract"
    return "end"


def check_duplicates(state: AgentState):
    db = SessionLocal()

    try:
        new_memories = []
        duplicate_memories = []

        for item in state.get("extracted_memories", []):
            existing = find_similar_memory(
                db=db,
                user_id=state["user_id"],
                memory_text=item["memory_text"]
            )

            if existing:
                duplicate_memories.append(item["memory_text"])
            else:
                new_memories.append(item)

        return {
            "new_memories": new_memories,
            "duplicate_memories": duplicate_memories
        }

    finally:
        db.close()


def store_memories(state: AgentState):
    db = SessionLocal()
    saved_memories = []

    try:
        for item in state.get("new_memories", []):
            memory_text = item["memory_text"]

            embedding = embedding_model.encode(
                memory_text
            ).tolist()

            memory = create_memory(
                db=db,
                user_id=state["user_id"],
                memory_text=memory_text,
                memory_type=item["memory_type"],
                importance_score=item["importance_score"]
            )

            try:
                store_memory_vector(
                    memory_id=memory.id,
                    embedding=embedding
                )
            except Exception:
                db.delete(memory)
                db.commit()
                raise

            saved_memories.append({
                "id": memory.id,
                "memory_text": memory.memory_text,
                "memory_type": memory.memory_type,
                "importance_score": memory.importance_score
            })

        return {"saved_memories": saved_memories}

    finally:
        db.close()


builder = StateGraph(AgentState)

builder.add_node("decide", decide_memory)
builder.add_node("extract", extract_memory)
builder.add_node("check_duplicates", check_duplicates)
builder.add_node("store", store_memories)

builder.add_edge(START, "decide")

builder.add_conditional_edges(
    "decide",
    memory_decision_router,
    {
        "extract": "extract",
        "end": END
    }
)

builder.add_edge("extract", "check_duplicates")
builder.add_edge("check_duplicates", "store")
builder.add_edge("store", END)

graph = builder.compile()