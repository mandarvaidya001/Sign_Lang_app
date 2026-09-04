import os
import cv2
import numpy as np
from tensorflow.keras.models import load_model

from mediapipe_utils import extract_landmarks


# ============================================================
# CONFIGURATION
# ============================================================

SEQUENCE_LENGTH = 30
EXPECTED_FEATURES = 225

MODEL_NAME = "word_model_normalized_attention.keras"
LABEL_NAME = "word_labels.npy"

VIDEO_EXTENSIONS = (
    ".mp4",
    ".mov",
    ".avi",
    ".mkv"
)

# ------------------------------------------------------------
# Greeting classes
# ------------------------------------------------------------

GREETING_CLASSES = [
    "Alright",
    "Good afternoon",
    "Good evening",
    "Good Morning",
    "Good night",
    "Hello",
    "How are you",
    "Pleased",
    "Thank you"
]


# ============================================================
# PROJECT PATH
# ============================================================

# Current file:
#
# Sign_Lang_app/
#     modules/
#         words/
#             python/
#                 test_greetings.py
#
# Therefore go up:
#
# python -> words -> modules -> Sign_Lang_app

CURRENT_FILE = os.path.abspath(__file__)

PYTHON_FOLDER = os.path.dirname(
    CURRENT_FILE
)

WORDS_MODULE_FOLDER = os.path.dirname(
    PYTHON_FOLDER
)

MODULES_FOLDER = os.path.dirname(
    WORDS_MODULE_FOLDER
)

PROJECT_ROOT = os.path.dirname(
    MODULES_FOLDER
)


# ============================================================
# DATASET PATH
# ============================================================

GREETING_DATASET_PATH = os.path.join(
    PROJECT_ROOT,
    "Dataset",
    "Words",
    "Greetings"
)


# ============================================================
# MODEL PATH
# ============================================================

MODEL_PATH = os.path.join(
    PROJECT_ROOT,
    "modules",
    "words",
    "models"
)

MODEL_FILE = os.path.join(
    MODEL_PATH,
    MODEL_NAME
)

LABEL_FILE = os.path.join(
    MODEL_PATH,
    LABEL_NAME
)


# ============================================================
# DISPLAY PATHS
# ============================================================

print()
print("=" * 60)
print("              GREETING DATASET TEST")
print("=" * 60)

print()
print("Project Root:")
print(PROJECT_ROOT)

print()
print("Greeting Dataset:")
print(GREETING_DATASET_PATH)

print()
print("Model:")
print(MODEL_FILE)

print()
print("Labels:")
print(LABEL_FILE)


# ============================================================
# CHECK DATASET
# ============================================================

if not os.path.exists(
    GREETING_DATASET_PATH
):

    print()
    print("ERROR: Greeting dataset folder not found!")
    print()
    print(
        GREETING_DATASET_PATH
    )

    raise SystemExit


# ============================================================
# CHECK MODEL
# ============================================================

if not os.path.exists(
    MODEL_FILE
):

    print()
    print("ERROR: Model file not found!")
    print()
    print(
        MODEL_FILE
    )

    raise SystemExit


# ============================================================
# CHECK LABEL FILE
# ============================================================

if not os.path.exists(
    LABEL_FILE
):

    print()
    print("ERROR: Label file not found!")
    print()
    print(
        LABEL_FILE
    )

    raise SystemExit


# ============================================================
# LOAD MODEL
# ============================================================

print()
print("Loading model...")

model = load_model(
    MODEL_FILE
)


# ============================================================
# LOAD LABELS
# ============================================================

labels = np.load(
    LABEL_FILE,
    allow_pickle=True
)

labels = np.asarray(
    labels
).astype(str)


# ============================================================
# MODEL INFORMATION
# ============================================================

print()
print("=" * 60)
print("MODEL INFORMATION")
print("=" * 60)

print(
    "Model output classes :",
    model.output_shape[-1]
)

print(
    "Label file classes   :",
    len(labels)
)

print()
print("All model classes:")

for i, label in enumerate(
    labels
):

    print(
        f"{i:2d} -> {label}"
    )


# ============================================================
# MODEL / LABEL VALIDATION
# ============================================================

if model.output_shape[-1] != len(labels):

    print()
    print("=" * 60)
    print("ERROR: MODEL / LABEL MISMATCH")
    print("=" * 60)

    print(
        "Model outputs :",
        model.output_shape[-1]
    )

    print(
        "Labels        :",
        len(labels)
    )

    print()
    print(
        "Do not continue testing."
    )

    raise SystemExit


print()
print(
    "Model and label mapping are compatible."
)


# ============================================================
# GET VIDEO FILES
# ============================================================

def get_video_files(
    folder
):

    if not os.path.isdir(
        folder
    ):

        return []


    videos = []

    for filename in sorted(
        os.listdir(folder)
    ):

        if filename.lower().endswith(
            VIDEO_EXTENSIONS
        ):

            videos.append(
                filename
            )


    return videos


# ============================================================
# EXTRACT VIDEO LANDMARK SEQUENCE
# ============================================================

def extract_video_sequence(
    video_path
):

    cap = cv2.VideoCapture(
        video_path
    )


    if not cap.isOpened():

        return None


    frames = []


    try:

        while True:

            ret, frame = cap.read()


            if not ret:

                break


            # ------------------------------------------------
            # Extract normalized landmarks
            # ------------------------------------------------

            landmarks = extract_landmarks(
                frame
            )


            if landmarks is None:

                continue


            landmarks = np.asarray(
                landmarks,
                dtype=np.float32
            )


            # ------------------------------------------------
            # Check frame shape
            # ------------------------------------------------

            if landmarks.shape != (
                EXPECTED_FEATURES,
            ):

                continue


            frames.append(
                landmarks
            )


    finally:

        cap.release()


    # --------------------------------------------------------
    # No valid frames
    # --------------------------------------------------------

    if len(frames) == 0:

        return None


    frames = np.asarray(
        frames,
        dtype=np.float32
    )


    # ========================================================
    # EXACTLY 30 FRAMES
    # ========================================================

    if len(frames) < SEQUENCE_LENGTH:

        last_frame = frames[-1]


        while len(frames) < SEQUENCE_LENGTH:

            frames = np.vstack(
                [
                    frames,
                    last_frame[
                        np.newaxis,
                        :
                    ]
                ]
            )


    elif len(frames) > SEQUENCE_LENGTH:

        indices = np.linspace(
            0,
            len(frames) - 1,
            SEQUENCE_LENGTH,
            dtype=int
        )


        frames = frames[
            indices
        ]


    # ========================================================
    # FINAL SHAPE CHECK
    # ========================================================

    expected_shape = (
        SEQUENCE_LENGTH,
        EXPECTED_FEATURES
    )


    if frames.shape != expected_shape:

        return None


    # ========================================================
    # CHECK NUMERICAL VALUES
    # ========================================================

    if not np.isfinite(
        frames
    ).all():

        return None


    return frames


# ============================================================
# PREDICT ONE VIDEO
# ============================================================

def predict_video(
    video_path
):

    sequence = extract_video_sequence(
        video_path
    )


    if sequence is None:

        return None, 0.0


    # --------------------------------------------------------
    # Add batch dimension
    # --------------------------------------------------------

    input_data = np.expand_dims(
        sequence,
        axis=0
    )


    # --------------------------------------------------------
    # Model prediction
    # --------------------------------------------------------

    prediction = model.predict(
        input_data,
        verbose=0
    )


    probabilities = prediction[0]


    # --------------------------------------------------------
    # Highest probability
    # --------------------------------------------------------

    predicted_index = int(
        np.argmax(
            probabilities
        )
    )


    predicted_label = labels[
        predicted_index
    ]


    confidence = (
        float(
            probabilities[
                predicted_index
            ]
        )
        * 100
    )


    return (
        predicted_label,
        confidence
    )


# ============================================================
# TEST GREETING CLASSES
# ============================================================

total = 0
correct = 0
failed = 0


print()
print()
print("=" * 60)
print("              TESTING GREETINGS")
print("=" * 60)


# ============================================================
# EACH GREETING CLASS
# ============================================================

for class_name in GREETING_CLASSES:


    print()
    print()
    print("=" * 55)
    print(
        f"===== {class_name} ====="
    )
    print("=" * 55)


    # --------------------------------------------------------
    # Correct greeting path
    # --------------------------------------------------------

    class_folder = os.path.join(
        GREETING_DATASET_PATH,
        class_name
    )


    print(
        "Folder:",
        class_folder
    )


    # --------------------------------------------------------
    # Check folder
    # --------------------------------------------------------

    if not os.path.isdir(
        class_folder
    ):

        print()
        print(
            "ERROR: Folder not found!"
        )

        continue


    # --------------------------------------------------------
    # Get videos
    # --------------------------------------------------------

    videos = get_video_files(
        class_folder
    )


    print(
        "Videos:",
        len(videos)
    )


    class_total = 0
    class_correct = 0
    class_failed = 0


    # ========================================================
    # PROCESS VIDEOS
    # ========================================================

    for filename in videos:


        video_path = os.path.join(
            class_folder,
            filename
        )


        predicted, confidence = predict_video(
            video_path
        )


        # ----------------------------------------------------
        # Extraction failure
        # ----------------------------------------------------

        if predicted is None:

            print(
                f"{filename:22} -> FAILED"
            )

            failed += 1
            class_failed += 1

            continue


        # ----------------------------------------------------
        # Count
        # ----------------------------------------------------

        total += 1
        class_total += 1


        # ----------------------------------------------------
        # Correct prediction
        # ----------------------------------------------------

        if predicted == class_name:

            correct += 1
            class_correct += 1

            symbol = "✓"


        else:

            symbol = "✗"


        # ----------------------------------------------------
        # Display
        # ----------------------------------------------------

        print(
            f"{filename:22} -> "
            f"{predicted:18} "
            f"{confidence:6.2f}% "
            f"{symbol}"
        )


    # ========================================================
    # CLASS ACCURACY
    # ========================================================

    if class_total > 0:

        class_accuracy = (
            class_correct /
            class_total
        ) * 100


    else:

        class_accuracy = 0.0


    print()
    print(
        f"{class_name} Accuracy : "
        f"{class_accuracy:.2f}%"
    )


# ============================================================
# OVERALL GREETING ACCURACY
# ============================================================

print()
print()
print("=" * 60)
print("          GREETING OVERALL ACCURACY")
print("=" * 60)


print(
    f"Correct : {correct}"
)

print(
    f"Total   : {total}"
)

print(
    f"Failed  : {failed}"
)


if total > 0:

    overall_accuracy = (
        correct /
        total
    ) * 100


    print(
        f"Accuracy: {overall_accuracy:.2f}%"
    )


else:

    print(
        "Accuracy: No videos were successfully tested."
    )


# ============================================================
# END
# ============================================================

print()
print("=" * 60)
print("             GREETING TEST COMPLETE")
print("=" * 60)