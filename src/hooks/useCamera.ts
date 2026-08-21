import { useCallback, useEffect, useRef, useState } from "react";
import type { AppError } from "@/types";

interface UseCameraResult {
  videoRef: React.RefObject<HTMLVideoElement | null>;
  isReady: boolean;
  error: AppError | null;
  start: () => Promise<void>;
  stop: () => void;
  captureFrame: () => Promise<Blob | null>;
}

/**
 * Manages the browser camera preview and captures frames
 * for the Python recognition backend.
 */
export function useCamera(): UseCameraResult {
  const videoRef = useRef<HTMLVideoElement | null>(null);
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

      if (
        name === "NotAllowedError" ||
        name === "PermissionDeniedError"
      ) {
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

  /**
   * Captures the current browser camera frame.
   *
   * The returned JPEG Blob can be sent directly to
   * POST /predict in the Python backend.
   */
  const captureFrame = useCallback(async (): Promise<Blob | null> => {
  const video = videoRef.current;

  console.log("VIDEO DEBUG:", {
    exists: !!video,
    readyState: video?.readyState,
    videoWidth: video?.videoWidth,
    videoHeight: video?.videoHeight,
    paused: video?.paused,
    hasStream: !!video?.srcObject,
  });

  if (!video) {
    console.log("CAPTURE FAILED: video element is null");
    return null;
  }

  if (video.videoWidth === 0 || video.videoHeight === 0) {
    console.log("CAPTURE FAILED: video has no dimensions");
    return null;
  }

  const canvas = document.createElement("canvas");

  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;

  const context = canvas.getContext("2d");

  if (!context) {
    console.log("CAPTURE FAILED: canvas context unavailable");
    return null;
  }

  // Capture the CURRENT frame from the live camera.
  context.drawImage(
    video,
    0,
    0,
    canvas.width,
    canvas.height
  );

  return new Promise<Blob | null>((resolve) => {
    canvas.toBlob(
      (blob) => {
        console.log("CAPTURE RESULT:", blob);
        resolve(blob);
      },
      "image/jpeg",
      0.85
    );
  });
}, []);

  useEffect(() => stop, [stop]);

  return {
    videoRef,
    isReady,
    error,
    start,
    stop,
    captureFrame,
  };
}