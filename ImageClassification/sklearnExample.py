# Authors: Taylor Digilio and Tomas Cespedes
# Citations: https://docs.python.org/3/library/pathlib.html
# https://www.kaggle.com/crawford/monkey-classifier-cnn-xception-0-90-acc for data generator

from sklearn.ensemble import RandomForestClassifier
import numpy as np
import pandas as pd
import datetime as dt
from keras.applications import Xception
from keras.preprocessing.image import ImageDataGenerator
from pathlib import Path

# Import and load the data.
train_dir = Path('training/')
test_dir = Path('validation/')

# Provide column names and read in the labels.
cols = ['Label', 'Latin Name', 'Common Name', 'Train Images', 'Validation Images']
labels = pd.read_csv("monkey_labels.txt", names=cols, skiprows=1)


# get the common names of the monkeys
labels = labels['Common Name']

# Constants for our models
height=150
width=150
channels=3
batch_size=32
seed=1337

# Training generator.
train_datagen = ImageDataGenerator(rescale=1./255)
train_generator = train_datagen.flow_from_directory(train_dir,
                                                    target_size=(height, width),
                                                    batch_size=batch_size,
                                                    seed=seed,
                                                    class_mode='categorical')

# Test generator.
test_datagen = ImageDataGenerator(rescale=1./255)
test_generator = test_datagen.flow_from_directory(test_dir,
                                                  target_size=(height, width),
                                                  batch_size=batch_size,
                                                  seed=seed,
                                                  class_mode='categorical')

# Initialize the base model for generator using imagenet since it is pretrained.
base_model = Xception(weights='imagenet',
                      include_top=False,
                      input_shape=(height, width, channels))
base_model.summary()

# Extract all the features. (found an example online to follow here)
def extract_features(sample_count, datagen):
    """
    Extract the features from our data generators.
    :param sample_count: size of sample count
    :param datagen: a data generator
    :return: features and labels to use to predict with our model.
    """
    # Time how long it takes.
    start = dt.datetime.now()
    # Create an array of 0's the length of features.
    features = np.zeros(shape=(sample_count, 5, 5, 2048))
    # Create an array of 0's the length of 10.
    labels = np.zeros(shape=(sample_count, 10))
    # Update our generator
    generator = datagen
    i = 0

    # Go through inputs/labels in generator
    for inputs_batch, labels_batch in generator:
        # Stop our time and count it
        stop = dt.datetime.now()
        time = (stop - start).seconds
        # Display update
        print('\r',
              'Extracting features from batch', str(i + 1), '/', len(datagen),
              '-- run time:', time, 'seconds',
              end='')

        # Use base model to predict our inputs batch
        features_batch = base_model.predict(inputs_batch)

        # Update next batch
        features[i * batch_size : (i + 1) * batch_size] = features_batch
        labels[i * batch_size : (i + 1) * batch_size] = labels_batch
        i += 1

        # If batch is greater than sample count then break
        if i * batch_size >= sample_count:
            break

    print("\n")

    return features, labels

# Get our features and labels
train_features, train_labels = extract_features(1097, train_generator)
test_features, test_labels = extract_features(272, test_generator)

# Reshape our array
flat_dim = 5 * 5 * 2048
train_features = np.reshape(train_features, (1097, flat_dim))
test_features = np.reshape(test_features, (272, flat_dim))

# Random Forest is the most efficient sklearn classifier based on testing multiple options.
clf = RandomForestClassifier()
clf.fit(train_features, train_labels)

# Looking for accuracy score.
from sklearn.metrics import accuracy_score
preds = clf.predict(test_features)

# Accuracy of 0.6066176470588235
print("Accuracy", accuracy_score(test_labels, preds))
