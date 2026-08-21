import os
import cv2
import numpy as np
from tensorflow.keras.models import load_model

from config import (
    MODEL_PATH,
    SEQUENCE_LENGTH
)

from mediapipe_utils import extract_landmarks

# ==========================================
# CHANGE THIS VIDEO PATH
# ==========================================

VIDEO_PATH = r"C:\Users\MGV\OneDrive\Desktop\Sign_Lang_app\Dataset\Words\Animals\Fish\MVI_2984.MOV"

# ==========================================
# Load Model
# ==========================================

model = load_model(
    os.path.join(MODEL_PATH, "word_model.keras")
)

labels = np.load(
    os.path.join(MODEL_PATH, "word_labels.npy"),
    allow_pickle=True
)

print("Model Loaded")
print(labels)

# ==========================================
# Open Video
# ==========================================

cap = cv2.VideoCapture(VIDEO_PATH)

if not cap.isOpened():

    print("Cannot open video")

    exit()

sequence = []

while True:

    ret, frame = cap.read()

    if not ret:
        break

    landmarks = extract_landmarks(frame)

    if np.any(landmarks):

        sequence.append(landmarks)

    cv2.imshow("Video", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()

cv2.destroyAllWindows()

print()

print("Frames Collected :", len(sequence))

# ==========================================
# Prediction
# ==========================================

if len(sequence) < SEQUENCE_LENGTH:

    print("Not enough frames.")

    exit()

indices = np.linspace(
    0,
    len(sequence) - 1,
    SEQUENCE_LENGTH,
    dtype=int
)

sequence = np.array(sequence)[indices]
sequence = np.array(sequence)

sequence = np.expand_dims(sequence, axis=0)

prediction = model.predict(sequence, verbose=0)

index = np.argmax(prediction)

confidence = prediction[0][index] * 100

print()

print("==========================")

print("Prediction :", labels[index])

print("Confidence :", f"{confidence:.2f}%")

print("==========================")

probabilities = prediction[0]

print("\nClass Probabilities")

for label, prob in zip(labels, probabilities):
    print(f"{label:10} : {prob*100:.2f}%")