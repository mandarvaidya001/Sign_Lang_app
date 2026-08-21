import cv2
import numpy as np
import threading
from flask import Flask, request, jsonify
from flask_cors import CORS

# Import your existing ML functions
from predict import extract_landmarks, predict, speak_word


app = Flask(__name__)
CORS(app)
# =====================================
# Recognition State
# =====================================
generated_text = ""
speech_status = "idle"

# Latest letter predicted by /predict
current_prediction = None

# Cursor position inside generated_text
cursor_pos = 0

state_lock = threading.Lock()


def speak_text(text):
    global speech_status

    try:
        speech_status = "speaking"
        speak_word(text)
    finally:
        speech_status = "idle"


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "message": "HandTalk AI backend is running"
    })


@app.route("/predict", methods=["POST"])
def prediction():

    try:
        # Check whether an image was received
        if "image" not in request.files:
            return jsonify({
                "error": "No image received"
            }), 400

        image_file = request.files["image"]

        # Read image bytes
        image_bytes = image_file.read()

        # Convert bytes to NumPy array
        image_array = np.frombuffer(image_bytes, np.uint8)

        # Decode image
        frame = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

        if frame is None:
            return jsonify({
                "error": "Unable to decode image"
            }), 400

        # Extract hand landmarks using your existing function
        features, processed_frame, hand_count = extract_landmarks(frame)

        # No hand detected
        if features is None:
            return jsonify({
                "success": True,
                "letter": None,
                "confidence": 0,
                "hand_count": 0,
                "message": "No hand detected"
            })

        # Use your existing ML prediction function
        letter, confidence = predict(features)

        # Remember the latest predicted letter
        global current_prediction
        current_prediction = str(letter)

        return jsonify({
               "success": True,
               "letter": str(letter),
               "confidence": float(confidence),
               "hand_count": int(hand_count)
            })

    except Exception as e:

        print("Prediction Error:", e)

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500
# =====================================
# Generated Text
# =====================================

@app.route("/text", methods=["GET"])
def get_text():
    return jsonify({
        "text": generated_text
    })


# =====================================
# Recognition Actions
# =====================================

@app.route("/action", methods=["POST"])
def action():
    global generated_text
    global cursor_pos
    global current_prediction

    data = request.get_json(silent=True) or {}
    action_name = data.get("action")

    if action_name == "letter":
        letter = data.get("letter")

        if letter:
            generated_text = (
                generated_text[:cursor_pos]
                + str(letter)
                + generated_text[cursor_pos:]
            )
            cursor_pos += 1

    elif action_name == "space":
        # Accept the currently predicted letter
        if current_prediction:
            generated_text = (
                generated_text[:cursor_pos]
                + current_prediction
                + generated_text[cursor_pos:]
            )
            cursor_pos += 1

    elif action_name == "backspace":
        if cursor_pos > 0:
            generated_text = (
            generated_text[:cursor_pos - 1]
            + generated_text[cursor_pos:]
        )
        cursor_pos -= 1      

    elif action_name == "left":
        if cursor_pos > 0:
            cursor_pos -= 1

    elif action_name == "right":
       if cursor_pos < len(generated_text):
        cursor_pos += 1      

    elif action_name == "clear":
        generated_text = ""
        cursor_pos = 0

    elif action_name == "enter":
        text_to_speak = generated_text.strip()

        if text_to_speak:
            threading.Thread(
                target=speak_text,
                args=(text_to_speak,),
                daemon=True
            ).start()

    elif action_name == "quit":
        generated_text = ""
        cursor_pos = 0
        current_prediction = None

    else:
        return jsonify({
            "success": False,
            "error": "Invalid action"
        }), 400

    return jsonify({
         "success": True,
         "action": action_name,
         "text": generated_text,
         "cursor_pos": cursor_pos
    })
if __name__ == "__main__":

    print("\n================================")
    print("       HandTalk AI Backend")
    print("================================")
    print("Backend starting...")
    print("URL: http://127.0.0.1:5000")
    print("================================\n")

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )