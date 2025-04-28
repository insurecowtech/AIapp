# import faiss
# import os
# import numpy as np
# import pickle

# FAISS_INDEX_PATH = "faiss_store/index.faiss"
# METADATA_PATH = "faiss_store/metadata.pkl"
# DIM = 512  # for Facenet512

# os.makedirs("faiss_store", exist_ok=True)

# # Load or initialize
# if os.path.exists(FAISS_INDEX_PATH):
#     index = faiss.read_index(FAISS_INDEX_PATH)
#     with open(METADATA_PATH, "rb") as f:
#         metadata_list = pickle.load(f)
# else:
#     index = faiss.IndexFlatL2(DIM)
#     metadata_list = []

# def save_to_faiss(cow_id: str, embedding: list, metadata: dict):
#     vector = np.array(embedding).astype('float32').reshape(1, -1)
#     index.add(vector)
#     metadata_list.append({"cow_id": cow_id, **metadata})
#     _persist()

# def check_existing_faiss(embedding: list, threshold=20):
#     vector = np.array(embedding).astype('float32').reshape(1, -1)
#     D, I = index.search(vector, 1)
#     if I[0][0] == -1 or D[0][0] > threshold:
#         return None
#     return metadata_list[I[0][0]]["cow_id"]

# def delete_from_faiss(cow_id: str):
#     global metadata_list, index
#     keep = [i for i, m in enumerate(metadata_list) if m["cow_id"] != cow_id]
#     if len(keep) == len(metadata_list):
#         return False

#     metadata_list = [metadata_list[i] for i in keep]
#     embeddings = np.array([index.reconstruct(i) for i in keep]).astype("float32")
#     index.reset()
#     index.add(embeddings)
#     _persist()
#     return True

# def get_all_faiss_ids():
#     return list(set(m["cow_id"] for m in metadata_list))

# def _persist():
#     faiss.write_index(index, FAISS_INDEX_PATH)
#     with open(METADATA_PATH, "wb") as f:
#         pickle.dump(metadata_list, f)


import faiss
import numpy as np
import json
import os

EMBEDDING_DIM = 512
FAISS_INDEX_PATH = 'faiss_store/faiss_index.bin'
METADATA_PATH = 'faiss_store/metadata.json'
os.makedirs("faiss_store", exist_ok=True)

if os.path.exists(FAISS_INDEX_PATH):
    index = faiss.read_index(FAISS_INDEX_PATH)
    with open(METADATA_PATH, 'r') as f:
        metadata_list = json.load(f)
else:
    index = faiss.IndexFlatIP(EMBEDDING_DIM)
    metadata_list = []

def save_to_faiss(cow_id, embedding, metadata):
    embedding = np.array([embedding], dtype='float32')
    faiss.normalize_L2(embedding)
    index.add(embedding)

    metadata_list.append({
        "cow_id": cow_id,
        "metadata": metadata,
        "embedding": embedding.tolist()
    })
    faiss.write_index(index, FAISS_INDEX_PATH)
    with open(METADATA_PATH, 'w') as f:
        json.dump(metadata_list, f)

def check_existing_faiss(embedding, threshold):
    embedding = np.array([embedding], dtype='float32')
    faiss.normalize_L2(embedding)

    distances, indices = index.search(embedding, k=1)
    if distances[0][0] >= threshold:
        return metadata_list[indices[0][0]]["cow_id"]
    return None

def delete_from_faiss(cow_id):
    global metadata_list, index
    metadata_list = [meta for meta in metadata_list if meta["cow_id"] != cow_id]
    embeddings = [np.array(m["metadata"]["embedding"]) for m in metadata_list]
    embeddings = np.array(embeddings).astype('float32')
    index = faiss.IndexFlatIP(EMBEDDING_DIM)
    index.add(embeddings)
    faiss.write_index(index, FAISS_INDEX_PATH)
    with open(METADATA_PATH, 'w') as f:
        json.dump(metadata_list, f)

def get_all_faiss_ids():
    return list(set(m["cow_id"] for m in metadata_list))