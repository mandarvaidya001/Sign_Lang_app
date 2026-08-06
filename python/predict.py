import cv2
import os
import joblib
import numpy as np
import mediapipe as mp
import tensorflow as tf

from tkinter import Tk
from tkinter.filedialog import askopenfilename

from config import *

# =====================================
# Load Model
# =====================================

print("Loading HandTalk AI...")

model = tf.keras.models.load_model(FINAL_MODEL)

labels = np.load(LABEL_FILE, allow_pickle=True)

scaler = joblib.load(SCALER_FILE)

print("Model Loaded Successfully!")

# =====================================
# MediaPipe Hands
# =====================================

mp_hands = mp.solutions.hands

mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# =====================================
# Extract Landmarks
# =====================================

def angle_between(a, b, c):
    v1 = a - b
    v2 = c - b
    denom = np.linalg.norm(v1) * np.linalg.norm(v2)
    if denom < 1e-9:
        return 0.0
    cos_value = np.clip(np.dot(v1, v2) / denom, -1.0, 1.0)
    return float(np.arccos(cos_value))


def normalize_hand(hand_points):
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


def extract_landmarks(frame):

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    result = hands.process(rgb)

    if result.multi_hand_landmarks is None:
        return None, frame, 0

    landmark_list = []

    hand_landmarks = result.multi_hand_landmarks

    handedness = result.multi_handedness

    left = None
    right = None

    for lm, hand in zip(hand_landmarks, handedness):

        if hand.classification[0].label == "Left":
            left = lm
        else:
            right = lm

    def append_hand(hand):

        if hand is None:
            landmark_list.extend([0.0] * 73)
            return

        coords = []
        for point in hand.landmark:
            coords.extend([point.x, point.y, point.z])

        landmark_list.extend(normalize_hand(coords))

    append_hand(left)
    append_hand(right)

    for hand in hand_landmarks:
        mp_draw.draw_landmarks(
            frame,
            hand,
            mp_hands.HAND_CONNECTIONS
        )

    return np.array(landmark_list, dtype=np.float32), frame, len(hand_landmarks)

# =====================================
# Prediction
# =====================================

def predict(features):

    features = scaler.transform([features])

    prediction = model.predict(features, verbose=0)[0]

    index = np.argmax(prediction)

    confidence = prediction[index] * 100

    letter = labels[index]

    return letter, confidence
# =====================================
# Image Prediction
# =====================================

def image_mode():

    Tk().withdraw()

    file_path = askopenfilename(
        title="Select Image",
        filetypes=[
            ("Image Files", "*.jpg *.jpeg *.png")
        ]
    )

    if file_path == "":
        return

    frame = cv2.imread(file_path)

    features, frame, hand_count = extract_landmarks(frame)

    if features is None:

        cv2.putText(
            frame,
            "No Hand Detected",
            (20,40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0,0,255),
            2
        )

        cv2.imshow("HandTalk AI", frame)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        return

    letter, confidence = predict(features)

    cv2.putText(
        frame,
        f"Letter : {letter}",
        (20,40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0,255,0),
        2
    )

    cv2.putText(
        frame,
        f"Confidence : {confidence:.2f}%",
        (20,80),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255,255,255),
        2
    )

    cv2.putText(
        frame,
        f"Hands : {hand_count}",
        (20,120),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255,255,0),
        2
    )

    cv2.imshow("HandTalk AI", frame)

    cv2.waitKey(0)

    cv2.destroyAllWindows()
    # =====================================
# Camera Mode
# =====================================

def camera_mode():

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Unable to open camera.")
        return

    current_word = ""
    cursor_pos = 0

    current_letter = None
    while True:

        ret, frame = cap.read()

        if not ret:
            break

        frame = cv2.flip(frame,1)

        features, frame, hand_count = extract_landmarks(frame)

        if features is not None:

            letter, confidence = predict(features)
            current_letter = letter

            cv2.putText(
                frame,
                f"{letter}",
                (20,60),
                cv2.FONT_HERSHEY_SIMPLEX,
                2,
                (0,255,0),
                3
            )

            cv2.putText(
                frame,
                f"{confidence:.2f} %",
                (20,110),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255,255,255),
                2
            )

            cv2.putText(
                frame,
                f"Hands : {hand_count}",
                (20,150),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255,255,0),
                2
            )

        else:

            cv2.putText(
                frame,
                "No Hand Detected",
                (20,60),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0,0,255),
                2
            )
        cv2.putText(
            frame,
            f"Word: {current_word[:cursor_pos]}|{current_word[cursor_pos:]}",
            (20, 200),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 255, 255),
            2
        )    

        cv2.imshow("HandTalk AI", frame)

        key = cv2.waitKeyEx(1)

        # SPACE -> Add predicted letter
        if key == 32:
            if current_letter is not None:
             current_word = current_word[:cursor_pos] + str(current_letter) + current_word[cursor_pos:]
             cursor_pos += 1
             print("Current Word:", current_word)

        # LEFT ARROW -> Move cursor left
        elif key == 2424832:
           if cursor_pos > 0:
              cursor_pos -= 1

        # RIGHT ARROW -> Move cursor right
        elif key == 2555904:
            if cursor_pos < len(current_word):
               cursor_pos += 1     

        # BACKSPACE -> Delete letter before cursor
        elif key in (8, 127):
          if cursor_pos > 0:
             current_word = current_word[:cursor_pos - 1] + current_word[cursor_pos:]
             cursor_pos -= 1
             print("Current Word:", current_word)
        
        # C -> Clear entire word
        elif key in (ord('c'), ord('C')):
            current_word = ""
            cursor_pos = 0
            print("Word Cleared")

        # ENTER -> Complete word
        elif key in (10, 13):
            if current_word:
                print("Completed Word:", current_word)

        # Q -> Quit
        elif key in (ord('q'), ord('Q')):
            break

        

        

    cap.release()

    cv2.destroyAllWindows()

if __name__ == "__main__":
    print("\n==============================")
    print("        HandTalk AI")
    print("==============================")
    print("1. Image Prediction")
    print("2. Live Camera")
    print("==============================")

    choice = input("Enter Choice : ")

    if choice == "1":
        image_mode()

    elif choice == "2":
        camera_mode()

    else:
        print("Invalid Choice")