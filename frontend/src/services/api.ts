import { API_BASE_URL } from "@/utils/constants";
import type { AppError } from "@/types";

/**
 * Thin HTTP wrapper around the existing Python backend.
 *
 * This module intentionally knows nothing about predictions, text, or
 * speech — it only knows how to talk to the backend and how to turn
 * network failures into `AppError`s the UI can render. Every other
 * service in this folder builds on top of it.
 */

export class ApiError extends Error implements AppError {
  type: AppError["type"];

  constructor(type: AppError["type"], message: string) {
    super(message);
    this.type = type;
    this.name = "ApiError";
  }
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  let response: Response;

  try {
    response = await fetch(`${API_BASE_URL}${path}`, {
      headers: { "Content-Type": "application/json" },
      ...init,
    });
  } catch {
    throw new ApiError(
      "backend-unavailable",
      "Can't reach the recognition server right now.",
    );
  }

  if (!response.ok) {
    if (response.status === 503) {
      throw new ApiError(
        "model-loading-failed",
        "The recognition model is still starting up.",
      );
    }
    throw new ApiError(
      "prediction-unavailable",
      "The recognition server returned an unexpected response.",
    );
  }

  try {
    return (await response.json()) as T;
  } catch {
    // Some endpoints (e.g. /action) may legitimately return no body.
    return undefined as T;
  }
}

export const api = {
  get: <T>(path: string) => request<T>(path, { method: "GET" }),
  post: <T>(path: string, body?: unknown) =>
    request<T>(path, {
      method: "POST",
      body: body !== undefined ? JSON.stringify(body) : undefined,
    }),
};
