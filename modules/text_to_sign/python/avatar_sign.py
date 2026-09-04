import os
import cv2
import numpy as np


# ============================================================
# TEXT → ANIMATED ISL AVATAR
# ============================================================
#
# Existing landmark format:
#
#   Sequence shape : (30, 225)
#
#   0   - 98   : Pose       33 × 3
#   99  - 161  : Left hand  21 × 3
#   162 - 224  : Right hand 21 × 3
#
# ============================================================


# ============================================================
# PROJECT PATH
# ============================================================

PROJECT_ROOT = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "../../.."
    )
)

LANDMARK_ROOT = os.path.join(
    PROJECT_ROOT,
    "Dataset",
    "Words_Landmarks"
)


# ============================================================
# SETTINGS
# ============================================================

SEQUENCE_LENGTH = 30
FEATURES_PER_FRAME = 225

FPS = 20

WINDOW_NAME = "ISL Animated Avatar"


# Internal canvas.
# OpenCV will scale this to the screen.
CANVAS_WIDTH = 1280
CANVAS_HEIGHT = 720


# ============================================================
# SIGN DICTIONARY
# ============================================================

SIGN_DICTIONARY = {

    # -------------------------
    # Greetings
    # -------------------------

    "hello": "Hello",

    "thank you": "Thank you",

    "good morning": "Good Morning",

    "good afternoon": "Good afternoon",

    "good evening": "Good evening",

    "good night": "Good night",

    "how are you": "How are you",

    "pleased": "Pleased",

    "alright": "Alright",


    # -------------------------
    # Animals
    # -------------------------

    "animal": "Animal",

    "bird": "Bird",

    "cat": "Cat",

    "cow": "Cow",

    "dog": "Dog",

    "fish": "Fish",

    "horse": "Horse",

    "mouse": "Mouse",
}


# ============================================================
# NORMALIZE DATASET NAMES
# ============================================================

def normalize_name(text):

    if text is None:
        return ""

    text = str(text).lower().strip()

    text = text.replace(" ", "")
    text = text.replace("_", "")
    text = text.replace("-", "")

    return text


# ============================================================
# NORMALIZE USER INPUT
# ============================================================

def normalize_input(text):

    if text is None:
        return ""

    text = text.lower().strip()

    punctuation = [
        ",",
        ".",
        "!",
        "?",
        ";",
        ":"
    ]

    for char in punctuation:
        text = text.replace(char, " ")

    text = text.replace("_", " ")
    text = text.replace("-", " ")

    while "  " in text:
        text = text.replace("  ", " ")

    return text.strip()


# ============================================================
# FIND SIGN FOLDER
# ============================================================

def find_sign_folder(sign_name):

    target = normalize_name(sign_name)

    if not os.path.exists(LANDMARK_ROOT):

        return None


    for root, dirs, files in os.walk(
        LANDMARK_ROOT
    ):

        for directory in dirs:

            if normalize_name(directory) == target:

                return os.path.join(
                    root,
                    directory
                )


    return None


# ============================================================
# FIND LANDMARK FILE
# ============================================================

def find_npy_for_sign(sign_name):

    folder = find_sign_folder(
        sign_name
    )

    if folder is None:

        return None


    npy_files = []

    for filename in os.listdir(folder):

        if filename.lower().endswith(".npy"):

            npy_files.append(
                os.path.join(
                    folder,
                    filename
                )
            )


    if not npy_files:

        return None


    npy_files.sort(
        key=lambda x: x.lower()
    )


    return npy_files[0]


# ============================================================
# LOAD SEQUENCE
# ============================================================

def load_sequence(npy_path):

    try:

        sequence = np.load(
            npy_path
        )

    except Exception as e:

        print()
        print("ERROR loading landmark file:")
        print(npy_path)
        print(e)

        return None


    sequence = np.asarray(
        sequence,
        dtype=np.float32
    )


    # --------------------------------------------------------
    # Validate dimensions
    # --------------------------------------------------------

    if sequence.ndim != 2:

        print()
        print(
            "ERROR: Invalid landmark sequence."
        )

        print(
            "Shape:",
            sequence.shape
        )

        return None


    # --------------------------------------------------------
    # Validate feature count
    # --------------------------------------------------------

    if sequence.shape[1] != FEATURES_PER_FRAME:

        print()
        print(
            "ERROR: Unexpected landmark feature count."
        )

        print(
            "Expected:",
            FEATURES_PER_FRAME
        )

        print(
            "Found:",
            sequence.shape[1]
        )

        return None


    # --------------------------------------------------------
    # Resize frame count if necessary
    # --------------------------------------------------------

    if sequence.shape[0] != SEQUENCE_LENGTH:

        print(
            f"WARNING: Sequence contains "
            f"{sequence.shape[0]} frames."
        )

        print(
            f"Resizing to {SEQUENCE_LENGTH} frames."
        )

        sequence = resize_sequence(
            sequence,
            SEQUENCE_LENGTH
        )


    return sequence


# ============================================================
# RESIZE SEQUENCE
# ============================================================

def resize_sequence(
    sequence,
    target_length
):

    old_length = sequence.shape[0]


    if old_length == target_length:

        return sequence


    if old_length <= 1:

        return np.repeat(
            sequence,
            target_length,
            axis=0
        )


    old_positions = np.linspace(
        0,
        1,
        old_length
    )

    new_positions = np.linspace(
        0,
        1,
        target_length
    )


    resized = np.zeros(
        (
            target_length,
            sequence.shape[1]
        ),
        dtype=np.float32
    )


    for feature in range(
        sequence.shape[1]
    ):

        resized[:, feature] = np.interp(
            new_positions,
            old_positions,
            sequence[:, feature]
        )


    return resized


# ============================================================
# SPLIT LANDMARKS
# ============================================================

def split_landmarks(frame):

    # Pose
    pose = frame[
        0:99
    ].reshape(
        33,
        3
    )


    # Left hand
    left_hand = frame[
        99:162
    ].reshape(
        21,
        3
    )


    # Right hand
    right_hand = frame[
        162:225
    ].reshape(
        21,
        3
    )


    return (
        pose,
        left_hand,
        right_hand
    )


# ============================================================
# LANDMARK → SCREEN
# ============================================================

def landmark_to_screen(
    point,
    center_x,
    center_y,
    scale
):

    x = float(point[0])
    y = float(point[1])


    screen_x = int(
        center_x + x * scale
    )

    screen_y = int(
        center_y + y * scale
    )


    return (
        screen_x,
        screen_y
    )


# ============================================================
# POSE CONNECTIONS
# ============================================================

POSE_CONNECTIONS = [

    # Face
    (0, 1),
    (1, 2),
    (2, 3),
    (3, 7),

    (0, 4),
    (4, 5),
    (5, 6),
    (6, 8),

    (9, 10),

    # Shoulders
    (11, 12),

    # Left arm
    (11, 13),
    (13, 15),

    (15, 17),
    (15, 19),
    (15, 21),

    # Right arm
    (12, 14),
    (14, 16),

    (16, 18),
    (16, 20),
    (16, 22),

    # Torso
    (11, 23),
    (12, 24),
    (23, 24),

    # Left leg
    (23, 25),
    (25, 27),
    (27, 29),
    (29, 31),

    # Right leg
    (24, 26),
    (26, 28),
    (28, 30),
    (30, 32),
]


# ============================================================
# HAND CONNECTIONS
# ============================================================

HAND_CONNECTIONS = [

    # Thumb
    (0, 1),
    (1, 2),
    (2, 3),
    (3, 4),

    # Index
    (0, 5),
    (5, 6),
    (6, 7),
    (7, 8),

    # Middle
    (0, 9),
    (9, 10),
    (10, 11),
    (11, 12),

    # Ring
    (0, 13),
    (13, 14),
    (14, 15),
    (15, 16),

    # Pinky
    (0, 17),
    (17, 18),
    (18, 19),
    (19, 20),

    # Palm
    (5, 9),
    (9, 13),
    (13, 17),
]


# ============================================================
# DRAW CONNECTIONS
# ============================================================

def draw_connections(
    image,
    landmarks,
    connections,
    center_x,
    center_y,
    scale,
    thickness=3
):

    for start, end in connections:

        if start >= len(landmarks):
            continue

        if end >= len(landmarks):
            continue


        p1 = landmark_to_screen(
            landmarks[start],
            center_x,
            center_y,
            scale
        )


        p2 = landmark_to_screen(
            landmarks[end],
            center_x,
            center_y,
            scale
        )


        cv2.line(
            image,
            p1,
            p2,
            (220, 220, 220),
            thickness,
            cv2.LINE_AA
        )


# ============================================================
# DRAW LANDMARK POINTS
# ============================================================

def draw_points(
    image,
    landmarks,
    center_x,
    center_y,
    scale,
    radius=4
):

    for point in landmarks:

        x, y = landmark_to_screen(
            point,
            center_x,
            center_y,
            scale
        )


        cv2.circle(
            image,
            (x, y),
            radius,
            (255, 255, 255),
            -1,
            cv2.LINE_AA
        )


# ============================================================
# DRAW BODY
# ============================================================

def draw_body(
    image,
    pose,
    center_x,
    center_y,
    scale
):

    draw_connections(
        image,
        pose,
        POSE_CONNECTIONS,
        center_x,
        center_y,
        scale,
        5
    )


    draw_points(
        image,
        pose,
        center_x,
        center_y,
        scale,
        6
    )


# ============================================================
# DRAW HAND
# ============================================================

def draw_hand(
    image,
    hand,
    center_x,
    center_y,
    scale
):

    draw_connections(
        image,
        hand,
        HAND_CONNECTIONS,
        center_x,
        center_y,
        scale,
        3
    )


    draw_points(
        image,
        hand,
        center_x,
        center_y,
        scale,
        4
    )


# ============================================================
# DRAW AVATAR
# ============================================================

def draw_avatar(
    frame,
    sign_name,
    frame_number,
    total_frames
):

    canvas = np.zeros(
        (
            CANVAS_HEIGHT,
            CANVAS_WIDTH,
            3
        ),
        dtype=np.uint8
    )


    # --------------------------------------------------------
    # Split landmarks
    # --------------------------------------------------------

    pose, left_hand, right_hand = (
        split_landmarks(frame)
    )


    # --------------------------------------------------------
    # Avatar center
    # --------------------------------------------------------

    center_x = CANVAS_WIDTH // 2

    center_y = 390


    # --------------------------------------------------------
    # Avatar scale
    # --------------------------------------------------------

    scale = 300


    # --------------------------------------------------------
    # Draw body
    # --------------------------------------------------------

    draw_body(
        canvas,
        pose,
        center_x,
        center_y,
        scale
    )


    # --------------------------------------------------------
    # Draw left hand
    # --------------------------------------------------------

    draw_hand(
        canvas,
        left_hand,
        center_x,
        center_y,
        scale
    )


    # --------------------------------------------------------
    # Draw right hand
    # --------------------------------------------------------

    draw_hand(
        canvas,
        right_hand,
        center_x,
        center_y,
        scale
    )


    # ========================================================
    # TEXT
    # ========================================================

    cv2.putText(
        canvas,
        "TEXT -> INDIAN SIGN LANGUAGE",
        (35, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.0,
        (255, 255, 255),
        2,
        cv2.LINE_AA
    )


    cv2.putText(
        canvas,
        f"Sign: {sign_name}",
        (35, 95),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.95,
        (255, 255, 255),
        2,
        cv2.LINE_AA
    )


    cv2.putText(
        canvas,
        f"Frame: {frame_number + 1}/{total_frames}",
        (35, 135),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (200, 200, 200),
        2,
        cv2.LINE_AA
    )


    cv2.putText(
        canvas,
        "SPACE = Pause / Play",
        (35, CANVAS_HEIGHT - 55),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        (200, 200, 200),
        2,
        cv2.LINE_AA
    )


    cv2.putText(
        canvas,
        "Q / ESC = Quit",
        (35, CANVAS_HEIGHT - 25),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        (200, 200, 200),
        2,
        cv2.LINE_AA
    )


    return canvas


# ============================================================
# CREATE FULLSCREEN WINDOW
# ============================================================

def create_window():

    cv2.namedWindow(
        WINDOW_NAME,
        cv2.WINDOW_NORMAL
    )


    # --------------------------------------------------------
    # Try fullscreen
    # --------------------------------------------------------

    try:

        cv2.setWindowProperty(
            WINDOW_NAME,
            cv2.WND_PROP_FULLSCREEN,
            cv2.WINDOW_FULLSCREEN
        )

    except cv2.error:

        pass


# ============================================================
# PLAY ONE SIGN
# ============================================================

def play_sign(sign_name):

    npy_path = find_npy_for_sign(
        sign_name
    )


    if npy_path is None:

        print()
        print(
            f"ERROR: No landmark file found for: "
            f"{sign_name}"
        )

        return True


    print()
    print(
        "Playing:"
    )

    print(
        f"  Sign: {sign_name}"
    )

    print(
        f"  NPY: {npy_path}"
    )


    sequence = load_sequence(
        npy_path
    )


    if sequence is None:

        return True


    total_frames = len(
        sequence
    )


    if total_frames == 0:

        print(
            "ERROR: Empty landmark sequence."
        )

        return True


    # --------------------------------------------------------
    # Create window
    # --------------------------------------------------------

    create_window()


    frame_number = 0

    paused = False


    delay = max(
        1,
        int(1000 / FPS)
    )


    while True:

        # ----------------------------------------------------
        # Check if window still exists
        # ----------------------------------------------------

        try:

            visible = cv2.getWindowProperty(
                WINDOW_NAME,
                cv2.WND_PROP_VISIBLE
            )

            if visible < 1:

                cv2.destroyWindow(
                    WINDOW_NAME
                )

                return True

        except cv2.error:

            return True


        # ----------------------------------------------------
        # Current frame
        # ----------------------------------------------------

        frame = sequence[
            frame_number
        ]


        avatar = draw_avatar(
            frame,
            sign_name,
            frame_number,
            total_frames
        )


        cv2.imshow(
            WINDOW_NAME,
            avatar
        )


        # ----------------------------------------------------
        # Keyboard
        # ----------------------------------------------------

        if paused:

            key = cv2.waitKey(
                100
            ) & 0xFF

        else:

            key = cv2.waitKey(
                delay
            ) & 0xFF


        # ----------------------------------------------------
        # QUIT
        # ----------------------------------------------------

        if key in (
            ord("q"),
            ord("Q"),
            27
        ):

            cv2.destroyWindow(
                WINDOW_NAME
            )

            return False


        # ----------------------------------------------------
        # SPACE
        # ----------------------------------------------------

        if key == 32:

            paused = not paused

            continue


        # ----------------------------------------------------
        # PAUSED FRAME CONTROL
        # ----------------------------------------------------

        if paused:

            if key in (
                ord("d"),
                ord("D")
            ):

                frame_number += 1

                if frame_number >= total_frames:

                    frame_number = 0


            elif key in (
                ord("a"),
                ord("A")
            ):

                frame_number -= 1

                if frame_number < 0:

                    frame_number = (
                        total_frames - 1
                    )


            continue


        # ----------------------------------------------------
        # NEXT FRAME
        # ----------------------------------------------------

        frame_number += 1


        # ----------------------------------------------------
        # SIGN COMPLETE
        # ----------------------------------------------------

        if frame_number >= total_frames:

            frame_number = (
                total_frames - 1
            )


            final_avatar = draw_avatar(
                sequence[frame_number],
                sign_name,
                frame_number,
                total_frames
            )


            cv2.imshow(
                WINDOW_NAME,
                final_avatar
            )


            # Keep final frame visible briefly
            key = cv2.waitKey(
                300
            ) & 0xFF


            if key in (
                ord("q"),
                ord("Q"),
                27
            ):

                cv2.destroyWindow(
                    WINDOW_NAME
                )

                return False


            # ------------------------------------------------
            # Normal completion
            # ------------------------------------------------

            cv2.destroyWindow(
                WINDOW_NAME
            )

            return True


# ============================================================
# FIND LONGEST PHRASE
# ============================================================

def find_longest_phrase(
    words,
    start
):

    phrases = sorted(
        SIGN_DICTIONARY.keys(),
        key=lambda x: len(
            x.split()
        ),
        reverse=True
    )


    for phrase in phrases:

        phrase_words = phrase.split()

        phrase_length = len(
            phrase_words
        )


        if (
            start + phrase_length
            >
            len(words)
        ):

            continue


        candidate = words[
            start:
            start + phrase_length
        ]


        if candidate == phrase_words:

            return (
                phrase,
                phrase_length
            )


    return None


# ============================================================
# TEXT → SIGN SEQUENCE
# ============================================================

def convert_text_to_signs(
    text
):

    text = normalize_input(
        text
    )


    if not text:

        return []


    words = text.split()


    signs = []

    index = 0


    while index < len(words):

        match = find_longest_phrase(
            words,
            index
        )


        if match:

            phrase, length = match

            signs.append(
                SIGN_DICTIONARY[
                    phrase
                ]
            )

            index += length

            continue


        print()
        print(
            f"WARNING: No sign mapping for "
            f"'{words[index]}'"
        )


        index += 1


    return signs


# ============================================================
# SHOW AVAILABLE SIGNS
# ============================================================

def show_available_signs():

    print()
    print(
        "=" * 60
    )

    print(
        "AVAILABLE SIGNS"
    )

    print(
        "=" * 60
    )


    if not os.path.exists(
        LANDMARK_ROOT
    ):

        print(
            "Landmark directory not found:"
        )

        print(
            LANDMARK_ROOT
        )

        return


    found = []


    for root, dirs, files in os.walk(
        LANDMARK_ROOT
    ):

        for directory in dirs:

            folder = os.path.join(
                root,
                directory
            )


            try:

                files_inside = os.listdir(
                    folder
                )

            except OSError:

                continue


            has_npy = any(
                filename.lower().endswith(".npy")
                for filename in files_inside
            )


            if has_npy:

                found.append(
                    directory
                )


    for name in sorted(
        set(found),
        key=lambda x: x.lower()
    ):

        print(
            "✓",
            name
        )


    print(
        "=" * 60
    )


# ============================================================
# MAIN
# ============================================================

def main():

    print()
    print(
        "=" * 60
    )

    print(
        "       TEXT → ANIMATED ISL AVATAR"
    )

    print(
        "=" * 60
    )

    print()

    print(
        "Landmark directory:"
    )

    print(
        LANDMARK_ROOT
    )


    if not os.path.exists(
        LANDMARK_ROOT
    ):

        print()
        print(
            "ERROR: Landmark directory does not exist."
        )

        return


    show_available_signs()


    print()
    print(
        "Commands:"
    )

    print(
        "  signs → show available signs"
    )

    print(
        "  exit  → close program"
    )

    print()
    print(
        "Avatar controls:"
    )

    print(
        "  SPACE → pause/play"
    )

    print(
        "  A     → previous frame"
    )

    print(
        "  D     → next frame"
    )

    print(
        "  Q/ESC → stop animation"
    )


    while True:

        print()


        try:

            text = input(
                "Enter word/sentence: "
            )


        except KeyboardInterrupt:

            print()
            print(
                "Program stopped."
            )

            break


        except EOFError:

            print()
            break


        # ----------------------------------------------------
        # EXIT
        # ----------------------------------------------------

        if text.strip().lower() == "exit":

            break


        # ----------------------------------------------------
        # SHOW SIGNS
        # ----------------------------------------------------

        if text.strip().lower() == "signs":

            show_available_signs()

            continue


        if not text.strip():

            continue


        # ----------------------------------------------------
        # Convert input
        # ----------------------------------------------------

        signs = convert_text_to_signs(
            text
        )


        if not signs:

            print()
            print(
                "No known signs found."
            )

            continue


        # ----------------------------------------------------
        # Display sequence
        # ----------------------------------------------------

        print()
        print(
            "=" * 60
        )

        print(
            "SIGN SEQUENCE"
        )

        print(
            "=" * 60
        )


        for number, sign in enumerate(
            signs,
            1
        ):

            print(
                f"{number}. {sign}"
            )


        print(
            "=" * 60
        )


        # ----------------------------------------------------
        # Play signs
        # ----------------------------------------------------

        should_continue = True


        for sign in signs:

            should_continue = play_sign(
                sign
            )


            if not should_continue:

                print()
                print(
                    "Avatar stopped by user."
                )

                break


    cv2.destroyAllWindows()


# ============================================================
# START
# ============================================================

if __name__ == "__main__":

    main()