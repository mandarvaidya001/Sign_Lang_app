# Backend API Architecture

# Purpose

This document defines how the frontend communicates with the existing Python backend.

The backend already contains a working Artificial Intelligence pipeline.

The frontend must reuse this pipeline instead of replacing it.

The backend remains responsible for all AI-related tasks.

The frontend remains responsible for presentation and user interaction.

---

# Architecture Overview

Frontend (React)

↓

Backend API (Python)

↓

Prediction Engine

↓

TensorFlow Model

↓

Prediction Result

The frontend must never perform AI prediction.

The backend remains the single source of truth.

---

# Existing Backend Responsibilities

The backend already performs:

- Camera initialization
- MediaPipe hand detection
- Landmark extraction
- Landmark normalization
- TensorFlow model prediction
- Confidence calculation
- Generated text management
- Text-to-speech
- Resource cleanup

These implementations already exist.

Reuse them.

Do not rewrite them.

---

# Frontend Responsibilities

The frontend is responsible for:

- Displaying pages
- Displaying the webcam
- Displaying predictions
- Displaying generated text
- Sending user actions
- Showing loading states
- Showing errors
- Providing a premium user interface

The frontend should never implement AI logic.

---

# Communication Model

The frontend communicates with the backend through API endpoints.

The backend returns data.

The frontend updates the interface.

Example:

React

↓

API Request

↓

Python

↓

Prediction

↓

JSON Response

↓

React UI Update

---

# Camera

The backend owns the camera.

Do not create another camera pipeline inside React.

The existing camera processing should remain unchanged.

---

# Recognition Pipeline

Existing pipeline:

Camera

↓

MediaPipe

↓

Landmark Extraction

↓

Normalization

↓

Scaler

↓

TensorFlow Model

↓

Prediction

↓

Generated Text

↓

Speech

This flow should remain unchanged.

---

# Information Sent To Frontend

The backend should provide:

Current Prediction

Prediction Confidence

Generated Text

Recognition Mode

Camera Status

Speech Status

System Errors

The frontend displays this information.

---

# User Actions Sent To Backend

The frontend sends only user actions.

Examples:

Start Recognition

Stop Recognition

Space

Enter

Clear

Quit

Recognition Mode Selection

The backend processes these actions.

---

# Speech

The backend remains responsible for:

Text-to-Speech

The frontend only displays:

Speaking...

Ready

---

# Error Handling

Backend errors should return friendly messages.

Examples:

Camera unavailable

Permission denied

Prediction unavailable

Model loading failed

The frontend should display user-friendly notifications.

---

# Future API Endpoints (Conceptual)

The implementation may expose endpoints similar to:

GET /status

Returns backend status.

POST /start

Starts recognition.

POST /stop

Stops recognition.

GET /prediction

Returns latest prediction.

GET /text

Returns generated text.

POST /action

Accepts:

Space

Enter

Clear

Quit

GET /health

Returns backend health status.

These endpoints are conceptual.

Claude should design the implementation according to the existing backend architecture rather than forcing these exact routes.

---

# Development Rules

Never duplicate backend logic.

Never retrain the AI model.

Never move AI prediction into React.

Never replace MediaPipe.

Never replace TensorFlow.

Keep the backend and frontend loosely coupled.

Keep communication clean and maintainable.

---

# Long-Term Goal

The architecture should allow the frontend to evolve independently while continuing to use the existing Python AI engine.

The existing AI pipeline is the foundation of the application.

The frontend is a modern interface built around that foundation.