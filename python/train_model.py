import os
import joblib
import numpy as np
import pandas as pd
import tensorflow as tf
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.metrics import (
    classification_report,
    confusion_matrix
)
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler

from sklearn.model_selection import train_test_split

from tensorflow.keras.models import Sequential

from tensorflow.keras.layers import (
    Dense,
    Dropout,
    BatchNormalization
)

from tensorflow.keras.callbacks import (
    EarlyStopping,
    ReduceLROnPlateau,
    ModelCheckpoint
)

from config import *

print("=" * 60)
print("          SignBridge AI - Training")
print("=" * 60)

# -------------------------------------------------
# Load Dataset
# -------------------------------------------------

print("\nLoading CSV...")

df = pd.read_csv(RAW_CSV)

print("Dataset Shape :", df.shape)

# -------------------------------------------------
# Features & Labels
# -------------------------------------------------

X = df.drop(columns=["image", "label"]).values.astype(np.float32)

y = df["label"].values

print("Feature Shape :", X.shape)

# -------------------------------------------------
# Encode Labels
# -------------------------------------------------

encoder = LabelEncoder()

y = encoder.fit_transform(y)

print("\nClasses")

print(encoder.classes_)

np.save(LABEL_FILE, encoder.classes_)

# -------------------------------------------------
# Standard Scaler
# -------------------------------------------------

print("\nScaling Features...")

scaler = StandardScaler()

X = scaler.fit_transform(X)

joblib.dump(
    scaler,
    SCALER_FILE
)

print("Scaler Saved")

# -------------------------------------------------
# Train Test Split
# -------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(

    X,

    y,

    test_size=0.20,

    random_state=42,

    stratify=y

)

print("\nTraining Samples :", len(X_train))

print("Testing Samples  :", len(X_test))

# -------------------------------------------------
# Build Model
# -------------------------------------------------

num_classes = len(encoder.classes_)

model = Sequential()

model.add(
    Dense(
        768,
        activation="relu",
        input_shape=(X_train.shape[1],)
    )
)

model.add(BatchNormalization())
model.add(Dropout(0.45))

model.add(
    Dense(
        512,
        activation="relu"
    )
)

model.add(BatchNormalization())
model.add(Dropout(0.35))

model.add(
    Dense(
        256,
        activation="relu"
    )
)

model.add(BatchNormalization())
model.add(Dropout(0.25))

model.add(
    Dense(
        128,
        activation="relu"
    )
)

model.add(
    Dense(
        num_classes,
        activation="softmax"
    )
)

model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

model.summary()
# -------------------------------------------------
# Callbacks
# -------------------------------------------------

checkpoint = ModelCheckpoint(
    filepath=MODEL_FILE,
    monitor="val_accuracy",
    save_best_only=True,
    verbose=1
)

early_stop = EarlyStopping(
    monitor="val_loss",
    patience=12,
    restore_best_weights=True,
    verbose=1
)

reduce_lr = ReduceLROnPlateau(
    monitor="val_loss",
    factor=0.5,
    patience=4,
    min_lr=1e-6,
    verbose=1
)

callbacks = [
    checkpoint,
    early_stop,
    reduce_lr
]

# -------------------------------------------------
# Train Model
# -------------------------------------------------

print("\nStarting Training...\n")

history = model.fit(

    X_train,
    y_train,

    validation_split=0.2,

    epochs=100,

    batch_size=32,

    callbacks=callbacks,

    verbose=1

)

print("\nTraining Completed!")

# -------------------------------------------------
# Save Final Model
# -------------------------------------------------

model.save(FINAL_MODEL)

print(f"\nFinal Model Saved : {FINAL_MODEL}")

# -------------------------------------------------
# Evaluate Model
# -------------------------------------------------

print("\nEvaluating Model...")

loss, accuracy = model.evaluate(
    X_test,
    y_test,
    verbose=0
)

print("=" * 50)
print(f"Test Accuracy : {accuracy*100:.2f}%")
print(f"Test Loss     : {loss:.4f}")
print("=" * 50)

# -------------------------------------------------
# Predictions
# -------------------------------------------------

y_pred_prob = model.predict(
    X_test,
    verbose=0
)

y_pred = np.argmax(
    y_pred_prob,
    axis=1
)
# -------------------------------------------------
# Classification Report
# -------------------------------------------------

print("\nGenerating Classification Report...\n")

report = classification_report(
    y_test,
    y_pred,
    target_names=encoder.classes_
)

print(report)

with open(CLASSIFICATION_REPORT, "w") as f:
    f.write(report)

print("Classification Report Saved")

# -------------------------------------------------
# Confusion Matrix
# -------------------------------------------------

cm = confusion_matrix(
    y_test,
    y_pred
)

plt.figure(figsize=(12, 10))

sns.heatmap(
    cm,
    annot=True,
    fmt="d",
    cmap="Blues",
    xticklabels=encoder.classes_,
    yticklabels=encoder.classes_
)

plt.title("Confusion Matrix")

plt.xlabel("Predicted")

plt.ylabel("Actual")

plt.tight_layout()

plt.savefig(CONFUSION_MATRIX)

plt.close()

print("Confusion Matrix Saved")

# -------------------------------------------------
# Accuracy / Loss Graph
# -------------------------------------------------

plt.figure(figsize=(10, 6))

plt.plot(
    history.history["accuracy"],
    label="Training Accuracy"
)

plt.plot(
    history.history["val_accuracy"],
    label="Validation Accuracy"
)

plt.plot(
    history.history["loss"],
    label="Training Loss"
)

plt.plot(
    history.history["val_loss"],
    label="Validation Loss"
)

plt.title("Training History")

plt.xlabel("Epoch")

plt.ylabel("Value")

plt.legend()

plt.grid(True)

plt.tight_layout()

plt.savefig(TRAINING_GRAPH)

plt.close()

print("Training Graph Saved")

# -------------------------------------------------
# Finished
# -------------------------------------------------

print("\n" + "="*60)
print("Training Pipeline Completed Successfully!")
print("="*60)

print(f"\nModel            : {FINAL_MODEL}")
print(f"Scaler           : {SCALER_FILE}")
print(f"Labels           : {LABEL_FILE}")
print(f"Report           : {CLASSIFICATION_REPORT}")
print(f"Confusion Matrix : {CONFUSION_MATRIX}")
print(f"Training Graph   : {TRAINING_GRAPH}")

print("\nReady for prediction!")