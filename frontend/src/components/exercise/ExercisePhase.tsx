"use client";

import { useState, useRef, useEffect } from "react";
import { Terminal, Send, Camera, Loader2, Cpu, Flag, AlertTriangle, SkipForward } from "lucide-react";
import { cn } from "@/lib/utils";
import { exerciseMessage, transcribeImage } from "@/lib/api";
import LatexRenderer from "@/components/shared/LatexRenderer";
import type { Exercise, ChatMessage } from "@/lib/types";

interface ExercisePhaseProps {
  sessionId: string;
  exercise: Exercise;
  ocrProvider: string;
  onFinish: () => void;
  onSkip: () => void;
}

export default function ExercisePhase({
  sessionId,
  exercise,
  ocrProvider,
  onFinish,
  onSkip,
}: ExercisePhaseProps) {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [transcribing, setTranscribing] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const chatEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  async function handleSubmit() {
    if (!input.trim() || loading) return;
    const msg = input.trim();
    setInput("");
    setLoading(true);

    setError(null);
    setMessages((prev) => [...prev, { role: "user", content: msg }]);

    try {
      const res = await exerciseMessage(sessionId, { message: msg });
      setMessages(res.conversation_history);
    } catch (e) {
      setMessages((prev) => prev.slice(0, -1));
      setError(e instanceof Error ? e.message : "Erreur lors de l'envoi");
      setInput(msg); // Restore input so user can retry
    } finally {
      setLoading(false);
    }
  }

  function handleKeyDown(e: React.KeyboardEvent<HTMLTextAreaElement>) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
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

  return (
    <div className="w-full max-w-3xl mx-auto space-y-6">
      {/* Exercise Card */}
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
                exercice.tex
              </div>
            </div>
            <div className="px-2 py-1 rounded bg-purple-500/10 text-[10px] font-mono text-purple-400 border border-purple-500/20">
              EXERCICE
            </div>
          </div>
          <div className="p-4 sm:p-6">
            <LatexRenderer
              content={exercise.enonce}
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
                    ? "bg-purple-600 text-white rounded-br-md"
                    : "bg-white/[0.03] border border-white/10 text-white/80 rounded-bl-md"
                )}
              >
                {msg.role === "assistant" && (
                  <div className="flex items-center gap-1.5 mb-2">
                    <Cpu className="w-3 h-3 text-purple-400" />
                    <span className="text-[10px] sm:text-[9px] font-bold text-purple-400 uppercase tracking-wider">
                      Guidage
                    </span>
                  </div>
                )}
                <LatexRenderer content={msg.content} className="prose-invert prose-sm" />
              </div>
            </div>
          ))}
          {loading && (
            <div className="flex justify-start">
              <div className="bg-white/[0.03] border border-white/10 rounded-2xl rounded-bl-md px-4 py-3">
                <Loader2 className="w-4 h-4 text-purple-400 animate-spin" />
              </div>
            </div>
          )}
          <div ref={chatEndRef} />
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
      <div className="rounded-xl border border-white/10 bg-white/[0.02] p-1">
        <div className="bg-[#0f0f0f] rounded-lg border border-white/5 p-3">
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Pose une question, propose une piste..."
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
              <button
                onClick={onFinish}
                className="flex items-center gap-1.5 px-4 py-2.5 sm:px-3 sm:py-1.5 rounded-lg text-xs sm:text-[11px] font-medium text-white/40 border border-white/5 hover:text-white/60 hover:border-white/10 transition-all min-h-[44px] sm:min-h-0"
              >
                <Flag className="w-4 h-4 sm:w-3 sm:h-3" />
                Terminer
              </button>
              {messages.length > 0 && (
                <button
                  onClick={onSkip}
                  className="flex items-center gap-1 px-3 py-2.5 sm:px-2 sm:py-1.5 rounded-lg text-xs sm:text-[11px] font-medium text-white/20 hover:text-white/40 transition-all min-h-[44px] sm:min-h-0"
                >
                  <SkipForward className="w-3 h-3" />
                  Passer
                </button>
              )}
            </div>
            <button
              onClick={handleSubmit}
              disabled={!input.trim() || loading}
              className={cn(
                "flex items-center gap-1.5 px-5 py-2.5 sm:px-4 sm:py-1.5 rounded-lg text-xs sm:text-[11px] font-semibold transition-all min-h-[44px] sm:min-h-0",
                input.trim() && !loading
                  ? "bg-purple-600 text-white hover:bg-purple-700"
                  : "bg-white/5 text-white/20 cursor-not-allowed"
              )}
            >
              <Send className="w-4 h-4 sm:w-3 sm:h-3" />
              Envoyer
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
