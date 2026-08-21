# LIVE RECOGNITION SCREEN IMPLEMENTATION

# Objective

Design and implement the main Live Recognition Screen for the Sign Language Recognition System.

This screen is the core of the entire application.

The primary objective is to provide users with a clean, intuitive, and professional interface for interacting with the existing AI model.

This page should highlight the AI model, not the user interface.

Every design decision should help users focus on the live recognition experience.

---

# User Journey

Landing Page

↓

Recognition Mode Selection

↓

Live Recognition Screen

↓

Text Formation

↓

Speech Output

↓

Quit

↓

Landing Page

---

# General Layout

The interface occupies the full viewport.

No scrolling.

Everything remains centered.

Structure:

Top Navigation

↓

Camera Section

↓

Current Prediction

↓

Generated Text

↓

Control Buttons

---

# Navigation

Left:

Application Logo

Sign Language Recognition

Right:

Current Mode

Examples:

Letter Recognition

Word Recognition

A small Back button may be provided to return to the Recognition Mode Selection screen.

---

# Camera Section

The webcam preview is the primary visual element.

Requirements:

- Positioned at the center of the page
- Large display area
- Responsive dimensions
- Rounded corners
- Thin border
- Soft shadow
- Dark container

The webcam preview must not contain floating buttons or unnecessary overlays.

The camera should remain the visual focus.

---

# Camera Behaviour

Do not open the camera until:

Landing Page

↓

Start Recognition

↓

Recognition Mode

↓

Camera Permission

↓

Recognition Screen

If permission is denied:

Display a friendly message.

Provide a Retry button.

Do not crash the application.

---

# Loading State

While the camera is initializing, display:

Loading Camera...

Preparing AI Recognition...

Include a subtle loading animation.

Do not show an empty black rectangle.

---

# Recognition State

When recognition starts:

Display the live webcam feed.

Continuously receive predictions from the backend.

Update the prediction smoothly.

Do not flicker.

Do not rapidly resize text.

---

# Current Prediction

Display:

Current Prediction

Example:

APPLE

Requirements:

- Large typography
- High contrast
- Center aligned
- Smooth transition when prediction changes

The prediction should appear below the webcam.

Never overlay prediction text on top of the video.

---

# Generated Text

Display the complete generated output.

Example:

HELLO HOW ARE YOU

Requirements:

- Rounded container
- High contrast
- Readable spacing
- Responsive width
- Comfortable padding

The generated text updates only through the existing backend logic.

Do not implement custom prediction logic in the frontend.

---

# Control Buttons

Display four primary controls.

Space

Enter

Clear

Quit

Buttons should:

- Have equal size
- Use consistent spacing
- Be responsive
- Have hover effects
- Support keyboard navigation

---

# Button Behaviour

## Space

Insert a space into the generated text using the existing backend functionality.

Do not implement a separate text engine.

---

## Enter

Finalize the generated text.

Trigger the existing text-to-speech functionality.

Play speech automatically.

While speech is playing:

Display:

Speaking...

Optionally animate a small speaker icon.

---

## Clear

Remove all generated text.

Reset the generated output.

The prediction process should continue running.

---

## Quit

Stop recognition.

Release webcam resources.

Return to the Landing Page.

The transition should feel smooth.

---

# Recognition Modes

The screen should adapt automatically.

If Letter Recognition was selected:

Display:

Mode: Letter Recognition

If Word Recognition was selected:

Display:

Mode: Word Recognition

No other layout changes are required.

---

# Motion Guidelines

Use Motion for:

- Camera container fade-in
- Prediction updates
- Generated text appearance
- Button hover animations
- Page transitions

Avoid:

Bounce

Flash

Heavy rotation

Aggressive animations

Animations should remain subtle.

---

# Error Handling

Gracefully handle:

Camera unavailable

Permission denied

Prediction unavailable

Backend connection failure

Model loading failure

Display clear and friendly messages.

Never expose Python errors directly to users.

---

# Accessibility

Maintain:

High contrast

Readable typography

Keyboard navigation

Visible focus states

Large click targets

Simple interactions

---

# Performance

Prioritize:

Fast camera startup

Smooth prediction updates

Efficient rendering

Minimal re-renders

Responsive UI

Avoid unnecessary computations inside React components.

---

# Backend Integration

Reuse the existing backend.

Do not rewrite:

- Prediction pipeline
- AI model
- Landmark extraction
- Camera processing
- Text formation logic
- Text-to-speech implementation

The frontend should communicate with the backend and display the results.

---

# Success Criteria

The user should be able to:

1. Open the recognition screen.
2. Allow camera access.
3. Perform sign language gestures.
4. View predictions in real time.
5. Build readable text.
6. Hear the generated speech.
7. Quit the session and safely return to the Landing Page.

The interface should feel modern, premium, responsive, and focused on demonstrating the AI model.