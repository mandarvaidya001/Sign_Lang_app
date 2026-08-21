# Frontend Project Structure

# Purpose

This document defines the recommended folder structure for the frontend of the Sign Language Recognition System.

The goal is to keep the project modular, maintainable, scalable, and easy to understand.

Each file and folder should have a single responsibility.

The frontend should remain independent from the AI implementation while integrating cleanly with the existing Python backend.

---

# Technology Stack

Frontend Framework

React

Build Tool

Vite

Programming Language

TypeScript (Preferred)

Styling

Tailwind CSS

Animations

Motion

Icons

Lucide React

Routing

React Router

---

# Recommended Folder Structure

frontend/

├── public/
│
├── src/
│   │
│   ├── assets/
│   │
│   ├── components/
│   │   │
│   │   ├── Button/
│   │   ├── Camera/
│   │   ├── GeneratedText/
│   │   ├── Loading/
│   │   ├── Logo/
│   │   ├── ModeCard/
│   │   ├── Navbar/
│   │   ├── Prediction/
│   │   └── SpeechStatus/
│   │
│   ├── pages/
│   │   │
│   │   ├── LandingPage/
│   │   ├── ModeSelection/
│   │   └── Recognition/
│   │
│   ├── services/
│   │   ├── api.ts
│   │   ├── prediction.ts
│   │   └── speech.ts
│   │
│   ├── hooks/
│   │
│   ├── context/
│   │
│   ├── types/
│   │
│   ├── utils/
│   │
│   ├── styles/
│   │
│   ├── App.tsx
│   │
│   └── main.tsx
│
├── package.json
│
└── vite.config.ts

---

# Component Responsibilities

LandingPage

Display:

- Title
- Subtitle
- Start Recognition Button

No backend communication.

---

ModeSelection

Display:

- Letter Recognition
- Word Recognition
- Sentence Recognition (Coming Soon)

Navigate to Recognition Screen.

---

Recognition

Responsible for:

- Camera UI
- Prediction Display
- Generated Text
- Control Buttons
- Backend communication

---

Navbar

Display:

- Project Logo
- GitHub Button
- Documentation Button

Minimal design.

---

Camera Component

Responsible only for displaying the camera feed.

Do not implement prediction logic here.

---

Prediction Component

Display the latest prediction returned by the backend.

Do not modify prediction values.

---

Generated Text Component

Display the text created using the existing backend logic.

---

Speech Status Component

Display:

- Speaking
- Ready

Visual feedback only.

---

# Services

The services folder should contain all backend communication.

Never call backend APIs directly from UI components.

Example:

Component

↓

Service

↓

Backend

This keeps the code clean and reusable.

---

# Hooks

Store reusable React hooks here.

Examples:

- Camera state
- Recognition state
- Speech state

---

# Context

Use Context only for global application state.

Avoid unnecessary global state.

---

# Assets

Store:

Images

Icons

Illustrations

Logos

Videos (if used)

---

# Styling

Tailwind CSS should be used for nearly all styling.

Avoid inline CSS unless absolutely necessary.

---

# Design Principles

Use reusable components.

Keep files small.

Avoid duplicate code.

Keep UI separate from backend logic.

Keep animations lightweight.

Maintain consistent spacing.

---

# Backend Integration

The frontend must communicate with the existing Python backend.

Reuse:

- Prediction pipeline
- Existing text generation
- Existing speech functionality

Do not rewrite backend functionality.

---

# Future Scalability

The architecture should support future additions such as:

- Sentence Recognition
- Mobile Support
- Authentication
- User Dashboard
- Analytics
- Conversation History

without major restructuring.