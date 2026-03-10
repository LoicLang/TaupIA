"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import {
  ChevronRight,
  Terminal,
  BookOpen,
  GraduationCap,
  ListChecks,
  Loader2,
} from "lucide-react";
import { cn } from "@/lib/utils";
import {
  getChapters,
  getLlmProviders,
  getOcrProviders,
  createSession,
  startKholle,
} from "@/lib/api";
import type { Chapter } from "@/lib/types";

// --- Background components ---

function GridBackground() {
  return (
    <div className="absolute inset-0 z-0 overflow-hidden pointer-events-none">
      <div
        className="absolute inset-0 opacity-[0.15]"
        style={{
          backgroundImage: `linear-gradient(#4f46e5 1px, transparent 1px), linear-gradient(90deg, #4f46e5 1px, transparent 1px)`,
          backgroundSize: "40px 40px",
          maskImage:
            "radial-gradient(ellipse 60% 50% at 50% 0%, #000 30%, transparent 100%)",
          WebkitMaskImage:
            "radial-gradient(ellipse 60% 50% at 50% 0%, #000 30%, transparent 100%)",
        }}
      />
      <div className="absolute inset-0 bg-gradient-to-b from-transparent via-[#0a0a0a]/50 to-[#0a0a0a]" />
    </div>
  );
}

function GlowOrbs() {
  return (
    <div className="absolute inset-0 z-0 pointer-events-none overflow-hidden">
      <div className="absolute -top-[10%] left-[20%] w-[40%] h-[40%] rounded-full bg-indigo-600/20 blur-[120px]" />
      <div className="absolute top-[10%] right-[20%] w-[30%] h-[30%] rounded-full bg-blue-600/10 blur-[100px]" />
    </div>
  );
}

function formatChapterTitle(title: string): string {
  const trimmed = title.trim();
  if (!trimmed) {
    return trimmed;
  }

  const lettersOnly = trimmed.replace(/[^A-Za-zÀ-ÖØ-öø-ÿ]/g, "");
  const isMostlyUppercase =
    lettersOnly.length > 0 && lettersOnly === lettersOnly.toUpperCase();

  if (!isMostlyUppercase) {
    return trimmed;
  }

  return trimmed
    .toLowerCase()
    .replace(/\b([a-zà-öø-ÿ])/g, (match) => match.toUpperCase())
    .replace(/\bR\b/g, "R")
    .replace(/\bC\b/g, "C")
    .replace(/\bN\b/g, "N");
}

// --- Main Page ---

export default function SetupPage() {
  const router = useRouter();

  // Data from API
  const [chapters, setChapters] = useState<Chapter[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Form state
  const [chapterId, setChapterId] = useState("");
  const [difficulty, setDifficulty] = useState(3);
  const [aiProvider, setAiProvider] = useState("deepseek");
  const [ocrProvider, setOcrProvider] = useState("kimi");
  const [format, setFormat] = useState<"full" | "exercise_only">("full");
  const [starting, setStarting] = useState(false);

  // Load data
  useEffect(() => {
    async function load() {
      try {
        const [ch, llm, ocr] = await Promise.all([
          getChapters(),
          getLlmProviders(),
          getOcrProviders(),
        ]);
        setChapters(ch);

        if (ch.length > 0) setChapterId(ch[0].id);
        // Defaults: deepseek pour LLM, kimi pour OCR (fallback au premier dispo)
        if (llm.length > 0) setAiProvider(llm.includes("deepseek") ? "deepseek" : llm[0]);
        if (ocr.length > 0) setOcrProvider(ocr.includes("kimi") ? "kimi" : ocr[0]);
      } catch (e) {
        setError(
          e instanceof Error ? e.message : "Impossible de contacter le serveur"
        );
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  // Start kholle
  async function handleStart() {
    if (!chapterId) return;
    setStarting(true);
    setError(null);
    try {
      const session = await createSession();
      await startKholle(session.id, {
        chapter_id: chapterId,
        difficulty,
        ai_provider: aiProvider,
        ocr_provider: ocrProvider,
        format,
      });
      router.push(`/session/${session.id}`);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Erreur au demarrage");
      setStarting(false);
    }
  }

  return (
    <div className="relative min-h-screen flex flex-col items-center justify-center bg-[#0a0a0a] text-white font-sans antialiased overflow-hidden">
      <GridBackground />
      <GlowOrbs />

      <div className="relative z-10 flex flex-col items-center text-center px-4 sm:px-6 max-w-2xl w-full">
        {/* Badge */}
        <span className="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-indigo-500/20 bg-indigo-500/5 text-[11px] font-bold tracking-[0.15em] uppercase text-indigo-400 mb-6">
          <span className="relative flex h-2 w-2">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-indigo-400 opacity-75" />
            <span className="relative inline-flex rounded-full h-2 w-2 bg-indigo-500" />
          </span>
          Simulateur MPSI
        </span>

        {/* Title */}
        <h1 className="text-5xl md:text-6xl font-bold tracking-tight mb-3 bg-clip-text text-transparent bg-gradient-to-b from-white to-white/60 leading-[1.1]">
          Taup<span className="text-indigo-500">IA</span>
        </h1>
        <p className="text-base text-white/50 max-w-md mb-10 font-medium leading-relaxed">
          Configure ta session de kholle et lance-toi.
        </p>

        {/* Setup Card */}
        <div className="w-full rounded-2xl border border-white/10 bg-white/[0.02] backdrop-blur-md p-1">
          <div className="bg-[#0f0f0f] rounded-xl overflow-hidden border border-white/5">
            {/* Header Bar */}
            <div className="flex items-center justify-between px-6 py-3 border-b border-white/5 bg-white/[0.01]">
              <div className="flex items-center gap-4">
                <div className="flex gap-1.5">
                  <div className="w-2.5 h-2.5 rounded-full bg-white/10" />
                  <div className="w-2.5 h-2.5 rounded-full bg-white/10" />
                  <div className="w-2.5 h-2.5 rounded-full bg-white/10" />
                </div>
                <div className="flex items-center gap-2 text-[11px] font-mono text-white/40">
                  <Terminal className="w-3 h-3" />
                  configuration.toml
                </div>
              </div>
              <div className="px-2 py-1 rounded bg-indigo-500/10 text-[10px] font-mono text-indigo-400 border border-indigo-500/20">
                SETUP
              </div>
            </div>

            {/* Form Content */}
            <div className="p-6 md:p-8 space-y-6">
              {loading ? (
                <div className="flex items-center justify-center py-12">
                  <Loader2 className="w-6 h-6 text-indigo-400 animate-spin" />
                  <span className="ml-3 text-sm text-white/40">
                    Chargement...
                  </span>
                </div>
              ) : (
                <>
                  {/* Chapter Select */}
                  <div className="space-y-2 text-left">
                    <label className="text-xs sm:text-[11px] font-bold text-indigo-400 uppercase tracking-wider flex items-center gap-2">
                      <BookOpen className="w-3.5 h-3.5 sm:w-3 sm:h-3" />
                      Chapitre
                    </label>
                    <select
                      value={chapterId}
                      onChange={(e) => setChapterId(e.target.value)}
                      className="w-full bg-white/[0.03] border border-white/10 rounded-xl px-4 py-3 text-sm text-white/90 focus:outline-none focus:border-indigo-500/50 focus:ring-1 focus:ring-indigo-500/20 appearance-none cursor-pointer"
                    >
                      {chapters.map((ch) => (
                        <option
                          key={ch.id}
                          value={ch.id}
                          className="bg-[#0f0f0f] text-white"
                        >
                          {formatChapterTitle(ch.title)}
                        </option>
                      ))}
                    </select>
                  </div>

                  {/* Difficulty */}
                  <div className="space-y-2 text-left">
                    <label className="text-xs sm:text-[11px] font-bold text-indigo-400 uppercase tracking-wider flex items-center gap-2">
                      <GraduationCap className="w-3.5 h-3.5 sm:w-3 sm:h-3" />
                      Difficulté ({difficulty}/5)
                    </label>
                    <div className="flex gap-2">
                      {[1, 2, 3, 4, 5].map((d) => (
                        <button
                          key={d}
                          onClick={() => setDifficulty(d)}
                          className={cn(
                            "flex-1 py-2.5 rounded-lg text-sm font-semibold transition-all",
                            d === difficulty
                              ? "bg-indigo-600 text-white shadow-lg shadow-indigo-500/20"
                              : "bg-white/[0.03] text-white/50 border border-white/10 hover:bg-white/[0.06]"
                          )}
                        >
                          {d}
                        </button>
                      ))}
                    </div>
                  </div>

                  {/* Format */}
                  <div className="space-y-2 text-left">
                    <label className="text-xs sm:text-[11px] font-bold text-indigo-400 uppercase tracking-wider flex items-center gap-2">
                      <ListChecks className="w-3.5 h-3.5 sm:w-3 sm:h-3" />
                      Format
                    </label>
                    <div className="grid grid-cols-2 gap-2">
                      <button
                        onClick={() => setFormat("full")}
                        className={cn(
                          "py-2.5 px-3 rounded-lg text-sm font-medium transition-all text-left",
                          format === "full"
                            ? "bg-indigo-600 text-white shadow-lg shadow-indigo-500/20"
                            : "bg-white/[0.03] text-white/50 border border-white/10 hover:bg-white/[0.06]"
                        )}
                      >
                        Question + Exercice
                      </button>
                      <button
                        onClick={() => setFormat("exercise_only")}
                        className={cn(
                          "py-2.5 px-3 rounded-lg text-sm font-medium transition-all text-left",
                          format === "exercise_only"
                            ? "bg-indigo-600 text-white shadow-lg shadow-indigo-500/20"
                            : "bg-white/[0.03] text-white/50 border border-white/10 hover:bg-white/[0.06]"
                        )}
                      >
                        Exercice seul
                      </button>
                    </div>
                  </div>

                  {/* Error */}
                  {error && (
                    <div className="p-3 rounded-lg bg-red-500/10 border border-red-500/20 text-red-400 text-sm">
                      {error}
                    </div>
                  )}

                  {/* Start Button */}
                  <button
                    onClick={handleStart}
                    disabled={!chapterId || starting}
                    className={cn(
                      "w-full group flex items-center justify-center gap-2 px-8 py-4 sm:py-3.5 font-semibold text-sm rounded-full transition-all min-h-[48px]",
                      starting || !chapterId
                        ? "bg-white/10 text-white/30 cursor-not-allowed"
                        : "bg-white text-black hover:shadow-[0_0_20px_rgba(255,255,255,0.3)] hover:scale-[1.02] active:scale-95"
                    )}
                  >
                    {starting ? (
                      <>
                        <Loader2 className="w-4 h-4 animate-spin" />
                        Démarrage...
                      </>
                    ) : (
                      <>
                        Commencer la kholle
                        <ChevronRight className="w-4 h-4 transition-transform group-hover:translate-x-1" />
                      </>
                    )}
                  </button>
                </>
              )}
            </div>
          </div>
        </div>

        {/* Footer */}
        <p className="mt-8 text-[11px] text-white/20">
          TaupIA — Simulateur de kholles pour CPGE scientifiques
        </p>
      </div>
    </div>
  );
}
