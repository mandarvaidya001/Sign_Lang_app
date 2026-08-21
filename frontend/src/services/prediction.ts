import { api } from "@/services/api";
import type {
  BackendStatusResponse,
  GeneratedTextResponse,
  PredictionResponse,
  RecognitionAction,
  RecognitionMode,
} from "@/types";

/**
 * Talks to the existing recognition pipeline (MediaPipe + TensorFlow) that
 * already runs in the Python backend. This service never predicts anything
 * itself — it only forwards requests and relays whatever the backend says.
 *
 * Conceptual endpoints, per 06_Backend_API_Architecture.md:
 *   POST /start        start recognition for a given mode
 *   POST /stop          stop recognition, release camera resources
 *   GET  /prediction    latest predicted letter/word
 *   GET  /text           current generated text
 *   POST /action         Space / Enter / Clear / Quit
 *   GET  /status | /health   backend + model readiness
 */
export const predictionService = {
  start(mode: RecognitionMode) {
    return api.post<void>("/start", { mode });
  },

  stop() {
    return api.post<void>("/stop");
  },

  getPrediction() {
    return api.get<PredictionResponse>("/prediction");
  },

  getGeneratedText() {
    return api.get<GeneratedTextResponse>("/text");
  },

  sendAction(action: RecognitionAction) {
    return api.post<void>("/action", { action });
  },

  getStatus() {
    return api.get<BackendStatusResponse>("/status");
  },
};
