import cv2
import numpy as np
import mediapipe as mp
import joblib
from collections import Counter, deque
from config import MODEL_PATH

# -----------------------------
# MediaPipe Initialization
# -----------------------------
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# -----------------------------
# Load Scaler (if available)
# -----------------------------
try:
    scaler = joblib.load(f"{MODEL_PATH}/scaler.pkl")
except:
    scaler = None


# -----------------------------
# Draw Hand Landmarks
# -----------------------------
def draw_landmarks(frame, results):

    if results.multi_hand_landmarks:

        for hand_landmarks in results.multi_hand_landmarks:

            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )


# -----------------------------
# Extract Features
# -----------------------------
def extract_features(image):

    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    results = hands.process(rgb)

    left = [0.0] * 63
    right = [0.0] * 63

    if not results.multi_hand_landmarks:
        return None, results

    for handedness, landmarks in zip(
            results.multi_handedness,
            results.multi_hand_landmarks):

        hand = handedness.classification[0].label

        values = []

        for lm in landmarks.landmark:

            values.extend([
                lm.x,
                lm.y,
                lm.z
            ])

        if hand == "Left":
            left = values
        else:
            right = values

    features = np.array(left + right, dtype=np.float32)

    if scaler is not None:
        features = scaler.transform(features.reshape(1, -1))
    else:
        features = features.reshape(1, -1)

    return features, results


# -----------------------------
# Predict Letter
# -----------------------------
def predict_letter(model, labels, features):

    prediction = model.predict(
        features,
        verbose=0
    )

    index = np.argmax(prediction)

    confidence = prediction[0][index] * 100

    letter = labels[index]

    return letter, confidence

# ---------------------------------------
# Stable Prediction
# ---------------------------------------

prediction_history = deque(maxlen=STABLE_FRAMES)

def get_stable_prediction(letter):
    prediction_history.append(letter)

    if len(prediction_history) < STABLE_FRAMES:
        return None

    return Counter(prediction_history).most_common(1)[0][0]


# ---------------------------------------
# Draw Information
# ---------------------------------------

def draw_info(frame,
              letter,
              confidence,
              current_word,
              sentence,
              fps,
              hands):

    cv2.rectangle(frame, (0, 0), (420, 210), (0, 0, 0), -1)

    cv2.putText(frame,
                f"Letter : {letter}",
                (15, 35),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0,255,0),
                2)

    cv2.putText(frame,
                f"Confidence : {confidence:.2f} %",
                (15,65),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255,255,255),
                2)

    cv2.putText(frame,
                f"Word : {current_word}",
                (15,95),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255,255,0),
                2)

    cv2.putText(frame,
                f"Sentence : {sentence}",
                (15,125),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0,255,255),
                2)

    cv2.putText(frame,
                f"Hands : {hands}",
                (15,155),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255,255,255),
                2)

    cv2.putText(frame,
                f"FPS : {fps}",
                (15,185),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255,255,255),
                2)