import os
import cv2
import imgaug as aug
import numpy as np
import pandas as pd
import imgaug.augmenters as iaa
from pathlib import Path
from keras.applications import InceptionV3
from keras.models import Model
from keras.applications.vgg16 import preprocess_input
from keras.layers import Dense, Dropout
from keras.callbacks import ModelCheckpoint, EarlyStopping
from keras.utils import to_categorical
import tensorflow as tf

# Set the seed so results are reproducible
seed=11291996
np.random.seed(seed)
tf.set_random_seed(seed)
aug.seed(seed)

# Disable AVX warnings (if need be, does not affect performance)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# Load data set and process it
train_dir = Path('training/')
validation_dir = Path('validation/')
labels = Path('monkey_labels.txt')

# Establish the column names
column_names = ['Label', 'Latin Name', 'Common Name', 'Train Images', 'Validation Images']

# Read the labels as a pandas df
labels_info = pd.read_csv("monkey_labels.txt", names = column_names, skiprows=1)

# dictionary for mapping labels
labels_dict= {'n0':0, 'n1':1, 'n2':2, 'n3':3, 'n4':4, 'n5':5, 'n6':6, 'n7':7, 'n8':8, 'n9':9}

# map labels to common names (latin names are also available if desired)
names_dict = dict(zip(labels_dict.values(), labels_info["Common Name"]))

# Since we have a relatively small dataset, we can load it all into memory.
# However, this is almost always never the case when it comes to problems like this.
# So instead, we are going store data into dataframes, then create a Data Generator
# to upload data on the fly.
# Since we need to do this atleast twice (one for training and one for validation,
# possibly a third time for testing data) we can create a method to do this for us.
def data_frame_creator(directory_path):
    """
    :param directory_path: the path of the directory in which the images are stored.
    :return: a pandas data frame which contains our shuffled images in their respective labels.
    """

    # Creating a dataframe for the training dataset
    data_frame = []

    # Iterate through each folder in the directory (each species)
    for folder in os.listdir(directory_path):
        # Define the path to the images from that folder
        folder_path = directory_path / folder

        # Get the list of all the images stored in that directory
        images_list = sorted(folder_path.glob('*.jpg'))

        # Store each image path as a tuple with the respective label
        for image_path in images_list:
            data_frame.append((str(image_path), labels_dict[folder]))

    # Create a pandas data frame from our data_frame array
    data_frame = pd.DataFrame(data_frame, columns=['image', 'label'], index=None)
    # Shuffle the data around
    data_frame = data_frame.sample(frac=1.).reset_index(drop=True)

    return data_frame

# Get our training and validation data sets using our generate_data method
train_df = data_frame_creator(train_dir)
valid_df = data_frame_creator(validation_dir)

# Establish constants for our images (rows, columns, batch size, and number of classes)
# The rows, cols, and channels change based on model we use.
height, width, channels, batch_size, nb_classes = 299, 299, 3, 8, 10

# As was mentioned before, we do not have a lot of data in our data sets. Since
# deep models work best with the most data, we can create more data by
# rotating, randomizing brightness, and doing horizontal flips.
# This can be done by using the imgaug library.
seq = iaa.OneOf([
    iaa.Affine(rotate=20), # rotations
    iaa.Multiply((1.2, 1.5)), #randomize brightness
    iaa.Fliplr() # horizontal flips

])

# Implement the generator to get our data
def generator(data, batchsize, validation=False):
    """
    :param data: the dataframe that we want to look at (training or validation)
    :param batchsize: the size of the data we want to grab (set to 8)
    :param validation: whether we are looking at training or validation set
    :yield: a batch of data and a batch of labels
    """

    # Total number of samples in the data that is passed
    n = len(data)

    # cast to an int using np.ceil
    number_batches = int(np.ceil(n / batchsize))

    # Get an array of all indices of the data given
    indices = np.arange(n)

    # Create 2 numpy arrays of zeros for batch data and labels using our
    # pre-defined constants
    data_batch = np.zeros(
        (batchsize, height, width, channels),
        dtype=np.float32)
    labels_batch = np.zeros(
        (batchsize, nb_classes),
        dtype=np.float32)

    # Run until we cant anymore
    while True:
        # Check if we are looking at the training data
        if not validation:
            # If so, shuffle our indices
            np.random.shuffle(indices)

        for i in range(number_batches):
            # Get the next group of data
            next_batch = indices[i*batchsize: (i + 1)*batchsize]

            # Now process the batch
            for j, index in enumerate(next_batch):
                # Use integer-based index location to get our image array
                image = cv2.imread(data.iloc[index]['image'])
                # Convert color space from Blue_Green_Red to Red_Green_Blue
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                # Use integer-based index location to get the label
                label = data.iloc[index]['label']

                # If data is training, augment the image.
                if not validation:
                    image = seq.augment_image(image)


                # Resize our images to fit our row/column shape
                # This is so all images are the same size
                image = cv2.resize(image, (height, width)).astype(np.float32)

                # Update the data batch with the new image
                data_batch[j] = image
                # Convert array of labeled data to one-hot vector
                labels_batch[j] = to_categorical(
                    label,
                    num_classes=nb_classes)

            # Adequate images to format of our model
            data_batch = preprocess_input(data_batch)

            # Yield our features and labels
            yield data_batch, labels_batch

# Get our training data generator using training data frame
train_data = generator(train_df, batch_size)

# Get our validation data generator using validation data frame
valid_data = generator(valid_df, batch_size, validation=True)

# Build our model using InceptionV3 class
# Input shape needs to be (299, 299, 3)
model = InceptionV3(
    input_shape=(height, width, channels),
    weights='imagenet',
    include_top=True
)

#  get the output of the second last dense layer
base_model_output = model.layers[-2].output

# add new layers
x = Dropout(0.7, name='drop2')(base_model_output)
output = Dense(10, activation='softmax', name='fc3')(x)

# define a new model
model = Model(model.input, output)

# Freeze all the base model layers
for layer in model.layers[:-1]:
    layer.trainable=False

# Compile the model aiming for accuracy
# A lot of optimizers we can use, decided to go with adam
model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy'])

# Get the summary of the model
model.summary()

# load the weights of the best iteration once the training finishes
earlystop = EarlyStopping(patience=10, restore_best_weights=True)

# checkpoint to save model, only save the best
checkpoint = ModelCheckpoint(filepath="model1", save_best_only=True)


# number of training and validation steps for training and validation
nb_train_steps = int(np.ceil(len(train_df)/batch_size))
nb_valid_steps = int(np.ceil(len(valid_df)/batch_size))

# Number of times we want our model to run the training
# Keep low for testing purposes
number_of_epochs = 1

# Fit the model using train features and labels
history = model.fit_generator(
    train_data, epochs=number_of_epochs,
    steps_per_epoch=nb_train_steps, validation_data=valid_data,
    validation_steps=nb_valid_steps, callbacks=[earlystop, checkpoint],
    verbose=2
)

# Print out our test accuracy
print("Test Accuracy:", history.history['acc'])



