import type { ReactNode } from "react";
import { motion } from "motion/react";
import { ArrowUpRight } from "lucide-react";
import { cn } from "@/utils/cn";

interface ModeCardProps {
  icon: ReactNode;
  title: string;
  description: string;
  available: boolean;
  onSelect: () => void;
}

/**
 * One recognition-mode option. Available cards are fully interactive
 * (keyboard + pointer); the disabled "Coming Soon" card is inert by
 * design — no click handler, no hover lift, reduced opacity — so users
 * can immediately tell it apart from the two real options.
 */
export function ModeCard({
  icon,
  title,
  description,
  available,
  onSelect,
}: ModeCardProps) {
  const content = (
    <>
      <div className="flex items-center justify-between">
        <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-[color:var(--color-accent)]/15 text-[color:var(--color-gradient-highlight)]">
          {icon}
        </div>
        {available ? (
          <ArrowUpRight
            className="h-4 w-4 text-white/30 transition-colors group-hover:text-white/70"
            aria-hidden="true"
          />
        ) : (
          <span className="rounded-full border border-white/10 bg-white/5 px-2.5 py-1 text-[11px] font-medium tracking-wide text-white/50">
            Coming Soon
          </span>
        )}
      </div>
      <h3 className="mt-6 text-lg font-medium text-white">{title}</h3>
      <p className="mt-1.5 text-sm leading-relaxed text-white/55">
        {description}
      </p>
    </>
  );

  const sharedClasses =
    "group relative w-full rounded-3xl border p-7 text-left backdrop-blur-md transition-colors";

  if (!available) {
    return (
      <div
        className={cn(
          sharedClasses,
          "cursor-default border-white/[0.06] bg-white/[0.015] opacity-50",
        )}
        aria-disabled="true"
      >
        {content}
      </div>
    );
  }

  return (
    <motion.button
      type="button"
      onClick={onSelect}
      whileHover={{ y: -4, scale: 1.02 }}
      whileTap={{ scale: 0.99 }}
      transition={{ duration: 0.25, ease: "easeOut" }}
      className={cn(
        sharedClasses,
        "cursor-pointer border-white/10 bg-white/[0.03] hover:border-[color:var(--color-accent)]/40 hover:shadow-[0_0_36px_rgba(48,84,255,0.18)]",
      )}
    >
      {content}
    </motion.button>
  );
}
