
# SkillPilot_AI — Real-Time Procedural Skill Intelligence System

##  Overview

SkillPilot_AI is a real-time AI-powered procedural training assistant designed for vocational education domains such as dentistry, healthcare, and technical skills training.

It uses webcam-based hand tracking and spatial analysis to monitor, evaluate, and guide students while performing precision-based physical tasks — without requiring any specialized hardware.

---

## Problem Statement

In vocational training environments:

- One instructor monitors 30–40 students simultaneously
- Critical errors often go unnoticed
- Incorrect techniques become permanent muscle memory
- Students lack objective self-assessment tools

---

## Solution

SkillPilot_AI provides:

- Real-time hand tracking using standard webcams
- Step-by-step procedural validation
- Immediate corrective feedback
- AI-generated performance reports
- Fatigue and consistency analysis

All of this runs directly in the browser with **zero hardware cost**.

---

## Key Innovations

### 1. Step Skip Detection
Detects if a student skips a required step in a procedure and immediately flags it.

### 2. Intent vs Execution Gap Analysis
Identifies hesitation, repeated corrections, and motion inconsistency — not just correctness.

### 3. Adaptive Difficulty System
Dynamically adjusts tolerance levels based on user skill level:
- Beginner
- Intermediate
- Expert

### 4. Critical vs Minor Error Classification
Classifies mistakes into:
- Critical (safety risk)
- Minor (efficiency issue)

### 5. Spatial Awareness Mapping
Tracks hand movement across defined zones:
- Safe Zone
- Precision Zone
- Unsafe Zone

### 6. Fatigue Progress Curve
Analyzes micro-tremors over time to detect fatigue trends and recommend breaks.

### 7. Attempt Replay with Error Overlay
Replays user attempts with highlighted deviations in angles and positioning.

### 8. Auto Skill Report Generation
After each session, generates a detailed report including:
- Accuracy score
- Step completion status
- Fatigue level
- Improvement suggestions

---

## 🛠️ Tech Stack

- **Frontend:** HTML, CSS, Vanilla JavaScript
- **Hand Tracking:** MediaPipe Hands (21 landmark detection)
- **Video Input:** WebRTC (getUserMedia)
- **Rendering:** Canvas API
- **AI Feedback:** Gemini 1.5 Flash API

---

## How It Works

1. Webcam captures live hand movement
2. MediaPipe extracts 21 hand landmarks (x, y, z)
3. System evaluates movement against predefined JSON procedure schema
4. Real-time validation engine checks:
   - Angles
   - Spatial zones
   - Step sequence
   - Dwell time
5. Feedback is generated instantly via UI + AI suggestions

---

## 📊 Procedure Schema (Example)

```json
{
  "procedure": "Dental Probe Handling",
  "steps": [
    {
      "id": 1,
      "name": "Initial Grip",
      "requirements": {
        "grip_angle": { "min": 25, "max": 45, "joints": [4, 0, 8] },
        "dwell_time": 2,
        "zone": "precision"
      },
      "alert": "Adjust your grip to a lighter precision hold"
    }
  ]
}
