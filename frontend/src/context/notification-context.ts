import { createContext } from "react";
import type { AppError } from "@/types";

export interface NotificationContextValue {
  notify: (error: AppError) => void;
}

export const NotificationContext =
  createContext<NotificationContextValue | null>(null);
