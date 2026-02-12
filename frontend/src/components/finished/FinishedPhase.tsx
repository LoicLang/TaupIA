"use client";

import { useRouter } from "next/navigation";
import {
  Trophy,
  BarChart3,
  BookOpen,
  GraduationCap,
  ArrowRight,
  AlertTriangle,
  CheckCircle,
  Info,
} from "lucide-react";
import { cn } from "@/lib/utils";
import type { FinishResponse } from "@/lib/types";

interface FinishedPhaseProps {
  results: FinishResponse;
}

export default function FinishedPhase({ results }: FinishedPhaseProps) {
  const router = useRouter();
  const avg = results.average_score;

  const level =
    avg >= 80
      ? { color: "emerald", icon: CheckCircle, label: "Excellent", message: "Tu maîtrises bien ce chapitre." }
      : avg >= 60
      ? { color: "amber", icon: Info, label: "Correct", message: "Quelques points restent à consolider." }
      : { color: "red", icon: AlertTriangle, label: "À retravailler", message: "Il faut revoir les fondamentaux de ce chapitre." };

  return (
    <div className="w-full max-w-2xl mx-auto space-y-8">
      {/* Score Card */}
      <div className="rounded-2xl border border-white/10 bg-white/[0.02] backdrop-blur-md p-1">
        <div className="bg-[#0f0f0f] rounded-xl overflow-hidden border border-white/5 p-5 sm:p-8 text-center">
          <Trophy className="w-10 h-10 text-indigo-400 mx-auto mb-4" />
          <h2 className="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-b from-white to-white/60 mb-2">
            Kholle terminée
          </h2>

          {/* Average Score */}
          <div className="mt-6 mb-8">
            <div
              className={cn(
                "inline-flex items-center gap-2 px-6 py-3 rounded-full text-lg font-bold border",
                avg >= 80
                  ? "bg-emerald-500/10 text-emerald-400 border-emerald-500/20"
                  : avg >= 60
                  ? "bg-amber-500/10 text-amber-400 border-amber-500/20"
                  : "bg-red-500/10 text-red-400 border-red-500/20"
              )}
            >
              <level.icon className="w-5 h-5" />
              {avg.toFixed(1)}/100
            </div>
          </div>

          {/* Feedback */}
          <div
            className={cn(
              "p-4 rounded-xl border text-sm text-left",
              avg >= 80
                ? "bg-emerald-500/5 border-emerald-500/20 text-emerald-300"
                : avg >= 60
                ? "bg-amber-500/5 border-amber-500/20 text-amber-300"
                : "bg-red-500/5 border-red-500/20 text-red-300"
            )}
          >
            <p className="font-semibold mb-1">{level.label}</p>
            <p className="text-white/50">{level.message}</p>
          </div>

          {/* Stats */}
          <div className="grid grid-cols-3 gap-2 sm:gap-4 mt-8">
            <div className="p-4 rounded-xl bg-white/[0.03] border border-white/5">
              <BarChart3 className="w-4 h-4 text-indigo-400 mx-auto mb-2" />
              <p className="text-lg font-bold text-white/90">{avg.toFixed(1)}</p>
              <p className="text-[11px] sm:text-[10px] font-bold text-white/30 uppercase tracking-wider">
                Score moyen
              </p>
            </div>
            <div className="p-4 rounded-xl bg-white/[0.03] border border-white/5">
              <BookOpen className="w-4 h-4 text-indigo-400 mx-auto mb-2" />
              <p className="text-lg font-bold text-white/90">
                {results.question_count}
              </p>
              <p className="text-[11px] sm:text-[10px] font-bold text-white/30 uppercase tracking-wider">
                Questions
              </p>
            </div>
            <div className="p-4 rounded-xl bg-white/[0.03] border border-white/5">
              <GraduationCap className="w-4 h-4 text-indigo-400 mx-auto mb-2" />
              <p className="text-lg font-bold text-white/90">
                {results.exercise_count}
              </p>
              <p className="text-[11px] sm:text-[10px] font-bold text-white/30 uppercase tracking-wider">
                Exercices
              </p>
            </div>
          </div>

          {/* Individual scores */}
          {results.scores.length > 0 && (
            <div className="mt-6 space-y-2">
              <p className="text-[10px] font-bold text-white/30 uppercase tracking-wider text-left">
                Scores par question
              </p>
              <div className="flex gap-2 flex-wrap">
                {results.scores.map((s, i) => (
                  <div
                    key={i}
                    className={cn(
                      "px-3 py-1.5 rounded-lg text-[11px] font-bold border",
                      s >= 75
                        ? "bg-emerald-500/10 text-emerald-400 border-emerald-500/20"
                        : s >= 50
                        ? "bg-amber-500/10 text-amber-400 border-amber-500/20"
                        : "bg-red-500/10 text-red-400 border-red-500/20"
                    )}
                  >
                    Q{i + 1}: {s}/100
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>

      {/* New Session Button */}
      <button
        onClick={() => router.push("/")}
        className="w-full group flex items-center justify-center gap-2 px-8 py-4 sm:py-3.5 bg-white text-black font-semibold text-sm rounded-full hover:shadow-[0_0_20px_rgba(255,255,255,0.3)] hover:scale-[1.02] active:scale-95 transition-all min-h-[48px]"
      >
        Nouvelle session
        <ArrowRight className="w-4 h-4 transition-transform group-hover:translate-x-1" />
      </button>
    </div>
  );
}
