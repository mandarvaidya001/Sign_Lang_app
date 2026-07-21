import tensorflow as tf
from config import FINAL_MODEL, MODEL_PATH
import os

# Load trained model
model = tf.keras.models.load_model(FINAL_MODEL)

# Convert to TensorFlow Lite
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()

# Save model
tflite_path = os.path.join(MODEL_PATH, "sign_model.tflite")

with open(tflite_path, "wb") as f:
    f.write(tflite_model)

print("✅ TensorFlow Lite model saved at:")
print(tflite_path)