import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'
import io
import uuid
import time
import base64
import numpy as np
from PIL import Image
from src.app.app import RegisterCow, IdentifyCow
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify


app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key


# Configure upload folder
UPLOAD_FOLDER = 'static/uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 1000 * 1024 * 1024  # 16MB max upload size




# Allowed file extensions
ALLOWED_VIDEO_EXTENSIONS = {'mp4', 'mov', 'avi', 'webm', 'mkv', 'flv', 'mpeg', 'wmv'}
ALLOWED_IMAGE_EXTENSIONS = {'jpg', 'jpeg', 'png', 'heic'}



# In-memory storage (replace with your database)
registered_cows = {}
insurance_claims = {}




def allowed_video_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_VIDEO_EXTENSIONS

def allowed_image_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS


def Image_ArrayTobase64(img_array):
    if img_array.dtype != np.uint8:
        img_array = img_array.astype(np.uint8)

    # Convert numpy array to PIL Image
    pil_image = Image.fromarray(img_array)

    # Save the image to a bytes buffer
    img_buffer = io.BytesIO()
    pil_image.save(img_buffer, format="PNG")

    # Get the base64 encoded string
    img_base64 = base64.b64encode(img_buffer.getvalue()).decode("utf-8")
    
    # data URL for rendering in HTML
    data_url = f"data:image/png;base64,{img_base64}"
    return data_url

import requests

def get_geolocation():
    try:
        # Use an IP geolocation API (e.g., ipinfo.io)
        response = requests.get('https://ipinfo.io/json')
        data = response.json()
        
        # Extract location details
        # ip = data.get('ip', 'N/A')
        city = data.get('city', 'N/A')
        region = data.get('region', 'N/A')
        country = data.get('country', 'N/A')
        # loc = data.get('loc', 'N/A')  # Latitude and longitude
        
        # print(f"IP: {ip}")
        # print(f"Location: {city}, {region}, {country}")
        # print(f"Coordinates: {loc}")
        # return loc.split(',')  # Returns [latitude, longitude]

        return f'{city}, {region}, {country}'
    except Exception as e:
        print(f"Error fetching geolocation: {e}")
        return None



@app.route('/')
def home():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':
        # Check if the post request has the file part
        if 'video' not in request.files:
            flash('No video file provided', 'error')
            return redirect(request.url)
        
        file = request.files['video']
        
        # If user does not select file, browser also submits an empty part
        if file.filename == '':
            flash('No video selected', 'error')
            return redirect(request.url)
        
        if file and allowed_video_file(file.filename):
            # Generate unique filename
            filename = secure_filename(file.filename)
            unique_filename = f"{uuid.uuid4()}_{filename}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            
            # time.sleep(3600)

            file.save(filepath)
            print("Video saved at:", filepath, '\n')
            
            animal_name, cow_id, no_of_frames, segmentation_img, reg_flag, message = RegisterCow(filepath)

            os.remove(filepath)  # Remove the video file after processing -- Later On Storage in DB

             # Return animal_name, cow_id, annotated_image_frames, segmentation_img, registration flag, message
            print(message, '\n')
            if reg_flag:
                image_url = Image_ArrayTobase64(segmentation_img)
                flash(message, 'success')
                return render_template('register_success.html',
                                        animal_name=animal_name,
                                        registration_id=cow_id,
                                        geo_location = get_geolocation(),
                                        date=time.strftime('%Y-%m-%d %H:%M:%S'),
                                        no_of_frames=no_of_frames,
                                        image_url=image_url,
                                        message=message
                                       )
            
            else:
                flash(message, 'error')
                return redirect(request.url)
            
            # Get form data
            # cow_name = request.form.get('cowName', '')
            # cow_id = request.form.get('cowId', '')
            # breed = request.form.get('breed', '')
            # age = request.form.get('age', '')
            
            # # Generate a unique registration ID
            # registration_id = str(uuid.uuid4())
            
            # # Store cow information (replace with database storage)
            # registered_cows[registration_id] = {
            #     'name': cow_name,
            #     'cow_id': cow_id,
            #     'breed': breed,
            #     'age': age,
            #     'video_path': filepath,
            #     'registration_date': time.strftime('%Y-%m-%d %H:%M:%S')
            # }
            
            # # Simulate processing delay
            # time.sleep(1)
            
            # flash('Cow successfully registered', 'success')
            # return render_template('register_success.html', 
            #                       registration_id=registration_id, 
            #                       cow_name=cow_name)


        else:
            flash('Invalid file format. Please upload MP4, MOV, or AVI video', 'error')
            return redirect(request.url)
    
    return render_template('register.html')



@app.route('/claim', methods=['GET', 'POST'])
def claim():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'image' not in request.files:
            flash('No image file provided', 'error')
            return redirect(request.url)
        
        file = request.files['image']
        
        # If user does not select file, browser also submits an empty part
        if file.filename == '':
            flash('No image selected', 'error')
            return redirect(request.url)
        
        if file and allowed_image_file(file.filename):
            # Generate unique filename
            filename = secure_filename(file.filename)
            unique_filename = f"{uuid.uuid4()}_{filename}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)

            # time.sleep(3600)

            file.save(filepath)
            print("Image saved at:", filepath, '\n')
            message, matched_id, seg_img = IdentifyCow(filepath)

            os.remove(filepath)  # Remove the image file after processing -- Later On Storage in DB

            print("DEBUG --> ", message, matched_id, seg_img, '\n')

            if matched_id is not None and seg_img is not None:
                flash(message, 'success')
                return render_template('claim_success.html',
                                        matched_id=matched_id,
                                        geo_location = get_geolocation(),
                                        date=time.strftime('%Y-%m-%d %H:%M:%S'),
                                        image_url=Image_ArrayTobase64(seg_img),
                                        message=message
                                       )
                                       

            elif matched_id is None and seg_img is not None:
                flash(message, 'error')
                image_url = Image_ArrayTobase64(seg_img)
                return render_template('claim_failed.html',
                                        image_url=image_url,
                                        matched_id=matched_id,
                                       )
            
            else:
                flash(message, 'error')
                return render_template('claim.html')

            
            # # Get form data
            # claim_id = request.form.get('claimId', '')
            # cow_id = request.form.get('cowId', '')
            # reason = request.form.get('reason', '')
            
            # # Generate a unique claim ID
            # claim_ref = str(uuid.uuid4())
            
            # # Simulate verification process
            # time.sleep(2)
            
            # # For demo purposes, we'll randomly determine success or failure
            # import random
            # verification_success = random.random() > 0.3
            
            # if verification_success:
            #     # Store claim information (replace with database storage)
            #     insurance_claims[claim_ref] = {
            #         'claim_id': claim_id,
            #         'cow_id': cow_id,
            #         'reason': reason,
            #         'image_path': filepath,
            #         'claim_date': time.strftime('%Y-%m-%d %H:%M:%S'),
            #         'status': 'verified'
            #     }
                
            #     return render_template('claim_success.html')
            # else:
            #     return render_template('claim_failed.html')
        else:
            flash('Invalid file format. Please upload JPG, PNG, or HEIC image', 'error')
            return render_template('claim.html')
    
    return render_template('claim.html')
    # return jsonify({'message': 'Hello World', 'status': 200})

# API endpoint for backend integration
@app.route('/api/cows', methods=['GET'])
def get_cows():
    return jsonify(registered_cows)

@app.route('/api/claims', methods=['GET'])
def get_claims():
    return jsonify(insurance_claims)



#if __name__ == '__main__':
#    app.run(debug=False)
