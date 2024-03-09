# -*- coding: utf-8 -*-
"""digit recogniser.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1dKBePshG5VfwdJ1mRwIeRYKUsOxtCZIX
"""

import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.activations import linear, relu, sigmoid
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dropout, BatchNormalization
import matplotlib.pyplot as plt
import pandas as pd

train_data = pd.read_csv('/content/train.csv')
test_data = pd.read_csv('/content/test.csv')

train_data.head()

test_data.head()

print(f"Train data shape: {train_data.shape}")
print(f"Test data shape: {test_data.shape}")

X_train = train_data.iloc[:, 1:].values  # All rows, all columns except the first column
y_train = train_data.iloc[:, 0].values   # All rows, just the first column (labels)
X_test = test_data.values

X_train = X_train.reshape(X_train.shape[0], 28, 28)  # Reshape to (num_samples, 28, 28, 1)
X_test = X_test.reshape(X_test.shape[0], 28, 28)     # Reshape to (num_samples, 28, 28, 1)

X_train = X_train / 255.0
X_test = X_test / 255.0


print(f"X_train shape: {X_train.shape}")
print(f"y_train shape: {y_train.shape}")
print(f"X_test shape: {X_test.shape}")

num_images = 10
fig, axes = plt.subplots(2, num_images // 2, figsize=(10, 4))  # Create a grid
for i in range(num_images):

    img = X_train[i].reshape(28, 28)

    row = i // (num_images // 2)
    col = i % (num_images // 2)
    if num_images // 2 == 1:
        ax = axes[row]
    else:
        ax = axes[row, col]
    ax.imshow(img, cmap='gray')
    ax.set_title(f"Label: {y_train[i]}")
    ax.axis('off')

plt.tight_layout()
plt.show()

tf.random.set_seed(1234)


num_classes = 10


model = Sequential([
    Conv2D(32, (3, 3), activation='relu', padding='same', input_shape=(28, 28, 1)),
    BatchNormalization(),
    MaxPooling2D((2, 2)),
    Dropout(0.25),

    Conv2D(64, (3, 3), activation='relu', padding='same'),
    BatchNormalization(),
    Conv2D(64, (3, 3), activation='relu', padding='same'),
    MaxPooling2D((2, 2)),
    Dropout(0.25),

    Conv2D(128, (3, 3), activation='relu', padding='same'),
    BatchNormalization(),
    Conv2D(128, (3, 3), activation='relu', padding='same'),
    MaxPooling2D((2, 2)),
    Dropout(0.4),

    Flatten(),
    Dense(128, activation='relu'),
    BatchNormalization(),
    Dropout(0.5),
    Dense(num_classes, activation='softmax')
])


model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])


model.summary()

history = model.fit(X_train, y_train, epochs=20, batch_size=32, validation_split=0.2)

accuracy = history.history['accuracy']
val_accuracy = history.history['val_accuracy']
loss = history.history['loss']
val_loss = history.history['val_loss']
epochs = range(1, len(accuracy) + 1)

# Plotting training and validation accuracy
plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
plt.plot(epochs, accuracy, 'bo-', label='Training accuracy')
plt.plot(epochs, val_accuracy, 'ro-', label='Validation accuracy')
plt.title('Training and Validation Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()

# Plotting training and validation loss
plt.subplot(1, 2, 2)
plt.plot(epochs, loss, 'bo-', label='Training loss')
plt.plot(epochs, val_loss, 'ro-', label='Validation loss')
plt.title('Training and Validation Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()

plt.tight_layout()
plt.show()

predictions = model.predict(X_test)
predicted_classes = np.argmax(predictions, axis=1)

import matplotlib.pyplot as plt

num_images_to_show = 50
fig, axes = plt.subplots(5, num_images_to_show // 5, figsize=(10, 10))

for i in range(num_images_to_show):

    img = X_test[i].reshape(28, 28)

    row = i // (num_images_to_show // 5)
    col = i % (num_images_to_show // 5)

    axes[row, col].imshow(img, cmap='gray')
    axes[row, col].set_title(f"Pred: {predicted_classes[i]}")
    axes[row, col].axis('off')

plt.tight_layout()
plt.show()

predictions_df = pd.DataFrame({
    'ImageId': range(1, len(predicted_classes) + 1),
    'Label': predicted_classes
})

predictions_df.to_csv('submission.csv', index=False)
