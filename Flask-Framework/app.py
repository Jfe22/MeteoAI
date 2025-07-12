from flask import Flask, jsonify
from flask_cors import CORS
import os
import re
import datetime
import requests
import json
import io
import base64
from PIL import Image
import numpy as np
from model import *

app = Flask(__name__)
cors = CORS(app) # Allow access from any origin

# IPMA IMAGES URL
IPMA_RADAR_URL = 'https://www.ipma.pt/resources.www/transf/radar/por/pcr-'
# STATIONS INFORMATION
STATIONS = {
    1200554: {
        'district': 'Faro',
        'radar_box': (736, 1546, 936, 1746)
    },
    1200558: {
        'district': 'Evora',
        'radar_box': (740, 1183, 940, 1383)
    },
    1200562: {
        'district': 'Beja',
        'radar_box': (735, 1546, 935, 1746)
    },
    1200570: {
        'district': 'Castelo Branco',
        'radar_box': (817, 886, 1017, 1086)
    },
    1200571: {
        'district': 'Portalegre',
        'radar_box': (829, 1012, 1029, 1212)
    },
    1200575: {
        'district': 'Braganca',
        'radar_box': (953, 401, 1153, 601)
    },
    1210683: {
        'district': 'Guarda',
        'radar_box': (859, 712, 1059, 912)
    },
    1210702: {
        'district': 'Aveiro',
        'radar_box': (603, 687, 803, 887)
    },
    1210707: {
        'district': 'Coimbra',
        'radar_box': (645, 792, 845, 992)
    },
    1210718: {
        'district': 'Leiria',
        'radar_box': (574, 902, 774, 1102)
    },
    1210734: {
        'district': 'Santarem',
        'radar_box': (597, 1026, 797, 1226)
    },
    1210770: {
        'district': 'Setubal',
        'radar_box': (559, 1193, 759, 1393)
    },
    1240566: {
        'district': 'Vila Real',
        'radar_box': (770, 527, 970, 727)
    },
    1240610: {
        'district': 'Viana do Castelo',
        'radar_box': (570, 428, 770, 628)
    },
    1240675: {
        'district': 'Viseu',
        'radar_box': (740, 682, 940, 882)
    },
    1240903: {
        'district': 'Porto',
        'radar_box': (611, 562, 811, 762)
    },
    6212124: {
        'district': 'Braga',
        'radar_box': (645, 463, 845, 663)
    },
    7240919: {
        'district': 'Lisboa',
        'radar_box': (513, 1149, 713, 1349)
    }
}

# Function to remove black pixels from the image
def remove_black_pixels(image):
    # Convert the image to RGBA mode (if it's not already in RGBA mode)
    image = image.convert('RGBA')
    # Get the pixel data as a list of tuples
    pixels = list(image.getdata())
    # Replace every black pixel with transparent
    new_pixels = []
    for pixel in pixels:
        if pixel[0] == 0 and pixel[1] == 0 and pixel[2] == 0:
            new_pixels.append((0, 0, 0, 0))
        else:
            new_pixels.append(pixel)
    # Create a new image with the same size and mode as the original image
    new_image = Image.new(image.mode, image.size)
    # Update the new image with the new pixel data
    new_image.putdata(new_pixels)
    # Return the new image
    return new_image

# Function to get the radar image from IPMA
def get_radar_image(timestamp):
    try:
        # Format the datetime string
        timestamp_str = timestamp.strftime("%Y-%m-%dT%H%M")
        # Build image URL
        image_url = IPMA_RADAR_URL + timestamp_str + '.png'
        # Get radar image
        response = requests.get(image_url)
        response.raise_for_status()
        image_data = io.BytesIO(response.content)
        img = Image.open(image_data)
        # Remove black pixels from the image
        image = remove_black_pixels(img)
        # Return the image
        return image
    except Exception as e:
        print(e)
        return None

# Function to get the sequence of radar images
def get_radar_images_sequence(seq_length):
    # Initialize list to store the sequence of radar images
    images = []
    # Get current date and time
    current_datetime = datetime.datetime.now(datetime.UTC)
    # Round current time to the nearest multiple of 5 minutes
    rounded_datetime = current_datetime - datetime.timedelta(minutes=current_datetime.minute % 5)
    # Delay the time by 10 minutes
    target_datetime = rounded_datetime - datetime.timedelta(minutes=10)
    # Generate sequence of timestamps
    timestamps = [target_datetime - datetime.timedelta(hours=i) for i in reversed(range(seq_length))]
    for timestamp in timestamps:
        image = get_radar_image(timestamp)
        images.append(image)
    # Return sequence of images
    return images

# Function to process the radar image
def process_radar_image(image, station_id):
    # Crop the image
    cropped_image = image.crop(STATIONS[station_id]['radar_box'])
    # Resize the image
    resized_image = cropped_image.resize((IMAGE_WIDTH, IMAGE_HEIGHT))
    # Convert the image to an array
    image_array = np.array(resized_image)
    # Normalize pixel values to be between 0 and 1
    image_array = image_array / 255
    # Return the processed image array
    return image_array

# Function to extract the value of the hour difference from the model_weights filename
def extract_number_from_filename(filename):
    pattern = r'\d+'  # Regular expression pattern to match one or more digits
    match = re.search(pattern, filename)
    if match:
        return int(match.group())
    else:
        return None

# Route to get the sequence of radar images
@app.route('/radar-images', methods=['GET'])
def radar_images():
    try:
        images = get_radar_images_sequence(SEQUENCE_LENGTH)
        images_strs = []
        for img in images:
            if img is not None:
                buffered = io.BytesIO()
                img.save(buffered, format="PNG")
                img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
                images_strs.append(img_str)
            else:
                images_strs.append(None)

        return jsonify({
            'image1': images_strs[0],
            'image2': images_strs[1],
            'image3': images_strs[2]
        })
    except Exception as e:
        print(e)
        return jsonify({'error': 'Ocorreu um erro'}), 500

# Route to get rain predictions
@app.route('/predict-rain', methods=['GET'])
def predict_rain():
    try:
        images = get_radar_images_sequence(SEQUENCE_LENGTH)
        full_hour_prediction_dictionary = {}
        model_weights_list = os.listdir("model_weights/")
        for model_weights in model_weights_list:
            model.load_weights("model_weights/"+str(model_weights))
            current_hour_prediction_dictionary = {}
            for station_id in STATIONS.keys():
                station_images = []
                for img in images:
                    image = process_radar_image(img, station_id)
                    station_images.append(image)
                predictions = model.predict(np.expand_dims(station_images, axis=0))
                current_hour_prediction_dictionary[STATIONS[station_id]['district']] = int(np.argmax(predictions[0]))
            full_hour_prediction_dictionary[extract_number_from_filename(model_weights)] = current_hour_prediction_dictionary
        return json.dumps(full_hour_prediction_dictionary)
    except Exception as e:
        print(e)
        return jsonify({'error': 'Ocorreu um erro'}), 500


if __name__ == '__main__':
    app.run()
