/** Base URL of the existing Python backend. Override via VITE_API_BASE_URL. */
export const API_BASE_URL: string =
  (import.meta.env.VITE_API_BASE_URL as string | undefined) ??
  "http://localhost:5000";

/** How often the frontend polls the backend for a fresh prediction. */
export const PREDICTION_POLL_INTERVAL_MS = 400;

/** How often the frontend polls the backend for the generated text. */
export const TEXT_POLL_INTERVAL_MS = 800;

export const GITHUB_URL =
  "https://github.com/your-org/sign-language-recognition";

export const DOCS_URL = "/docs";
