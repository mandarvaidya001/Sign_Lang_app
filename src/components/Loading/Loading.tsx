import { motion } from "motion/react";
import { cn } from "@/utils/cn";

interface LoadingProps {
  className?: string;
  size?: number;
}

/** A quiet rotating ring, used wherever the app is waiting on the backend. */
export function Loading({ className, size = 28 }: LoadingProps) {
  return (
    <motion.div
      role="status"
      aria-label="Loading"
      className={cn(
        "rounded-full border-2 border-white/15 border-t-[color:var(--color-accent)]",
        className,
      )}
      style={{ width: size, height: size }}
      animate={{ rotate: 360 }}
      transition={{ duration: 0.9, repeat: Infinity, ease: "linear" }}
    />
  );
}
