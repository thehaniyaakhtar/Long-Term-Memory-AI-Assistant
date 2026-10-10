
from app.agent.retrieval import retrieve_relevant_memories

question = "What am I studying?"

memories = retrieve_relevant_memories(
    user_id=1,
    question=question
)

print("Question:", question)
print("\nRelevant memories:")

for memory in memories:
    print(memory["memory_text"])
