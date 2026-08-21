import { AnimatePresence, motion } from "motion/react";

interface PredictionProps {
  prediction: string | null;
  confidence: number | null;
}

/**
 * Shows only what the backend reports as the current prediction — the
 * frontend never guesses or smooths this value itself. Cross-fades
 * between values so changing predictions don't flicker.
 */
export function Prediction({ prediction, confidence }: PredictionProps) {
  return (
    <div className="flex flex-col items-center gap-2 text-center">
      <span className="text-xs font-medium uppercase tracking-[0.18em] text-white/40">
        Current Prediction
      </span>
      <div className="relative flex h-16 items-center justify-center">
        <AnimatePresence mode="wait">
          <motion.span
            key={prediction ?? "none"}
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -8 }}
            transition={{ duration: 0.25, ease: "easeOut" }}
            className="text-white text-5xl font-medium tracking-tight sm:text-6xl"
          >
            {prediction ?? "—"}
          </motion.span>
        </AnimatePresence>
      </div>
      {confidence !== null && (
        <span className="text-xs text-white/35">
          {Math.round(confidence )}% confidence
        </span>
      )}
    </div>
  );
}
