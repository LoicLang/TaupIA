import type { Metadata, Viewport } from "next";
import { Inter, JetBrains_Mono } from "next/font/google";
import ClerkWrapper from "@/components/shared/ClerkWrapper";
import AuthProvider from "@/components/shared/AuthProvider";
import "katex/dist/katex.min.css";
import "./globals.css";

const inter = Inter({
  variable: "--font-inter",
  subsets: ["latin"],
});

const jetbrainsMono = JetBrains_Mono({
  variable: "--font-jetbrains-mono",
  subsets: ["latin"],
});

export const viewport: Viewport = {
  width: "device-width",
  initialScale: 1,
  maximumScale: 1,
};

export const metadata: Metadata = {
  title: "TaupIA — Simulateur de kholles MPSI",
  description:
    "Prepare tes oraux de maths avec une IA qui evalue tes raisonnements.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <ClerkWrapper>
      <html lang="fr">
        <body
          className={`${inter.variable} ${jetbrainsMono.variable} antialiased bg-[#0a0a0a] text-white/90`}
        >
          <AuthProvider>{children}</AuthProvider>
        </body>
      </html>
    </ClerkWrapper>
  );
}
