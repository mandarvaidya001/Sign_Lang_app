import os

def create_directories():

    folders = [
        "csv",
        "models"
    ]

    for folder in folders:
        os.makedirs(folder, exist_ok=True)