import cv2
import mediapipe as mp
import numpy as np


# ==========================================
# MediaPipe Holistic
# ==========================================

mp_holistic = mp.solutions.holistic

holistic = mp_holistic.Holistic(
    static_image_mode=False,
    model_complexity=1,
    smooth_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)


# ==========================================
# Landmark Normalization
# ==========================================

def normalize_landmarks(landmarks):
    """
    Normalize 225 landmark features.

    Structure:
        Pose       : 99 values
        Left hand  : 63 values
        Right hand : 63 values

    Total:
        225 values

    Normalization:
        1. Center around shoulder midpoint.
        2. Scale using shoulder distance.
    """

    landmarks = landmarks.reshape(75, 3)

    # --------------------------------------
    # Pose landmarks
    # --------------------------------------

    pose = landmarks[:33]

    # MediaPipe Pose:
    # Left shoulder  = 11
    # Right shoulder = 12

    left_shoulder = pose[11]
    right_shoulder = pose[12]

    # --------------------------------------
    # Check whether shoulders exist
    # --------------------------------------

    shoulder_distance = np.linalg.norm(
        left_shoulder - right_shoulder
    )

    # If pose is missing or shoulders are invalid,
    # return original landmarks rather than
    # creating unstable values.

    if shoulder_distance < 1e-6:

        return landmarks.flatten().astype(np.float32)

    # --------------------------------------
    # Shoulder midpoint
    # --------------------------------------

    center = (
        left_shoulder + right_shoulder
    ) / 2.0

    # --------------------------------------
    # Translation normalization
    # --------------------------------------

    normalized = landmarks - center

    # --------------------------------------
    # Scale normalization
    # --------------------------------------

    normalized = normalized / shoulder_distance

    # --------------------------------------
    # Flatten back to 225 features
    # --------------------------------------

    return normalized.flatten().astype(np.float32)


# ==========================================
# Extract + Normalize Landmarks
# Output Shape: (225,)
# ==========================================

def extract_landmarks(frame):

    image = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2RGB
    )

    results = holistic.process(image)

    landmarks = []

    # ======================================
    # Pose
    # 33 × 3 = 99
    # ======================================

    if results.pose_landmarks:

        for lm in results.pose_landmarks.landmark:

            landmarks.extend([
                lm.x,
                lm.y,
                lm.z
            ])

    else:

        landmarks.extend([0.0] * 99)

    # ======================================
    # Left Hand
    # 21 × 3 = 63
    # ======================================

    if results.left_hand_landmarks:

        for lm in results.left_hand_landmarks.landmark:

            landmarks.extend([
                lm.x,
                lm.y,
                lm.z
            ])

    else:

        landmarks.extend([0.0] * 63)

    # ======================================
    # Right Hand
    # 21 × 3 = 63
    # ======================================

    if results.right_hand_landmarks:

        for lm in results.right_hand_landmarks.landmark:

            landmarks.extend([
                lm.x,
                lm.y,
                lm.z
            ])

    else:

        landmarks.extend([0.0] * 63)

    # ======================================
    # Convert to NumPy
    # ======================================

    landmarks = np.array(
        landmarks,
        dtype=np.float32
    )

    # ======================================
    # Normalize
    # ======================================

    landmarks = normalize_landmarks(
        landmarks
    )

    return landmarks