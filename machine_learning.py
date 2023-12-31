# -*- coding: utf-8 -*-
"""machine_learning.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1rF-tDgwq42k1xKvkdpSEIq9WGyg4p1_E
"""

import os
import matplotlib.pyplot as plt

import tensorflow as tf
from tensorflow.keras import layers
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from PIL import Image

from google.colab import drive

drive.mount('/content/drive')

# Chemin vers le répertoire contenant les images de chaque classe


train_data_dir = "/content/drive/MyDrive/projet_ML/train_data_dir"
test_data_dir = "/content/drive/MyDrive/projet_ML/test_data_dir"
new_data_dir = "/content/drive/MyDrive/projet_ML/new_data_dir"

# Paramètres du modèle
input_shape = (150, 150, 3)
num_classes = 2

# Prétraitement des données
train_datagen = ImageDataGenerator(rescale=1./255, validation_split=0.2)
test_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_directory(
    train_data_dir,
    target_size=input_shape[:2],
    batch_size=32,
    class_mode='categorical',
    subset='training'
)

validation_generator = train_datagen.flow_from_directory(
    train_data_dir,
    target_size=input_shape[:2],
    batch_size=32,
    class_mode='categorical',
    subset='validation'
)

# Création du modèle CNN
model = tf.keras.Sequential([
    layers.Conv2D(32, (3, 3), activation='relu', input_shape=input_shape),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(128, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.Dense(num_classes, activation='softmax')
])

# Compilation du modèle
model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# Entraînement du modèle
model.fit(train_generator, validation_data=validation_generator, epochs=10)

# Sauvegarde des poids du modèle
model.save_weights("/content/drive/MyDrive/projet_ML/poids_du_modele.h5")

# Évaluation du modèle sur l'ensemble de test
test_generator = test_datagen.flow_from_directory(
    test_data_dir,
    target_size=input_shape[:2],
    batch_size=32,
    class_mode='categorical'
)

loss, accuracy = model.evaluate(test_generator)
print("Loss:", loss)
print("Accuracy:", accuracy)

# Charger les poids du modèle entraîné
model.load_weights("/content/drive/MyDrive/projet_ML/poids_du_modele.h5")

# Préparation et redimensionnement du nouvel ensemble de données
new_datagen = ImageDataGenerator(rescale=1./255)
new_generator = new_datagen.flow_from_directory(
    new_data_dir,
    target_size=input_shape[:2],
    batch_size=32,
    class_mode='categorical',
    shuffle=False
)

# Prédiction sur les nouveaux exemples
predictions = model.predict(new_generator)

# Interprétation des prédictions
class_labels = train_generator.class_indices

plt.figure(figsize=(10, 10))
for i in range(1):
    if i >= len(new_generator.filenames):
        break

    plt.subplot(5, 5, i+1)
    plt.xticks([])
    plt.yticks([])
    plt.grid(False)

    # Chargement de l'image
    image_path = os.path.join(new_data_dir, new_generator.filenames[i])
    image = Image.open(image_path)

    plt.imshow(image, cmap=plt.cm.binary)
    predicted_label = predictions[i].argmax()
    class_name = list(class_labels.keys())[list(class_labels.values()).index(predicted_label)]
    plt.xlabel(class_name)

plt.show()