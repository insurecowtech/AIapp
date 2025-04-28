from src.models.embedding import extract_embeddings, assign_id
from src.database.vector_db import add_embeddings, query_embedding

def register_cow(cropped_image_paths):
    cow_id = assign_id()
    embeddings = extract_embeddings(cropped_image_paths)
    add_embeddings(embeddings, cow_id)
    return cow_id

def identify_cow(query_image_path):
    embedding = extract_embeddings([query_image_path])[0]
    results = query_embedding(embedding)
    if results and results['metadatas']:
        return results['metadatas'][0]['cow_id']
    else:
        return None
