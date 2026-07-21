import cv2
import numpy as np
import tensorflow as tf
import mediapipe as mp

from config import FINAL_MODEL, LABEL_FILE

# -----------------------------
# Load Model
# -----------------------------
print("Loading model...")

model = tf.keras.models.load_model(FINAL_MODEL)
labels = np.load(LABEL_FILE, allow_pickle=True)

print("Model Loaded!")

# -----------------------------
# MediaPipe
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
# Webcam
# -----------------------------
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Cannot open webcam.")
    exit()

print("Press Q to Quit")

while True:

    ret, frame = cap.read()

    if not ret:
        break

    frame = cv2.flip(frame, 1)

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(rgb)

    left = [0.0] * 63
    right = [0.0] * 63

    if results.multi_hand_landmarks:

        # Draw landmarks
        for hand_landmarks in results.multi_hand_landmarks:

            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

        # Extract landmarks
        for handedness, landmarks in zip(
                results.multi_handedness,
                results.multi_hand_landmarks):

            hand = handedness.classification[0].label

            values = []

            for lm in landmarks.landmark:
                values.extend([lm.x, lm.y, lm.z])

            if hand == "Left":
                left = values
            else:
                right = values

        features = np.array(left + right).reshape(1, 126)

        prediction = model.predict(features, verbose=0)

        idx = np.argmax(prediction)

        confidence = prediction[0][idx] * 100

        if confidence > 70:

            text = f"{labels[idx]}  {confidence:.1f}%"

        else:

            text = "Detecting..."

        cv2.putText(
            frame,
            text,
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

    cv2.imshow("SignBridge Prototype", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()