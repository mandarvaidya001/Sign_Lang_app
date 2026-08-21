import { motion } from "motion/react";

interface GeneratedTextProps {
  text: string;
}

/** Displays the accumulated text exactly as reported by the backend. */
export function GeneratedText({ text }: GeneratedTextProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, ease: "easeOut" }}
      className="mx-auto w-full max-w-2xl rounded-2xl border border-white/10 bg-white/[0.03] px-6 py-5 text-center backdrop-blur-md"
    >
      <p className="min-h-7 break-words text-lg font-normal tracking-wide text-white/90 sm:text-xl">
        {text.length > 0 ? (
          text
        ) : (
          <span className="text-white/30">Your text will appear here</span>
        )}
      </p>
    </motion.div>
  );
}
