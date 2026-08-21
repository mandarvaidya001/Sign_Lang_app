import { useEffect, useRef, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { motion } from "motion/react";
import { ArrowLeft, Space, CornerDownLeft, Eraser, Power } from "lucide-react";
import { Navbar } from "@/components/Navbar/Navbar";
import { Button } from "@/components/Button/Button";
import { Camera } from "@/components/Camera/Camera";
import { Prediction } from "@/components/Prediction/Prediction";
import { GeneratedText } from "@/components/GeneratedText/GeneratedText";
import { SpeechStatus } from "@/components/SpeechStatus/SpeechStatus";
import { AnimatedBackground } from "@/components/Background/AnimatedBackground";
import { useCamera } from "@/hooks/useCamera";
import { useRecognition } from "@/hooks/useRecognition";
import { useNotification } from "@/hooks/useNotification";
import { MODE_AVAILABLE, MODE_LABELS, type RecognitionMode } from "@/types";

const VALID_MODES: RecognitionMode[] = ["letter", "word", "sentence"];

/**
 * The core screen of the application. Combines the browser camera preview
 * (`useCamera`) with the backend session (`useRecognition`) but keeps them
 * fully decoupled — neither hook knows the other exists. All prediction,
 * text formation, and speech logic lives in the existing Python backend;
 * this page only renders what it's told and forwards button presses.
 */
export function Recognition() {
  const { mode: modeParam } = useParams<{ mode: string }>();
  const navigate = useNavigate();
  const { notify } = useNotification();

  const mode: RecognitionMode =
    modeParam && VALID_MODES.includes(modeParam as RecognitionMode)
      ? (modeParam as RecognitionMode)
      : "letter";

  const camera = useCamera();
  const recognition = useRecognition();
  const sessionStarted = useRef(false);
  const [isQuitting, setIsQuitting] = useState(false);

  // Redirect away from unavailable/invalid modes instead of rendering a
  // broken session.
  useEffect(() => {
    if (!modeParam || !VALID_MODES.includes(modeParam as RecognitionMode) || !MODE_AVAILABLE[mode]) {
      navigate("/select-mode", { replace: true });
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [modeParam]);

  // Camera only opens once this screen mounts — never on app load.
  useEffect(() => {
    camera.start();
    return () => camera.stop();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // Start the backend recognition session once the camera preview is ready.
  useEffect(() => {
    if (camera.isReady && !sessionStarted.current) {
      sessionStarted.current = true;
      recognition.startSession(mode);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [camera.isReady]);

  // Surface backend errors as friendly toasts.
  useEffect(() => {
    if (recognition.error) notify(recognition.error);
  }, [recognition.error, notify]);

  const handleQuit = async () => {
    setIsQuitting(true);
    await recognition.sendAction("quit");
    await recognition.stopSession();
    camera.stop();
    navigate("/");
  };

  return (
    <div className="relative flex h-svh w-full flex-col overflow-hidden">
      <AnimatedBackground subtle />

      <Navbar
        right={
          <div className="flex items-center gap-2">
            <span className="rounded-full border border-white/10 bg-white/[0.04] px-3.5 py-1.5 text-xs font-medium text-white/60">
              Mode: {MODE_LABELS[mode]}
            </span>
            <button
              type="button"
              onClick={() => navigate("/select-mode")}
              className="flex items-center gap-1.5 rounded-full px-3.5 py-2 text-sm text-white/70 transition hover:bg-white/[0.06] hover:text-white"
            >
              <ArrowLeft className="h-4 w-4" aria-hidden="true" />
              Back
            </button>
          </div>
        }
      />

      <main className="relative z-10 flex flex-1 flex-col items-center justify-center gap-6 px-6 py-4">
        <Camera
          videoRef={camera.videoRef}
          isReady={camera.isReady}
          error={camera.error}
          onRetry={camera.start}
        />

        <Prediction
          prediction={recognition.prediction}
          confidence={recognition.confidence}
        />

        <div className="flex flex-col items-center gap-3">
          <GeneratedText text={recognition.generatedText} />
          <SpeechStatus status={recognition.speechStatus} />
        </div>

        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4, delay: 0.15, ease: "easeOut" }}
          className="flex flex-wrap items-center justify-center gap-3"
        >
          <Button
            variant="control"
            icon={<Space className="h-4 w-4" aria-hidden="true" />}
            onClick={() => recognition.sendAction("space")}
            disabled={!recognition.backendReady}
          >
            Space
          </Button>
          <Button
            variant="control"
            icon={<CornerDownLeft className="h-4 w-4" aria-hidden="true" />}
            onClick={() => recognition.sendAction("enter")}
            disabled={!recognition.backendReady}
            active={recognition.speechStatus === "speaking"}
          >
            Enter
          </Button>
          <Button
            variant="control"
            icon={<Eraser className="h-4 w-4" aria-hidden="true" />}
            onClick={() => recognition.sendAction("clear")}
            disabled={!recognition.backendReady}
          >
            Clear
          </Button>
          <Button
            variant="control"
            icon={<Power className="h-4 w-4" aria-hidden="true" />}
            onClick={handleQuit}
            disabled={isQuitting}
            className="border-[color:var(--color-error)]/25 hover:border-[color:var(--color-error)]/50"
          >
            Quit
          </Button>
        </motion.div>
      </main>
    </div>
  );
}
