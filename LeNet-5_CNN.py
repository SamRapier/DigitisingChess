
import numpy as np
import pandas as pd
from time import time

from sklearn.model_selection import train_test_split
import tensorflow as tf
import keras
import keras.layers as layers
from keras.models import Sequential
from keras.preprocessing.image import ImageDataGenerator
from keras.utils.np_utils import to_categorical
from keras.callbacks import TensorBoard

import matplotlib.pyplot as plt

import os
import cv2
import PIL
from PIL import Image



labels = []
root_image_path = 'C:/Users/samra/OneDrive/CompSciUni/Year4/Project/images_chess_pieces/'
dirs = os.listdir(root_image_path)

for dir in dirs:
    for i in range(len(os.listdir(root_image_path + str(dir)))):
        labels.append(str(dir))

d = dict([(y,x+1) for x,y in enumerate(sorted(set(labels)))])
int_labels = np.asarray([d[x] for x in labels])



root_image_path = 'C:/Users/samra/OneDrive/CompSciUni/Year4/Project/images_chess_pieces/'
imagePath = 'C:/Users/samra/OneDrive/CompSciUni/Year4/Project/images_chess_pieces/bB/'
length = len(labels)


imageArr = []

# print(files)
dirs = os.listdir(root_image_path)

for dir in dirs:
    imagePath = root_image_path + str(dir) + '/'
    files = os.listdir(imagePath)

    for file in files:
        image = Image.open(imagePath + file)

        # imageArr.append(np.asarray(image))

        # resize image and ignore original aspect ratio
        img_resized = image.resize((25,25   ))
        imageArr.append(np.asarray(img_resized))


features = np.asarray(imageArr)
labels = np.asarray(int_labels)

train = {}
validation = {}
test = {}

train['features'], test['features'], train['labels'], test['labels'] = train_test_split(features, labels, test_size=0.15, random_state=0)
train['features'], validation['features'], train['labels'], validation['labels'] = train_test_split(train['features'], train['labels'], test_size=0.2, random_state=0)


print('# of training images:', train['features'].shape[0])
print('# of test images:', test['features'].shape[0])
print('# of validation images:', validation['features'].shape[0])

def display_image(position):
    image = train['features'][position].squeeze()
    plt.title('Example %d. Label: %s' % (int(position), train['labels'][position]))
    plt.imshow(image, cmap=plt.cm.gray_r)

# display_image(20070)


# Pad images with 0s
train['features']      = np.pad(train['features'], ((0,0),(2,2),(2,2),(0,0)), 'constant')
validation['features'] = np.pad(validation['features'], ((0,0),(2,2),(2,2),(0,0)), 'constant')
test['features']       = np.pad(test['features'], ((0,0),(2,2),(2,2),(0,0)), 'constant')
    
print("Updated Image Shape: {}".format(train['features'][0].shape))


model = keras.Sequential()

model.add(layers.Conv2D(filters=6, kernel_size=(3, 3), activation='relu', input_shape=(29,29,3)))
model.add(layers.AveragePooling2D())

model.add(layers.Conv2D(filters=16, kernel_size=(3, 3), activation='relu'))
model.add(layers.AveragePooling2D())

model.add(layers.Flatten())

model.add(layers.Dense(units=120, activation='relu'))

model.add(layers.Dense(units=84, activation='relu'))

model.add(layers.Dense(units=14, activation='softmax'))


model.summary()


model.compile(loss=keras.losses.categorical_crossentropy, optimizer=tf.keras.optimizers.Adam(), metrics=['accuracy'])

EPOCHS = 30
BATCH_SIZE = 128

X_train, y_train = train['features'], to_categorical(train['labels'])
X_validation, y_validation = validation['features'], to_categorical(validation['labels'])

train_generator = ImageDataGenerator().flow(X_train, y_train, batch_size=BATCH_SIZE)
validation_generator = ImageDataGenerator().flow(X_validation, y_validation, batch_size=BATCH_SIZE)

print('# of training images:', train['features'].shape[0])
print('# of validation images:', validation['features'].shape[0])

steps_per_epoch = X_train.shape[0]//BATCH_SIZE
validation_steps = X_validation.shape[0]//BATCH_SIZE

tensorboard = TensorBoard(log_dir="logs/{}".format(time()))


model.fit(train_generator, steps_per_epoch=steps_per_epoch, epochs=EPOCHS, validation_data=validation_generator, validation_steps=validation_steps, shuffle=True, callbacks=[tensorboard])


score = model.evaluate(test['features'], to_categorical(test['labels']))
print('Test loss:', score[0])
print('Test accuracy:', score[1])