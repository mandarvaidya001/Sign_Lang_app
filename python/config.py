import os


# -----------------------------
# Project Root
# -----------------------------
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# -----------------------------
# Folders
# -----------------------------
DATASET_PATH = os.path.join(PROJECT_ROOT, "Dataset")   # Note: matches your folder name
CSV_PATH = os.path.join(PROJECT_ROOT, "csv")
MODEL_PATH = os.path.join(PROJECT_ROOT, "models")

# -----------------------------
# Files
# -----------------------------
RAW_CSV = os.path.join(CSV_PATH, "raw_landmarks.csv")
MODEL_FILE = os.path.join(MODEL_PATH, "sign_model.keras")
FINAL_MODEL = os.path.join(MODEL_PATH, "sign_model_final.keras")
LABEL_FILE = os.path.join(MODEL_PATH, "labels.npy")
# Extra Files
SCALER_FILE = os.path.join(MODEL_PATH, "scaler.pkl")
CONFUSION_MATRIX = os.path.join(MODEL_PATH, "confusion_matrix.png")
TRAINING_GRAPH = os.path.join(MODEL_PATH, "training_graph.png")
CLASSIFICATION_REPORT = os.path.join(MODEL_PATH, "classification_report.txt")
# -----------------------------
# MediaPipe
# -----------------------------
MAX_NUM_HANDS = 2
MIN_DETECTION_CONFIDENCE = 0.5
# Prediction Settings
CONFIDENCE_THRESHOLD = 80.0
STABLE_FRAMES = 8