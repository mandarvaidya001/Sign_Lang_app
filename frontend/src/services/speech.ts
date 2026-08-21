import { predictionService } from "@/services/prediction";
import type { SpeechStatus } from "@/types";

/**
 * The backend owns text-to-speech (see 06_Backend_API_Architecture.md).
 * When the user presses Enter, the backend finalizes the text and speaks
 * it. The frontend's only job is to reflect that status ("Speaking...",
 * "Ready") — never to generate its own speech.
 *
 * `getSpeechStatus` is a thin pass-through over the backend status
 * endpoint so components don't need to know the shape of that response.
 */
export const speechService = {
  async getSpeechStatus(): Promise<SpeechStatus> {
    const status = await predictionService.getStatus();
    return status.speechStatus;
  },
};
