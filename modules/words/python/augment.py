import numpy as np

# ----------------------------------
# Small Gaussian Noise
# ----------------------------------

def add_noise(sequence, std=0.01):

    noise = np.random.normal(
        0,
        std,
        sequence.shape
    )

    return sequence + noise


# ----------------------------------
# Scale Landmarks
# ----------------------------------

def scale_landmarks(sequence):

    scale = np.random.uniform(
        0.95,
        1.05
    )

    return sequence * scale


# ----------------------------------
# Translate Landmarks
# ----------------------------------

def translate_landmarks(sequence):

    dx = np.random.uniform(-0.02, 0.02)
    dy = np.random.uniform(-0.02, 0.02)

    seq = sequence.copy()

    # x coordinates
    seq[:, 0::3] += dx

    # y coordinates
    seq[:, 1::3] += dy

    return seq


# ----------------------------------
# Random Augmentation
# ----------------------------------

def augment(sequence):

    choice = np.random.randint(3)

    if choice == 0:
        return add_noise(sequence)

    elif choice == 1:
        return scale_landmarks(sequence)

    else:
        return translate_landmarks(sequence)