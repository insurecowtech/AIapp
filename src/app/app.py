# import gradio as gr
from src.data.frame_extractor import extract_random_frames
from src.models.classifier import predict_image
from src.models.voting import majority_vote
from src.utils.logger import log_prediction  # We'll create this in Step 3
from src.models.detection import Detection
import os
import pandas as pd
# import concurrent.futures
from src.models.embedding import extract_embedding,parallel_preprocess,preprocess_muzzle_image, is_blurry
# from src.db.vector_store import save_to_vector_db, check_existing_cow, delete_cow, get_all_cow_ids #,get_all_cow_metadata
from src.utils.id_helper import generate_cow_id
from src.db.faiss_store import save_to_faiss, check_existing_faiss, delete_from_faiss, get_all_faiss_ids
import random
import cv2
import tempfile


# <Previous Working Code>

def embed_and_register(images, video_path):
    detected_existing_cow = None
    new_embeddings = []
    temp_paths = []
    for img in images:
        # Save image temporarily
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
            cv2.imwrite(tmp.name, img)
            temp_paths.append(tmp.name)
    loaded_images = [cv2.imread(p) for p in temp_paths]
    processed_images = parallel_preprocess(loaded_images)

    for img_path, proc_img in zip(temp_paths, processed_images):
        emb = extract_embedding(proc_img)
        if not emb:
            continue
        matched_id = check_existing_faiss(emb,threshold=0.90)
        if matched_id:
            detected_existing_cow = matched_id
            break
        else:
            new_embeddings.append((img_path, emb))

    if detected_existing_cow:
        return False, detected_existing_cow

    new_cow_id = generate_cow_id()
    for path, emb in new_embeddings:
        save_to_faiss(
            cow_id=new_cow_id,
            embedding=emb,
            metadata={
                "frame_name": os.path.basename(path),
                "video_name": os.path.basename(video_path),
                "cow_id": new_cow_id
            }
        )
    return True, new_cow_id


# def embed_and_register(images, video_path):

#     detected_existing_cow = None
#     new_embeddings = []

#     temp_paths = []
#     for img in images:
#         with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
#             cv2.imwrite(tmp.name, img)
#             temp_paths.append(tmp.name)

#     loaded_images = [cv2.imread(p) for p in temp_paths]
#     processed_images = []
#     valid_paths = []

#     for img, path in zip(loaded_images, temp_paths):
#         if not is_blurry(img, threshold=100.0):
#             processed = preprocess_muzzle_image(img)
#             processed_images.append(processed)
#             valid_paths.append(path)
#         else:
#             print(f"⚠️ Skipped blurry image: {path}")

#     for img_path, proc_img in zip(valid_paths, processed_images):
#         emb = extract_embedding(proc_img)
#         if not emb:
#             continue
#         matched_id = check_existing_faiss(emb, threshold=0.80)
#         if matched_id:
#             detected_existing_cow = matched_id
#             break
#         else:
#             new_embeddings.append((img_path, emb))

#     if detected_existing_cow:
#         return False, detected_existing_cow

#     new_cow_id = generate_cow_id()
#     for path, emb in new_embeddings:
#         save_to_faiss(
#             cow_id=new_cow_id,
#             embedding=emb,
#             metadata={
#                 "frame_name": os.path.basename(path),
#                 "video_name": os.path.basename(video_path),
#                 "cow_id": new_cow_id
#             }
#         )
#     return True, new_cow_id



def RegisterCow(video):
    message = ""
    try:
        video_path = video if isinstance(video, str) else video.name
        frame_paths = extract_random_frames(video_path, 100)
        sampled_frame_paths = random.sample(frame_paths, 3)
        predictions = [predict_image(frame) for frame in sampled_frame_paths]
        results = majority_vote(predictions)

        for sampled_frame_paths, prediction in zip(sampled_frame_paths, predictions):
            log_prediction(video_path, sampled_frame_paths, prediction)

        if results.lower() != 'domestic cattle':
            message = f"Given {results}. Wrong animal given, provide a cow video."
            return results, None, None, None, False, message
            # return f"Given {results}. Wrong animal given, provide a cow video.", None
        # print(results)

        
        detector = Detection()
        bounding = detector.detect_and_crop(frame_paths, batch_size=16)

        if len(bounding) < 3:
            # return f"Given animal {results}. Not enough muzzle detected.", None
            message = f"Given animal {results}. Not enough muzzle detected. Upload a proper video with clear cow visuals."
            return results, None, None, None, False, message


        is_new, cow_id = embed_and_register(bounding, video_path)

        if not is_new:
            # return f"Cow already exists in database as {cow_id}. Please do not register duplicates.", bounding[0]
            message = f"Cow already exists in database as {cow_id}. Please do not register duplicates."
            return results, cow_id, None, bounding[0], False, message

        message = "Registration Successful ✅"
        return results, cow_id, len(bounding), bounding[0], True, message 
        # return f"Registration successful ✅\nAssigned ID: {cow_id}\nMuzzle detection: {len(bounding)} frames", bounding[0]

    except Exception as e:
        print(e, 'Func -  RegisterCow, File - app.py, Path - src/app/app.py')
        message = f"Error occurred: {str(e)}, 'Func -  RegisterCow, File - app.py, Path - src/app/app.py'"
        return None, None, None, None, False, message


# Not Implemented Cow Data Deletion Function
# def delete_cow_interface(cow_id):
#     if delete_from_faiss(cow_id):
#         return f"✅ Cow ID {cow_id} successfully deleted."
#     return f"❌ Cow ID {cow_id} not found."




def IdentifyCow(image):
    message = ''
    try:
        # with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
        #     cv2.imwrite(tmp.name, image)
        #     image_path = tmp.name

        image_path = image if isinstance(image, str) else image.name

        prediction = predict_image(image_path)
        if prediction.lower() != 'domestic cattle':
            # return f"Given animal is '{prediction}', not a cow."
            message = f"Given animal is '{prediction}', not a cow."
            return message, None, None 

        detector = Detection()
        bounding = detector.detect_and_crop([image_path], batch_size=1)

        if not bounding:
            # return "❌ No muzzle detected in the image. Ensure the muzzle is clear, unobstructed, and facing camera."
            message = "❌ No muzzle detected in the image. Please try another image."
            return message, None, None


        processed_img = preprocess_muzzle_image(bounding[0])
        if processed_img is None:
            # return "❌ Image is too blurry. Please use a clearer image."
            message = "❌ Image is too blurry. Please use a clearer image."
            return message, None, None

        emb = extract_embedding(processed_img)
        if not emb:
            # return "❌ Failed to extract embedding."
            message = "❌ Failed to extract embedding."
            return message, None, None

        matched_id = check_existing_faiss(emb,0.90)
        if matched_id:
            # return f"✅ This cow is registered as: {matched_id}"
            message = f"✅ This cow is registered as: {matched_id}"
            return message, matched_id, bounding[0]
        

        # return "❌ No matching cow found in database."
        message = "❌ No matching cow found in database."
        return message, None, bounding[0]
    except Exception as e:
        # return f"Error: {str(e)}"
        message = f"Error occurred: {str(e)}"
        return message, None, None


if __name__ == "__main__":
    pass
    # with gr.Blocks() as demo:
    #     gr.Markdown("""
    #     ## Cow Muzzle Identification and Detection
    #     ⚠️ **Tip:** On mobile, if your webcam is not supported, use file upload instead.
    #     """)

    #     with gr.Tab("Register Cow"):
    #         video_input = gr.Video(label="Record or Upload Cow Video", sources=["webcam", "upload"])
    #         output_text = gr.Textbox(label="Result")
    #         image_output = gr.Image(label="Segmented Muzzle")
    #         submit_button = gr.Button("Process Video")
    #         submit_button.click(fn=process_video, inputs=video_input, outputs=[output_text, image_output])

    #     with gr.Tab("Delete Cow"):
    #         cow_list = gr.Dropdown(label="Select Cow ID")
    #         refresh_btn = gr.Button("🔄 Refresh List")
    #         delete_result = gr.Textbox(label="Deletion Result")
    #         delete_button = gr.Button("Delete Cow")

    #         def update_dropdown():
    #             return gr.update(choices=get_all_faiss_ids())

    #         refresh_btn.click(fn=update_dropdown, outputs=cow_list)
    #         delete_button.click(fn=delete_cow_interface, inputs=cow_list, outputs=delete_result)


    #     with gr.Tab("Claim Cow"):
    #         claim_input = gr.Image(label="Upload Muzzle Image")
    #         claim_result = gr.Textbox(label="Claim Result")
    #         # image_output = gr.Image(label="Segmented Muzzle")
    #         claim_button = gr.Button("Check Cow")
    #         claim_button.click(fn=claim_cow, inputs=claim_input, outputs= claim_result)

    # demo.launch(share=True)