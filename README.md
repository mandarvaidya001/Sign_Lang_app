# Sign Language Detection App

A real-time Sign Language Detection application built using Python, MediaPipe, OpenCV, and Machine Learning.

## Features

- Real-time webcam detection
- Hand landmark extraction using MediaPipe
- Predicts sign language alphabets
- Machine Learning model for classification

## Technologies

- Python
- OpenCV
- MediaPipe
- NumPy
- Scikit-learn

## Project Structure

```
Sign_Lang_App/
│
├── dataset/
├── models/
├── extract_landmarks.py
├── train_model.py
├── predict.py
├── README.md
└── requirements.txt
```

## Installation

```bash
pip install -r requirements.txt
```

## Run

```bash
python predict.py
```