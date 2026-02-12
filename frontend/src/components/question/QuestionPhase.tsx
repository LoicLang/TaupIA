"use client";

import { useState, useRef, useEffect } from "react";
import {
  Terminal,
  Send,
  Camera,
  ArrowRight,
  Loader2,
  CheckCircle,
  XCircle,
  Cpu,
  ChevronRight,
  AlertTriangle,
  SkipForward,
} from "lucide-react";
import { cn } from "@/lib/utils";
import { submitAnswer, forceValidate, transcribeImage } from "@/lib/api";
import LatexRenderer from "@/components/shared/LatexRenderer";
import type {
  Question,
  ChatMessage,
  AnswerResponse,
} from "@/lib/types";

interface QuestionPhaseProps {
  sessionId: string;
  question: Question;
  ocrProvider: string;
  onNextExercise: () => void;
  onSkip: () => void;
}

export default function QuestionPhase({
  sessionId,
  question,
  ocrProvider,
  onNextExercise,
  onSkip,
}: QuestionPhaseProps) {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [lastEval, setLastEval] = useState<AnswerResponse | null>(null);
  const [validated, setValidated] = useState(false);
  const [transcribing, setTranscribing] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const chatEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll chat on new messages
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  async function handleSubmit() {
    if (!input.trim() || loading) return;
    const answer = input.trim();
    setInput("");
    setLoading(true);

    setError(null);
    // Optimistic: add user message
    setMessages((prev) => [...prev, { role: "user", content: answer }]);

    try {
      const res = await submitAnswer(sessionId, { answer });
      setMessages(res.conversation_history);
      setLastEval(res);
      if (res.question_validated) setValidated(true);
    } catch (e) {
      // Remove optimistic message on error
      setMessages((prev) => prev.slice(0, -1));
      setError(e instanceof Error ? e.message : "Erreur lors de l'évaluation");
      setInput(answer); // Restore input so user can retry
    } finally {
      setLoading(false);
    }
  }

  async function handleForceValidate() {
    try {
      await forceValidate(sessionId);
      setValidated(true);
    } catch {}
  }

  async function handlePhotoUpload(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0];
    if (!file) return;
    setTranscribing(true);
    setError(null);
    try {
      const res = await transcribeImage(file, ocrProvider);
      setInput((prev) => (prev ? prev + "\n" + res.text : res.text));
    } catch (e) {
      setError(e instanceof Error ? e.message : "Erreur lors de la transcription");
    }
    setTranscribing(false);
    if (fileInputRef.current) fileInputRef.current.value = "";
  }

  function handleKeyDown(e: React.KeyboardEvent<HTMLTextAreaElement>) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  }

  return (
    <div className="w-full max-w-3xl mx-auto space-y-6">
      {/* Question Card */}
      <div className="rounded-2xl border border-white/10 bg-white/[0.02] backdrop-blur-md p-1">
        <div className="bg-[#0f0f0f] rounded-xl overflow-hidden border border-white/5">
          <div className="flex items-center justify-between px-4 sm:px-6 py-3 border-b border-white/5 bg-white/[0.01]">
            <div className="flex items-center gap-3 sm:gap-4">
              <div className="hidden sm:flex gap-1.5">
                <div className="w-2.5 h-2.5 rounded-full bg-white/10" />
                <div className="w-2.5 h-2.5 rounded-full bg-white/10" />
                <div className="w-2.5 h-2.5 rounded-full bg-white/10" />
              </div>
              <div className="flex items-center gap-2 text-xs sm:text-[11px] font-mono text-white/40">
                <Terminal className="w-3 h-3" />
                question_cours.tex
              </div>
            </div>
            <div className="px-2 py-1 rounded bg-indigo-500/10 text-[10px] font-mono text-indigo-400 border border-indigo-500/20">
              QUESTION
            </div>
          </div>
          <div className="p-4 sm:p-6">
            <LatexRenderer
              content={question.question_raw}
              className="text-white/90 leading-relaxed prose-invert prose-sm"
            />
          </div>
        </div>
      </div>

      {/* Chat History */}
      {messages.length > 0 && (
        <div className="space-y-4">
          {messages.map((msg, i) => (
            <div
              key={i}
              className={cn(
                "flex",
                msg.role === "user" ? "justify-end" : "justify-start"
              )}
            >
              <div
                className={cn(
                  "max-w-[85%] rounded-2xl px-4 py-3 text-sm",
                  msg.role === "user"
                    ? "bg-indigo-600 text-white rounded-br-md"
                    : "bg-white/[0.03] border border-white/10 text-white/80 rounded-bl-md"
                )}
              >
                <LatexRenderer content={msg.content} className="prose-invert prose-sm" />
              </div>
            </div>
          ))}
          {loading && (
            <div className="flex justify-start">
              <div className="bg-white/[0.03] border border-white/10 rounded-2xl rounded-bl-md px-4 py-3">
                <Loader2 className="w-4 h-4 text-indigo-400 animate-spin" />
              </div>
            </div>
          )}
          <div ref={chatEndRef} />
        </div>
      )}

      {/* Evaluation Feedback */}
      {lastEval && !loading && (
        <div className="p-4 rounded-xl bg-indigo-600/10 border border-indigo-500/20">
          <div className="flex items-center justify-between mb-3">
            <div className="flex items-center gap-2">
              <Cpu className="w-3 h-3 text-indigo-400" />
              <span className="text-xs sm:text-[10px] font-bold text-indigo-400 uppercase tracking-wider">
                Evaluation
              </span>
            </div>
            <div
              className={cn(
                "flex items-center gap-1.5 px-2.5 py-1 rounded-full text-[11px] font-bold",
                lastEval.score >= 75
                  ? "bg-emerald-500/10 text-emerald-400 border border-emerald-500/20"
                  : lastEval.score >= 50
                  ? "bg-amber-500/10 text-amber-400 border border-amber-500/20"
                  : "bg-red-500/10 text-red-400 border border-red-500/20"
              )}
            >
              {lastEval.score >= 75 ? (
                <CheckCircle className="w-3 h-3" />
              ) : (
                <XCircle className="w-3 h-3" />
              )}
              {lastEval.score}/100
            </div>
          </div>
          {lastEval.missing_points.length > 0 && (
            <div className="space-y-1 mb-3">
              <p className="text-[10px] font-bold text-white/40 uppercase tracking-wider">
                Points manquants
              </p>
              {lastEval.missing_points.map((p, i) => (
                <p key={i} className="text-[12px] text-white/60">
                  - {p}
                </p>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Actions after evaluation */}
      {validated && (
        <div className="flex gap-3">
          <button
            onClick={onNextExercise}
            className="flex-1 group flex items-center justify-center gap-2 px-6 py-3 bg-white text-black font-semibold text-sm rounded-full hover:shadow-[0_0_20px_rgba(255,255,255,0.3)] transition-all"
          >
            Passer à l'exercice
            <ArrowRight className="w-4 h-4 transition-transform group-hover:translate-x-1" />
          </button>
        </div>
      )}

      {/* Force validate button (if not validated and has answers) */}
      {!validated && messages.length > 0 && !loading && (
        <div className="flex flex-col gap-2">
          <button
            onClick={handleForceValidate}
            className="w-full px-4 py-3 sm:py-2 text-xs sm:text-[11px] font-medium text-white/30 border border-white/5 rounded-full hover:text-white/50 hover:border-white/10 transition-all min-h-[44px] sm:min-h-0"
          >
            Valider manuellement et passer à l'exercice
          </button>
          <button
            onClick={onSkip}
            className="w-full flex items-center justify-center gap-1.5 px-4 py-3 sm:py-2 text-xs sm:text-[11px] font-medium text-white/20 hover:text-white/40 transition-all min-h-[44px] sm:min-h-0"
          >
            <SkipForward className="w-3 h-3" />
            Passer à une autre question
          </button>
        </div>
      )}

      {/* Error Banner */}
      {error && (
        <div className="flex items-center gap-2 p-3 rounded-xl bg-red-500/10 border border-red-500/20 text-red-400 text-sm">
          <AlertTriangle className="w-4 h-4 flex-shrink-0" />
          <span className="flex-1">{error}</span>
          <button
            onClick={() => setError(null)}
            className="text-red-400/60 hover:text-red-400 text-xs font-medium"
          >
            Fermer
          </button>
        </div>
      )}

      {/* Input Area */}
      {!validated && (
        <div className="rounded-xl border border-white/10 bg-white/[0.02] p-1">
          <div className="bg-[#0f0f0f] rounded-lg border border-white/5 p-3">
            <textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Écris ta réponse... (Shift+Entrée pour nouvelle ligne)"
              rows={3}
              disabled={loading}
              className="w-full bg-transparent text-sm text-white/90 placeholder:text-white/30 focus:outline-none resize-none"
            />
            <div className="flex items-center justify-between mt-2 pt-2 border-t border-white/5">
              <div className="flex items-center gap-2">
                <input
                  ref={fileInputRef}
                  type="file"
                  accept="image/*"
                  capture="environment"
                  onChange={handlePhotoUpload}
                  className="hidden"
                />
                <button
                  onClick={() => fileInputRef.current?.click()}
                  disabled={transcribing}
                  className="flex items-center gap-1.5 px-4 py-2.5 sm:px-3 sm:py-1.5 rounded-lg text-xs sm:text-[11px] font-medium text-white/40 border border-white/5 hover:text-white/60 hover:border-white/10 transition-all min-h-[44px] sm:min-h-0"
                >
                  {transcribing ? (
                    <Loader2 className="w-4 h-4 sm:w-3 sm:h-3 animate-spin" />
                  ) : (
                    <Camera className="w-4 h-4 sm:w-3 sm:h-3" />
                  )}
                  Photo
                </button>
              </div>
              <button
                onClick={handleSubmit}
                disabled={!input.trim() || loading}
                className={cn(
                  "flex items-center gap-1.5 px-5 py-2.5 sm:px-4 sm:py-1.5 rounded-lg text-xs sm:text-[11px] font-semibold transition-all min-h-[44px] sm:min-h-0",
                  input.trim() && !loading
                    ? "bg-indigo-600 text-white hover:bg-indigo-700"
                    : "bg-white/5 text-white/20 cursor-not-allowed"
                )}
              >
                <Send className="w-4 h-4 sm:w-3 sm:h-3" />
                Envoyer
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
