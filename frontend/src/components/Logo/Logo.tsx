import { cn } from "@/utils/cn";

interface LogoProps {
  className?: string;
  /** Show the "Sign Language Recognition" wordmark next to the mark. */
  withLabel?: boolean;
}

/**
 * Minimal geometric mark: two overlapping strokes suggesting a hand
 * gesture being read as a signal, rendered in the accent blue. Kept
 * simple so it never competes with the webcam for attention.
 */
export function Logo({ className, withLabel = true }: LogoProps) {
  return (
    <div className={cn("flex items-center gap-2.5", className)}>
      <svg
        width="24"
        height="24"
        viewBox="0 0 24 24"
        fill="none"
        aria-hidden="true"
      >
        <rect width="24" height="24" rx="7" fill="#3054FF" />
        <path
          d="M7 15.5 12 8l5 7.5"
          stroke="white"
          strokeWidth="1.6"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
        <circle cx="12" cy="15.5" r="1.4" fill="white" />
      </svg>
      {withLabel && (
        <span className="text-[15px] font-medium tracking-tight text-white">
          Sign Language Recognition
        </span>
      )}
    </div>
  );
}
