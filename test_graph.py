
from app.agent.graph import graph

messages = [
    "I am studying AIML.",
    "I am studying AIML.",
    "Hey, how are you?"
]

for message in messages:
    result = graph.invoke({
        "user_message": message,
        "user_id": 1
    })

    print("\nMessage:", message)
    print("Should remember:", result["should_remember"])
    print("Extracted:", result.get("extracted_memories", []))
    print("New memories:", result.get("new_memories", []))
    print("Duplicates:", result.get("duplicate_memories", []))
    print("--------------------")