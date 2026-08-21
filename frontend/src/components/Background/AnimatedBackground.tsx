import { motion } from "motion/react";

interface AnimatedBackgroundProps {
  /** Reduces glow intensity for screens where content needs to lead. */
  subtle?: boolean;
}

/**
 * A quiet, drifting gradient mesh evoking a neural signal rather than a
 * literal network diagram. Pure CSS/SVG — no video, no heavy particle
 * system — so it stays cheap to render and never distracts from the
 * camera or copy in front of it.
 */
export function AnimatedBackground({ subtle = false }: AnimatedBackgroundProps) {
  return (
    <div
      aria-hidden="true"
      className="pointer-events-none fixed inset-0 overflow-hidden bg-black"
    >
      <motion.div
        className="absolute -top-1/4 left-1/2 h-[70vh] w-[70vh] -translate-x-1/2 rounded-full"
        style={{
          background:
            "radial-gradient(circle, rgba(48,84,255,0.35) 0%, rgba(48,84,255,0) 70%)",
          filter: "blur(10px)",
          opacity: subtle ? 0.5 : 0.85,
        }}
        animate={{ scale: [1, 1.08, 1], x: ["0%", "3%", "0%"] }}
        transition={{ duration: 16, repeat: Infinity, ease: "easeInOut" }}
      />
      <motion.div
        className="absolute bottom-[-20%] right-[-10%] h-[55vh] w-[55vh] rounded-full"
        style={{
          background:
            "radial-gradient(circle, rgba(180,192,255,0.18) 0%, rgba(180,192,255,0) 70%)",
          filter: "blur(10px)",
          opacity: subtle ? 0.4 : 0.7,
        }}
        animate={{ scale: [1, 1.1, 1], y: ["0%", "-4%", "0%"] }}
        transition={{ duration: 20, repeat: Infinity, ease: "easeInOut" }}
      />

      {/* faint signal grid — dots that suggest landmarks/coordinates */}
      <svg className="absolute inset-0 h-full w-full opacity-[0.07]">
        <defs>
          <pattern
            id="grid-dots"
            width="42"
            height="42"
            patternUnits="userSpaceOnUse"
          >
            <circle cx="1.2" cy="1.2" r="1.2" fill="white" />
          </pattern>
        </defs>
        <rect width="100%" height="100%" fill="url(#grid-dots)" />
      </svg>

      <div className="absolute inset-0 bg-gradient-to-b from-transparent via-transparent to-black/60" />
    </div>
  );
}
