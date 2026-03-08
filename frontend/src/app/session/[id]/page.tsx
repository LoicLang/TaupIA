"use client";

import { useState, useEffect, useCallback } from "react";
import { useParams, useRouter } from "next/navigation";
import { Loader2, ArrowLeft, AlertTriangle } from "lucide-react";
import { GridBackground, GlowOrbs } from "@/components/shared/GridBackground";
import QuestionPhase from "@/components/question/QuestionPhase";
import ExercisePhase from "@/components/exercise/ExercisePhase";
import FinishedPhase from "@/components/finished/FinishedPhase";
import { getSession, nextExercise, finishKholle, skipCurrent } from "@/lib/api";
import type { Session, FinishResponse, Exercise } from "@/lib/types";

// --- Progress Steps ---

const STEPS_FULL = [
  { key: "setup", label: "Setup" },
  { key: "question_cours", label: "Question" },
  { key: "exercice", label: "Exercice" },
  { key: "finished", label: "Résultats" },
];

const STEPS_EXERCISE_ONLY = [
  { key: "setup", label: "Setup" },
  { key: "exercice", label: "Exercice" },
  { key: "finished", label: "Résultats" },
];

function ProgressBar({ phase, format }: { phase: string; format: string }) {
  const steps = format === "exercise_only" ? STEPS_EXERCISE_ONLY : STEPS_FULL;
  const currentIndex = steps.findIndex((s) => s.key === phase);

  return (
    <div className="flex items-center gap-1 w-full max-w-md mx-auto">
      {steps.map((step, i) => (
        <div key={step.key} className="flex items-center flex-1">
          <div className="flex flex-col items-center flex-1">
            <div
              className={`h-1 w-full rounded-full transition-all ${
                i <= currentIndex
                  ? "bg-indigo-500"
                  : "bg-white/10"
              }`}
            />
            <span
              className={`text-[10px] sm:text-[9px] mt-1.5 font-bold uppercase tracking-wider ${
                i <= currentIndex ? "text-indigo-400" : "text-white/20"
              }`}
            >
              {step.label}
            </span>
          </div>
        </div>
      ))}
    </div>
  );
}

// --- Main Page ---

export default function SessionPage() {
  const params = useParams();
  const router = useRouter();
  const sessionId = params.id as string;

  const [session, setSession] = useState<Session | null>(null);
  const [exercise, setExercise] = useState<Exercise | null>(null);
  const [finishResults, setFinishResults] = useState<FinishResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [fatalError, setFatalError] = useState<string | null>(null);
  const [transitionError, setTransitionError] = useState<string | null>(null);
  const [transitioning, setTransitioning] = useState(false);

  // Load session
  useEffect(() => {
    async function load() {
      try {
        const s = await getSession(sessionId);
        setSession(s);
        if (s.current_exercise) setExercise(s.current_exercise);
      } catch (e) {
        setFatalError(e instanceof Error ? e.message : "Session introuvable");
      } finally {
        setLoading(false);
      }
    }
    load();
  }, [sessionId]);

  // Handle transition to exercise
  const handleNextExercise = useCallback(async () => {
    setTransitioning(true);
    setTransitionError(null);
    try {
      const res = await nextExercise(sessionId);
      if (res.phase === "finished" || !res.exercise) {
        const finish = await finishKholle(sessionId);
        setFinishResults(finish);
        setSession((prev) => prev ? { ...prev, phase: "finished" } : prev);
      } else {
        setExercise(res.exercise);
        setSession((prev) => prev ? { ...prev, phase: "exercice" } : prev);
      }
    } catch (e) {
      setTransitionError(e instanceof Error ? e.message : "Erreur lors de la transition");
    } finally {
      setTransitioning(false);
    }
  }, [sessionId]);

  // Handle finish
  const handleFinish = useCallback(async () => {
    setTransitioning(true);
    setTransitionError(null);
    try {
      const res = await finishKholle(sessionId);
      setFinishResults(res);
      setSession((prev) => prev ? { ...prev, phase: "finished" } : prev);
    } catch (e) {
      setTransitionError(e instanceof Error ? e.message : "Erreur lors de la finalisation");
    } finally {
      setTransitioning(false);
    }
  }, [sessionId]);

  // Handle skip (new question or exercise)
  const handleSkip = useCallback(async () => {
    setTransitioning(true);
    setTransitionError(null);
    try {
      const res = await skipCurrent(sessionId);
      if (res.phase === "finished") {
        const finish = await finishKholle(sessionId);
        setFinishResults(finish);
        setSession((prev) => prev ? { ...prev, phase: "finished" } : prev);
      } else if (res.phase === "question_cours" && res.question) {
        setSession((prev) =>
          prev
            ? { ...prev, phase: "question_cours", current_question: res.question, conversation_history: [], question_validated: false }
            : prev
        );
      } else if (res.phase === "exercice" && res.exercise) {
        setExercise(res.exercise);
        setSession((prev) => prev ? { ...prev, phase: "exercice", conversation_history: [] } : prev);
      }
    } catch (e) {
      setTransitionError(e instanceof Error ? e.message : "Erreur lors du skip");
    } finally {
      setTransitioning(false);
    }
  }, [sessionId]);

  // Loading state
  if (loading) {
    return (
      <div className="relative min-h-screen flex items-center justify-center bg-[#0a0a0a]">
        <GridBackground />
        <GlowOrbs />
        <div className="relative z-10 flex items-center gap-3">
          <Loader2 className="w-6 h-6 text-indigo-400 animate-spin" />
          <span className="text-sm text-white/40">Chargement de la session...</span>
        </div>
      </div>
    );
  }

  // Fatal error state (session not found, etc.)
  if (fatalError || !session) {
    return (
      <div className="relative min-h-screen flex items-center justify-center bg-[#0a0a0a]">
        <GridBackground />
        <GlowOrbs />
        <div className="relative z-10 text-center space-y-4">
          <AlertTriangle className="w-8 h-8 text-red-400 mx-auto" />
          <p className="text-red-400 text-sm">{fatalError || "Session introuvable"}</p>
          <button
            onClick={() => router.push("/setup")}
            className="flex items-center gap-2 px-5 py-3 sm:px-4 sm:py-2 mx-auto text-sm text-white/60 border border-white/10 rounded-full hover:bg-white/5 transition-all min-h-[44px]"
          >
            <ArrowLeft className="w-4 h-4" />
            Retour à l&apos;accueil
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="relative min-h-screen bg-[#0a0a0a] text-white font-sans antialiased overflow-hidden">
      <GridBackground />
      <GlowOrbs />

      {/* Transition overlay — covers content but doesn't destroy it */}
      {transitioning && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-[#0a0a0a]/80 backdrop-blur-sm">
          <div className="flex items-center gap-3">
            <Loader2 className="w-6 h-6 text-indigo-400 animate-spin" />
            <span className="text-sm text-white/40">Passage à la suite...</span>
          </div>
        </div>
      )}

      <div className="relative z-10 max-w-4xl mx-auto px-4 sm:px-6 py-6 sm:py-8">
        {/* Header */}
        <div className="flex items-center justify-between mb-6">
          <button
            onClick={() => router.push("/setup")}
            className="flex items-center gap-1.5 text-xs sm:text-[11px] font-medium text-white/30 hover:text-white/60 transition-colors py-2 sm:py-0"
          >
            <ArrowLeft className="w-3 h-3" />
            Accueil
          </button>
          <h1 className="text-lg font-bold tracking-tight">
            Taup<span className="text-indigo-500">IA</span>
          </h1>
          <div className="w-16" /> {/* Spacer for centering */}
        </div>

        {/* Progress */}
        <div className="mb-10">
          <ProgressBar phase={session.phase} format={session.format} />
        </div>

        {/* Transition Error Banner */}
        {transitionError && (
          <div className="mb-6 flex items-center gap-2 p-3 rounded-xl bg-red-500/10 border border-red-500/20 text-red-400 text-sm">
            <AlertTriangle className="w-4 h-4 flex-shrink-0" />
            <span className="flex-1">{transitionError}</span>
            <button
              onClick={() => setTransitionError(null)}
              className="text-red-400/60 hover:text-red-400 text-xs font-medium"
            >
              Fermer
            </button>
          </div>
        )}

        {/* Phase Content with fade-in animation */}
        <div key={session.phase} className="animate-fade-in-up">
          {session.phase === "question_cours" && session.current_question && (
            <QuestionPhase
              key={session.current_question.id}
              sessionId={sessionId}
              question={session.current_question}
              ocrProvider={session.ocr_provider}
              onNextExercise={handleNextExercise}
              onSkip={handleSkip}
            />
          )}

          {session.phase === "exercice" && exercise && (
            <ExercisePhase
              key={exercise.id}
              sessionId={sessionId}
              exercise={exercise}
              ocrProvider={session.ocr_provider}
              onFinish={handleFinish}
              onSkip={handleSkip}
            />
          )}

          {session.phase === "finished" && finishResults && (
            <FinishedPhase results={finishResults} />
          )}
        </div>
      </div>
    </div>
  );
}
