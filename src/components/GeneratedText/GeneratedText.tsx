import { motion } from "motion/react";

interface GeneratedTextProps {
  text: string;
  cursorPosition: number;
}

export function GeneratedText({
  text,
  cursorPosition,
}: GeneratedTextProps) {
  const safeCursorPosition = Math.max(
    0,
    Math.min(cursorPosition, text.length),
  );

  const beforeCursor = text.slice(0, safeCursorPosition);
  const afterCursor = text.slice(safeCursorPosition);

  return (
    <motion.div
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, ease: "easeOut" }}
      className="mx-auto w-full max-w-2xl rounded-2xl border border-white/10 bg-white/[0.03] px-6 py-5 text-center backdrop-blur-md"
    >
      <p className="min-h-7 break-words text-lg font-normal tracking-wide text-white/90 sm:text-xl">
        {text.length > 0 ? (
          <>
            {beforeCursor}
            <motion.span
               aria-hidden="true"
               animate={{ opacity: [1, 0, 1] }}
               transition={{
               duration: 1,
               repeat: Infinity,
               ease: "easeInOut",
               }}
               className="mx-0.5 inline-block h-6 w-0 border-l-2 border-white align-middle"
               />
            {afterCursor}
          </>
        ) : (
          <>
            <motion.span
                 aria-hidden="true"
                 animate={{ opacity: [1, 0, 1] }}
                 transition={{
                 duration: 1,
                 repeat: Infinity,
                 ease: "easeInOut",
              }}
               className="mx-0.5 inline-block h-6 w-0 border-l-2 border-white align-middle"
              />
            <span className="text-white/30">
              Your text will appear here
            </span>
          </>
        )}
      </p>
    </motion.div>
  );
}