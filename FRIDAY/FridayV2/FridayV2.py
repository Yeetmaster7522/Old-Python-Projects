import os

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'

import tensorflow as tf
import keras
from keras import layers
import numpy as np
import matplotlib.pyplot as plt

model = keras.models.Sequential([
    keras.layers.Rescaling(1./255, input_shape=(500, 500, 3)),
    keras.layers.Conv2D(32, (3, 3), activation='relu'),
    keras.layers.MaxPooling2D((2, 2)),
    keras.layers.Conv2D(64, (3, 3), activation='relu'),
    keras.layers.MaxPooling2D((2, 2)),
    keras.layers.Conv2D(64, (3, 3), activation='relu'),
    keras.layers.Flatten(),
    keras.layers.Dense(128, activation='relu'),
    keras.layers.Dense(2)
])

model.compile(
    optimizer="adam",
    loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True),
    metrics=["accuracy"]
)

probability_model = keras.Sequential([
    model,
    keras.layers.Softmax()
])

batch_size = 32
img_height = 500
img_width = 500

train_ds = keras.utils.image_dataset_from_directory(
    'FRIDAY\FridayV2\images',
    validation_split=0.2,
    subset="training",
    seed=123,
    image_size=(img_height, img_width),
    batch_size=batch_size
    )

val_ds = keras.utils.image_dataset_from_directory(
    'FRIDAY\FridayV2\images',
    validation_split=0.2,
    subset="validation",
    seed=123,
    image_size=(img_height, img_width),
    batch_size=batch_size
    )

history = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=10
)

loss, accuracy = model.evaluate(val_ds)
print(f"Validation accuracy: {accuracy}")
