from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

client = QdrantClient(
    host = "localhost",
    port = 6333
)

COLLECTION_NAME = "memories"

def create_collection():
    collections = client.get_collections().collections
    
    existing_names = [
        collection.name
        for collection in collections
    ]
    
    if COLLECTION_NAME not in existing_names:
        client.create_collection(
            collection_name = COLLECTION_NAME,
            vector_config = VectorParams(
                size = 384,
                distance = Distance.COSINE
            )
        )
        
        print("Collection created!")
        
    else:
        print("Collection already exists")