import os
import cv2
import time
import numpy as np
from collections import deque

from tensorflow.keras.models import load_model

from config import (
    MODEL_PATH,
    SEQUENCE_LENGTH,
    CONFIDENCE_THRESHOLD,
    STABLE_FRAMES
)

from mediapipe_utils import (
    extract_landmarks,
    holistic
)


# ==========================================================
# CONFIGURATION
# ==========================================================

MODEL_FILE = os.path.join(
    MODEL_PATH,
    "word_model_normalized_attention.keras"
)

LABEL_FILE = os.path.join(
    MODEL_PATH,
    "word_labels.npy"
)

FEATURES_PER_FRAME = 225

# IMPORTANT:
# Training uses 30 frames sampled from a video.
# Therefore live camera first collects more frames,
# then samples 30 frames from them.
LIVE_BUFFER_SIZE = 90

PREDICTION_INTERVAL = 5

SMOOTHING_WINDOW = 5

MIN_MARGIN = 5.0

CAMERA_INDEX = 0


# ==========================================================
# LOAD MODEL
# ==========================================================

print()
print("=" * 60)
print("             HANDTALK AI")
print("       LIVE WORD RECOGNITION")
print("=" * 60)

print()
print("Loading model...")

if not os.path.exists(MODEL_FILE):
    print("ERROR: Model not found:")
    print(MODEL_FILE)
    raise SystemExit

if not os.path.exists(LABEL_FILE):
    print("ERROR: Label file not found:")
    print(LABEL_FILE)
    raise SystemExit


model = load_model(
    MODEL_FILE
)

labels = np.load(
    LABEL_FILE,
    allow_pickle=True
)

labels = np.array(
    [str(x) for x in labels]
)


print()
print("Model loaded successfully.")

print(
    "Model outputs :",
    model.output_shape[-1]
)

print(
    "Number labels :",
    len(labels)
)

print(
    "Sequence      :",
    SEQUENCE_LENGTH
)

print(
    "Features/frame:",
    FEATURES_PER_FRAME
)

print(
    "Live buffer   :",
    LIVE_BUFFER_SIZE
)

print()
print("Classes:")

for i, label in enumerate(labels):
    print(
        f"{i:2d} -> {label}"
    )


if model.output_shape[-1] != len(labels):

    print()
    print(
        "ERROR: Model output count and label count "
        "do not match."
    )

    raise SystemExit


# ==========================================================
# SAMPLE LIVE BUFFER
# ==========================================================

def sample_live_buffer(
    buffer
):

    if len(buffer) < SEQUENCE_LENGTH:

        return None


    # Convert deque/list to numpy array

    data = np.asarray(
        buffer,
        dtype=np.float32
    )


    # ------------------------------------------------------
    # Uniformly select 30 frames from the larger buffer.
    #
    # This is the important change.
    # ------------------------------------------------------

    indices = np.linspace(
        0,
        len(data) - 1,
        SEQUENCE_LENGTH
    ).astype(int)


    sampled = data[
        indices
    ]


    if sampled.shape != (
        SEQUENCE_LENGTH,
        FEATURES_PER_FRAME
    ):

        return None


    return sampled


# ==========================================================
# MODEL PREDICTION
# ==========================================================

def predict_sequence(
    sequence
):

    data = np.asarray(
        sequence,
        dtype=np.float32
    )


    if data.shape != (
        SEQUENCE_LENGTH,
        FEATURES_PER_FRAME
    ):

        return None


    if not np.isfinite(data).all():

        return None


    data = np.expand_dims(
        data,
        axis=0
    )


    try:

        probabilities = model.predict(
            data,
            verbose=0
        )[0]

    except Exception as e:

        print(
            "\nPrediction error:",
            e
        )

        return None


    probabilities = np.asarray(
        probabilities,
        dtype=np.float32
    )


    return probabilities


# ==========================================================
# TOP PREDICTIONS
# ==========================================================

def get_top_predictions(
    probabilities,
    count=3
):

    if probabilities is None:
        return []


    indices = np.argsort(
        probabilities
    )[::-1][:count]


    result = []


    for index in indices:

        result.append(
            (
                labels[index],
                float(
                    probabilities[index]
                    * 100
                )
            )
        )


    return result


# ==========================================================
# MEDIAPIPE STATUS
# ==========================================================

def get_detection_status(
    frame
):

    rgb = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2RGB
    )


    results = holistic.process(
        rgb
    )


    pose = (
        results.pose_landmarks
        is not None
    )


    left = (
        results.left_hand_landmarks
        is not None
    )


    right = (
        results.right_hand_landmarks
        is not None
    )


    return (
        pose,
        left,
        right
    )


# ==========================================================
# DRAW UI
# ==========================================================

def draw_ui(
    frame,
    status,
    buffer_length,
    pose_detected,
    left_hand_detected,
    right_hand_detected,
    current_word,
    confidence,
    top_predictions,
    stable_count,
    margin
):

    # ------------------------------------------------------
    # STATUS
    # ------------------------------------------------------

    if status == "RECOGNIZED":

        status_color = (
            0,
            255,
            0
        )

    elif status in (
        "UNCERTAIN",
        "LOW CONFIDENCE"
    ):

        status_color = (
            0,
            255,
            255
        )

    else:

        status_color = (
            255,
            255,
            255
        )


    cv2.putText(
        frame,
        f"Status : {status}",
        (20, 35),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.70,
        status_color,
        2
    )


    # ------------------------------------------------------
    # POSE
    # ------------------------------------------------------

    cv2.putText(
        frame,
        "Pose       : "
        + (
            "YES"
            if pose_detected
            else
            "NO"
        ),
        (20, 68),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.55,
        (
            0,
            255,
            0
        )
        if pose_detected
        else
        (
            0,
            0,
            255
        ),
        2
    )


    # ------------------------------------------------------
    # LEFT HAND
    # ------------------------------------------------------

    cv2.putText(
        frame,
        "Left Hand  : "
        + (
            "YES"
            if left_hand_detected
            else
            "NO"
        ),
        (20, 96),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.55,
        (
            0,
            255,
            0
        )
        if left_hand_detected
        else
        (
            0,
            0,
            255
        ),
        2
    )


    # ------------------------------------------------------
    # RIGHT HAND
    # ------------------------------------------------------

    cv2.putText(
        frame,
        "Right Hand : "
        + (
            "YES"
            if right_hand_detected
            else
            "NO"
        ),
        (20, 124),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.55,
        (
            0,
            255,
            0
        )
        if right_hand_detected
        else
        (
            0,
            0,
            255
        ),
        2
    )


    # ------------------------------------------------------
    # BUFFER
    # ------------------------------------------------------

    cv2.putText(
        frame,
        f"Buffer : "
        f"{buffer_length}/{LIVE_BUFFER_SIZE}",
        (20, 160),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.60,
        (
            255,
            255,
            0
        ),
        2
    )


    # ------------------------------------------------------
    # MODEL SEQUENCE
    # ------------------------------------------------------

    if buffer_length >= LIVE_BUFFER_SIZE:

        sequence_text = (
            "Model sequence : 30/30"
        )

    else:

        sequence_text = (
            "Collecting 90 frames..."
        )


    cv2.putText(
        frame,
        sequence_text,
        (20, 190),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.52,
        (
            255,
            255,
            255
        ),
        2
    )


    # ------------------------------------------------------
    # WORD
    # ------------------------------------------------------

    cv2.putText(
        frame,
        f"Word : {current_word}",
        (20, 230),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.0,
        (
            255,
            0,
            0
        ),
        3
    )


    # ------------------------------------------------------
    # CONFIDENCE
    # ------------------------------------------------------

    cv2.putText(
        frame,
        f"Confidence : "
        f"{confidence:.2f}%",
        (20, 270),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.62,
        (
            0,
            255,
            255
        ),
        2
    )


    # ------------------------------------------------------
    # MARGIN
    # ------------------------------------------------------

    cv2.putText(
        frame,
        f"Top-2 Margin : "
        f"{margin:.2f}%",
        (20, 302),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.55,
        (
            220,
            220,
            220
        ),
        2
    )


    # ------------------------------------------------------
    # STABILITY
    # ------------------------------------------------------

    cv2.putText(
        frame,
        f"Stable : "
        f"{stable_count}/{STABLE_FRAMES}",
        (20, 334),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.55,
        (
            255,
            255,
            255
        ),
        2
    )


    # ------------------------------------------------------
    # TOP 3
    # ------------------------------------------------------

    cv2.putText(
        frame,
        "Top Predictions:",
        (20, 370),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.58,
        (
            255,
            255,
            255
        ),
        2
    )


    y = 400


    for i, (
        word,
        probability
    ) in enumerate(
        top_predictions
    ):

        cv2.putText(
            frame,
            f"{i + 1}. "
            f"{word} : "
            f"{probability:.2f}%",
            (20, y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.53,
            (
                200,
                200,
                255
            ),
            2
        )

        y += 27


    # ------------------------------------------------------
    # HELP
    # ------------------------------------------------------

    cv2.putText(
        frame,
        "Q = Quit     R = Reset",
        (
            20,
            frame.shape[0] - 20
        ),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.55,
        (
            255,
            255,
            255
        ),
        2
    )


# ==========================================================
# MAIN
# ==========================================================

def main():

    cap = cv2.VideoCapture(
        CAMERA_INDEX
    )


    if not cap.isOpened():

        print(
            "ERROR: Could not open camera."
        )

        return


    cap.set(
        cv2.CAP_PROP_FRAME_WIDTH,
        1280
    )

    cap.set(
        cv2.CAP_PROP_FRAME_HEIGHT,
        720
    )


    # ======================================================
    # LIVE BUFFER
    # ======================================================

    live_buffer = deque(
        maxlen=LIVE_BUFFER_SIZE
    )


    # ======================================================
    # PROBABILITY SMOOTHING
    # ======================================================

    probability_history = deque(
        maxlen=SMOOTHING_WINDOW
    )


    # ======================================================
    # STATE
    # ======================================================

    current_word = "Waiting..."

    confidence = 0.0

    margin = 0.0

    top_predictions = []

    status = "WAITING"

    last_prediction_frame = 0

    frame_counter = 0

    last_candidate = None

    stable_count = 0


    print()
    print(
        "========================================"
    )
    print(
        "CAMERA STARTED"
    )
    print(
        "========================================"
    )

    print(
        "Collecting 90 frames before prediction."
    )

    print(
        "Q = Quit"
    )

    print(
        "R = Reset"
    )

    print()


    # ======================================================
    # LOOP
    # ======================================================

    while True:

        ret, frame = cap.read()


        if not ret:

            print(
                "\nERROR: Could not read camera."
            )

            break


        # --------------------------------------------------
        # MIRROR
        # --------------------------------------------------

        frame = cv2.flip(
            frame,
            1
        )


        # --------------------------------------------------
        # LANDMARK EXTRACTION
        # --------------------------------------------------

        try:

            raw_landmarks = (
                extract_landmarks(
                    frame
                )
            )

        except Exception as e:

            raw_landmarks = None

            print(
                "\nLandmark extraction error:",
                e
            )


        # --------------------------------------------------
        # VALIDATE
        # --------------------------------------------------

        landmarks = None


        if raw_landmarks is not None:

            try:

                data = np.asarray(
                    raw_landmarks,
                    dtype=np.float32
                )


                if data.shape == (
                    FEATURES_PER_FRAME,
                ):

                    if np.isfinite(
                        data
                    ).all():

                        landmarks = data

            except Exception:
                landmarks = None


        # --------------------------------------------------
        # ADD VALID FRAME
        # --------------------------------------------------

        if landmarks is not None:

            live_buffer.append(
                landmarks
            )


        frame_counter += 1


        # --------------------------------------------------
        # DETECTION STATUS
        # --------------------------------------------------

        try:

            (
                pose_detected,
                left_hand_detected,
                right_hand_detected
            ) = get_detection_status(
                frame
            )

        except Exception:

            pose_detected = False
            left_hand_detected = False
            right_hand_detected = False


        # ==================================================
        # WAIT UNTIL BUFFER IS FULL
        # ==================================================

        if len(live_buffer) < LIVE_BUFFER_SIZE:

            status = "COLLECTING"

            current_word = (
                "Collecting..."
            )

            confidence = 0.0

            margin = 0.0

            top_predictions = []

            stable_count = 0

            last_candidate = None


        # ==================================================
        # BUFFER READY
        # ==================================================

        else:

            if (
                frame_counter
                -
                last_prediction_frame
                >=
                PREDICTION_INTERVAL
            ):

                # ==========================================
                # SAMPLE 30 FRAMES
                # ==========================================

                sampled_sequence = (
                    sample_live_buffer(
                        live_buffer
                    )
                )


                if sampled_sequence is not None:

                    # ======================================
                    # PREDICT
                    # ======================================

                    probabilities = (
                        predict_sequence(
                            sampled_sequence
                        )
                    )


                    last_prediction_frame = (
                        frame_counter
                    )


                    if probabilities is not None:

                        # ==================================
                        # STORE PROBABILITIES
                        # ==================================

                        probability_history.append(
                            probabilities
                        )


                        # ==================================
                        # AVERAGE TEMPORALLY
                        # ==================================

                        averaged = np.mean(
                            np.stack(
                                probability_history
                            ),
                            axis=0
                        )


                        # ==================================
                        # SORT
                        # ==================================

                        sorted_indices = np.argsort(
                            averaged
                        )[::-1]


                        best_index = int(
                            sorted_indices[0]
                        )


                        second_index = int(
                            sorted_indices[1]
                        )


                        # ==================================
                        # TOP-1
                        # ==================================

                        confidence = (
                            float(
                                averaged[
                                    best_index
                                ]
                            )
                            * 100
                        )


                        # ==================================
                        # TOP-2
                        # ==================================

                        second_confidence = (
                            float(
                                averaged[
                                    second_index
                                ]
                            )
                            * 100
                        )


                        # ==================================
                        # MARGIN
                        # ==================================

                        margin = (
                            confidence
                            -
                            second_confidence
                        )


                        # ==================================
                        # WORD
                        # ==================================

                        predicted_word = (
                            labels[
                                best_index
                            ]
                        )


                        # ==================================
                        # TOP 3
                        # ==================================

                        top_predictions = (
                            get_top_predictions(
                                averaged,
                                3
                            )
                        )


                        # ==================================
                        # ACCEPTANCE
                        # ==================================

                        accepted = (
                            confidence
                            >=
                            CONFIDENCE_THRESHOLD
                            and
                            margin
                            >=
                            MIN_MARGIN
                        )


                        if accepted:

                            # ==============================
                            # STABILITY
                            # ==============================

                            if (
                                predicted_word
                                ==
                                last_candidate
                            ):

                                stable_count += 1

                            else:

                                last_candidate = (
                                    predicted_word
                                )

                                stable_count = 1


                            # ==============================
                            # FINAL PREDICTION
                            # ==============================

                            if (
                                stable_count
                                >=
                                STABLE_FRAMES
                            ):

                                current_word = (
                                    predicted_word
                                )

                                status = (
                                    "RECOGNIZED"
                                )


                        else:

                            status = (
                                "UNCERTAIN"
                            )

                            stable_count = 0

                            last_candidate = None


                        # ==================================
                        # TERMINAL
                        # ==================================

                        print(
                            f"\r"
                            f"Prediction: "
                            f"{predicted_word:<20}"
                            f"Confidence: "
                            f"{confidence:6.2f}%"
                            f" Margin: "
                            f"{margin:6.2f}%",
                            end=""
                        )


        # ==================================================
        # DRAW
        # ==================================================

        draw_ui(
            frame,
            status,
            len(live_buffer),
            pose_detected,
            left_hand_detected,
            right_hand_detected,
            current_word,
            confidence,
            top_predictions,
            stable_count,
            margin
        )


        # ==================================================
        # DISPLAY
        # ==================================================

        cv2.imshow(
            "HandTalk AI - Live Word Recognition",
            frame
        )


        # ==================================================
        # KEY
        # ==================================================

        key = (
            cv2.waitKey(1)
            &
            0xFF
        )


        # ==================================================
        # QUIT
        # ==================================================

        if key == ord("q"):

            break


        # ==================================================
        # RESET
        # ==================================================

        if key == ord("r"):

            live_buffer.clear()

            probability_history.clear()

            current_word = (
                "Waiting..."
            )

            confidence = 0.0

            margin = 0.0

            top_predictions = []

            status = "RESET"

            last_candidate = None

            stable_count = 0

            last_prediction_frame = 0

            frame_counter = 0

            print(
                "\n\nPrediction reset."
            )


    # ======================================================
    # CLEANUP
    # ======================================================

    cap.release()

    cv2.destroyAllWindows()

    print()
    print()
    print(
        "Camera stopped."
    )


# ==========================================================
# ENTRY POINT
# ==========================================================

if __name__ == "__main__":

    main()