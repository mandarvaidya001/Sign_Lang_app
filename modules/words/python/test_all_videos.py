import os
import cv2
import numpy as np
from tensorflow.keras.models import load_model

from config import (
    DATASET_PATH,
    MODEL_PATH,
    SEQUENCE_LENGTH
)

from mediapipe_utils import extract_landmarks

# =====================================================
# Load Model
# =====================================================

model = load_model(
    os.path.join(MODEL_PATH, "word_model.keras")
)

labels = np.load(
    os.path.join(MODEL_PATH, "word_labels.npy"),
    allow_pickle=True
)

print("\nModel Loaded")
print("Classes:", labels)

# =====================================================
# Test Dataset
# =====================================================

total = 0
correct = 0

results = []

for class_name in labels:

    folder = os.path.join(
    DATASET_PATH,
    class_name
)

    if not os.path.exists(folder):
        continue

    print(f"\n===== {class_name} =====")

    class_total = 0
    class_correct = 0

    for video in sorted(os.listdir(folder)):

        if not video.lower().endswith((".mp4", ".mov")):
            continue

        path = os.path.join(folder, video)

        cap = cv2.VideoCapture(path)

        frames = []

        while True:

            ret, frame = cap.read()

            if not ret:
                break

            landmarks = extract_landmarks(frame)

            frames.append(landmarks)

        cap.release()

        if len(frames) == 0:
            continue

        # SAME sampling as training
        indices = np.linspace(
            0,
            len(frames) - 1,
            SEQUENCE_LENGTH,
            dtype=int
        )

        sequence = np.array(frames)[indices]

        prediction = model.predict(
            np.expand_dims(sequence, axis=0),
            verbose=0
        )

        index = np.argmax(prediction)

        predicted = labels[index]

        confidence = prediction[0][index] * 100

        ok = predicted == class_name

        symbol = "✓" if ok else "✗"

        print(
            f"{video:20} -> {predicted:10} {confidence:6.2f}% {symbol}"
        )

        total += 1
        class_total += 1

        if ok:
            correct += 1
            class_correct += 1

    acc = class_correct / class_total * 100

    print(
        f"{class_name} Accuracy : {acc:.2f}%"
    )

print("\n================================")

print("Overall Accuracy")

print("================================")

print(f"Correct : {correct}")

print(f"Total   : {total}")

print(f"Accuracy: {correct/total*100:.2f}%")