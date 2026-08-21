import { useCallback, useEffect, useRef, useState } from "react";
import { ApiError } from "@/services/api";
import { predictionService } from "@/services/prediction";
import {
  PREDICTION_POLL_INTERVAL_MS,
  TEXT_POLL_INTERVAL_MS,
} from "@/utils/constants";
import type {
  AppError,
  RecognitionAction,
  RecognitionMode,
  SpeechStatus,
} from "@/types";

interface UseRecognitionResult {
  prediction: string | null;
  confidence: number | null;
  generatedText: string;
  speechStatus: SpeechStatus;
  backendReady: boolean;
  error: AppError | null;
  startSession: (mode: RecognitionMode) => Promise<void>;
  stopSession: () => Promise<void>;
  sendAction: (action: RecognitionAction) => Promise<void>;
}

/**
 * Owns the "session" side of the Recognition screen: starting/stopping
 * recognition on the backend, polling for the latest prediction and
 * generated text, and forwarding button presses. All AI logic — landmark
 * extraction, inference, text formation, speech — happens server-side;
 * this hook only relays it into React state.
 */
export function useRecognition(): UseRecognitionResult {
  const [prediction, setPrediction] = useState<string | null>(null);
  const [confidence, setConfidence] = useState<number | null>(null);
  const [generatedText, setGeneratedText] = useState("");
  const [speechStatus, setSpeechStatus] = useState<SpeechStatus>("idle");
  const [backendReady, setBackendReady] = useState(false);
  const [error, setError] = useState<AppError | null>(null);

  const predictionTimer = useRef<ReturnType<typeof setInterval> | null>(null);
  const textTimer = useRef<ReturnType<typeof setInterval> | null>(null);
  const active = useRef(false);

  const clearTimers = useCallback(() => {
    if (predictionTimer.current) clearInterval(predictionTimer.current);
    if (textTimer.current) clearInterval(textTimer.current);
    predictionTimer.current = null;
    textTimer.current = null;
  }, []);

  const handleError = useCallback((err: unknown) => {
    if (err instanceof ApiError) {
      setError({ type: err.type, message: err.message });
    } else {
      setError({ type: "unknown", message: "Something went wrong." });
    }
  }, []);

  const startSession = useCallback(
    async (mode: RecognitionMode) => {
      setError(null);
      try {
        await predictionService.start(mode);
        setBackendReady(true);
        active.current = true;

        predictionTimer.current = setInterval(async () => {
          if (!active.current) return;
          try {
            const result = await predictionService.getPrediction();
            setPrediction(result.prediction);
            setConfidence(result.confidence);
          } catch (err) {
            if (active.current) handleError(err);
          }
        }, PREDICTION_POLL_INTERVAL_MS);

        textTimer.current = setInterval(async () => {
          if (!active.current) return;
          try {
            const [text, status] = await Promise.all([
              predictionService.getGeneratedText(),
              predictionService.getStatus(),
            ]);
            setGeneratedText(text.text);
            setSpeechStatus(status.speechStatus);
          } catch (err) {
            if (active.current) handleError(err);
          }
        }, TEXT_POLL_INTERVAL_MS);
      } catch (err) {
        setBackendReady(false);
        handleError(err);
      }
    },
    [handleError],
  );

  const stopSession = useCallback(async () => {
    active.current = false;
    clearTimers();
    try {
      await predictionService.stop();
    } catch {
      // The camera/session is going away regardless; a failed stop call
      // shouldn't block navigation back to the Landing Page.
    }
    setBackendReady(false);
    setPrediction(null);
    setConfidence(null);
    setGeneratedText("");
    setSpeechStatus("idle");
  }, [clearTimers]);

  const sendAction = useCallback(
    async (action: RecognitionAction) => {
      try {
        await predictionService.sendAction(action);
        if (action === "clear") {
          setGeneratedText("");
        }
      } catch (err) {
        handleError(err);
      }
    },
    [handleError],
  );

  useEffect(() => {
    return () => {
      active.current = false;
      clearTimers();
    };
  }, [clearTimers]);

  return {
    prediction,
    confidence,
    generatedText,
    speechStatus,
    backendReady,
    error,
    startSession,
    stopSession,
    sendAction,
  };
}
