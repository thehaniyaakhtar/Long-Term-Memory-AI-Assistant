from app.agent.graph import graph


messages = [
    "I am studying AIML.",
    "Hey, how are you?"
]


for message in messages:

    result = graph.invoke({
        "user_message": message
    })

    print("\nMessage:", message)

    print(
        "Should remember:",
        result["should_remember"]
    )

    print(
        "Extracted memories:",
        result.get("extracted_memories", [])
    )

    print("--------------------")