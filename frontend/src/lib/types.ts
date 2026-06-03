// Types TypeScript — miroir de backend/schemas/session.py

export interface Session {
  id: string;
  phase: "setup" | "question_cours" | "exercice" | "finished";
  chapter_id: string | null;
  difficulty: number;
  ai_provider: string;
  ocr_provider: string;
  format: "full" | "exercise_only";
  current_question: Question | null;
  current_exercise: Exercise | null;
  conversation_history: ChatMessage[];
  question_validated: boolean;
  scores: number[];
}

export interface Question {
  id: string;
  question_raw: string;
  chapter_id: string;
  difficulty: number;
  attendus_json?: string;
  erreurs_frequentes_json?: string;
  relances_prof_json?: string;
  [key: string]: unknown;
}

export interface Exercise {
  id: string;
  enonce: string;
  indications?: string;
  correction?: string;
  difficulty?: number;
  chapter_id?: string;
  [key: string]: unknown;
}

export interface ChatMessage {
  role: "user" | "assistant";
  content: string;
}

export interface Chapter {
  id: string;
  title: string;
  question_count: number;
  semestre?: number;
  importance?: number;
  difficulties?: number[];
}

// --- Request types ---

export interface StartKholleRequest {
  chapter_id: string;
  difficulty: number;
  ai_provider: string;
  ocr_provider: string;
  format: "full" | "exercise_only";
}

export interface AnswerRequest {
  answer: string;
}

export interface ExerciseMessageRequest {
  message: string;
}

// --- Response types ---

export interface StartKholleResponse {
  phase: string;
  question: Question | null;
  exercise: Exercise | null;
}

export interface AnswerResponse {
  feedback: string;
  is_complete: boolean;
  score: number;
  missing_points: string[];
  question_validated: boolean;
  conversation_history: ChatMessage[];
  debug_prompt_data?: {
    system_prompt: string;
    user_prompt: string;
  } | null;
}

export interface ExerciseMessageResponse {
  guidance: string;
  conversation_history: ChatMessage[];
  // Set when the agent switched the exercise mid-conversation (deviation).
  exercise?: Exercise | null;
}

export interface NextExerciseResponse {
  phase: string;
  exercise: Exercise | null;
}

export interface SkipResponse {
  phase: string;
  question: Question | null;
  exercise: Exercise | null;
}

export interface FinishResponse {
  phase: string;
  scores: number[];
  average_score: number;
  question_count: number;
  exercise_count: number;
}

export interface ProviderInfo {
  id: string;
  name: string;
  available: boolean;
}
