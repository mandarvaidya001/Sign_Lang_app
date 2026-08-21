import os
from config import DATASET_PATH


# ==========================================
# Get all class names
# ==========================================

def get_classes():

    classes = [
        folder
        for folder in os.listdir(DATASET_PATH)
        if os.path.isdir(os.path.join(DATASET_PATH, folder))
    ]

    return sorted(classes)


# ==========================================
# Get videos of one class
# ==========================================

def get_videos(class_name):

    class_path = os.path.join(DATASET_PATH, class_name)

    videos = [
        file
        for file in os.listdir(class_path)
        if file.lower().endswith((".mp4", ".mov", ".avi"))
    ]

    return sorted(videos)


# ==========================================
# Get full video path
# ==========================================

def get_video_path(class_name, video_name):

    return os.path.join(
        DATASET_PATH,
        class_name,
        video_name
    )


# ==========================================
# Count Dataset
# ==========================================

def dataset_summary():

    classes = get_classes()

    total = 0

    print("\n==============================")
    print("DATASET SUMMARY")
    print("==============================")

    for cls in classes:

        count = len(get_videos(cls))

        total += count

        print(f"{cls:<12} : {count}")

    print("------------------------------")
    print("Classes :", len(classes))
    print("Videos  :", total)
    print("==============================")