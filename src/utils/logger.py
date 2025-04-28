import csv
import os
from datetime import datetime

def log_prediction(video_path, frame_path, prediction):
    log_file = 'prediction_logs.csv'
    file_exists = os.path.isfile(log_file)

    with open(log_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['Timestamp', 'Video Path', 'Frame Path', 'Predicted Class', 'Confidence Score'])

        # Determine the predicted class and confidence score
        if isinstance(prediction, dict):
            predicted_class = max(prediction, key=prediction.get)
            confidence_score = prediction[predicted_class]
        else:
            predicted_class = prediction
            confidence_score = 'N/A'  # Confidence not available

        writer.writerow([datetime.now().isoformat(), video_path, frame_path, predicted_class, confidence_score])
