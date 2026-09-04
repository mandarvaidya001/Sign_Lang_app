import os

# =====================================
# PROJECT ROOT
# =====================================

PROJECT_ROOT = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",      # python
        "..",      # words
        ".."       # Sign_Lang_app
    )
)

# =====================================
# DATASET PATHS
# =====================================

# =====================================
# DATASET
# =====================================

DATASET_PATH = os.path.join(
    PROJECT_ROOT,
    "Dataset",
    "Words",
    "Animals"
)

# =====================================
# OUTPUT FOLDERS
# =====================================

SEQUENCE_PATH = os.path.join(
    PROJECT_ROOT,
    "Dataset",
    "Words_Landmarks"
)

MODEL_PATH = os.path.join(
    PROJECT_ROOT,
    "modules",
    "words",
    "models"
)

LOG_PATH = os.path.join(
    PROJECT_ROOT,
    "modules",
    "words",
    "logs"
)

# =====================================
# VIDEO SETTINGS
# =====================================

SEQUENCE_LENGTH = 30

# =====================================
# MEDIAPIPE SETTINGS
# =====================================

MAX_NUM_HANDS = 2

MIN_DETECTION_CONFIDENCE = 0.5
MIN_TRACKING_CONFIDENCE = 0.5

# =====================================
# PREDICTION SETTINGS
# =====================================

CONFIDENCE_THRESHOLD = 80.0      # Show prediction only above 80%
STABLE_FRAMES = 5                # Same prediction for 5 frames

# =====================================
# CREATE DIRECTORIES
# =====================================

os.makedirs(SEQUENCE_PATH, exist_ok=True)
os.makedirs(MODEL_PATH, exist_ok=True)
os.makedirs(LOG_PATH, exist_ok=True)

# =====================================
# DEBUG (Optional)
# =====================================

if __name__ == "__main__":
    print("PROJECT_ROOT :", PROJECT_ROOT)
    print("DATASET_PATH :", DATASET_PATH)
    print("SEQUENCE_PATH:", SEQUENCE_PATH)
    print("MODEL_PATH   :", MODEL_PATH)
    print("LOG_PATH     :", LOG_PATH)