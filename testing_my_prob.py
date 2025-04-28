

import cv2

def extract_and_display_frames(video_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise IOError(f"Cannot open video file: {video_path}")

    frame_idx = 0
    total_frames = 0  # Will count incrementally (optional)

    while True:
        ret, frame = cap.read()
        if not ret:
            break  # End of video

        frame_idx += 1
        total_frames = frame_idx  # Update total as we go

        # Display frame with index
        cv2.imshow('Frame', frame)
        cv2.setWindowTitle('Frame', f'Frame {frame_idx}')

        # Exit on 'q' key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Interrupted by user.")
            break

    cap.release()
    cv2.destroyAllWindows()
    print(total_frames)
    print(f"Done. Displayed {frame_idx} frames.")

if __name__ == "__main__":
    video_file = r"C:\Users\Arnab\Videos\New folder\VID-20250423-WA0002.mp4"
    # video_file = r"E:\PythonProjects\INCW_FRONTEND_NEW\static\uploads\4673040d-0bbb-4dcc-9324-42ac60e7b2b5_camera_recording.webm"
    extract_and_display_frames(video_file)



# import requests

# def get_ip_geolocation():
#     try:
#         # Use an IP geolocation API (e.g., ipinfo.io)
#         response = requests.get('https://ipinfo.io/json')
#         data = response.json()
        
#         # Extract location details
#         # ip = data.get('ip', 'N/A')
#         city = data.get('city', 'N/A')
#         region = data.get('region', 'N/A')
#         country = data.get('country', 'N/A')
#         # loc = data.get('loc', 'N/A')  # Latitude and longitude
        
#         # print(f"IP: {ip}")
#         # print(f"Location: {city}, {region}, {country}")
#         # print(f"Coordinates: {loc}")
#         # return loc.split(',')  # Returns [latitude, longitude]

#         return f'{city}, {region}, {country}'
#     except Exception as e:
#         print(f"Error fetching geolocation: {e}")
#         return None

