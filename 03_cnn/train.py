#!/usr/bin/env python
# coding: utf-8

import os
import math
import numpy as np
from keras.models import Sequential  # NN Activation
from keras.layers import Conv2D  # Convolution Operation
from keras.layers import MaxPooling2D # Pooling
from keras.layers import Dropout
from keras.layers import Flatten
from keras.layers import Dense # Fully Connected Networks
from keras.preprocessing import image
from keras.preprocessing.image import ImageDataGenerator
from argparse import ArgumentParser


'''
Reading input data (training, validation, test)
'''
parser = ArgumentParser()
parser.add_argument('dir_data', help='Directory path that contains training, validation, and testing data')
dir_train = os.path.join(parser.dir_data, 'training')
dir_validation = os.path.join(parser.dir_data, 'validation')

# TODO: training/validation grouping

# reading training data
label_train = []
for filename in os.listdir(dir_train):
    if filename.endswith(".jpg"):
        group, group_id = tuple(map(int, os.path.splitext(filename)[0].split('_')))
        label_train.append(group)

# reading validation data
label_validation = []
for filename in os.listdir(dir_validation):
    if filename.endswith(".jpg"):
        group, group_id = tuple(map(int, os.path.splitext(filename)[0].split('_')))
        label_validation.append(group)

# Fitting the CNN to the images
batch_size = 32    
train_datagen = ImageDataGenerator(rescale = 1./255, shear_range = 0.2, zoom_range = 0.2, horizontal_flip = True)
validation_datagen = ImageDataGenerator(rescale = 1./255)
training_data = train_datagen.flow_from_directory(dir_train, target_size = (128, 128), batch_size = batch_size)
validation_data = validation_datagen.flow_from_directory(dir_validation, target_size = (128, 128), batch_size = batch_size)


'''
Building a CNN:
    Convolution layer -> Max pooling -> Convolution layer -> Max pooling -> ... -> Convolution layer -> Max pooling -> Flattening
'''

# Initializing CNN
model = Sequential()  

# First convolutional layer (and max pooling)
model.add(Conv2D(16, (3, 3), input_shape = (128, 128, 3), activation = 'relu'))
model.add(MaxPooling2D(pool_size = (2, 2)))

# Second convolutional layer (and max pooling)
model.add(Conv2D(16, (3, 3), activation = 'relu'))
model.add(MaxPooling2D(pool_size = (2, 2)))

# Third convolutional layer (and max pooling)
model.add(Conv2D(16, (3, 3), activation = 'relu'))
model.add(MaxPooling2D(pool_size = (2, 2)))

# Dropout layer prevents overfitting
model.add(Dropout(0.25))

# Flattening
model.add(Flatten())

# Feedforward Neural Network
model.add(Dense(units = 64, activation = 'relu'))
model.add(Dense(units = 11, activation= 'softmax'))

# Compile CNN
model.compile(optimizer = 'adam', loss = 'categorical_crossentropy', metrics = ['accuracy'])

# Show summary of the CNN network
model.summary()


'''
Training CNN
'''
steps_per_epoch = math.ceil(9866 / batch_size)
validation_steps = math.ceil(3430 / batch_size)
epochs = 1
model.fit_generator(training_data, steps_per_epoch = steps_per_epoch, epochs = epochs, validation_data = validation_data, validation_steps = validation_steps)

# Saving model
model.save('hw3.h5')