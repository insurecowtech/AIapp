import os
import cv2
from ultralytics import YOLO
import numpy as np
from concurrent.futures import ThreadPoolExecutor
import torch

# print(os.getcwd(), "From src/models/detection.py")


class Detection:
    def __init__(self):
        # Change The model path. The Original Path is "/src/models/YOLOv11L_Detection.pt" 
        self.__MODEL_PATH = os.path.join(os.getcwd(), 'src', 'models', 'YOLOv11L_Detection.pt')
        # self.__MODEL_CONFIDENCE = 0.5
        self.confidence_threshold = 0.5
        self.detection_limit = 15
        self.__IMG_SIZE = (640, 640)
        # self.__DETECTION_LIMIT = 15
        self.model = self.load_model()
        self.output_dir = 'cropped_muzzles'
        os.makedirs(self.output_dir, exist_ok=True)

    def load_model(self):
        # For Mac OS System, Use MPS instead of CPU
        return YOLO(self.__MODEL_PATH).to('cuda' if torch.cuda.is_available() else 'cpu')
    
    
    def load_images_parallel(self, frame_paths):
        with ThreadPoolExecutor() as executor:
            images = list(executor.map(cv2.imread, frame_paths))
        return images


    # def DetectMuzzle(self, frame_paths, model=None):
    #     if model is None:
    #         model = self.LoadModel()
    #     detections = {}
    #     detection_count = 0
    #     for idx, frame_path in enumerate(frame_paths):
    #         img = cv2.imread(frame_path)
    #         if img is None:
    #             continue
    #         results = model(img, conf=self.__MODEL_CONFIDENCE, verbose=False)
    #         if results and results[0].boxes.xyxy.shape[0] > 0:
    #             box = results[0].boxes.xyxy.cpu().numpy()
    #             detections[idx] = {'image': img, 'coord': box}
    #             detection_count += 1
    #         if detection_count >= self.__DETECTION_LIMIT:
    #             break
    #     return detections
    # def DetectMuzzle(self, frame_paths, model=None):
    #     if model is None:
    #         model = self.LoadModel()
    #     cropped_images = []
    #     for frame_path in frame_paths:
    #         img = cv2.imread(frame_path)
    #         if img is None:
    #             continue
    #         results = model(img, conf=self.__MODEL_CONFIDENCE, verbose=False)
    #         if results and results[0].boxes.xyxy.shape[0] > 0:
    #             boxes = results[0].boxes.xyxy.cpu().numpy()
    #             for box in boxes:
    #                 x1, y1, x2, y2 = map(int, box)
    #                 cropped = img[y1:y2, x1:x2]
    #                 cropped_images.append(cropped)
    #         if len(cropped_images) >= self.__DETECTION_LIMIT:
    #             break
    #     return cropped_images

    # def preprocess_image(self, image):
    #     # Resize and normalize the image
    #     preprocessed = cv2.resize(image, self.__IMG_SIZE)
    #     preprocessed = preprocessed / 255.0
    #     return preprocessed
    # def preprocess_images(self, images):
    #     with ThreadPoolExecutor() as executor:
    #         preprocessed_images = list(executor.map(self.preprocess_image, images))
    #     return preprocessed_images
    
    def detect_and_crop(self, frame_paths, batch_size=16):
        # images = [cv2.imread(fp) for fp in frame_paths]
        images = self.load_images_parallel(frame_paths)
        results = []

        # Batch detection using YOLO
        for i in range(0, len(images), batch_size):
            batch = images[i:i+batch_size]
            results.extend(self.model(batch, conf=self.confidence_threshold, verbose=False))

        cropped_images = []
        # segmentation_image = None
        # total_processed = 0

        for img, result in zip(images, results):
            if result.masks is not None and result.masks.data.shape[0] > 0:
                mask = result.masks.data[0].cpu().numpy()
                mask = cv2.resize(mask, (img.shape[1], img.shape[0]))
                x1, y1, x2, y2 = result.boxes.xyxy[0].cpu().numpy().astype(int)
                masked_img = cv2.bitwise_and(img, img, mask=mask.astype(np.uint8))
                segmentation_crop = masked_img[y1:y2, x1:x2]
                cropped_images.append(segmentation_crop)
            elif result.boxes.xyxy.shape[0] > 0:
                box = result.boxes.xyxy[0].cpu().numpy().astype(int)
                x1, y1, x2, y2 = box
                cropped = img[y1:y2, x1:x2]
                cropped_images.append(cropped)

        return cropped_images  

        # for idx, (img, result) in enumerate(zip(images, results)):
        #     if result.boxes.xyxy.shape[0] > 0:
        #         box = result.boxes.xyxy[0].cpu().numpy().astype(int)
        #         x1, y1, x2, y2 = box
        #         cropped = img[y1:y2, x1:x2]

        #         if segmentation_image is None:
        #             if result.masks is not None and result.masks.data.shape[0] > 0:
        #                 mask = result.masks.data[0].cpu().numpy()
        #                 mask = cv2.resize(mask, (img.shape[1], img.shape[0]))
        #                 masked_img = cv2.bitwise_and(img, img, mask=mask.astype(np.uint8))
        #                 segmentation_image = masked_img[y1:y2, x1:x2]
        #             else:
        #                 segmentation_image = cropped

        #         save_path = os.path.join(self.output_dir, f'crop_{idx}.jpg')
        #         cv2.imwrite(save_path, cropped)
        #         cropped_images.append(save_path)
        #         total_processed += 1

        #     if total_processed >= self.detection_limit:
        #         break

        # if segmentation_image is None and cropped_images:
        #     segmentation_image = cv2.imread(cropped_images[0])

        # return segmentation_image, cropped_images

    
    # def detect_and_crop(self, frame_paths):
    #     model = self.load_model()
    #     images = [cv2.imread(fp) for fp in frame_paths]
    #     results = model(images, conf=self.confidence_threshold, verbose=False)

    #     cropped_images = []
    #     segmentation_image = None

    #     for idx, (img, result) in enumerate(zip(images, results)):
    #         if result.boxes.xyxy.shape[0] > 0:
    #             box = result.boxes.xyxy[0].cpu().numpy().astype(int)
    #             x1, y1, x2, y2 = box
    #             cropped = img[y1:y2, x1:x2]

    #             if segmentation_image is None:
    #                 # Attempt to use segmentation mask
    #                 if result.masks is not None and result.masks.data.shape[0] > 0:
    #                     mask = result.masks.data[0].cpu().numpy()
    #                     mask = cv2.resize(mask, (img.shape[1], img.shape[0]))
    #                     masked_img = cv2.bitwise_and(img, img, mask=mask.astype(np.uint8))
    #                     segmentation_image = masked_img[y1:y2, x1:x2]
    #                 else:
    #                     # If segmentation mask is not available, use bounding box crop
    #                     segmentation_image = cropped

    #                 print(f"No segmentation mask found for image {idx}, using bounding box crop")
    #                 save_path = os.path.join(self.output_dir, f'crop_{idx}.jpg')
    #                 cv2.imwrite(save_path, cropped)
    #                 cropped_images.append(save_path)
    #             else:
    #                 # Save cropped image
    #                 save_path = os.path.join(self.output_dir, f'crop_{idx}.jpg')
    #                 cv2.imwrite(save_path, cropped)
    #                 cropped_images.append(save_path)

    #             if len(cropped_images) >= self.detection_limit:
    #                 break
    #     if segmentation_image is None and cropped_images:
    #         segmentation_image = cv2.imread(cropped_images[0])

    #     return segmentation_image, cropped_images
