/**
 * Shared type definitions for the Sign Language Recognition frontend.
 *
 * These types describe the contract between the frontend and the existing
 * Python backend. The frontend never predicts anything itself — it only
 * displays what the backend reports and forwards user actions.
 */

/** The recognition modes exposed by the product. */
export type RecognitionMode = "letter" | "word" | "sentence";

/** Human readable labels for each mode, used throughout the UI. */
export const MODE_LABELS: Record<RecognitionMode, string> = {
  letter: "Letter Recognition",
  word: "Word Recognition",
  sentence: "Sentence Recognition",
};

/** Whether a given mode is currently available in this build. */
export const MODE_AVAILABLE: Record<RecognitionMode, boolean> = {
  letter: true,
  word: true,
  sentence: false,
};

/** Lifecycle of the camera / recognition session on the Recognition screen. */
export type SessionStatus =
  | "idle" // not started yet
  | "requesting-permission"
  | "initializing" // camera granted, backend starting up
  | "active" // live recognition running
  | "error";

/** Speech playback status, mirrored from the backend. */
export type SpeechStatus = "idle" | "speaking";

/** Category of error the app can surface to the user. */
export type AppErrorType =
  | "camera-permission-denied"
  | "camera-unavailable"
  | "backend-unavailable"
  | "prediction-unavailable"
  | "model-loading-failed"
  | "unknown";

export interface AppError {
  type: AppErrorType;
  message: string;
}

/** Response shape for GET /prediction */
export interface PredictionResponse {
  letter: string;
  confidence: number;
  hand_count: number;
  success: boolean;
}
/** Response shape for GET /text */
export interface GeneratedTextResponse {
  text: string;
}

/** Response shape for GET /status and GET /health */
export interface BackendStatusResponse {
  online: boolean;
  cameraReady: boolean;
  modelReady: boolean;
  speechStatus: SpeechStatus;
}

/** Actions the frontend can send to the backend via POST /action */
export type RecognitionAction =
  | "letter"
  | "space"
  | "backspace"
  | "left"
  | "right"
  | "enter"
  | "clear"
  | "quit";
