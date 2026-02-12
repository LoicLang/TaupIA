// Client API type pour le backend FastAPI

import type {
  Session,
  Chapter,
  StartKholleRequest,
  StartKholleResponse,
  AnswerRequest,
  AnswerResponse,
  ExerciseMessageRequest,
  ExerciseMessageResponse,
  NextExerciseResponse,
  SkipResponse,
  FinishResponse,
  ProviderInfo,
} from "./types";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
const DEFAULT_TIMEOUT = 60_000; // 60s — les appels LLM peuvent etre lents

// --- Auth token ---

type TokenGetter = () => Promise<string | null>;
let _getAuthToken: TokenGetter | null = null;

/**
 * Enregistre un getter de token Clerk.
 * Appele une fois dans AuthProvider (layout).
 */
export function setAuthTokenGetter(getter: TokenGetter) {
  _getAuthToken = getter;
}

// --- Request helper ---

async function request<T>(
  path: string,
  options?: RequestInit & { timeout?: number }
): Promise<T> {
  const { timeout = DEFAULT_TIMEOUT, ...fetchOptions } = options || {};

  // Recuperer le token Clerk si disponible
  let token: string | null = null;
  if (_getAuthToken) {
    try {
      token = await _getAuthToken();
    } catch {
      // Pas de token (dev local sans Clerk)
    }
  }

  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
  };

  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeout);

  try {
    const res = await fetch(`${API_URL}${path}`, {
      headers,
      signal: controller.signal,
      ...fetchOptions,
    });
    if (!res.ok) {
      const body = await res.json().catch(() => ({}));
      throw new Error(body.detail || `Erreur ${res.status}`);
    }
    return res.json();
  } catch (e) {
    if (e instanceof DOMException && e.name === "AbortError") {
      throw new Error("Le serveur met trop de temps a repondre. Reessaie.");
    }
    if (e instanceof TypeError && e.message.includes("fetch")) {
      throw new Error("Impossible de contacter le serveur. Verifie que le backend est lance.");
    }
    throw e;
  } finally {
    clearTimeout(timer);
  }
}

// --- Chapters ---

export function getChapters(): Promise<Chapter[]> {
  return request("/api/chapters");
}

// --- Providers ---

export function getLlmProviders(): Promise<string[]> {
  return request("/api/providers/llm");
}

export function getOcrProviders(): Promise<string[]> {
  return request("/api/providers/ocr");
}

// --- Sessions ---

export function createSession(): Promise<Session> {
  return request("/api/sessions", { method: "POST" });
}

export function getSession(sessionId: string): Promise<Session> {
  return request(`/api/sessions/${sessionId}`);
}

export function deleteSession(sessionId: string): Promise<void> {
  return request(`/api/sessions/${sessionId}`, { method: "DELETE" });
}

// --- Kholle Flow ---

export function startKholle(
  sessionId: string,
  data: StartKholleRequest
): Promise<StartKholleResponse> {
  return request(`/api/sessions/${sessionId}/start`, {
    method: "POST",
    body: JSON.stringify(data),
  });
}

export function submitAnswer(
  sessionId: string,
  data: AnswerRequest
): Promise<AnswerResponse> {
  return request(`/api/sessions/${sessionId}/answer`, {
    method: "POST",
    body: JSON.stringify(data),
    timeout: 90_000, // LLM evaluation peut etre lente
  });
}

export function forceValidate(
  sessionId: string
): Promise<{ question_validated: boolean }> {
  return request(`/api/sessions/${sessionId}/force-validate`, {
    method: "POST",
  });
}

export function nextExercise(
  sessionId: string
): Promise<NextExerciseResponse> {
  return request(`/api/sessions/${sessionId}/next-exercise`, {
    method: "POST",
  });
}

export function exerciseMessage(
  sessionId: string,
  data: ExerciseMessageRequest
): Promise<ExerciseMessageResponse> {
  return request(`/api/sessions/${sessionId}/exercise/message`, {
    method: "POST",
    body: JSON.stringify(data),
    timeout: 90_000,
  });
}

export function finishKholle(sessionId: string): Promise<FinishResponse> {
  return request(`/api/sessions/${sessionId}/finish`, { method: "POST" });
}

export function skipCurrent(sessionId: string): Promise<SkipResponse> {
  return request(`/api/sessions/${sessionId}/skip`, { method: "POST" });
}

// --- OCR ---

export async function transcribeImage(
  file: File,
  ocrProvider: string = "kimi"
): Promise<{ text: string }> {
  // Recuperer le token Clerk si disponible
  let token: string | null = null;
  if (_getAuthToken) {
    try {
      token = await _getAuthToken();
    } catch {
      // Pas de token
    }
  }

  const formData = new FormData();
  formData.append("file", file);
  formData.append("ocr_provider", ocrProvider);

  const headers: Record<string, string> = {
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
  };

  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), 60_000);

  try {
    const res = await fetch(`${API_URL}/api/ocr/transcribe`, {
      method: "POST",
      body: formData,
      headers,
      signal: controller.signal,
    });
    if (!res.ok) {
      const body = await res.json().catch(() => ({}));
      throw new Error(body.detail || `Erreur OCR ${res.status}`);
    }
    return res.json();
  } catch (e) {
    if (e instanceof DOMException && e.name === "AbortError") {
      throw new Error("La transcription met trop de temps. Reessaie.");
    }
    if (e instanceof TypeError && e.message.includes("fetch")) {
      throw new Error("Impossible de contacter le serveur.");
    }
    throw e;
  } finally {
    clearTimeout(timer);
  }
}
