# RECOGNITION MODE SELECTION IMPLEMENTATION

# Objective

Design and implement the Recognition Mode Selection screen for the Sign Language Recognition System.

This screen acts as the transition between the Landing Page and the Live Recognition Screen.

Its purpose is to let users choose which recognition mode they want to use.

The interface should remain minimal, modern, intuitive, and visually consistent with the Landing Page.

---

# User Experience

After clicking **Start Recognition** on the Landing Page, the user should smoothly transition to this screen.

The user should immediately understand that there are multiple recognition modes.

The interaction should require only one click.

The page should feel fast and responsive.

---

# Technical Requirements

Use:

- React
- Tailwind CSS
- Motion
- Lucide React

Follow the design language defined in:

- 03_UI_Design_Guidelines.md

---

# Layout

The page occupies the full viewport.

Everything should be centered.

Structure:

Application Title

↓

Page Heading

↓

Three Recognition Cards

↓

Back Button (optional)

No scrolling.

---

# Header

Display:

Sign Language Recognition

Small subtitle:

Choose a Recognition Mode

---

# Recognition Cards

Display three cards.

Each card should have:

- Icon
- Title
- Short Description
- Status
- Hover Animation

Cards should be evenly spaced.

Responsive layout:

Desktop:
Three cards in one row.

Tablet:
Two cards then one below.

Mobile:
One card per row.

---

# Card 1

Title:

Letter Recognition

Description:

Recognize individual alphabet gestures.

Status:

Available

Action:

Navigate to the Live Recognition Screen.

---

# Card 2

Title:

Word Recognition

Description:

Recognize predefined words using AI.

Status:

Available

Action:

Navigate to the Live Recognition Screen.

---

# Card 3

Title:

Sentence Recognition

Description:

Recognize complete sentences.

Status:

Coming Soon

Requirements:

Display disabled appearance.

Reduce opacity.

Disable click interaction.

Display a "Coming Soon" badge.

Do not navigate anywhere.

---

# Card Design

Cards should include:

Rounded corners

Soft border

Glassmorphism effect

Subtle shadow

Blue glow on hover

Smooth scale animation

Cards should appear premium.

---

# Icons

Suggested icons:

Letter Recognition

Type icon

Word Recognition

Languages or BookText icon

Sentence Recognition

MessageSquare icon

Use Lucide React icons only.

---

# Hover Behaviour

Available cards:

Lift slightly

Blue glow

Scale approximately 1.02

Cursor pointer

Smooth transition

Disabled card:

No lift

No glow

Default cursor

Lower opacity

---

# Motion

Animate:

Page entry

Cards

Hover effects

Do not use:

Bounce

Shake

Heavy rotation

Animations should remain subtle.

---

# Color Palette

Use the design system.

Background:

#000000

Cards:

Dark glass surface

Accent:

#3054FF

Text:

White

Secondary text:

White with reduced opacity

---

# Navigation

When the user selects:

Letter Recognition

↓

Navigate to:

Recognition Screen

When the user selects:

Word Recognition

↓

Navigate to:

Recognition Screen

When the user selects:

Sentence Recognition

↓

Remain on the current page.

Display:

Coming Soon

---

# Back Button

Optional.

If included:

Return to Landing Page.

Maintain consistent button styling.

---

# Accessibility

Cards should be keyboard accessible.

Visible focus states.

Large click targets.

High contrast.

Readable typography.

---

# Performance

Avoid unnecessary re-renders.

Animate efficiently.

Maintain fast navigation.

---

# Success Criteria

The user should understand the available recognition modes within a few seconds.

The user should easily distinguish:

Available features

vs.

Future features.

Selecting an available mode should immediately transition to the Live Recognition Screen.

The page should maintain the same premium AI application design established on the Landing Page.
