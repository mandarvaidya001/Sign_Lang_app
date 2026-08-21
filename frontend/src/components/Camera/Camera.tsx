import { motion } from "motion/react";
import { VideoOff } from "lucide-react";
import { Loading } from "@/components/Loading/Loading";
import type { AppError } from "@/types";
import { cn } from "@/utils/cn";

interface CameraProps {
  videoRef: React.RefObject<HTMLVideoElement | null>;
  isReady: boolean;
  error: AppError | null;
  onRetry: () => void;
  className?: string;
}

/**
 * Purely presentational: renders whatever `useCamera` gives it. Contains
 * no prediction or landmark logic — that lives entirely in the backend.
 */
export function Camera({ videoRef, isReady, error, onRetry, className }: CameraProps) {
  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.98 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.5, ease: "easeOut" }}
      className={cn(
        "relative mx-auto aspect-video w-full max-w-3xl overflow-hidden rounded-3xl border border-white/10 bg-white/[0.02] shadow-[0_20px_60px_rgba(0,0,0,0.5)]",
        className,
      )}
    >
      <video
        ref={videoRef}
        muted
        playsInline
        className={cn(
          "h-full w-full scale-x-[-1] object-cover transition-opacity duration-500",
          isReady && !error ? "opacity-100" : "opacity-0",
        )}
      />

      {!isReady && !error && (
        <div className="absolute inset-0 flex flex-col items-center justify-center gap-4 bg-black/40">
          <Loading />
          <div className="text-center">
            <p className="text-sm font-medium text-white/85">
              Loading Camera...
            </p>
            <p className="mt-1 text-xs text-white/45">
              Preparing AI Recognition...
            </p>
          </div>
        </div>
      )}

      {error && (
        <div className="absolute inset-0 flex flex-col items-center justify-center gap-4 bg-black/60 px-8 text-center">
          <VideoOff className="h-8 w-8 text-white/40" aria-hidden="true" />
          <div>
            <p className="text-sm font-medium text-white/85">
              {error.type === "camera-permission-denied"
                ? "Camera access was denied"
                : "Camera unavailable"}
            </p>
            <p className="mt-1 max-w-xs text-xs text-white/45">
              {error.message}
            </p>
          </div>
          <button
            type="button"
            onClick={onRetry}
            className="rounded-full border border-white/15 bg-white/[0.06] px-4 py-2 text-xs font-medium text-white transition hover:border-white/30 hover:bg-white/[0.1]"
          >
            Retry
          </button>
        </div>
      )}
    </motion.div>
  );
}
