import os
import cv2
import re


# ============================================================
# TEXT → SIGN LANGUAGE
# ============================================================
#
# This program:
#
#   User text
#       ↓
#   Phrase matching
#       ↓
#   Sign folder
#       ↓
#   Any video inside that folder
#       ↓
#   Play sign
#
# Example:
#
#   "Hello"
#       → Hello
#
#   "Good Morning"
#       → Good Morning
#
#   "How are you"
#       → How are you
#
#   "Hello, how are you?"
#       → Hello
#       → How are you
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


SIGN_FOLDER = os.path.join(
    PROJECT_ROOT,
    "Dataset",
    "Sign_Output"
)


# ============================================================
# SUPPORTED VIDEO FORMATS
# ============================================================

VIDEO_EXTENSIONS = (
    ".mp4",
    ".mov",
    ".avi",
    ".mkv",
    ".webm",
    ".MP4",
    ".MOV",
    ".AVI",
    ".MKV",
    ".WEBM"
)


# ============================================================
# SIGN DICTIONARY
# ============================================================
#
# LEFT SIDE:
#   What the user types
#
# RIGHT SIDE:
#   Actual folder name inside Sign_Output
#
# The right side should match your folder names.
#
# However, the program ignores:
#
#   spaces
#   underscores
#   hyphens
#   capitalization
#
# while searching.
#
# ============================================================

SIGN_DICTIONARY = {

    # --------------------------------------------------------
    # GREETINGS
    # --------------------------------------------------------

    "hello":
        "Hello",

    "thank you":
        "Thank you",

    "good morning":
        "Good Morning",

    "good afternoon":
        "Good afternoon",

    "good evening":
        "Good evening",

    "good night":
        "Good night",

    "how are you":
        "How are you",

    "pleased":
        "Pleased",

    "alright":
        "Alright",


    # --------------------------------------------------------
    # ANIMALS
    # --------------------------------------------------------

    "animal":
        "Animal",

    "bird":
        "Bird",

    "cat":
        "Cat",

    "cow":
        "Cow",

    "dog":
        "Dog",

    "fish":
        "Fish",

    "horse":
        "Horse",

    "mouse":
        "Mouse"
}


# ============================================================
# NORMALIZE TEXT FOR COMPARISON
# ============================================================
#
# Examples:
#
# Good Morning
# good morning
# Good_Morning
# good-morning
# GOOD MORNING
#
# ALL become:
#
# goodmorning
#
# ============================================================

def normalize_for_comparison(text):

    if text is None:

        return ""


    text = str(text)

    text = text.lower()

    text = text.strip()


    # Remove spaces

    text = text.replace(
        " ",
        ""
    )


    # Remove underscores

    text = text.replace(
        "_",
        ""
    )


    # Remove hyphens

    text = text.replace(
        "-",
        ""
    )


    return text


# ============================================================
# NORMALIZE USER INPUT
# ============================================================

def normalize_input(text):

    if text is None:

        return ""


    text = text.lower()


    # --------------------------------------------------------
    # Replace punctuation with spaces.
    #
    # We DON'T simply remove punctuation because:
    #
    # "hello,how"
    #
    # should become:
    #
    # "hello how"
    # --------------------------------------------------------

    text = re.sub(
        r"[^\w\s-]",
        " ",
        text
    )


    # Convert underscores to spaces

    text = text.replace(
        "_",
        " "
    )


    # Convert hyphens to spaces

    text = text.replace(
        "-",
        " "
    )


    # Remove extra spaces

    text = re.sub(
        r"\s+",
        " ",
        text
    )


    return text.strip()


# ============================================================
# FIND ACTUAL SIGN FOLDER
# ============================================================
#
# This searches the REAL folders in:
#
# Dataset/Sign_Output/
#
# Therefore:
#
# "Good Morning"
#
# can find:
#
# Good Morning
# Good_Morning
# Good-Morning
# GOOD MORNING
#
# ============================================================

def find_sign_folder(
    sign_name
):

    if not os.path.exists(
        SIGN_FOLDER
    ):

        return None


    target = normalize_for_comparison(
        sign_name
    )


    try:

        folders = os.listdir(
            SIGN_FOLDER
        )

    except Exception as e:

        print(
            f"ERROR reading sign folder: {e}"
        )

        return None


    for folder_name in folders:

        folder_path = os.path.join(
            SIGN_FOLDER,
            folder_name
        )


        if not os.path.isdir(
            folder_path
        ):

            continue


        normalized_folder = (
            normalize_for_comparison(
                folder_name
            )
        )


        if normalized_folder == target:

            return folder_path


    return None


# ============================================================
# FIND ANY VIDEO INSIDE SIGN FOLDER
# ============================================================
#
# Video filename does NOT matter.
#
# Example:
#
# Hello/
#     MVI_1234.MOV
#
# works.
#
# Hello/
#     hello.mp4
#
# also works.
#
# ============================================================

def find_sign_video(
    sign_name
):

    folder = find_sign_folder(
        sign_name
    )


    if folder is None:

        return None


    try:

        files = os.listdir(
            folder
        )

    except Exception as e:

        print(
            f"ERROR reading folder: {folder}"
        )

        print(e)

        return None


    videos = []


    for filename in files:

        filepath = os.path.join(
            folder,
            filename
        )


        if not os.path.isfile(
            filepath
        ):

            continue


        if filename.lower().endswith(
            (
                ".mp4",
                ".mov",
                ".avi",
                ".mkv",
                ".webm"
            )
        ):

            videos.append(
                filepath
            )


    if not videos:

        return None


    videos.sort(
        key=lambda x: x.lower()
    )


    # --------------------------------------------------------
    # Use first available video.
    # --------------------------------------------------------

    return videos[0]


# ============================================================
# BUILD AVAILABLE SIGN FOLDERS
# ============================================================
#
# This is useful for debugging.
#
# ============================================================

def get_available_sign_folders():

    available = {}


    if not os.path.exists(
        SIGN_FOLDER
    ):

        return available


    try:

        folders = os.listdir(
            SIGN_FOLDER
        )

    except Exception:

        return available


    for folder_name in folders:

        folder_path = os.path.join(
            SIGN_FOLDER,
            folder_name
        )


        if not os.path.isdir(
            folder_path
        ):

            continue


        normalized = (
            normalize_for_comparison(
                folder_name
            )
        )


        available[
            normalized
        ] = folder_name


    return available


# ============================================================
# CHECK WHETHER SIGN EXISTS
# ============================================================

def sign_exists(
    sign_name
):

    return (
        find_sign_folder(
            sign_name
        )
        is not None
    )


# ============================================================
# FIND SIGN VIDEO
# ============================================================
#
# This function also prints useful debugging information.
#
# ============================================================

def get_video_for_sign(
    sign_name
):

    folder = find_sign_folder(
        sign_name
    )


    if folder is None:

        print()
        print(
            f"WARNING: Sign folder not found:"
        )

        print(
            f"  {sign_name}"
        )

        return None


    video = find_sign_video(
        sign_name
    )


    if video is None:

        print()
        print(
            f"WARNING: No video found inside:"
        )

        print(
            f"  {folder}"
        )

        return None


    return video


# ============================================================
# FIND LONGEST MATCHING PHRASE
# ============================================================
#
# This is the most important part for sentences.
#
# Example:
#
# Input:
#
# "Hello how are you"
#
# The program checks:
#
# "how are you"
#
# before:
#
# "how"
#
# so the complete phrase is preserved.
#
# ============================================================

def find_longest_phrase(
    words,
    start_index
):

    if start_index >= len(
        words
    ):

        return None


    remaining_words = words[
        start_index:
    ]


    # --------------------------------------------------------
    # Sort phrases by number of words.
    #
    # Longest phrase first.
    # --------------------------------------------------------

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
            start_index
            +
            phrase_length
            >
            len(words)
        ):

            continue


        candidate = words[
            start_index:
            start_index + phrase_length
        ]


        if candidate == phrase_words:

            return (
                phrase,
                phrase_length
            )


    return None


# ============================================================
# CONVERT TEXT TO SIGNS
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


    i = 0


    while i < len(words):


        # ----------------------------------------------------
        # Find longest possible phrase.
        # ----------------------------------------------------

        match = find_longest_phrase(
            words,
            i
        )


        if match is not None:

            phrase, length = match


            sign_folder_name = (
                SIGN_DICTIONARY[
                    phrase
                ]
            )


            signs.append(
                {
                    "input": phrase,
                    "sign": sign_folder_name
                }
            )


            i += length

            continue


        # ----------------------------------------------------
        # No dictionary match.
        # ----------------------------------------------------

        unknown_word = words[i]


        signs.append(
            {
                "input": unknown_word,
                "sign": None
            }
        )


        i += 1


    return signs


# ============================================================
# DISPLAY SIGN SEQUENCE
# ============================================================

def print_sign_sequence(
    signs
):

    print()
    print(
        "=" * 60
    )

    print(
        "             SIGN SEQUENCE"
    )

    print(
        "=" * 60
    )


    for index, item in enumerate(
        signs,
        start=1
    ):

        input_text = item[
            "input"
        ]

        sign = item[
            "sign"
        ]


        if sign is None:

            print(
                f"{index}. "
                f"{input_text}"
                f" → [NO SIGN]"
            )

        else:

            print(
                f"{index}. "
                f"{input_text}"
                f" → {sign}"
            )


    print(
        "=" * 60
    )


# ============================================================
# PLAY ONE SIGN VIDEO
# ============================================================

def play_sign_video(
    video_path,
    sign_name
):

    print()
    print(
        f"Playing sign: {sign_name}"
    )

    print(
        f"Video: {video_path}"
    )


    cap = cv2.VideoCapture(
        video_path
    )


    if not cap.isOpened():

        print(
            "ERROR: Could not open video."
        )

        return False


    fps = cap.get(
        cv2.CAP_PROP_FPS
    )


    if fps <= 0:

        fps = 25


    delay = max(
        1,
        int(
            1000 / fps
        )
    )


    window_name = (
        f"ISL Sign - {sign_name}"
    )


    while True:

        ret, frame = cap.read()


        if not ret:

            break


        # ----------------------------------------------------
        # Resize large videos for display.
        # ----------------------------------------------------

        max_width = 1100

        max_height = 700


        height, width = (
            frame.shape[:2]
        )


        scale = min(
            max_width / width,
            max_height / height,
            1.0
        )


        if scale < 1.0:

            frame = cv2.resize(
                frame,
                (
                    int(
                        width * scale
                    ),
                    int(
                        height * scale
                    )
                )
            )


        # ----------------------------------------------------
        # Display sign name.
        # ----------------------------------------------------

        cv2.putText(
            frame,
            f"ISL: {sign_name}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            (0, 255, 0),
            2
        )


        cv2.putText(
            frame,
            "Q / ESC = Stop",
            (20, 75),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2
        )


        cv2.imshow(
            window_name,
            frame
        )


        key = (
            cv2.waitKey(
                delay
            )
            &
            0xFF
        )


        if key == ord("q"):

            cap.release()

            cv2.destroyWindow(
                window_name
            )

            return False


        if key == 27:

            cap.release()

            cv2.destroyWindow(
                window_name
            )

            return False


    cap.release()


    cv2.destroyWindow(
        window_name
    )


    return True


# ============================================================
# PLAY SIGN SEQUENCE
# ============================================================

def play_sign_sequence(
    signs
):

    if not signs:

        print(
            "No signs found."
        )

        return


    print_sign_sequence(
        signs
    )


    for item in signs:

        sign_name = item[
            "sign"
        ]


        # ----------------------------------------------------
        # Unknown word
        # ----------------------------------------------------

        if sign_name is None:

            print()
            print(
                f"Skipping unknown word:"
                f" {item['input']}"
            )

            continue


        # ----------------------------------------------------
        # Find corresponding video
        # ----------------------------------------------------

        video = get_video_for_sign(
            sign_name
        )


        if video is None:

            continue


        # ----------------------------------------------------
        # Play video
        # ----------------------------------------------------

        should_continue = (
            play_sign_video(
                video,
                sign_name
            )
        )


        if not should_continue:

            break


# ============================================================
# SHOW AVAILABLE SIGNS
# ============================================================

def show_available_signs():

    print()
    print(
        "=" * 60
    )

    print(
        "             AVAILABLE SIGNS"
    )

    print(
        "=" * 60
    )


    folders = get_available_sign_folders()


    if not folders:

        print(
            "No sign folders found."
        )

        print()
        print(
            "Expected location:"
        )

        print(
            SIGN_FOLDER
        )

        return


    # --------------------------------------------------------
    # Show actual folder names.
    # --------------------------------------------------------

    actual_names = sorted(
        folders.values(),
        key=lambda x: x.lower()
    )


    for name in actual_names:

        video = find_sign_video(
            name
        )


        if video is not None:

            print(
                f"✓ {name}"
            )

        else:

            print(
                f"⚠ {name}"
                f"  [no video]"
            )


    print(
        "=" * 60
    )


# ============================================================
# TEST DICTIONARY
# ============================================================

def test_dictionary():

    print()
    print(
        "=" * 60
    )

    print(
        "             DICTIONARY TEST"
    )

    print(
        "=" * 60
    )


    test_phrases = [

        "Hello",

        "hello",

        "HELLO",

        "Good Morning",

        "Good_Morning",

        "good-morning",

        "GOOD MORNING",

        "How are you",

        "How_are_you",

        "how-are-you",

        "Thank you",

        "Thank_you",

        "thank-you"

    ]


    for text in test_phrases:

        signs = convert_text_to_signs(
            text
        )


        print()

        print(
            f"Input: {text}"
        )

        print(
            "Result:",
            signs
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
        "        TEXT → INDIAN SIGN LANGUAGE"
    )

    print(
        "=" * 60
    )


    print()
    print(
        "Sign database:"
    )

    print(
        SIGN_FOLDER
    )


    # --------------------------------------------------------
    # CHECK SIGN DATABASE
    # --------------------------------------------------------

    if not os.path.exists(
        SIGN_FOLDER
    ):

        print()
        print(
            "ERROR:"
        )

        print(
            "Sign_Output folder does not exist."
        )

        print()
        print(
            "Create:"
        )

        print(
            SIGN_FOLDER
        )

        return


    # --------------------------------------------------------
    # Show available folders
    # --------------------------------------------------------

    show_available_signs()


    # --------------------------------------------------------
    # Commands
    # --------------------------------------------------------

    print()
    print(
        "Commands:"
    )

    print(
        "  exit   → Close program"
    )

    print(
        "  signs  → Show available signs"
    )

    print(
        "  test   → Test phrase matching"
    )


    # ========================================================
    # INPUT LOOP
    # ========================================================

    while True:

        print()

        try:

            text = input(
                "Enter word/sentence: "
            )

        except KeyboardInterrupt:

            print()
            print(
                "\nProgram stopped."
            )

            break

        except EOFError:

            print()

            break


        # ----------------------------------------------------
        # EXIT
        # ----------------------------------------------------

        if text.lower().strip() == "exit":

            break


        # ----------------------------------------------------
        # SHOW SIGNS
        # ----------------------------------------------------

        if text.lower().strip() == "signs":

            show_available_signs()

            continue


        # ----------------------------------------------------
        # TEST
        # ----------------------------------------------------

        if text.lower().strip() == "test":

            test_dictionary()

            continue


        # ----------------------------------------------------
        # Empty input
        # ----------------------------------------------------

        if not text.strip():

            print(
                "Please enter some text."
            )

            continue


        # ----------------------------------------------------
        # Convert input
        # ----------------------------------------------------

        signs = convert_text_to_signs(
            text
        )


        if not signs:

            print(
                "No matching signs."
            )

            continue


        # ----------------------------------------------------
        # Display result
        # ----------------------------------------------------

        print_sign_sequence(
            signs
        )


        # ----------------------------------------------------
        # Play signs
        # ----------------------------------------------------

        play_sign_sequence(
            signs
        )


    cv2.destroyAllWindows()


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":

    main()