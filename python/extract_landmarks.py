import os
import cv2
import mediapipe as mp
import numpy as np
import pandas as pd

from config import *

mp_hands = mp.solutions.hands

hands = mp_hands.Hands(
    static_image_mode=True,
    max_num_hands=2,
    min_detection_confidence=0.5
)


def angle_between(a, b, c):
    v1 = a - b
    v2 = c - b
    denom = np.linalg.norm(v1) * np.linalg.norm(v2)
    if denom < 1e-9:
        return 0.0
    cos_value = np.clip(np.dot(v1, v2) / denom, -1.0, 1.0)
    return float(np.arccos(cos_value))


def normalize_hand(hand_points):
    """
    Normalize landmarks relative to wrist and hand size
    and add angular features for each finger.
    """

    pts = np.array(hand_points, dtype=np.float32).reshape(21, 3)

    wrist = pts[0]
    pts = pts - wrist

    scale = np.max(np.linalg.norm(pts, axis=1))
    if scale < 1e-6:
        scale = 1.0

    pts = pts / scale

    angles = []
    fingers = [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10, 11, 12],
        [13, 14, 15, 16],
        [17, 18, 19, 20]
    ]

    for finger in fingers:
        angles.append(angle_between(pts[finger[0]], pts[finger[1]], pts[finger[2]]))
        angles.append(angle_between(pts[finger[1]], pts[finger[2]], pts[finger[3]]))

    return pts.flatten().tolist() + angles


columns = ["image"]

for h in [1, 2]:
    for i in range(21):
        columns += [
            f"H{h}_x{i}",
            f"H{h}_y{i}",
            f"H{h}_z{i}"
        ]
    for i in range(10):
        columns.append(f"H{h}_angle{i}")

columns.append("label")

data = []

processed = 0
skipped = 0
one_hand = 0
two_hands = 0
no_hand = 0

print("Extracting landmarks...\n")

for label in sorted(os.listdir(DATASET_PATH)):

    folder = os.path.join(DATASET_PATH, label)

    if not os.path.isdir(folder):
        continue

    print(f"Processing {label}...")

    for image_name in os.listdir(folder):

        path = os.path.join(folder, image_name)

        image = cv2.imread(path)

        if image is None:
            skipped += 1
            continue

        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        results = hands.process(rgb)

        if not results.multi_hand_landmarks:

            no_hand += 1
            skipped += 1
            continue

        left = [0.0] * 73
        right = [0.0] * 73

        if len(results.multi_hand_landmarks) == 1:
            one_hand += 1
        else:
            two_hands += 1

        for handedness, landmarks in zip(
            results.multi_handedness,
            results.multi_hand_landmarks
        ):

            coords = []

            for lm in landmarks.landmark:
                coords.extend([lm.x, lm.y, lm.z])

            coords = normalize_hand(coords)

            hand = handedness.classification[0].label

            if hand == "Left":
                left = coords
            else:
                right = coords

        row = [image_name]
        row.extend(left)
        row.extend(right)
        row.append(label)

        data.append(row)

        processed += 1

df = pd.DataFrame(data, columns=columns)

df.to_csv(RAW_CSV, index=False)

print("\n==============================")
print("Extraction Complete")
print("==============================")
print(f"Processed Images : {processed}")
print(f"Skipped Images   : {skipped}")
print(f"No Hand          : {no_hand}")
print(f"One Hand         : {one_hand}")
print(f"Two Hands        : {two_hands}")

print("\nClass Distribution")
print(df["label"].value_counts().sort_index())

print(f"\nCSV saved to : {RAW_CSV}")