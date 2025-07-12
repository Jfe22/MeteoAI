# Library for operating system functionalities
import os
# Library for numerical operations
import numpy as np
# Library for interactive data visualization
import matplotlib.pyplot as plt
# Library for image processing and manipulation
from PIL import Image
# Library for date and time operations
from datetime import timedelta
import time
# Libraries for Deep Learning models
import tensorflow as tf
from tensorflow import keras
# PSJ method module
import psj


def count_occurrences_of_each_value(arr):
    unique, counts = np.unique(arr, return_counts=True)
    return dict(zip(unique, counts))


def generate_replacement_image(folder_path, image_datetime, method):
    match method:
        case 'copy_previous':
            new_image_datetime = image_datetime - timedelta(hours=1)
            new_image_date_string = image_datetime.strftime("%Y-%m-%d")
            new_image_datetime_string = new_image_datetime.strftime("%Y-%m-%dT%H%M")
            new_image_path = folder_path + '/' + new_image_date_string + '/' + new_image_datetime_string + '.png'
            # If the image exist, open it
            if os.path.exists(new_image_path):
                return Image.open(new_image_path)
            # If the image doesn't exist, return None
            else:
                return None
        case 'copy_next':
            new_image_datetime = image_datetime + timedelta(hours=1)
            new_image_date_string = image_datetime.strftime("%Y-%m-%d")
            new_image_datetime_string = new_image_datetime.strftime("%Y-%m-%dT%H%M")
            new_image_path = folder_path + '/' + new_image_date_string + '/' + new_image_datetime_string + '.png'
            # If the image exist, open it
            if os.path.exists(new_image_path):
                return Image.open(new_image_path)
            # If the image doesn't exist, return None
            else:
                return None
        case _:
            return None


def show_dataset_sample_static(images_array, labels_array, class_names):
    # Iterate over the classes
    for i, class_name in enumerate(class_names):
        # Find an example index for each class
        index = labels_array.tolist().index(i)

        # Plot the image
        plt.subplot(1, len(class_names), i + 1)
        plt.xticks([])
        plt.yticks([])
        plt.imshow(images_array[index])
        plt.xlabel(class_name)

    # Show the figure
    plt.show()


def show_dataset_sample_timeseries(images_array, labels_array, class_names, sequence_len):
    # One row for each class
    num_rows = len(class_names)
    # One column for each image in the sequence + the label
    num_cols = sequence_len + 1

    # Create a figure with subplots
    fig, subplots = plt.subplots(num_rows, num_cols)

    # Iterate over the classes
    for i, class_name in enumerate(class_names):
        # Find an example index for each class
        index = labels_array.tolist().index(i)

        # Iterate over the images in the sequence
        for j in range(sequence_len):
            # Get the subplot
            subplot = subplots[i, j]
            # Get the image
            img = images_array[index, j, :, :, :]
            # Show the image
            subplot.imshow(img)
            subplot.set_xticks([])
            subplot.set_yticks([])
            subplot.set_frame_on(True)

        # Add label in the last column
        subplot = subplots[i, -1]
        subplot.text(0.5, 0.5, class_name, fontsize=12, ha='center', va='center')
        subplot.set_xticks([])
        subplot.set_yticks([])
        subplot.set_frame_on(True)

    # Show the figure
    plt.tight_layout()
    plt.show()


def get_weight_initializer(base_model, num_neurons, input_size, output_size, images_array, labels_array, method, seed):
    match method:
        case 'psj':
            print('Method PSJ')
            psj_method = psj.PSJmethod(base_model, num_neurons, input_size, output_size, images_array, labels_array)
            return tf.constant_initializer(psj_method), tf.constant_initializer(psj.iniL2(num_neurons, num_neurons)), keras.initializers.Ones()
        case 'glorot_normal':
            print('Method GlorotNormal')
            glorot_normal = keras.initializers.GlorotNormal(seed=seed)
            return glorot_normal, glorot_normal, glorot_normal
        case 'glorot_uniform':
            print('Method GlorotUniform')
            glorot_uniform = keras.initializers.GlorotUniform(seed=seed)
            return glorot_uniform, glorot_uniform, glorot_uniform
        case 'he_normal':
            print('Method HeNormal')
            he_normal = keras.initializers.HeNormal(seed=seed)
            return he_normal, he_normal, he_normal
        case 'he_uniform':
            print('Method HeUniform')
            he_uniform = keras.initializers.HeUniform(seed=seed)
            return he_uniform, he_uniform, he_uniform
        case 'lecun_normal':
            print('Method LecunNormal')
            lecun_normal = keras.initializers.LecunNormal(seed=seed)
            return lecun_normal, lecun_normal, lecun_normal
        case 'lecun_uniform':
            print('Method LecunUniform')
            lecun_uniform = keras.initializers.LecunUniform(seed=seed)
            return lecun_uniform, lecun_uniform, lecun_uniform
        case 'orthogonal':
            print('Method Orthogonal')
            orthogonal = keras.initializers.Orthogonal()
            return orthogonal, orthogonal, orthogonal
        case 'random_normal':
            print('Method RandomNormal')
            random_normal = keras.initializers.RandomNormal(mean=0., stddev=1.)
            return random_normal, random_normal, random_normal
        case 'random_uniform':
            print('Method RandomUniform')
            random_uniform = keras.initializers.RandomUniform(minval=0., maxval=1.)
            return random_uniform, random_uniform, random_uniform
        case 'identity':
            print('Method Identity')
            identity = keras.initializers.Identity()
            return identity, identity, identity
        case 'truncated_normal':
            print('Method TruncatedNormal')
            truncated_normal = keras.initializers.TruncatedNormal(mean=0., stddev=0.5)
            return truncated_normal, truncated_normal, truncated_normal
        case 'variance_scaling':
            print('Method VarianceScaling')
            variance_scaling = keras.initializers.VarianceScaling(scale=0.1, mode='fan_in', distribution='uniform')
            return variance_scaling, variance_scaling, variance_scaling
        case 'zeros':
            print('Method Zeros')
            zeros = keras.initializers.Zeros()
            return zeros, zeros, zeros
        case 'ones':
            print('Method Ones')
            ones = keras.initializers.Ones()
            return ones, ones, ones
        case _:
            print('No Method Selected, using default (GlorotUniform)')
            glorot_uniform = keras.initializers.GlorotUniform(seed=seed)
            return glorot_uniform, glorot_uniform, glorot_uniform


class TimeHistory(keras.callbacks.Callback):
    def on_train_begin(self, logs={}):
        self.times = []

    def on_epoch_begin(self, batch, logs={}):
        self.epoch_time_start = time.time()

    def on_epoch_end(self, batch, logs={}):
        self.times.append(time.time() - self.epoch_time_start)


class SequenceImageGenerator(keras.utils.Sequence):
    def __init__(self, image_sequences, labels, batch_size, datagen, shuffle=True):
        self.image_sequences = image_sequences
        self.labels = labels
        self.batch_size = batch_size
        self.datagen = datagen
        self.shuffle = shuffle
        self.indices = np.arange(len(self.image_sequences))
        self.on_epoch_end()

    def __len__(self):
        return int(np.ceil(len(self.image_sequences) / self.batch_size))

    def on_epoch_end(self):
        if self.shuffle:
            np.random.shuffle(self.indices)

    def __getitem__(self, index):
        batch_indices = self.indices[index * self.batch_size:(index + 1) * self.batch_size]
        batch_sequences = self.image_sequences[batch_indices]
        batch_labels = self.labels[batch_indices]

        # Apply augmentation to each image in the sequence
        augmented_sequences = np.zeros_like(batch_sequences)
        for i, seq in enumerate(batch_sequences):
            for j, img in enumerate(seq):
                augmented = self.datagen.random_transform(img)
                augmented_sequences[i, j] = augmented

        return augmented_sequences, batch_labels
