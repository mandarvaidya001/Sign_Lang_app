import type { ButtonHTMLAttributes, ReactNode } from "react";
import { motion } from "motion/react";
import { cn } from "@/utils/cn";

type ButtonVariant = "primary" | "secondary" | "control";

// motion.button re-types a handful of DOM event handlers (animation/drag
// events) to carry Motion's own payloads, so they're dropped from the
// native HTML attributes we spread onto it.
type NativeButtonProps = Omit<
  ButtonHTMLAttributes<HTMLButtonElement>,
  | "onAnimationStart"
  | "onAnimationEnd"
  | "onAnimationIteration"
  | "onDrag"
  | "onDragStart"
  | "onDragEnd"
>;

interface ButtonProps extends NativeButtonProps {
  variant?: ButtonVariant;
  icon?: ReactNode;
  /** Places the icon after the label instead of before it. */
  iconTrailing?: boolean;
  active?: boolean;
}

const base =
  "inline-flex items-center justify-center gap-2 font-medium transition-colors focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[color:var(--color-accent)] disabled:cursor-not-allowed disabled:opacity-40";

const variants: Record<ButtonVariant, string> = {
  primary:
    "rounded-full bg-white px-7 py-3.5 text-[15px] text-black shadow-[0_8px_30px_rgba(48,84,255,0.18)]",
  secondary:
    "rounded-full border border-white/15 bg-white/[0.04] px-7 py-3.5 text-[15px] text-white backdrop-blur-md",
  control:
    "min-w-[104px] rounded-2xl border border-white/10 bg-white/[0.04] px-5 py-3.5 text-sm text-white backdrop-blur-md",
};

/**
 * Shared button primitive used across all three screens. `primary` and
 * `secondary` follow the Landing Page spec (pill shapes, glass secondary);
 * `control` is the rounded rectangle used for Space / Enter / Clear / Quit
 * on the Recognition screen.
 */
export function Button({
  variant = "primary",
  icon,
  iconTrailing = false,
  active = false,
  className,
  children,
  ...props
}: ButtonProps) {
  return (
    <motion.button
      whileHover={props.disabled ? undefined : { scale: 1.03, y: -1 }}
      whileTap={props.disabled ? undefined : { scale: 0.98 }}
      transition={{ duration: 0.2, ease: "easeOut" }}
      className={cn(
        base,
        variants[variant],
        variant === "control" &&
          active &&
          "border-[color:var(--color-accent)]/50 bg-[color:var(--color-accent)]/15",
        variant === "secondary" &&
          "hover:border-white/30 hover:shadow-[0_0_24px_rgba(48,84,255,0.25)]",
        className,
      )}
      {...props}
    >
      {icon && !iconTrailing && <span className="shrink-0">{icon}</span>}
      {children}
      {icon && iconTrailing && <span className="shrink-0">{icon}</span>}
    </motion.button>
  );
}
