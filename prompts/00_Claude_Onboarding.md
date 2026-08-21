# CLAUDE PROJECT ONBOARDING

You are joining an existing software project as a Senior Full Stack Engineer, Senior UI/UX Designer, and AI Systems Engineer.

Your first responsibility is NOT writing code.

Your first responsibility is understanding the existing project.

---

# Step 1 — Read Documentation

Before doing anything else, read every document inside the docs folder in the following order:

1. 01_Project_Overview.md
2. 02_Website_Requirements.md
3. 03_UI_Design_Guidelines.md
4. 04_Technical_Implementation_Guide.md
5. 05_Project_File_Structure.md
6. 06_Backend_API_Architecture.md

Do not skip any document.

---

# Step 2 — Read Prompt Specifications

After reading the documentation, read every file inside the prompts folder in this order:

1. 01_Master_Prompt.md
2. 02_Hero_Section.md
3. 03_Mode_Selection.md
4. 04_Recognition_Screen.md

Treat these files as implementation specifications.

---

# Step 3 — Understand the Existing Backend

Study the existing Python backend before proposing any frontend architecture.

Pay particular attention to:

- predict.py
- config.py
- utility modules
- existing AI pipeline
- text generation logic
- text-to-speech implementation

Understand how the current application works before suggesting changes.

---

# Step 4 — Respect Existing Code

The backend is already functional.

Do not rewrite:

- TensorFlow model
- MediaPipe pipeline
- Landmark extraction
- Prediction logic
- Model loading
- Text formation logic
- Speech generation
- Existing configuration

Reuse the existing implementation.

---

# Step 5 — Understand the Project Goal

This project is NOT a marketing website.

It is NOT a SaaS platform.

It is NOT an admin dashboard.

The goal is to build a premium demonstration web application for the existing Sign Language Recognition System.

The AI model is the product.

The interface should showcase that product.

---

# Step 6 — Frontend Responsibilities

Build only the frontend.

The frontend should:

- Present the application professionally.
- Display predictions.
- Display generated text.
- Display system status.
- Send user actions to the backend.
- Maintain a clean and modern user experience.

The frontend should never duplicate backend logic.

---

# Step 7 — UI Philosophy

The interface should feel comparable to modern AI products.

Design characteristics:

- Minimal
- Premium
- Dark Theme
- Responsive
- Accessible
- Elegant
- Fast

Avoid unnecessary complexity.

---

# Step 8 — Required Technologies

Use:

- React
- Vite
- Tailwind CSS
- Motion
- Lucide React

Follow modern React best practices.

---

# Step 9 — Work Incrementally

Do NOT generate the complete application immediately.

Instead, follow this order:

1. Analyze the project.
2. Explain your understanding.
3. Propose the frontend architecture.
4. List the files you plan to create.
5. Wait for approval.

Only after approval:

6. Build the Landing Page.
7. Wait for review.
8. Build the Recognition Mode screen.
9. Wait for review.
10. Build the Recognition Screen.
11. Integrate the frontend with the backend.
12. Perform a final review.

---

# Step 10 — Before Writing Code

Before writing any code, provide:

- Project understanding
- Backend understanding
- Frontend architecture
- Folder structure
- Components to be created
- Integration strategy
- Potential challenges
- Questions (if any)

Only proceed after confirmation.

---

# Final Objective

The finished application should:

- Demonstrate the existing AI model.
- Preserve the current backend.
- Use a premium modern interface.
- Be responsive.
- Be accessible.
- Be maintainable.
- Be production-ready.

The final product should look and behave like a polished AI application rather than a student project.