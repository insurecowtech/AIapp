import cv2
import random
import os
import numpy as np
# def extract_random_frames(video_path, num_frames, output_dir="data/processed"):
#     """
#     Extracts a specified number of random frames from the video.

#     Args:
#         video_path (str): Path to the input video file.
#         num_frames (int): Number of random frames to extract.
#         output_dir (str): Directory to save the extracted frames.

#     Returns:
#         List[str]: Paths to the extracted frame images.
#     """
#     if not os.path.exists(output_dir):
#         os.makedirs(output_dir)

#     cap = cv2.VideoCapture(video_path)
#     if not cap.isOpened():
#         raise ValueError(f"Cannot open video file: {video_path}")

#     total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
#     print(total_frames)
#     if total_frames < num_frames:
#         cap.release()
#         raise ValueError(f"Video must have at least {num_frames} frames.")

#     frame_indices = sorted(random.sample(range(total_frames), num_frames))
#     frame_paths = []

#     for idx in frame_indices:
#         cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
#         ret, frame = cap.read()
#         if ret:
#             frame_filename = f"frame_{idx}.jpg"
#             frame_path = os.path.join(output_dir, frame_filename)
#             cv2.imwrite(frame_path, frame)
#             frame_paths.append(frame_path)
#         else:
#             raise ValueError(f"Failed to read frame at index {idx}.")

#     cap.release()
#     return frame_paths


# import cv2
# import random
# import os

# def extract_random_frames(video_path, num_frames, output_dir="data/processed"):
#     if not os.path.exists(output_dir):
#         os.makedirs(output_dir)

#     cap = cv2.VideoCapture(video_path)
#     if not cap.isOpened():
#         raise ValueError(f"Cannot open video file: {video_path}")


#     total_frames = 0
#     while cap.isOpened():
#         ret, _ = cap.read()
#         if not ret:
#             break
#         total_frames += 1
#     cap.release()

#     # total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

#     # if total_frames <= 0 or total_frames >= 99999:
#     #     # Fallback: manually count frames if metadata is missing
#     #     print("⚠️ Frame count not available, counting manually...")
#     #     frame_count = 0
#     #     while True:
#     #         ret, _ = cap.read()
#     #         if not ret:
#     #             break
#     #         frame_count += 1
#     #     cap.release()

#         # # Reopen to sample from known frame range
#         # cap = cv2.VideoCapture(video_path)
#         # total_frames = frame_count

#     print(f"Total frames: {total_frames}")

#     if total_frames < num_frames:
#         cap.release()
#         raise ValueError(f"Video must have at least {num_frames} frames.")

#     # frame_indices = sorted(random.sample(range(total_frames), num_frames))

#     frame_paths = []

#     for idx in range(1,total_frames,10):
#         # cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
#         cap.set(total_frames, idx)
#         ret, frame = cap.read()
#         if ret and np.mean(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)) > 50:
#             frame_filename = f"frame_{idx}.jpg"
#             frame_path = os.path.join(output_dir, frame_filename)
#             cv2.imwrite(frame_path, frame)
#             frame_paths.append(frame_path)
#         else:
#             raise ValueError(f"Failed to read frame at index {idx}.")

#     cap.release()
#     return frame_paths

def extract_random_frames(video_path, num_frames, output_dir="data/processed"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # First pass: count total frames reliably
    cap = cv2.VideoCapture(video_path)
    total_frames = 0
    while True:
        ret, _ = cap.read()
        if not ret:
            break
        total_frames += 1
    cap.release()

    print(f"Total frames: {total_frames}")

    if total_frames < num_frames:
        raise ValueError(f"Video must have at least {num_frames} frames.")

    # Generate random indices (now using 0-based indexing)
    frame_indices = sorted(random.sample(range(total_frames), num_frames))
    
    # Second pass: extract frames sequentially
    cap = cv2.VideoCapture(video_path)
    frame_paths = []
    current_idx = 0
    saved_count = 0

    while cap.isOpened() and saved_count < num_frames:
        ret, frame = cap.read()
        if not ret:
            break

        # Check if current frame is one of our targets
        if current_idx == frame_indices[saved_count]:
            # Optional: Skip dark frames
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            if np.mean(gray) > 50:
                frame_filename = f"frame_{current_idx}.jpg"
                frame_path = os.path.join(output_dir, frame_filename)
                cv2.imwrite(frame_path, frame)
                frame_paths.append(frame_path)
                saved_count += 1
            else:
                print(f"Skipped dark frame {current_idx}")

        current_idx += 1

    cap.release()
    
    if len(frame_paths) != num_frames:
        raise ValueError(f"Only extracted {len(frame_paths)}/{num_frames} valid frames")
    
    return frame_paths
