import os

# =============================
# Project Root
# =============================

PROJECT_ROOT = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",   # python
        "..",   # alphabet
        ".."    # SIGN_LANG_APP
    )
)

# =============================
# Folders
# =============================

DATASET_PATH = os.path.join(PROJECT_ROOT, "Dataset", "Alphabet")

CSV_PATH = os.path.join(
    PROJECT_ROOT,
    "modules",
    "alphabet",
    "csv"
)

MODEL_PATH = os.path.join(
    PROJECT_ROOT,
    "modules",
    "alphabet",
    "models"
)

# Create folders if missing
os.makedirs(CSV_PATH, exist_ok=True)
os.makedirs(MODEL_PATH, exist_ok=True)

# =============================
# Files
# =============================

RAW_CSV = os.path.join(CSV_PATH, "raw_landmarks.csv")

MODEL_FILE = os.path.join(MODEL_PATH, "sign_model.keras")

FINAL_MODEL = os.path.join(MODEL_PATH, "sign_model_final.keras")

LABEL_FILE = os.path.join(MODEL_PATH, "labels.npy")

SCALER_FILE = os.path.join(MODEL_PATH, "scaler.pkl")

CONFUSION_MATRIX = os.path.join(MODEL_PATH, "confusion_matrix.png")

TRAINING_GRAPH = os.path.join(MODEL_PATH, "training_graph.png")

CLASSIFICATION_REPORT = os.path.join(MODEL_PATH, "classification_report.txt")

# =============================
# MediaPipe
# =============================

MAX_NUM_HANDS = 2
MIN_DETECTION_CONFIDENCE = 0.5

# =============================
# Prediction
# =============================

CONFIDENCE_THRESHOLD = 80.0
STABLE_FRAMES = 8