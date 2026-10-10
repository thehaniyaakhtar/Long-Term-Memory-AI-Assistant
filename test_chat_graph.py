
from app.agent.chat_graph import chat_graph

result = chat_graph.invoke({
    "user_id": 1,
    "question": "What am I studying?",
    "memories": [],
    "compressed_context": "",
    "answer": ""
})

print("Question:", result["question"])
print("Retrieved memories:", result["memories"])
print("Compressed context:", result["compressed_context"])
print("Answer:", result["answer"])
