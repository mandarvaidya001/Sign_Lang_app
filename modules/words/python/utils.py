import cv2
import numpy as np

from config import SEQUENCE_LENGTH


# ==========================================
# Read all frames from a video
# ==========================================

def read_video(video_path):

    cap = cv2.VideoCapture(video_path)

    frames = []

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        frames.append(frame)

    cap.release()

    return frames


# ==========================================
# Uniform Frame Sampling
# Returns exactly SEQUENCE_LENGTH frames
# ==========================================

def sample_frames(video_path):

    frames = read_video(video_path)

    if len(frames) == 0:
        return None

    # Short video → duplicate frames
    if len(frames) < SEQUENCE_LENGTH:

        while len(frames) < SEQUENCE_LENGTH:
            frames.append(frames[-1])

    # Uniform sampling
    indices = np.linspace(
        0,
        len(frames) - 1,
        SEQUENCE_LENGTH,
        dtype=int
    )

    sampled = [frames[i] for i in indices]

    return sampled


# ==========================================
# Video Information
# ==========================================

def get_video_info(video_path):

    cap = cv2.VideoCapture(video_path)

    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    cap.release()

    return frame_count, fps