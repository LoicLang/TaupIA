"use client";

import { ClerkProvider } from "@clerk/nextjs";
import { frFR } from "@clerk/localizations";

const isClerkConfigured = !!process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY;

/**
 * Wrapper conditionnel pour Clerk.
 * En dev local sans NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY, on skip Clerk.
 */
export default function ClerkWrapper({ children }: { children: React.ReactNode }) {
  if (!isClerkConfigured) {
    return <>{children}</>;
  }

  return (
    <ClerkProvider
      localization={frFR}
      afterSignInUrl="/setup"
      afterSignUpUrl="/setup"
    >
      {children}
    </ClerkProvider>
  );
}
