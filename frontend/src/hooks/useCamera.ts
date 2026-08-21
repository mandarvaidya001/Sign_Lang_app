import { useCallback, useEffect, useRef, useState } from "react";
import type { AppError } from "@/types";

interface UseCameraResult {
  videoRef: React.RefObject<HTMLVideoElement | null>;
  isReady: boolean;
  error: AppError | null;
  start: () => Promise<void>;
  stop: () => void;
}

/**
 * Manages the on-screen camera preview shown to the user.
 *
 * Note on architecture: the existing Python backend owns the actual
 * recognition pipeline (MediaPipe + TensorFlow) and performs its own
 * capture for prediction. This hook is only responsible for the visual
 * preview the person sees in the browser, requested only once they reach
 * the Recognition screen — never on page load. If a future backend
 * revision streams frames to the browser instead (e.g. an MJPEG/WebRTC
 * feed), only this hook needs to change; every component that consumes
 * `videoRef` stays the same.
 */
export function useCamera(): UseCameraResult {
  const videoRef = useRef<HTMLVideoElement>(null);
  const streamRef = useRef<MediaStream | null>(null);
  const [isReady, setIsReady] = useState(false);
  const [error, setError] = useState<AppError | null>(null);

  const stop = useCallback(() => {
    streamRef.current?.getTracks().forEach((track) => track.stop());
    streamRef.current = null;
    setIsReady(false);
  }, []);

  const start = useCallback(async () => {
    setError(null);
    setIsReady(false);

    if (!navigator.mediaDevices?.getUserMedia) {
      setError({
        type: "camera-unavailable",
        message: "This browser doesn't support camera access.",
      });
      return;
    }

    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: { facingMode: "user" },
        audio: false,
      });
      streamRef.current = stream;
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        await videoRef.current.play();
      }
      setIsReady(true);
    } catch (err) {
      const name = err instanceof DOMException ? err.name : "";
      if (name === "NotAllowedError" || name === "PermissionDeniedError") {
        setError({
          type: "camera-permission-denied",
          message: "Camera access was denied.",
        });
      } else {
        setError({
          type: "camera-unavailable",
          message: "No camera could be found or accessed.",
        });
      }
    }
  }, []);

  useEffect(() => stop, [stop]);

  return { videoRef, isReady, error, start, stop };
}
