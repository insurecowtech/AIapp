# from deepface import DeepFace
# import uuid
# import numpy as np

# def extract_embeddings(image_paths, model_name="Facenet512"):
#     embeddings = []
#     for img_path in image_paths:
#         embedding_obj = DeepFace.represent(img_path=img_path, model_name=model_name, enforce_detection=False)
#         if embedding_obj:
#             embeddings.append(embedding_obj[0]["embedding"])
#     return embeddings

# def assign_id():
#     return str(uuid.uuid4())
# from deepface import DeepFace

# def extract_embedding(image_path, model_name="Facenet512"):
#     try:
#         embedding_objs = DeepFace.represent(img_path=image_path, model_name=model_name, enforce_detection=False)
#         return embedding_objs[0]["embedding"]
#     except Exception as e:
#         print(f"Embedding extraction failed for {image_path}: {e}")
#         return None
from deepface import DeepFace
import tempfile
import cv2
import numpy as np
from concurrent.futures import ThreadPoolExecutor

def preprocess_muzzle_image(img,blur_threshold=100.0, check_blur=True):
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    if check_blur:
        variance = cv2.Laplacian(gray, cv2.CV_64F).var()
        if variance < blur_threshold:
            print(f"⚠️ Image skipped due to low sharpness (variance: {variance:.2f})")
            return None
    # Enhance contrast using CLAHE
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray)
    
    # Resize image consistently
    processed = cv2.resize(enhanced, (160, 160))
    
    # Convert single channel grayscale to 3-channel
    processed = cv2.cvtColor(processed, cv2.COLOR_GRAY2BGR)
    
    return processed

def parallel_preprocess(images):
    with ThreadPoolExecutor() as executor:
        processed_images = list(executor.map(preprocess_muzzle_image, images))
    return processed_images


def is_blurry(image, threshold=100.0):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    variance = cv2.Laplacian(gray, cv2.CV_64F).var()
    return variance < threshold


# def extract_embedding(image_input, model_name="ArcFace"):
#     try:
#         if isinstance(image_input, np.ndarray):
#             with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
#                 cv2.imwrite(tmp.name, image_input)
#                 img_path = tmp.name
#         else:
#             img_path = image_input

#         img = cv2.imread(img_path)
#         processed_img = preprocess_muzzle_image(img)

#         embedding_objs = DeepFace.represent(processed_img, model_name=model_name, enforce_detection=False)
#         embedding = embedding_objs[0]["embedding"]
#         embedding = embedding / np.linalg.norm(embedding)
#         return embedding.tolist()
#     except Exception as e:
#         print(f"Embedding extraction failed for input: {e}")
#         return None

def extract_embedding(processed_img, model_name="Facenet512"):
    try:
        embedding_objs = DeepFace.represent(processed_img, model_name=model_name, enforce_detection=False)
        embedding = embedding_objs[0]["embedding"]
        embedding = embedding / np.linalg.norm(embedding)
        return embedding.tolist()
    except Exception as e:
        print(f"Embedding extraction failed: {e}")
        return None