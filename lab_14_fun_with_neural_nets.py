# -*- coding: utf-8 -*-
"""Lab 14 Fun with Neural Nets

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1vLWz4KhDQWYnuDP0Da-XV2xJhkzEmq94

<img src="http://imgur.com/1ZcRyrc.png" style="float: left; margin: 20px; height: 55px">

# Lab: Fun with Neural Nets

---

Below is a procedure for building a neural network to recognize handwritten digits.  The data is from [Kaggle](https://www.kaggle.com/c/digit-recognizer/data), and you will submit your results to Kaggle to test how well you did!

1. Load the training data (`train.csv`) from [Kaggle](https://www.kaggle.com/c/digit-recognizer/data)
2. Setup X and y (feature matrix and target vector)
3. Split X and y into train and test subsets.
4. Preprocess your data

   - When dealing with image data, you need to normalize your `X` by dividing each value by the max value of a pixel (255).
   - Since this is a multiclass classification problem, keras needs `y` to be a one-hot encoded matrix
   
5. Create your network.
   - Remember that for multi-class classification you need a softmax activation function on the output layer.
   - You may want to consider using regularization or dropout to improve performance.
   
6. Train your network.
7. If you are unhappy with your model performance, try to tighten up your model by adding hidden layers, adding hidden layer units, chaining the activation functions on the hidden layers, etc.
8. Load in [Kaggle's](https://www.kaggle.com/c/digit-recognizer/data) `test.csv`
9. Create your predictions (these should be numbers in the range 0-9).
10. Save your predictions and submit them to Kaggle.

---

For this lab, you should complete the above sequence of steps for **_at least_** two of the four "configurations":

1. Using a `tensorflow` network (we did _not_ cover this in class!)
2. Using a `keras` convolutional network
3. Using a `keras` network with regularization
4. Using a `tensorflow` convolutional network (we did _not_ cover this in class!)
"""

#connect GGD
import os
from google.colab import drive

drive.mount("/content/gdrive")

root_path = r"/content/gdrive/MyDrive/Colab Notebooks/Lab 14" #Colab Notebooks is a folder in Google drive
os.chdir(root_path)
os.getcwd()

# Import libraries and modules
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPooling2D
from tensorflow.keras import utils

train = pd.read_csv('train.csv')
train.head()

test = pd.read_csv('test.csv')
test.head()



#Setup X and y (feature matrix and target vector) and split X and y into train and test subsets.
X = train.drop(columns='label').values
y = train['label'].values

X.shape, y.shape

X[0].shape

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state= 42)

X_train.min(), X_train.max()

X_test.min(), X_test.max()

# Make sure each value is a float 
X_train = X_train.astype('float32')
X_test = X_test.astype('float32')

X_train /= 255.0
X_test /= 255

X_train.shape

# Reshape each image to be 28 x 28 x 1
X_train = X_train.reshape(X_train.shape[0], 28, 28, 1)
X_test = X_test.reshape(X_test.shape[0], 28, 28, 1)
X_train.shape, X_test.shape

#check value of y
y_train[:10]

# check frequency of y values
pd.Series(y_train).value_counts(normalize= True).mul(100).round(2).sort_index()

# y has value ranging from 0 to 9, each value has about 10%

# Change y_train to dummy code #One hot encoded our y
y_train = utils.to_categorical(y_train, 10)
y_test = utils.to_categorical(y_test, 10)

y_train[:10]

# Building nueral network model

# Instantiate a CNN
model= Sequential()

# Add a convolutional layer
model.add(Conv2D(# number of filters
                       filters=16,
                       # height/width of filter
                       kernel_size=(3,3),
                       # activation function 
                       activation='relu',
                       # shape of input (image)
                       input_shape=(28,28,1)))

# Add a pooling layer
model.add(MaxPooling2D(pool_size=(2,2))) 
# dimensions of region of pooling

# Add another convolutional layer
model.add(Conv2D(64,
                       kernel_size=(3,3),
                       activation='relu'))

# Add another pooling layer
model.add(MaxPooling2D(pool_size=(2,2)))

# We have to remember to flatten to go from the 
# "box" to the vertical line of nodes!
model.add(Flatten())

# Add a densely-connected layer with 64 neurons
model.add(Dense(64, activation='relu'))

# Let's try to avoid overfitting!
#model.add(Dropout(0.25))

# Add a densely-connected layer with 64 neurons
model.add(Dense(64, activation='relu'))
# Let's try to avoid overfitting!
#model.add(Dropout(0.5))


# Add a densely-connected layer with 32 neurons
model.add(Dense(32, activation='relu'))

# Let's try to avoid overfitting!
#model.add(Dropout(0.5))

# Add a final layer with 10 neurons.
model.add(Dense(10, activation='softmax'))

# Compile model
model.compile(loss='categorical_crossentropy',
                    optimizer='adam',
                    metrics=['accuracy'])

# Fit model on training data
history = model.fit(X_train,
                          y_train,
                          batch_size=128,
                          validation_data=(X_test, y_test),
                          epochs=15,
                          verbose=1)

# Check out our train loss and test loss over epochs
train_loss = history.history['loss']
test_loss = history.history['val_loss']
epoch_labels = history.epoch

# Set figure size
plt.figure(figsize=(12, 8))

# Generate line plot of training, testing loss over epochs
plt.plot(train_loss, label='Training Loss', color='#185fad')
plt.plot(test_loss, label='Testing Loss', color='orange')

# Set title
plt.title('Training and Testing Loss by Epoch', fontsize=25)
plt.xlabel('Epoch', fontsize=18)
plt.ylabel('Categorical Crossentropy', fontsize=18)
plt.xticks(epoch_labels, epoch_labels) # (ticks, labels)

plt.legend(fontsize=18);

# Check out our train loss and test loss over epochs
train_loss = history.history['accuracy']
test_loss = history.history['val_accuracy']
epoch_labels = history.epoch

# Set figure size
plt.figure(figsize=(12, 8))

# Generate line plot of training, testing loss over epochs
plt.plot(train_loss, label='Training Accuracy', color='#185fad')
plt.plot(test_loss, label='Testing Accuracy', color='orange')

# Set title
plt.title('Training and Testing Accuracy by Epoch', fontsize=25)
plt.xlabel('Epoch', fontsize=18)
plt.ylabel('Categorical Crossentropy', fontsize=18)
plt.xticks(epoch_labels, epoch_labels) # (ticks, labels)

plt.legend(fontsize=18);

# Load validation dataset in Kaggle's test.csv
valid = pd.read_csv('test.csv')
valid.head()

#check shape of validation dataset
valid.shape

#Create predictions
valid = valid.values
valid = valid.reshape(valid.shape[0], 28, 28, 1)
preds = model.predict(valid)

#save predictions
df = pd.DataFrame(data={"ImageId": range(1,28001), 
                        "Label": [np.where(a == np.max(a))[0][0] for a in preds]})
df.to_csv("./answer.csv", sep=',',index=False)
