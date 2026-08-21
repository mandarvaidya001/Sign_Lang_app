import { api } from "@/services/api";
import type {
  PredictionResponse,
  RecognitionMode,
} from "@/types";

/**
 * Talks to the existing Python recognition backend.
 *
 * The backend expects an image/frame at:
 * POST /predict
 *
 * The backend then:
 * 1. Decodes the frame
 * 2. Extracts hand landmarks
 * 3. Runs the existing ML model
 * 4. Returns letter, confidence and hand_count
 */
export const predictionService = {
  /**
   * Send one camera frame to the Python backend.
   */
  getPrediction(image: Blob) {
    return api.postImage<PredictionResponse>("/predict", image);
  },

  /**
   * Recognition mode is currently handled by the frontend.
   * Kept here so the existing hook architecture can be migrated
   * without breaking the type contract.
   */
  start(_mode: RecognitionMode) {
    return Promise.resolve();
  },

  /**
   * The current Python backend does not expose /stop.
   */
  stop() {
    return Promise.resolve();
  },

  /**
   * The current Python backend does not expose /text yet.
   */
  getGeneratedText() {
  return api.get("/text") as Promise<{ text: string }>;
},
sendAction(
  action:
    | "letter"
    | "space"
    | "backspace"
    | "left"
    | "right"
    | "enter"
    | "clear"
    | "quit",
  letter?: string
) {
  return api.post("/action", { action, letter });
},
getStatus() {
  return api.get("/health");
},
};