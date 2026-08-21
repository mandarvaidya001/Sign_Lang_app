import { useCallback, useEffect, useRef, useState } from "react";
import { ApiError } from "@/services/api";
import { predictionService } from "@/services/prediction";

import {
  PREDICTION_POLL_INTERVAL_MS,
  TEXT_POLL_INTERVAL_MS,
} from "@/utils/constants";
import type {
  AppError,
  BackendStatusResponse,
  RecognitionAction,
  RecognitionMode,
  SpeechStatus,
} from "@/types";

interface UseRecognitionResult {
  prediction: string | null;
  confidence: number | null;
  generatedText: string;
  cursorPosition: number;
  speechStatus: SpeechStatus;
  backendReady: boolean;
  error: AppError | null;
  startSession: (mode: RecognitionMode) => Promise<void>;
  stopSession: () => Promise<void>;
  sendAction: (action: RecognitionAction, letter?: string) => Promise<void>;
}

/**
 * Owns the "session" side of the Recognition screen: starting/stopping
 * recognition on the backend, polling for the latest prediction and
 * generated text, and forwarding button presses. All AI logic — landmark
 * extraction, inference, text formation, speech — happens server-side;
 * this hook only relays it into React state.
 */
export function useRecognition(
  captureFrame: () => Promise<Blob | null>,
): UseRecognitionResult {
  const [prediction, setPrediction] = useState<string | null>(null);
  const [confidence, setConfidence] = useState<number | null>(null);
  const [generatedText, setGeneratedText] = useState("");
  const [cursorPosition, setCursorPosition] = useState(0);
  const [speechStatus, setSpeechStatus] = useState<SpeechStatus>("idle");
  const [backendReady, setBackendReady] = useState(false);
  const [error, setError] = useState<AppError | null>(null);

  const predictionTimer = useRef<ReturnType<typeof setInterval> | null>(null);
  console.log("useRecognition hook loaded");
  const textTimer = useRef<ReturnType<typeof setInterval> | null>(null);
  const active = useRef(false);
  const predictionInProgress = useRef(false);
  
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
        console.log("Recognition session started");

       predictionTimer.current = setInterval(async () => {
  if (!active.current || predictionInProgress.current) return;

  predictionInProgress.current = true;

  try {
    const image = await captureFrame();

    if (!image) return;

    console.log("Captured frame:", image);

    const result = await predictionService.getPrediction(image);

    console.log("BACKEND RESULT:", result);

    setPrediction(result.letter);
    setConfidence(result.confidence);
    


  } catch (err) {
    if (active.current) {
      handleError(err);
    }
  } finally {
    predictionInProgress.current = false;
  }
}, PREDICTION_POLL_INTERVAL_MS); 

        textTimer.current = setInterval(async () => {
          if (!active.current) return;
          try {
           const [text, status] = await Promise.all([
    predictionService.getGeneratedText(),
    predictionService.getStatus(),
       ]);

        console.log("FRONTEND GENERATED TEXT:", text.text);

       setGeneratedText(text.text);
            setSpeechStatus((status as BackendStatusResponse).speechStatus);
          } catch (err) {
            if (active.current) handleError(err);
          }
        }, TEXT_POLL_INTERVAL_MS);
      } catch (err) {
        setBackendReady(false);
        handleError(err);
      }
    },
    [handleError, captureFrame],
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
  async (action: RecognitionAction, letter?: string) => {
    try {
      await predictionService.sendAction(action, letter);

      if (action === "clear") {
        setGeneratedText("");
        setCursorPosition(0);
      }

      if (action === "backspace") {
        setCursorPosition((pos) => Math.max(0, pos - 1));
      }

      if (action === "left") {
        setCursorPosition((pos) => Math.max(0, pos - 1));
      }

      if (action === "right") {
        setCursorPosition((pos) =>
          Math.min(generatedText.length, pos + 1)
        );
      }

      if (action === "space") {
        setCursorPosition((pos) => pos + 1);
      }

      if (action === "letter") {
        setCursorPosition((pos) => pos + 1);
      }
    } catch (err) {
      handleError(err);
    }
  },
  [handleError, generatedText.length],
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
  cursorPosition,
  speechStatus,
  backendReady,
  error,
  startSession,
  stopSession,
  sendAction,
};
}
