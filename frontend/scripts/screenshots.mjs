/**
 * Generate the README screenshots by driving the live app with Playwright.
 *
 * Captures real, unscripted LLM exchanges that show TaupIA's pedagogy: the
 * examiner evaluates demandingly and guides with questions instead of handing
 * over the answer, and the student can steer the session (deviation).
 *
 * Prerequisites (both must be running):
 *   backend:  ALLOW_DEVIATION=true uvicorn backend.main:app --port 8000
 *   frontend: npm run dev            (http://localhost:3000)
 *
 * Run:  npm run screenshots
 * Output: assets/screenshots/*.png
 */

import { chromium } from "playwright";
import { mkdirSync } from "fs";
import { dirname, join } from "path";
import { fileURLToPath } from "url";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..", "..");
const OUT = join(ROOT, "assets", "screenshots");
const API = "http://localhost:8000";
const APP = "http://localhost:3000";

mkdirSync(OUT, { recursive: true });

async function startSession({ chapter, difficulty = 3, format }) {
  const s = await (await fetch(`${API}/api/sessions`, { method: "POST" })).json();
  await fetch(`${API}/api/sessions/${s.id}/start`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      chapter_id: chapter, difficulty,
      ai_provider: "kimi", ocr_provider: "kimi", format,
    }),
  });
  return s.id;
}

async function main() {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({
    viewport: { width: 880, height: 900 },
    deviceScaleFactor: 2,
  });

  const shoot = async (name) => {
    await page.waitForTimeout(1400); // let KaTeX + fade-in settle
    await page.screenshot({ path: join(OUT, name), fullPage: true });
    console.log("shot:", name);
  };

  const send = async (text, urlPart) => {
    await page.fill("textarea", text);
    await Promise.all([
      page.waitForResponse((r) => r.url().includes(urlPart) && r.status() === 200, { timeout: 120000 }),
      page.click('button:has-text("Envoyer")'),
    ]);
  };

  // 1. Setup — the entry point
  try {
    await page.goto(`${APP}/setup`, { waitUntil: "domcontentloaded" });
    await page.waitForTimeout(3500);
    await shoot("setup.png");
  } catch (e) { console.error("setup:", e.message); }

  // 2. Question phase — demanding evaluation + Socratic guidance
  try {
    const id = await startSession({ chapter: "suites_reelles", difficulty: 2, format: "full" });
    await page.goto(`${APP}/session/${id}`, { waitUntil: "domcontentloaded" });
    await page.waitForSelector("textarea", { timeout: 40000 });
    await send("Je crois voir l'idée mais je n'arrive pas à le formuler rigoureusement. Tu peux m'aider à structurer ?", "/answer");
    await shoot("question-feedback.png");
  } catch (e) { console.error("question:", e.message); }

  // 3. Exercise phase — the examiner refuses to hand over the solution
  try {
    const id = await startSession({ chapter: "applications_lineaires", difficulty: 3, format: "exercise_only" });
    await page.goto(`${APP}/session/${id}`, { waitUntil: "domcontentloaded" });
    await page.waitForSelector("textarea", { timeout: 40000 });
    await send("Je suis bloqué, peux-tu juste me donner la réponse ?", "/exercise/message");
    await shoot("exercise-socratic.png");
  } catch (e) { console.error("exercise:", e.message); }

  // 4. Deviation — fresh session, the student asks for a harder exercise up front
  try {
    const id = await startSession({ chapter: "applications_lineaires", difficulty: 2, format: "exercise_only" });
    await page.goto(`${APP}/session/${id}`, { waitUntil: "domcontentloaded" });
    await page.waitForSelector("textarea", { timeout: 40000 });
    await Promise.all([
      page.waitForResponse((r) => r.url().includes("/exercise/message") && r.status() === 200, { timeout: 120000 }),
      page.click('button:has-text("Plus difficile")'),
    ]);
    await shoot("deviation.png");
  } catch (e) { console.error("deviation:", e.message); }

  await browser.close();
  console.log("done ->", OUT);
}

main().catch((e) => { console.error(e); process.exit(1); });
