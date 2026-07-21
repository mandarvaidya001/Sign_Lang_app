import os
import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

from config import *

# -----------------------------
# Create folders
# -----------------------------
os.makedirs(MODEL_PATH, exist_ok=True)

# -----------------------------
# Load Dataset
# -----------------------------
print("Loading dataset...")

df = pd.read_csv(RAW_CSV)

print(df.head())

# -----------------------------
# Features
# -----------------------------
X = df.drop(columns=["image", "label"]).values

# -----------------------------
# Labels
# -----------------------------
encoder = LabelEncoder()

y = encoder.fit_transform(df["label"])

np.save(LABEL_FILE, encoder.classes_)

print("Classes:", encoder.classes_)

# -----------------------------
# Split
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# -----------------------------
# Model
# -----------------------------
model = Sequential([

    Dense(256, activation="relu", input_shape=(126,)),
    Dropout(0.3),

    Dense(128, activation="relu"),
    Dropout(0.3),

    Dense(64, activation="relu"),

    Dense(len(encoder.classes_), activation="softmax")

])

model.compile(
    optimizer="adam",
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

# -----------------------------
# Callbacks
# -----------------------------
callbacks = [

    EarlyStopping(
        monitor="val_loss",
        patience=10,
        restore_best_weights=True
    ),

    ModelCheckpoint(
        MODEL_FILE,
        save_best_only=True
    )

]

# -----------------------------
# Train
# -----------------------------
history = model.fit(

    X_train,
    y_train,

    validation_split=0.2,

    epochs=100,

    batch_size=32,

    callbacks=callbacks,

    verbose=1

)

# -----------------------------
# Evaluate
# -----------------------------
loss, accuracy = model.evaluate(X_test, y_test)

print("\n")
print("=" * 40)
print(f"Test Accuracy : {accuracy*100:.2f}%")
print("=" * 40)

# -----------------------------
# Save Final Model
# -----------------------------
model.save(FINAL_MODEL)

print("\nModel Saved Successfully!")
print(FINAL_MODEL)