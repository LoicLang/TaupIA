"use client";

import { SignUp } from "@clerk/nextjs";
import { GridBackground, GlowOrbs } from "@/components/shared/GridBackground";

export default function SignUpPage() {
  return (
    <div className="relative min-h-screen flex flex-col items-center justify-center bg-[#0a0a0a] text-white">
      <GridBackground />
      <GlowOrbs />

      <div className="relative z-10 flex flex-col items-center text-center mb-8">
        <h1 className="text-4xl md:text-5xl font-bold tracking-tight mb-2 bg-clip-text text-transparent bg-gradient-to-b from-white to-white/60">
          Taup<span className="text-indigo-500">IA</span>
        </h1>
        <p className="text-sm text-white/40">
          Cree ton compte pour acceder au simulateur.
        </p>
      </div>

      <div className="relative z-10">
        <SignUp
          appearance={{
            elements: {
              rootBox: "mx-auto",
              card: "bg-[#0f0f0f] border border-white/10 shadow-2xl",
            },
          }}
        />
      </div>
    </div>
  );
}
