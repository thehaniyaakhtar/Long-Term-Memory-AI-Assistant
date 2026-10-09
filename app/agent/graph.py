from typing import TypedDict
from app.memory.duplicate_service import find_similar_memory

from langgraph.graph import (
    StateGraph,
    START,
    END
)

from app.memory.memory_decision import should_remember
from app.memory.extraction_service import extract_memories


class AgentState(TypedDict):
    user_message: str
    should_remember: bool
    extracted_memories: list
    duplicate_memories: list


def decide_memory(state: AgentState):

    result = should_remember(
        state["user_message"]
    )

    return {
        "should_remember": result
    }


def extract_memory(state: AgentState):

    memories = extract_memories(
        state["user_message"]
    )

    return {
        "extracted_memories": memories
    }


def memory_decision_router(state: AgentState):

    if state["should_remember"]:
        return "extract"

    return "end"


builder = StateGraph(AgentState)


# Nodes
builder.add_node(
    "decide",
    decide_memory
)

builder.add_node(
    "extract",
    extract_memory
)


# START → decide
builder.add_edge(
    START,
    "decide"
)


# Decide → extract OR end
builder.add_conditional_edges(
    "decide",
    memory_decision_router,
    {
        "extract": "extract",
        "end": END
    }
)


# Extract → END
builder.add_edge(
    "extract",
    END
)


graph = builder.compile()