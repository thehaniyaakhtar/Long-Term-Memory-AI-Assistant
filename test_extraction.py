from app.memory.extraction_service import extract_memories


message = (
    "I am studying AIML and want to pursue "
    "a Master's in Europe."
)

memories = extract_memories(message)

for memory in memories:
    print(memory)