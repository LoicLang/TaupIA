import Link from "next/link";
import {
  BookOpen,
  Camera,
  MessageSquare,
  Database,
  Brain,
  Zap,
  Terminal,
  ChevronRight,
} from "lucide-react";

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-[#0a0a0a] text-white/90 selection:bg-indigo-500/30 selection:text-white font-sans antialiased overflow-x-hidden">
      {/* BACKGROUND ELEMENTS */}
      <div className="fixed inset-0 z-0 overflow-hidden pointer-events-none">
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

        {/* Glow Orbs */}
        <div className="absolute -top-[10%] left-[20%] w-[40%] h-[40%] rounded-full bg-indigo-600/20 blur-[120px]" />
        <div className="absolute top-[10%] right-[20%] w-[30%] h-[30%] rounded-full bg-blue-600/10 blur-[100px]" />
      </div>

      <main className="relative z-10">
        {/* HERO SECTION */}
        <section className="pt-32 pb-20 px-6 max-w-7xl mx-auto flex flex-col items-center text-center">
          <span className="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-indigo-500/20 bg-indigo-500/5 text-[11px] font-bold tracking-[0.15em] uppercase text-indigo-400 mb-8">
            <span className="relative flex h-2 w-2">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-indigo-400 opacity-75" />
              <span className="relative inline-flex rounded-full h-2 w-2 bg-indigo-500" />
            </span>
            Simulateur MPSI
          </span>

          <h1 className="text-6xl md:text-8xl font-bold tracking-tight mb-6">
            <span className="bg-gradient-to-b from-white to-white/60 bg-clip-text text-transparent">
              Taup
            </span>
            <span className="text-indigo-500">IA</span>
          </h1>

          <p className="max-w-2xl text-lg md:text-xl text-white/50 font-medium mb-10 leading-relaxed">
            Prepare tes kholles de maths avec une IA qui raisonne comme un vrai
            kholleur. Une progression guidee sans jamais donner la solution
            directe.
          </p>

          <div className="flex flex-col sm:flex-row gap-4 mb-20">
            <Link
              href="/sign-up"
              className="group flex items-center justify-center gap-2 px-8 py-3 bg-white text-black font-semibold text-sm rounded-full hover:bg-white/90 transition-all active:scale-[0.98]"
            >
              Rejoindre la waitlist
              <ChevronRight className="w-4 h-4 transition-transform group-hover:translate-x-1" />
            </Link>
            <Link
              href="/sign-in"
              className="px-8 py-3 text-sm font-medium text-white/70 border border-white/10 rounded-full hover:bg-white/5 transition-all text-center"
            >
              Deja inscrit ? Se connecter
            </Link>
          </div>

          {/* APP MOCKUP */}
          <div className="w-full max-w-4xl mx-auto px-4">
            <div className="rounded-2xl border border-white/10 bg-white/[0.02] backdrop-blur-md p-1 shadow-2xl shadow-indigo-500/10">
              <div className="bg-[#0f0f0f] rounded-xl overflow-hidden border border-white/5 text-left">
                {/* Window Header */}
                <div className="flex items-center justify-between px-6 py-3 border-b border-white/5 bg-white/[0.01]">
                  <div className="flex items-center gap-4">
                    <div className="flex gap-1.5">
                      <div className="w-2.5 h-2.5 rounded-full bg-white/10" />
                      <div className="w-2.5 h-2.5 rounded-full bg-white/10" />
                      <div className="w-2.5 h-2.5 rounded-full bg-white/10" />
                    </div>
                    <div className="flex items-center gap-2 text-[11px] font-mono text-white/40">
                      <Terminal className="w-3 h-3" />
                      exercice_limites.tex
                    </div>
                  </div>
                </div>

                {/* Content */}
                <div className="p-8 font-mono text-sm sm:text-base leading-relaxed">
                  <div className="text-indigo-400 mb-4 text-[10px] font-bold uppercase tracking-widest">
                    Enonce du kholleur
                  </div>
                  <div className="text-white/80 space-y-4">
                    <p>
                      Soit f: R → R une fonction continue.
                    </p>
                    <p>
                      On suppose que pour tout x, y dans R, f(x+y) = f(x) +
                      f(y).
                    </p>
                    <p className="pb-6 border-b border-white/5">
                      Montrez que f est une fonction lineaire de la forme f(x) =
                      ax.
                    </p>

                    <div className="pt-4 flex gap-3">
                      <div className="w-1.5 h-1.5 rounded-full bg-indigo-500 mt-2 shrink-0 animate-pulse" />
                      <p className="text-white/40 italic">
                        Par quoi souhaites-tu commencer ? Peux-tu d'abord
                        determiner f(0) et f(nx) pour n entier naturel ?
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* COMMENT CA MARCHE SECTION */}
        <section className="py-24 px-6 max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold tracking-tight bg-gradient-to-b from-white to-white/60 bg-clip-text text-transparent mb-4">
              Comment ca marche
            </h2>
            <div className="h-1 w-20 bg-indigo-500/50 mx-auto rounded-full" />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {[
              {
                icon: <BookOpen className="w-6 h-6 text-indigo-400" />,
                title: "Choisis ton chapitre",
                desc: "20 chapitres du programme MPSI, difficulte de 1 a 5.",
              },
              {
                icon: <Camera className="w-6 h-6 text-indigo-400" />,
                title: "Reponds par texte ou photo",
                desc: "Ecris ta reponse ou prends en photo ton brouillon.",
              },
              {
                icon: <MessageSquare className="w-6 h-6 text-indigo-400" />,
                title: "L'IA te guide",
                desc: "Methode socratique : l'IA ne donne jamais la reponse, elle te pousse a raisonner.",
              },
            ].map((step, idx) => (
              <div key={idx} className="group relative">
                <div className="flex flex-col items-center text-center p-8 transition-all">
                  <div className="w-14 h-14 rounded-2xl border border-white/10 bg-white/[0.03] flex items-center justify-center mb-6 group-hover:border-indigo-500/30 transition-colors">
                    {step.icon}
                  </div>
                  <h3 className="text-lg font-bold mb-3">{step.title}</h3>
                  <p className="text-white/40 text-sm leading-relaxed">
                    {step.desc}
                  </p>
                </div>
                {idx < 2 && (
                  <div className="hidden md:block absolute top-1/4 -right-4 w-8 h-[1px] bg-white/10" />
                )}
              </div>
            ))}
          </div>
        </section>

        {/* FEATURES SECTION */}
        <section className="py-24 px-6 bg-white/[0.01] border-y border-white/5">
          <div className="max-w-7xl mx-auto">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-16 mb-16">
              <div>
                <span className="text-[10px] font-bold uppercase tracking-wider text-indigo-400 mb-4 block">
                  Technologie de pointe
                </span>
                <h2 className="text-4xl font-bold tracking-tight bg-gradient-to-b from-white to-white/60 bg-clip-text text-transparent leading-tight">
                  L'intelligence artificielle au service de la prepa.
                </h2>
              </div>
              <div className="flex items-end">
                <p className="text-white/40 font-medium">
                  Les derniers modeles de langage combines avec une base de
                  connaissances mathematiques structuree pour garantir une
                  rigueur absolue.
                </p>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {[
                {
                  icon: <Camera className="w-5 h-5 text-indigo-400" />,
                  title: "OCR manuscrit",
                  desc: "Prends en photo ta copie, l'IA lit ton ecriture et analyse ta reponse en temps reel.",
                },
                {
                  icon: <Database className="w-5 h-5 text-indigo-400" />,
                  title: "Knowledge Graph",
                  desc: "928 noeuds, 2236 aretes. Definitions et theoremes exacts du programme officiel MPSI.",
                },
                {
                  icon: <Brain className="w-5 h-5 text-indigo-400" />,
                  title: "Methode socratique",
                  desc: "L'IA identifie tes erreurs et te guide avec des indices progressifs sans jamais spoiler la solution.",
                },
                {
                  icon: <Zap className="w-5 h-5 text-indigo-400" />,
                  title: "Multi-provider IA",
                  desc: "DeepSeek, Gemini, Claude, Kimi. Choisis le modele qui correspond le mieux a ton style.",
                },
              ].map((feature, idx) => (
                <div
                  key={idx}
                  className="rounded-2xl border border-white/10 bg-white/[0.02] backdrop-blur-md p-1 group hover:border-indigo-500/20 transition-all"
                >
                  <div className="bg-[#0f0f0f] rounded-xl p-6 border border-white/5 h-full">
                    <div className="flex items-start gap-4">
                      <div className="shrink-0 w-10 h-10 rounded-lg bg-indigo-500/10 flex items-center justify-center">
                        {feature.icon}
                      </div>
                      <div>
                        <h4 className="font-bold text-white/90 mb-2">
                          {feature.title}
                        </h4>
                        <p className="text-sm text-white/40 leading-relaxed">
                          {feature.desc}
                        </p>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* CTA FINAL SECTION */}
        <section className="py-32 px-6 max-w-4xl mx-auto text-center">
          <div className="relative p-12 rounded-3xl border border-indigo-500/20 bg-indigo-500/[0.02] overflow-hidden">
            <div className="absolute top-0 left-1/2 -translate-x-1/2 w-64 h-64 bg-indigo-600/10 blur-[100px]" />

            <h2 className="text-4xl font-bold tracking-tight mb-6 relative z-10">
              Pret pour ta prochaine kholle ?
            </h2>
            <p className="text-white/50 mb-10 text-lg relative z-10">
              Rejoins la waitlist et sois parmi les premiers a tester TaupIA.
            </p>

            <div className="flex justify-center relative z-10">
              <Link
                href="/sign-up"
                className="group flex items-center gap-2 px-10 py-4 bg-white text-black font-semibold text-sm rounded-full hover:bg-white/90 transition-all active:scale-[0.98] shadow-xl shadow-indigo-500/20"
              >
                Rejoindre la waitlist
                <ChevronRight className="w-4 h-4 transition-transform group-hover:translate-x-1" />
              </Link>
            </div>
          </div>
        </section>

        {/* FOOTER */}
        <footer className="py-12 px-6 border-t border-white/5">
          <div className="max-w-7xl mx-auto flex flex-col md:flex-row justify-between items-center gap-6">
            <div className="flex items-center gap-2">
              <span className="text-lg font-bold tracking-tight">
                Taup<span className="text-indigo-500">IA</span>
              </span>
              <span className="w-1 h-1 rounded-full bg-white/20" />
              <span className="text-[11px] font-mono text-white/40 tracking-tight">
                2026
              </span>
            </div>

            <p className="text-[11px] font-mono text-white/40 uppercase tracking-widest text-center">
              Simulateur de kholles pour CPGE scientifiques
            </p>
          </div>
        </footer>
      </main>
    </div>
  );
}
