# Import libraries
import tensorflow as tf
from tensorflow import keras
from ncps.keras import LTC
from ncps.wirings import AutoNCP

# Constants
PRECIPITATION_CLASSES = ['Sem Chuva', 'Chuva Fraca', 'Chuva Moderada', 'Chuva Forte']
IMAGE_WIDTH, IMAGE_HEIGHT, IMAGE_CHANNELS = 100, 100, 4
SEQUENCE_LENGTH = 3
HIDDEN_NEURONS = 64

# Build model
model = keras.Sequential([
    keras.layers.Input(shape=(SEQUENCE_LENGTH, IMAGE_HEIGHT, IMAGE_WIDTH, IMAGE_CHANNELS)),
    keras.layers.TimeDistributed(keras.layers.Conv2D(filters=32, kernel_size=(3, 3), activation='relu', strides=1, padding='same', data_format='channels_last')),
    keras.layers.TimeDistributed(keras.layers.BatchNormalization()),
    keras.layers.TimeDistributed(keras.layers.Conv2D(filters=32, kernel_size=(3, 3), activation='relu', strides=1, padding='same', data_format='channels_last')),
    keras.layers.TimeDistributed(keras.layers.BatchNormalization()),
    keras.layers.TimeDistributed(keras.layers.MaxPooling2D(pool_size=(2, 2), strides=2, padding='valid')),
    keras.layers.TimeDistributed(keras.layers.Dropout(0.35)),
    keras.layers.TimeDistributed(keras.layers.Conv2D(filters=64, kernel_size=(3, 3), activation='relu', strides=1, padding='same', data_format='channels_last')),
    keras.layers.TimeDistributed(keras.layers.BatchNormalization()),
    keras.layers.TimeDistributed(keras.layers.Conv2D(filters=64, kernel_size=(3, 3), strides=1, padding='same', activation='relu', data_format='channels_last')),
    keras.layers.TimeDistributed(keras.layers.BatchNormalization()),
    keras.layers.TimeDistributed(keras.layers.MaxPooling2D(pool_size=(2, 2), strides=2, padding='valid' )),
    keras.layers.TimeDistributed(keras.layers.Dropout(0.0035)),
    keras.layers.TimeDistributed(keras.layers.Flatten(name='flatten')),
    keras.layers.Reshape((SEQUENCE_LENGTH, IMAGE_HEIGHT * IMAGE_WIDTH * IMAGE_CHANNELS), name='reshape'),
    LTC(AutoNCP(HIDDEN_NEURONS, output_size=len(PRECIPITATION_CLASSES))),
    keras.layers.Dense(len(PRECIPITATION_CLASSES), activation='softmax')
])