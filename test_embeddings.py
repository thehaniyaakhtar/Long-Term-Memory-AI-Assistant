from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

text = "User likes ABC"

embedding = model.encode(text)

print("Embedding created")
print("Number of dimensions: ", len(embedding))
print("First 5 values: ", embedding[:5])
