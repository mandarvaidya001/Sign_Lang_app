import os
import time
import numpy as np
from tqdm import tqdm

from config import SEQUENCE_PATH

from dataset import (
    get_classes,
    get_videos,
    get_video_path
)

from utils import sample_frames
from mediapipe_utils import extract_landmarks


# ==========================================
# Process One Video
# ==========================================

def process_video(video_path):

    frames = sample_frames(video_path)

    if frames is None:

        return None

    sequence = []

    for frame in frames:

        landmarks = extract_landmarks(frame)

        # Make sure every frame has exactly
        # 225 features.

        if landmarks.shape != (225,):

            print(
                f"\nInvalid landmark shape: "
                f"{landmarks.shape}"
            )

            return None

        sequence.append(landmarks)

    sequence = np.array(
        sequence,
        dtype=np.float32
    )

    return sequence


# ==========================================
# Main
# ==========================================

def main():

    start = time.time()

    processed = 0
    skipped = 0
    failed = 0

    classes = get_classes()

    print("\n=====================================")
    print("NORMALIZED LANDMARK EXTRACTION")
    print("=====================================\n")

    print("Expected frame shape : (225,)")
    print("Expected sequence    : (30, 225)")
    print()

    for cls in classes:

        output_folder = os.path.join(
            SEQUENCE_PATH,
            cls
        )

        os.makedirs(
            output_folder,
            exist_ok=True
        )

        videos = get_videos(cls)

        for video in tqdm(
            videos,
            desc=cls
        ):

            video_path = get_video_path(
                cls,
                video
            )

            output_name = (
                os.path.splitext(video)[0]
                + ".npy"
            )

            output_path = os.path.join(
                output_folder,
                output_name
            )

            # ----------------------------------
            # IMPORTANT:
            # Old files must be deleted before
            # running this script.
            # ----------------------------------

            if os.path.exists(output_path):

                skipped += 1
                continue

            sequence = process_video(
                video_path
            )

            if sequence is None:

                failed += 1
                continue

            # ----------------------------------
            # Verify sequence
            # ----------------------------------

            if sequence.shape[1] != 225:

                print(
                    f"\nInvalid sequence shape "
                    f"for {video}: "
                    f"{sequence.shape}"
                )

                failed += 1
                continue

            # ----------------------------------
            # Save
            # ----------------------------------

            np.save(
                output_path,
                sequence
            )

            processed += 1

    end = time.time()

    print("\n=====================================")
    print("Extraction Complete")
    print("=====================================")

    print(f"Processed : {processed}")
    print(f"Skipped   : {skipped}")
    print(f"Failed    : {failed}")

    print(
        f"Time      : "
        f"{(end-start)/60:.2f} minutes"
    )


if __name__ == "__main__":

    main()