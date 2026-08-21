import os
import numpy as np

sequence_path = r"modules\words\sequences"

for root, dirs, files in os.walk(sequence_path):

    for file in files:

        if file.endswith(".npy"):

            path = os.path.join(
                root,
                file
            )

            data = np.load(path)

            print("File :", file)
            print("Shape:", data.shape)
            print("Min  :", data.min())
            print("Max  :", data.max())
            print("Mean :", data.mean())
            print()

            raise SystemExit