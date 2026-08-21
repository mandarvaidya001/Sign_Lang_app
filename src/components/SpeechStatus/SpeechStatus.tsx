import { AnimatePresence, motion } from "motion/react";
import { Volume2 } from "lucide-react";
import type { SpeechStatus as SpeechStatusType } from "@/types";

interface SpeechStatusProps {
  status: SpeechStatusType;
}

/** Visual-only reflection of the backend's text-to-speech state. */
export function SpeechStatus({ status }: SpeechStatusProps) {
  return (
    <AnimatePresence>
      {status === "speaking" && (
        <motion.div
          initial={{ opacity: 0, y: -6 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -6 }}
          transition={{ duration: 0.25 }}
          className="flex items-center gap-2 rounded-full border border-[color:var(--color-accent)]/30 bg-[color:var(--color-accent)]/10 px-4 py-1.5 text-xs font-medium text-[color:var(--color-gradient-highlight)]"
        >
          <motion.span
            animate={{ scale: [1, 1.15, 1] }}
            transition={{ duration: 1, repeat: Infinity, ease: "easeInOut" }}
          >
            <Volume2 className="h-3.5 w-3.5" aria-hidden="true" />
          </motion.span>
          Speaking...
        </motion.div>
      )}
    </AnimatePresence>
  );
}
