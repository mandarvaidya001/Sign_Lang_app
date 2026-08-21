import { useContext } from "react";
import {
  NotificationContext,
  type NotificationContextValue,
} from "@/context/notification-context";

/** Reads the notify() function provided by <NotificationProvider>. */
export function useNotification(): NotificationContextValue {
  const ctx = useContext(NotificationContext);
  if (!ctx) {
    throw new Error(
      "useNotification must be used within a NotificationProvider",
    );
  }
  return ctx;
}
