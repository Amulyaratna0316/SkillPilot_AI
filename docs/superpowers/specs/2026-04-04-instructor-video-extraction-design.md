# Instructor Video Persistence + AI Extraction Design

Date: 2026-04-04
Project: SkillPilot_AI
Files in scope: `instructor.html`, `index.html`

## Goals
- Persist instructor-uploaded videos so students can view them later.
- Link the uploaded video reference to the saved procedure.
- Display the ideal video on the student pre-session screen when a procedure is selected.
- Replace the Gemini video extraction flow with a robust, frame-by-frame extraction loop.

## Non-Goals
- No CSS, layout, or UI changes beyond wiring existing elements.
- No refactors outside the explicit handler/function replacements.

## Current Issues (Root Cause Summary)
- Upload handler only creates an object URL and never persists the video data.
- Extract flow uses a brittle timestamp/MediaPipe loop and does not match the requested Gemini frame-by-frame extraction.
- Student pre-session screen has no ideal video loader and therefore cannot display uploaded instructor video.

## Proposed Approach (Recommended)
1. Replace the video upload handler with the provided Base64 + localStorage implementation.
2. Attach the uploaded video key to the saved procedure right before storing it.
3. Add `loadIdealVideo(procedureId)` in `index.html` and call it when a procedure is selected in the pre-session screen.
4. Replace the existing extraction function with the provided frame-by-frame Gemini extraction function and add the companion `renderExtractedSteps()`.

This aligns with the user-provided exact snippets and avoids UI changes.

## Components and Data Flow

### 1) Video Upload and Persistence
- **Inputs:** `#videoUpload` file input (or renamed to match), local file.
- **Flow:** File → preview via object URL → read as base64 → save to `localStorage` under `instructorVideo_<timestamp>` → store pointer in `lastUploadedVideoKey`.
- **Fallback:** If `localStorage` throws, store `lastUploadedVideoKey = objecturl` and `lastUploadedVideoURL` pointing to preview src.
- **Outputs:** Persistent video key or session-only object URL.

### 2) Procedure Save With Video Link
- **Inputs:** `lastUploadedVideoKey` from localStorage.
- **Flow:** Add `procedure.videoKey` before pushing into `instructorProcedures`.
- **Outputs:** Procedures persisted with a video reference.

### 3) Student Pre-Session Ideal Video Display
- **Inputs:** Selected `procedureId`, `PROCEDURES` object, `idealVideoContainer` and child elements.
- **Flow:** Resolve `proc.videoKey` → load base64 or object URL → set `#idealVideo` src → reveal container and label.
- **Outputs:** Ideal video visible for students when available.

### 4) Gemini Extraction Loop
- **Inputs:** `#videoPreview` element, `geminiApiKey`.
- **Flow:** Sequentially seek video → capture frame to base64 → send to Gemini per frame → parse JSON → render editable step cards.
- **Outputs:** Editable extracted steps rendered; status text updated.

## Error Handling
- Missing API key: show alert and return.
- Missing video: show alert and return.
- localStorage overflow: switch to session-only object URL.
- Gemini errors: fall back to a placeholder step for that frame.

## Testing and Validation
- Upload a short video and verify `lastUploadedVideoKey` and base64 entry in localStorage.
- Save a procedure and confirm `videoKey` is stored inside it.
- In student pre-session screen, select the procedure and confirm video appears.
- Run extraction on a short video and confirm steps render with the status updates.

## Risks and Mitigations
- **localStorage size limits:** handled by object URL fallback and warning message.
- **Large videos:** encourage shorter demos; extraction loop limits frames to ~6.
- **Element ID mismatches:** ensure ID alignment with required handler snippet or add minimal adapter.

## Open Questions
- None. User approved replacing `skillpilot-core.html` usage with `index.html`.

