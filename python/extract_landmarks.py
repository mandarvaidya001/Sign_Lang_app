import os
import cv2
import mediapipe as mp
import pandas as pd

from tqdm import tqdm

from config import *

# -----------------------------
# Create output folder
# -----------------------------
os.makedirs(CSV_PATH, exist_ok=True)

# -----------------------------
# MediaPipe
# -----------------------------
mp_hands = mp.solutions.hands

hands = mp_hands.Hands(
    static_image_mode=True,
    max_num_hands=2,
    min_detection_confidence=0.5
)

rows = []

# Statistics
total_images = 0
processed = 0
zero_hand = 0
one_hand = 0
two_hand = 0

# -----------------------------
# Read Dataset
# -----------------------------
labels = sorted(os.listdir(DATASET_PATH))

for label in labels:

    folder = os.path.join(DATASET_PATH, label)

    if not os.path.isdir(folder):
        continue

    print(f"\nProcessing {label}")

    for image_name in tqdm(os.listdir(folder)):

        total_images += 1

        image_path = os.path.join(folder, image_name)

        image = cv2.imread(image_path)

        if image is None:
            continue

        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        results = hands.process(rgb)

        # No hand detected
        if not results.multi_hand_landmarks:
            zero_hand += 1
            continue

        # Prepare placeholders
        left = [0.0] * 63
        right = [0.0] * 63

        # Read detected hands
        for handedness, landmarks in zip(
            results.multi_handedness,
            results.multi_hand_landmarks
        ):

            hand_type = handedness.classification[0].label

            values = []

            for lm in landmarks.landmark:
                values.extend([lm.x, lm.y, lm.z])

            if hand_type == "Left":
                left = values
            else:
                right = values

        # Statistics
        if len(results.multi_hand_landmarks) == 1:
            one_hand += 1
        else:
            two_hand += 1

        sample = [image_name]
        sample.extend(left)
        sample.extend(right)
        sample.append(label)

        rows.append(sample)
        processed += 1

# -----------------------------
# Column Names
# -----------------------------
columns = ["image"]

for hand in ["L", "R"]:

    for i in range(21):

        columns.extend([
            f"{hand}_x{i}",
            f"{hand}_y{i}",
            f"{hand}_z{i}"
        ])

columns.append("label")

df = pd.DataFrame(rows, columns=columns)

df.to_csv(RAW_CSV, index=False)

# -----------------------------
# Summary
# -----------------------------
print("\n===========================")
print("Dataset Extraction Finished")
print("===========================")

print(f"Total Images      : {total_images}")
print(f"Processed         : {processed}")
print(f"Two Hands         : {two_hand}")
print(f"One Hand          : {one_hand}")
print(f"No Hand Detected  : {zero_hand}")

print(f"\nCSV Saved To:\n{RAW_CSV}")