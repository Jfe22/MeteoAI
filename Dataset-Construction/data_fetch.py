#!.\venv\Scripts\python.exe
# -*- coding: utf-8 -*-
"""
Filename: data_fetch.py
Authors: José Ferreira and Rúben Antunes
Created: 2025-03-27
Description: This script fetchs the IPMA precipitation data and images.
"""

# --Imports--

# Library for operating system functionalities
import os

# Library for data request
import requests

# Library for date and time functionalities
from datetime import datetime, timedelta

# Library for image processing and manipulation
from io import BytesIO
from PIL import Image

# Library for json files
import json

# --Constants--

# IPMA API URL (Last 3 hours precipitation data)
IPMA_API_URL = 'https://api.ipma.pt/open-data/observation/meteorology/stations/obs-surface.geojson'
# IPMA IMAGES URLS
IPMA_RADAR_URL = 'https://www.ipma.pt/resources.www/transf/radar/por/pcr-'
IPMA_SATELLITE_URL_1 = 'https://www.ipma.pt/resources.www/transf/satelite/por/msg-108/msg-108-'
IPMA_SATELLITE_URL_2 = 'https://www.ipma.pt/resources.www/transf/satelite/por/msg-108-topos/msg-108t-'
# STATIONS INFORMATION
STATIONS = {
    1200554: {
        'district': 'Faro',
        'radar_box': (736, 1546, 936, 1746),
        'satellite_box_1': (143, 301, 182, 340),
        'satellite_box_2': (110, 231, 140, 261)
    },
    1200558: {
        'district': 'Evora',
        'radar_box': (740, 1183, 940, 1383),
        'satellite_box_1': (144, 230, 182, 269),
        'satellite_box_2': (111, 177, 141, 207)
    },
    1200562: {
        'district': 'Beja',
        'radar_box': (735, 1546, 935, 1746),
        'satellite_box_1': (143, 301, 182, 340),
        'satellite_box_2': (110, 231, 140, 261)
    },
    1200570: {
        'district': 'Castelo Branco',
        'radar_box': (817, 886, 1017, 1086),
        'satellite_box_1': (159, 172, 197, 211),
        'satellite_box_2': (122, 132, 152, 162)
    },
    1200571: {
        'district': 'Portalegre',
        'radar_box': (829, 1012, 1029, 1212),
        'satellite_box_1': (161, 197, 200, 236),
        'satellite_box_2': (124, 151, 154, 181)
    },
    1200575: {
        'district': 'Braganca',
        'radar_box': (953, 401, 1153, 601),
        'satellite_box_1': (185, 78, 224, 117),
        'satellite_box_2': (142, 60, 172, 89)
    },
    1210683: {
        'district': 'Guarda',
        'radar_box': (859, 712, 1059, 912),
        'satellite_box_1': (167, 138, 206, 177),
        'satellite_box_2': (128, 106, 158, 136)
    },
    1210702: {
        'district': 'Aveiro',
        'radar_box': (603, 687, 803, 887),
        'satellite_box_1': (117, 133, 156, 172),
        'satellite_box_2': (90, 102, 120, 132)
    },
    1210707: {
        'district': 'Coimbra',
        'radar_box': (645, 792, 845, 992),
        'satellite_box_1': (125, 154, 164, 193),
        'satellite_box_2': (96, 118, 126, 148)
    },
    1210718: {
        'district': 'Leiria',
        'radar_box': (574, 902, 774, 1102),
        'satellite_box_1': (111, 175, 150, 214),
        'satellite_box_2': (86, 135, 116, 164)
    },
    1210734: {
        'district': 'Santarem',
        'radar_box': (597, 1026, 797, 1226),
        'satellite_box_1': (116, 199, 155, 238),
        'satellite_box_2': (89, 153, 119, 183)
    },
    1210770: {
        'district': 'Setubal',
        'radar_box': (559, 1193, 759, 1393),
        'satellite_box_1': (108, 232, 147, 271),
        'satellite_box_2': (83, 178, 113, 208)
    },
    1240566: {
        'district': 'Vila Real',
        'radar_box': (770, 527, 970, 727),
        'satellite_box_1': (149, 102, 188, 141),
        'satellite_box_2': (115, 78, 145, 108)
    },
    1240610: {
        'district': 'Viana do Castelo',
        'radar_box': (570, 428, 770, 628),
        'satellite_box_1': (110, 83, 149, 122),
        'satellite_box_2': (85, 64, 115, 94)
    },
    1240675: {
        'district': 'Viseu',
        'radar_box': (740, 682, 940, 882),
        'satellite_box_1': (144, 132, 182, 171),
        'satellite_box_2': (111, 102, 141, 132)
    },
    1240903: {
        'district': 'Porto',
        'radar_box': (611, 562, 811, 762),
        'satellite_box_1': (118, 109, 157, 148),
        'satellite_box_2': (91, 84, 121, 114)
    },
    6212124: {
        'district': 'Braga',
        'radar_box': (645, 463, 845, 663),
        'satellite_box_1': (125, 90, 164, 129),
        'satellite_box_2': (96, 69, 126, 99)
    },
    7240919: {
        'district': 'Lisboa',
        'radar_box': (513, 1149, 713, 1349),
        'satellite_box_1': (99, 223, 138, 262),
        'satellite_box_2': (76, 172, 106, 201)
    }
}


# --Functions--

# Image editing functions
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


# Data request functions
def get_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as error:
        raise SystemExit(error)
    return response

def get_image(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        image = Image.open(BytesIO(response.content))
        return image
    except Exception as error:
        print('Warning: failed to load image from ' + url)


def save_station_json_file(station_json):
    try:
        station_id = station_json['idEstacao']
        date_time = datetime.fromisoformat(station_json['time'])
        date_str, hour_str = date_time.strftime('%Y-%m-%d %H:%M').split()
        new_data = {}
        new_data[date_str] = {
            hour_str: {
                'precipitation': station_json['precAcumulada'],
                'temperature': station_json['temperatura'],
                'humidity': station_json['humidade'],
                'pressure': station_json['pressao'],
                'radiation': station_json['radiacao'],
                'wind_intensity_km': station_json['intensidadeVentoKM'],
                'wind_intensity_m': station_json['intensidadeVento'],
                'wind_direction': station_json['descDirVento']
            }
        }

        # Check if this station file already exists
        filepath = 'rawdata/values/'
        filename = filepath + str(station_id) + '.json'
        if not os.path.isfile(filename):
            if not os.path.exists(filepath):
                os.makedirs(filepath)
            # Create new empty json file
            with open(filename, 'w') as file:
                json.dump({}, file)

        # Load data from existing json file
        with open(filename, 'r') as file:
            old_data = json.load(file)

        if date_str not in old_data:
            old_data[date_str] = {}

        # Add new data to old data
        old_data[date_str][hour_str] = new_data[date_str][hour_str]

        # Update existing json file
        with open(filename, 'w') as file:
            json.dump(old_data, file, indent=4)
    except Exception as error:
        print(error)

def save_radar_and_satellite_images(unique_timestamps):
    # Fetch radar and satellite images for each timestamp
    for timestamp in unique_timestamps:
        radar_timestamp = timestamp.strftime('%Y-%m-%dT%H%M')
        satellite_timestamp = timestamp - timedelta(minutes=5)
        satellite_timestamp = satellite_timestamp.strftime('%Y-%m-%dT%H%M')

        radar_image_url = IPMA_RADAR_URL + radar_timestamp + '.png'
        satellite_image_url_1 = IPMA_SATELLITE_URL_1 + satellite_timestamp + '.png'
        satellite_image_url_2 = IPMA_SATELLITE_URL_2 + satellite_timestamp + '.png'

        radar_image = get_image(radar_image_url)
        radar_image = remove_black_pixels(radar_image)
        satellite_image_1 = get_image(satellite_image_url_1)
        satellite_image_2 = get_image(satellite_image_url_2)

        for station_id, station_info in STATIONS.items():
            try:
                if radar_image is not None:
                    # Crop image for each station
                    radar_image_cropped = radar_image.crop(station_info['radar_box'])
                    # Create directory if it doesn't exist
                    filepath1 = 'rawdata/images/radar/' + str(station_id) + '/' + timestamp.strftime('%Y-%m-%d')
                    if not os.path.exists(filepath1):
                        os.makedirs(filepath1)
                    # Save image
                    radar_image_cropped.save(filepath1 + '/' + radar_timestamp + '.png')

                if satellite_image_1 is not None:
                    # Crop image for each station
                    satellite_image_cropped_1 = satellite_image_1.crop(station_info['satellite_box_1'])
                    # Create directory if it doesn't exist
                    filepath2 = 'rawdata/images/satellite1/' + str(station_id) + '/' + timestamp.strftime('%Y-%m-%d')
                    if not os.path.exists(filepath2):
                        os.makedirs(filepath2)
                    # Save image
                    satellite_image_cropped_1.save(filepath2 + '/' + satellite_timestamp + '.png')
                
                if satellite_image_2 is not None:
                    # Crop image for each station
                    satellite_image_cropped_2 = satellite_image_2.crop(station_info['satellite_box_2'])
                    # Create directory if it doesn't exist
                    filepath3 = 'rawdata/images/satellite2/' + str(station_id) + '/' + timestamp.strftime('%Y-%m-%d')
                    if not os.path.exists(filepath3):
                        os.makedirs(filepath3)
                    # Save image
                    satellite_image_cropped_2.save(filepath3 + '/' + satellite_timestamp + '.png')
            except Exception as error:
                print(error)

def get_data_and_images_from_ipma():
    # Get json data from IPMA
    json_data = get_data(IPMA_API_URL).json()

    # Initialize list of unique timestamps
    unique_timestamps = set()

    # Fetch important data of each station
    for feature in json_data['features']:
        if feature['properties']['idEstacao'] in list(STATIONS.keys()):
            station_data = feature['properties']
            save_station_json_file(station_data)
            # Store unique timestamp
            timestamp = datetime.fromisoformat(station_data['time'])
            unique_timestamps.add(timestamp)

    print('Json files successfully updated!')

    save_radar_and_satellite_images(unique_timestamps)

    print('Images saved successfully!')

# --Main--

get_data_and_images_from_ipma()
