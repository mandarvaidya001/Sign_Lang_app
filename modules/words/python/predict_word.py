import os
import time
import cv2
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

# Predict every N camera frames
PREDICTION_INTERVAL = 3

# Number of recent predictions used for smoothing
SMOOTHING_WINDOW = 5

# Minimum confidence before accepting prediction
LIVE_CONFIDENCE_THRESHOLD = CONFIDENCE_THRESHOLD

# Time to keep recognized word on screen
DISPLAY_TIME = 2.0


# ==========================================================
# LOAD MODEL
# ==========================================================

print("\n========================================")
print("        HANDTALK AI")
print("    LIVE WORD RECOGNITION")
print("========================================")

if not os.path.exists(MODEL_FILE):

    print("\nERROR: Model file not found:")
    print(MODEL_FILE)
    exit()


if not os.path.exists(LABEL_FILE):

    print("\nERROR: Label file not found:")
    print(LABEL_FILE)
    exit()


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


print("\nModel Loaded Successfully")
print(
    "Model:",
    os.path.basename(MODEL_FILE)
)

print(
    "Classes:",
    labels
)

print(
    "Number of Classes:",
    len(labels)
)

print(
    "Sequence Length:",
    SEQUENCE_LENGTH
)

print(
    "Features / Frame:",
    FEATURES_PER_FRAME
)

print("========================================\n")


# ==========================================================
# PREDICTION FUNCTION
# ==========================================================

def predict_sequence(sequence):

    data = np.asarray(
        sequence,
        dtype=np.float32
    )

    expected_shape = (
        SEQUENCE_LENGTH,
        FEATURES_PER_FRAME
    )

    if data.shape != expected_shape:

        print(
            "Invalid sequence shape:",
            data.shape
        )

        return (
            None,
            0.0,
            None
        )


    # Add batch dimension
    #
    # (30,225)
    #     ↓
    # (1,30,225)

    data = np.expand_dims(
        data,
        axis=0
    )


    probabilities = model.predict(
        data,
        verbose=0
    )[0]


    predicted_index = int(
        np.argmax(probabilities)
    )


    confidence = (
        float(
            probabilities[predicted_index]
        ) * 100
    )


    predicted_word = labels[
        predicted_index
    ]


    return (
        predicted_word,
        confidence,
        probabilities
    )


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


    results = []

    for index in indices:

        results.append(
            (
                labels[index],
                float(
                    probabilities[index] * 100
                )
            )
        )


    return results


# ==========================================================
# PRINT ALL CLASS PROBABILITIES
# ==========================================================

def print_all_probabilities(
    probabilities
):

    if probabilities is None:

        return


    print(
        "\n=============================="
    )

    print(
        "LIVE CLASS PROBABILITIES"
    )

    print(
        "=============================="
    )


    indices = np.argsort(
        probabilities
    )[::-1]


    for index in indices:

        print(
            f"{labels[index]:10s} : "
            f"{probabilities[index] * 100:6.2f}%"
        )


    print(
        "=============================="
    )


# ==========================================================
# LANDMARK STATUS
# ==========================================================

def get_landmark_status(frame):

    """
    Used only for displaying whether
    pose/hands are currently visible.

    It does NOT control sequence collection.
    """

    rgb = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2RGB
    )


    results = holistic.process(
        rgb
    )


    pose_detected = (
        results.pose_landmarks
        is not None
    )


    left_hand_detected = (
        results.left_hand_landmarks
        is not None
    )


    right_hand_detected = (
        results.right_hand_landmarks
        is not None
    )


    return (
        pose_detected,
        left_hand_detected,
        right_hand_detected
    )


# ==========================================================
# DRAW UI
# ==========================================================

def draw_ui(
    frame,
    status,
    frames,
    pose_detected,
    left_hand_detected,
    right_hand_detected,
    current_word,
    confidence,
    top_predictions,
    stable_count
):

    # ======================================================
    # STATUS
    # ======================================================

    cv2.putText(
        frame,
        f"Status : {status}",
        (20, 35),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.75,
        (0, 255, 0),
        2
    )


    # ======================================================
    # LANDMARK STATUS
    # ======================================================

    pose_color = (
        (0, 255, 0)
        if pose_detected
        else (0, 0, 255)
    )

    left_color = (
        (0, 255, 0)
        if left_hand_detected
        else (0, 0, 255)
    )

    right_color = (
        (0, 255, 0)
        if right_hand_detected
        else (0, 0, 255)
    )


    cv2.putText(
        frame,
        f"Pose       : "
        f"{'YES' if pose_detected else 'NO'}",
        (20, 70),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.58,
        pose_color,
        2
    )


    cv2.putText(
        frame,
        f"Left Hand  : "
        f"{'YES' if left_hand_detected else 'NO'}",
        (20, 98),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.58,
        left_color,
        2
    )


    cv2.putText(
        frame,
        f"Right Hand : "
        f"{'YES' if right_hand_detected else 'NO'}",
        (20, 126),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.58,
        right_color,
        2
    )


    # ======================================================
    # FRAME BUFFER
    # ======================================================

    cv2.putText(
        frame,
        f"Frames : "
        f"{frames}/{SEQUENCE_LENGTH}",
        (20, 165),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.68,
        (255, 255, 0),
        2
    )


    # ======================================================
    # WORD
    # ======================================================

    cv2.putText(
        frame,
        f"Word : {current_word}",
        (20, 210),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.05,
        (255, 0, 0),
        3
    )


    # ======================================================
    # CONFIDENCE
    # ======================================================

    cv2.putText(
        frame,
        f"Confidence : "
        f"{confidence:.2f}%",
        (20, 250),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.68,
        (0, 255, 255),
        2
    )


    # ======================================================
    # STABILITY
    # ======================================================

    cv2.putText(
        frame,
        f"Stable : "
        f"{stable_count}/{STABLE_FRAMES}",
        (20, 285),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.62,
        (255, 255, 255),
        2
    )


    # ======================================================
    # TOP 3
    # ======================================================

    cv2.putText(
        frame,
        "Top Predictions:",
        (20, 325),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.62,
        (255, 255, 255),
        2
    )


    y = 355


    for i, (
        word,
        probability
    ) in enumerate(top_predictions):

        cv2.putText(
            frame,
            f"{i + 1}. "
            f"{word} : "
            f"{probability:.2f}%",
            (20, y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.58,
            (200, 200, 255),
            2
        )

        y += 28


    # ======================================================
    # HELP
    # ======================================================

    cv2.putText(
        frame,
        "Q = Quit",
        (20, 455),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.58,
        (255, 255, 255),
        2
    )


# ==========================================================
# MAIN
# ==========================================================

def main():

    cap = cv2.VideoCapture(
        0
    )


    if not cap.isOpened():

        print(
            "\nERROR: Could not open camera."
        )

        return


    # ======================================================
    # CAMERA SETTINGS
    # ======================================================

    cap.set(
        cv2.CAP_PROP_FRAME_WIDTH,
        1280
    )

    cap.set(
        cv2.CAP_PROP_FRAME_HEIGHT,
        720
    )


    # ======================================================
    # SEQUENCE BUFFER
    # ======================================================

    sequence = deque(
        maxlen=SEQUENCE_LENGTH
    )


    # ======================================================
    # PREDICTION HISTORY
    # ======================================================

    prediction_history = deque(
        maxlen=SMOOTHING_WINDOW
    )


    # ======================================================
    # VARIABLES
    # ======================================================

    current_word = "Waiting..."

    confidence = 0.0

    stable_count = 0

    last_prediction = ""

    top_predictions = []

    frame_counter = 0

    last_prediction_frame = 0

    status = "WAITING"

    display_until = 0


    # ======================================================
    # CAMERA LOOP
    # ======================================================

    while True:

        ret, frame = cap.read()


        if not ret:

            print(
                "Could not read camera frame."
            )

            break


        # ==================================================
        # MIRROR CAMERA
        # ==================================================

        frame = cv2.flip(
            frame,
            1
        )


        # ==================================================
        # EXTRACT NORMALIZED LANDMARKS
        # ==================================================

        landmarks = extract_landmarks(
            frame
        )


        # ==================================================
        # LANDMARK STATUS
        # ==================================================

        (
            pose_detected,
            left_hand_detected,
            right_hand_detected
        ) = get_landmark_status(
            frame
        )


        # ==================================================
        # ADD FRAME
        #
        # We DO NOT require both hands.
        #
        # Pose + one hand is valid.
        # ==================================================

        valid_frame = (
            pose_detected
            and (
                left_hand_detected
                or right_hand_detected
            )
        )


        if valid_frame:

            sequence.append(
                landmarks
            )


        frame_counter += 1


        # ==================================================
        # COLLECTING
        # ==================================================

        if len(sequence) < SEQUENCE_LENGTH:

            status = "COLLECTING"

            current_word = (
                "Collecting..."
            )

            confidence = 0.0


        # ==================================================
        # PREDICTION
        # ==================================================

        else:

            if (
                frame_counter
                - last_prediction_frame
                >= PREDICTION_INTERVAL
            ):

                (
                    predicted_word,
                    new_confidence,
                    probabilities
                ) = predict_sequence(
                    list(sequence)
                )


                last_prediction_frame = (
                    frame_counter
                )


                if predicted_word is not None:

                    confidence = (
                        new_confidence
                    )


                    top_predictions = (
                        get_top_predictions(
                            probabilities,
                            3
                        )
                    )


                    # ==================================
                    # PRINT PROBABILITIES
                    # ==================================

                    print_all_probabilities(
                        probabilities
                    )


                    # ==================================
                    # CONFIDENCE FILTER
                    # ==================================

                    if (
                        confidence
                        >= LIVE_CONFIDENCE_THRESHOLD
                    ):

                        prediction_history.append(
                            predicted_word
                        )


                        # ==================================
                        # TEMPORAL MAJORITY VOTE
                        # ==================================

                        if len(
                            prediction_history
                        ) >= 3:

                            counts = {}

                            for word in (
                                prediction_history
                            ):

                                counts[word] = (
                                    counts.get(
                                        word,
                                        0
                                    ) + 1
                                )


                            stable_word = max(
                                counts,
                                key=counts.get
                            )


                            stable_votes = (
                                counts[
                                    stable_word
                                ]
                            )


                            # ==================================
                            # STABLE PREDICTION
                            # ==================================

                            if (
                                stable_word
                                == last_prediction
                            ):

                                stable_count += 1

                            else:

                                last_prediction = (
                                    stable_word
                                )

                                stable_count = 1


                            if (
                                stable_count
                                >= STABLE_FRAMES
                            ):

                                current_word = (
                                    stable_word
                                )

                                status = (
                                    "RECOGNIZED"
                                )

                                display_until = (
                                    time.time()
                                    + DISPLAY_TIME
                                )


                                print(
                                    "\n################################"
                                )

                                print(
                                    " FINAL LIVE PREDICTION"
                                )

                                print(
                                    " Word:",
                                    stable_word
                                )

                                print(
                                    f" Confidence:"
                                    f" {confidence:.2f}%"
                                )

                                print(
                                    "################################"
                                )


                        else:

                            status = (
                                "ANALYZING"
                            )


                    else:

                        status = (
                            "LOW CONFIDENCE"
                        )

                        stable_count = 0

                        last_prediction = ""


                        # Don't allow an old
                        # prediction to dominate.

                        prediction_history.clear()


        # ==================================================
        # RESET DISPLAY
        # ==================================================

        if (
            display_until > 0
            and time.time()
            > display_until
        ):

            current_word = (
                "Recognizing..."
            )

            display_until = 0


        # ==================================================
        # DRAW
        # ==================================================

        draw_ui(

            frame,

            status,

            len(sequence),

            pose_detected,

            left_hand_detected,

            right_hand_detected,

            current_word,

            confidence,

            top_predictions,

            stable_count

        )


        # ==================================================
        # DISPLAY CAMERA
        # ==================================================

        cv2.imshow(
            "HandTalk AI - "
            "Live Word Recognition",
            frame
        )


        # ==================================================
        # QUIT
        # ==================================================

        key = (
            cv2.waitKey(1)
            & 0xFF
        )


        if key == ord("q"):

            break


    # ======================================================
    # CLEANUP
    # ======================================================

    cap.release()

    cv2.destroyAllWindows()


# ==========================================================
# ENTRY POINT
# ==========================================================

if __name__ == "__main__":

    main()