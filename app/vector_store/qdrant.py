# Import tools needed to connect to Qdrant
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

# Python program to your local Qdrant server
client = QdrantClient(
    host = "localhost",
    port = 6333
)

# name of collection
COLLECTION_NAME = "memories"

# defines a function that creates the Qdrant collection
def create_collection():
    # gets all collections currently in Qdrant
    collections = client.get_collections().collections
    
    # extract just their names
    existing_names = [
        collection.name
        for collection in collections
    ]
    
    if COLLECTION_NAME not in existing_names:
        client.create_collection(
            collection_name = COLLECTION_NAME,
            vectors_config = VectorParams(
                # each embedding will have 384 numbers
                size = 384,
                distance = Distance.COSINE
                # Qdrant will use cosine similarity to determine how similar 2 memories are
            )
        )
        
        print("Collection created!")
        
    else:
        print("Collection already exists")
        
        
def store_memory_vector(
    memory_id,
    embedding
):
    client.upsert(
        collection_name = COLLECTION_NAME,
        points = [
            {
                "id": memory_id,
                "vector": embedding,
                "payload": {
                    "memory_id" : memory_id
                }
            }
        ]
    )
    
    print("Memory vector stores in Qdrant")

def search_memory_vectors(
    query_embedding,
    limit = 5
):
    results = client.query_points(
        collection_name = COLLECTION_NAME,
        query = query_embedding,
        limit = limit
    )
    
    return results.points