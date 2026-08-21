import { useCallback, useRef, useState, type ReactNode } from "react";
import { AnimatePresence, motion } from "motion/react";
import { AlertTriangle, X } from "lucide-react";
import type { AppError } from "@/types";
import { NotificationContext } from "@/context/notification-context";

interface Notification {
  id: number;
  message: string;
}

/**
 * Renders friendly, human-readable error banners in a fixed corner of the
 * screen. Backend/network failures are translated to plain language
 * upstream (see services/api.ts) — this component only presents them.
 */
export function NotificationProvider({ children }: { children: ReactNode }) {
  const [notifications, setNotifications] = useState<Notification[]>([]);
  const nextId = useRef(0);

  const notify = useCallback((error: AppError) => {
    const id = nextId.current++;
    setNotifications((prev) => [...prev, { id, message: error.message }]);
    setTimeout(() => {
      setNotifications((prev) => prev.filter((n) => n.id !== id));
    }, 5000);
  }, []);

  const dismiss = (id: number) => {
    setNotifications((prev) => prev.filter((n) => n.id !== id));
  };

  return (
    <NotificationContext.Provider value={{ notify }}>
      {children}
      <div className="pointer-events-none fixed bottom-6 left-1/2 z-50 flex w-full max-w-md -translate-x-1/2 flex-col gap-2 px-4">
        <AnimatePresence>
          {notifications.map((n) => (
            <motion.div
              key={n.id}
              initial={{ opacity: 0, y: 12, scale: 0.98 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              exit={{ opacity: 0, y: 8, scale: 0.98 }}
              transition={{ duration: 0.25 }}
              className="pointer-events-auto flex items-center gap-3 rounded-2xl border border-white/10 bg-black/80 px-4 py-3 text-sm text-white shadow-[0_8px_30px_rgba(0,0,0,0.5)] backdrop-blur-xl"
            >
              <AlertTriangle
                className="h-4 w-4 shrink-0 text-[var(--color-warning)]"
                aria-hidden="true"
              />
              <span className="flex-1 text-white/85">{n.message}</span>
              <button
                type="button"
                onClick={() => dismiss(n.id)}
                aria-label="Dismiss notification"
                className="shrink-0 rounded-full p-1 text-white/50 transition hover:bg-white/10 hover:text-white"
              >
                <X className="h-3.5 w-3.5" />
              </button>
            </motion.div>
          ))}
        </AnimatePresence>
      </div>
    </NotificationContext.Provider>
  );
}
