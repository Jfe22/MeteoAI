#!.\venv\Scripts\python.exe
# -*- coding: utf-8 -*-
"""
Filename: dataset_construction.py
Authors: José Ferreira and Rúben Antunes
Created: 2025-03-27
Description: This script creates the precipitation_dataset used in the training of the Liquid Neural Network.
"""

# --Imports--

# Library for operating system functionalities
import os

# Library for date and time functionalities
from datetime import datetime, timedelta

# Library for directories management
import shutil

# Library for json files
import json

# --Constants--

RAWDATA_PATH = 'rawdata/'
RAWDATA_VALUES_PATH = RAWDATA_PATH + 'values/'
RAWDATA_IMAGES_PATH = RAWDATA_PATH + 'images/radar/'
DATASET_PATH = 'precipitation_dataset/'
DATASET_VALUES_PATH = DATASET_PATH + 'values/'
DATASET_IMAGES_PATH = DATASET_PATH + 'images/'
NORMALIZATION_TECHNIQUE = 1 # 1 for IPMA warnings, 2 for IPMA rain intensity

# --Functions--

def normalize_precipitation_value(precipitation_value):
	match NORMALIZATION_TECHNIQUE:
		case 1:
			# Classify precipitation based on IPMA warnings criteria
			if precipitation_value < 0:
				return -99
			elif precipitation_value >= 0 and precipitation_value < 3.6:
				return 0
			elif precipitation_value >= 3.6 and precipitation_value < 10:
				return 1
			elif precipitation_value >= 10 and precipitation_value < 20:
				return 2
			elif precipitation_value >= 20 and precipitation_value < 40:
				return 3
			elif precipitation_value >= 40:
				return 4
		case 2:
			# Classify precipitation based on IPMA rain intensity criteria
			if precipitation_value < 0:
				return -99
			if precipitation_value >= 0 and precipitation_value < 0.1:
				return 0
			elif precipitation_value >= 0.1 and precipitation_value < 0.5:
				return 1
			elif precipitation_value >= 0.5 and precipitation_value < 4:
				return 2
			elif precipitation_value >= 4:
				return 3
		case _:
			raise SystemExit("Invalid normalization technique!")

# Json files functions
def load_json_file(filename):
	try:
		with open(filename, 'r') as file:
			json_data = json.load(file)
	except Exception as error:
		raise SystemExit(error)
	return json_data

def save_json_file(json_data, filename):
	try:
		new_json_data = {}
		for day, hours in json_data.items():
			for hour, details in hours.items():
				precipitation_value = normalize_precipitation_value(details["precipitation"])
				if precipitation_value != -99:
					if day not in new_json_data:
						new_json_data[day] = {}
					new_json_data[day][hour] = precipitation_value
		with open(filename, 'w') as f:
			json.dump(new_json_data, f, indent=4)
	except Exception as error:
		raise SystemExit(error)

def create_dataset():
	# Delete existing dataset
	if os.path.exists(DATASET_PATH):
		print('Deleting existing dataset...')
		shutil.rmtree(DATASET_PATH)
		print('Dataset deleted!')

	# Create new dataset
	print('Creating new dataset...')
	os.makedirs(DATASET_VALUES_PATH)
	os.makedirs(DATASET_IMAGES_PATH)

	for filename in os.listdir(RAWDATA_VALUES_PATH):
		json_data = load_json_file(RAWDATA_VALUES_PATH + filename)
		save_json_file(json_data, DATASET_VALUES_PATH + filename)

	# Copy images from rawdata to dataset
	try:
		shutil.copytree(RAWDATA_IMAGES_PATH, DATASET_IMAGES_PATH, dirs_exist_ok = True)
	except Exception as error:
		raise SystemExit(error)
	print('Dataset created!')

# --Main--

create_dataset()
