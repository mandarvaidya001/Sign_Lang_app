import os
import cv2
from collections import Counter

from config import DATASET_PATH


def verify_dataset():

    print("\n=====================================")
    print("      DATASET VERIFICATION")
    print("=====================================\n")

    if not os.path.exists(DATASET_PATH):
        print("Dataset path not found!")
        print(DATASET_PATH)
        return

    classes = sorted([
        folder for folder in os.listdir(DATASET_PATH)
        if os.path.isdir(os.path.join(DATASET_PATH, folder))
    ])

    print(f"Dataset Path : {DATASET_PATH}")
    print(f"Total Classes: {len(classes)}\n")

    total_videos = 0
    corrupted = 0
    empty_classes = []
    extension_counter = Counter()

    print("-------------------------------------")
    print("Videos Per Class")
    print("-------------------------------------")

    for label in classes:

        class_path = os.path.join(DATASET_PATH, label)

        videos = [
            file for file in os.listdir(class_path)
            if file.lower().endswith((".mp4", ".mov", ".avi"))
        ]

        if len(videos) == 0:
            empty_classes.append(label)

        print(f"{label:<15} : {len(videos)}")

        total_videos += len(videos)

        for video in videos:

            extension = os.path.splitext(video)[1].upper()
            extension_counter[extension] += 1

            video_path = os.path.join(class_path, video)

            cap = cv2.VideoCapture(video_path)

            if not cap.isOpened():
                corrupted += 1

            cap.release()

    print("\n-------------------------------------")
    print("Summary")
    print("-------------------------------------")

    print(f"Total Videos      : {total_videos}")
    print(f"Corrupted Videos  : {corrupted}")

    print("\nVideo Extensions:")

    for ext, count in extension_counter.items():
        print(f"{ext:<5} : {count}")

    if empty_classes:
        print("\nEmpty Classes:")
        for folder in empty_classes:
            print(folder)
    else:
        print("\nNo Empty Classes Found.")

    print("\n=====================================")
    print("Verification Complete")
    print("=====================================\n")


if __name__ == "__main__":
    verify_dataset()