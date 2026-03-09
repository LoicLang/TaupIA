#!/usr/bin/env node
/**
 * Passe 2: Validate all exercise LaTeX through KaTeX.
 *
 * For each exercise, applies the same normalizeLatexContent logic as the
 * frontend LatexRenderer, then validates every $...$ and $$...$$ segment
 * through KaTeX. Also detects bare LaTeX commands outside $ delimiters.
 */

import { readFileSync, readdirSync } from "fs";
import { join, dirname } from "path";
import { fileURLToPath } from "url";
import katex from "../frontend/node_modules/katex/dist/katex.mjs";

const __dirname = dirname(fileURLToPath(import.meta.url));
const EXERCISES_DIR = join(__dirname, "..", "data", "exercices");

// --- Replicate LatexRenderer's normalizeLatexContent ---

const BARE_LATEX_BLOCK =
  /\\(?:begin\{|left|right|frac|sum|prod|int|lim|sqrt|mathbb|mathcal|mathscr|operatorname|overline|underline|vec|cdots|ldots|mapsto|longrightarrow|rightarrow|infty|times|leq|geq|neq|forall|exists|det|sin|cos|tan|ln|exp|partial|zeta|gamma|alpha|beta|theta|phi|psi|omega|subset|cup|cap|in)\b/;
const STRONG_MATH_MARKER = /\\[a-zA-Z]+|[_^{}]/;
const EXISTING_MATH_SEGMENT = /(\$\$[\s\S]*?\$\$|\$[\s\S]*?\$)/g;
const WEAK_MATH_TOKEN = /^[A-Za-z0-9()[\]{}[\],.+\-*/=<>|':]+$/;
const FRENCH_STOPWORDS = new Set([
  "a", "au", "aux", "avec", "car", "ce", "cette", "dans", "de", "des",
  "du", "en", "et", "la", "le", "les", "ou", "par", "pour", "resp",
  "si", "sur", "tout", "toute", "toutes", "tous", "une", "un",
]);

function isStrongMathToken(token) {
  const stripped = token.replace(/^[""']+/, "").replace(/[.,;:!?]+$/, "").trim();
  if (!stripped) return false;
  return STRONG_MATH_MARKER.test(stripped);
}

function isWeakMathToken(token) {
  const stripped = token.replace(/^[""']+/, "").replace(/[.,;:!?]+$/, "").trim();
  if (!stripped || STRONG_MATH_MARKER.test(stripped)) return false;
  if (/[À-ÖØ-öø-ÿ]/.test(stripped) || /[A-Za-z]'[A-Za-z]/.test(stripped)) return false;
  if (FRENCH_STOPWORDS.has(stripped.toLowerCase()) || /^[A-Za-z]{3,}$/.test(stripped)) return false;
  return WEAK_MATH_TOKEN.test(stripped);
}

function splitTrailingPunctuation(token) {
  let core = token;
  let trailing = "";
  while (/[.,;:!?]$/.test(core)) {
    trailing = core.slice(-1) + trailing;
    core = core.slice(0, -1);
  }
  const opens = (core.match(/\(/g) ?? []).length;
  const closes = (core.match(/\)/g) ?? []).length;
  while (core.endsWith(")") && closes > opens) {
    trailing = core.slice(-1) + trailing;
    core = core.slice(0, -1);
  }
  return [core, trailing];
}

function wrapInlineLatexRunsInPlainText(segment) {
  if (!segment || !STRONG_MATH_MARKER.test(segment)) return segment;
  const parts = segment.split(/(\s+)/);
  const result = [];
  let mathBuffer = [];

  const flushMathBuffer = () => {
    if (!mathBuffer.length) return;
    const joined = mathBuffer.join("");
    mathBuffer = [];
    const leadingWS = joined.match(/^\s*/)?.[0] ?? "";
    const trailingWS = joined.match(/\s*$/)?.[0] ?? "";
    const raw = joined.trim();
    if (!raw) return;
    const [core, trailingPunct] = splitTrailingPunctuation(raw);
    if (!core || !STRONG_MATH_MARKER.test(core)) {
      result.push(`${leadingWS}${raw}${trailingWS}`);
      return;
    }
    result.push(`${leadingWS}$${core}$${trailingPunct}${trailingWS}`);
  };

  const nextNonSpaceToken = (startIndex) => {
    for (let i = startIndex; i < parts.length; i++) {
      const candidate = parts[i];
      if (!candidate || /^\s+$/.test(candidate)) continue;
      return candidate;
    }
    return null;
  };

  for (let index = 0; index < parts.length; index++) {
    const part = parts[index];
    if (!part) continue;
    if (/^\s+$/.test(part)) {
      if (mathBuffer.length) mathBuffer.push(part);
      else result.push(part);
      continue;
    }
    const strongMath = isStrongMathToken(part);
    const weakMath = isWeakMathToken(part);
    const nextToken = nextNonSpaceToken(index + 1);
    const nextIsStrongMath = nextToken ? isStrongMathToken(nextToken) : false;
    if (strongMath || (weakMath && (mathBuffer.length > 0 || nextIsStrongMath))) {
      mathBuffer.push(part);
      continue;
    }
    flushMathBuffer();
    result.push(part);
  }
  flushMathBuffer();
  return result.join("");
}

function wrapInlineLatexRuns(paragraph) {
  if (!paragraph) return paragraph;
  return paragraph
    .split(EXISTING_MATH_SEGMENT)
    .map((segment) => {
      if (!segment || segment.startsWith("$")) return segment;
      return wrapInlineLatexRunsInPlainText(segment);
    })
    .join("");
}

function wrapBareLatexParagraphs(content) {
  return content
    .split(/\n{2,}/)
    .map((paragraph) => {
      const trimmed = wrapInlineLatexRuns(paragraph.trim());
      if (!trimmed || trimmed.includes("$")) return trimmed;
      const candidate = trimmed.replace(/^(?:(?:\d+|[a-z])\)\s*)+/i, "");
      if (!BARE_LATEX_BLOCK.test(candidate)) return trimmed;
      return `$$\n${trimmed}\n$$`;
    })
    .join("\n\n");
}

function extractBraceContent(text, startIndex) {
  if (text[startIndex] !== "{") return null;
  let depth = 0;
  for (let i = startIndex; i < text.length; i++) {
    if (text[i] === "{") depth++;
    else if (text[i] === "}") {
      depth--;
      if (depth === 0) return [text.slice(startIndex + 1, i), i + 1];
    }
  }
  return null;
}

function getMathSegmentRanges(text) {
  const ranges = [];
  for (const match of text.matchAll(EXISTING_MATH_SEGMENT)) {
    if (match.index === undefined) continue;
    ranges.push([match.index, match.index + match[0].length]);
  }
  return ranges;
}

function isInsideMathSegment(index, ranges) {
  return ranges.some(([start, end]) => index >= start && index < end);
}

function convertTextCommand(text, command, wrapper) {
  const pattern = new RegExp(`\\\\${command}\\{`, "g");
  const mathRanges = getMathSegmentRanges(text);
  let result = "";
  let lastIndex = 0;
  let match;
  while ((match = pattern.exec(text)) !== null) {
    if (isInsideMathSegment(match.index, mathRanges)) continue;
    const braceStart = match.index + match[0].length - 1;
    const extracted = extractBraceContent(text, braceStart);
    if (!extracted) continue;
    const [inner, endIndex] = extracted;
    result += text.slice(lastIndex, match.index) + `${wrapper}${inner}${wrapper}`;
    lastIndex = endIndex;
    pattern.lastIndex = endIndex;
  }
  result += text.slice(lastIndex);
  return result;
}

function convertLaTeXFormattingToMarkdown(content) {
  let result = content;
  result = convertTextCommand(result, "textbf", "**");
  result = convertTextCommand(result, "textit", "*");
  result = convertTextCommand(result, "emph", "*");
  result = convertTextCommand(result, "text", "");
  result = result.replace(/\\begin\{itemize\}/g, "");
  result = result.replace(/\\end\{itemize\}/g, "");
  result = result.replace(/\\begin\{enumerate\}/g, "");
  result = result.replace(/\\end\{enumerate\}/g, "");
  result = result.replace(/\\item\s*/g, "\n- ");
  result = result.replace(/\\noindent\s*/g, "");
  return result;
}

function normalizeLatexContent(content) {
  let normalized = content.trim().replace(/\r\n?/g, "\n");
  // Convert LaTeX formatting commands to Markdown BEFORE auto-wrapping
  normalized = convertLaTeXFormattingToMarkdown(normalized);
  normalized = normalized.replace(/\\(?=[À-ÖØ-öø-ÿ])/g, "");
  normalized = normalized.replace(/\\par\b/g, "\n\n");
  normalized = normalized.replace(/\\\[/g, "\n$$\n");
  normalized = normalized.replace(/\\\]/g, "\n$$\n");
  normalized = normalized.replace(/\\\(/g, "$");
  normalized = normalized.replace(/\\\)/g, "$");
  normalized = normalized.replace(/[ \t]+\n/g, "\n");
  normalized = normalized.replace(/\n{3,}/g, "\n\n");
  return wrapBareLatexParagraphs(normalized);
}

// --- Extract and validate math segments ---

function extractMathSegments(text) {
  const segments = [];
  // Match $$...$$ and $...$
  const regex = /\$\$([\s\S]*?)\$\$|\$([^$]*?)\$/g;
  let match;
  while ((match = regex.exec(text)) !== null) {
    const math = match[1] ?? match[2];
    const isDisplay = match[1] !== undefined;
    segments.push({ math, isDisplay, index: match.index });
  }
  return segments;
}

function detectBareLatex(text) {
  // Remove all $...$ and $$...$$ segments
  const stripped = text.replace(/\$\$[\s\S]*?\$\$/g, "").replace(/\$[^$]*?\$/g, "");
  // Look for LaTeX commands outside $
  const bareCommands = [];
  const cmdRegex = /\\([a-zA-Z]+)/g;
  let match;
  while ((match = cmdRegex.exec(stripped)) !== null) {
    const cmd = match[1];
    // Skip non-math commands that are OK outside $
    if (["par", "textbf", "textit", "text", "begin", "end", "item",
         "hline", "cline", "itemize", "enumerate"].includes(cmd)) continue;
    bareCommands.push(cmd);
  }
  return bareCommands;
}

function validateKatex(math, displayMode) {
  try {
    katex.renderToString(math, {
      throwOnError: true,
      displayMode,
      strict: false,  // Don't fail on unknown commands, just on syntax errors
    });
    return null;
  } catch (e) {
    return e.message;
  }
}

// --- Main ---

const files = readdirSync(EXERCISES_DIR)
  .filter((f) => f.endsWith(".json"))
  .sort();

const issues = [];
let totalExercises = 0;
let totalFields = 0;
let totalKatexErrors = 0;
let totalBareLatex = 0;

for (const file of files) {
  const data = JSON.parse(readFileSync(join(EXERCISES_DIR, file), "utf-8"));
  const exercises = data.exercises || [];

  for (const ex of exercises) {
    totalExercises++;

    // Collect all text fields from this exercise
    const fields = [];

    if (ex.statement_latex) {
      fields.push({ field: "statement_latex", text: ex.statement_latex });
    }

    for (const sq of ex.sub_questions || []) {
      if (sq.statement_latex) {
        fields.push({ field: `sub_q[${sq.label}].statement`, text: sq.statement_latex });
      }
      if (sq.solution_latex) {
        fields.push({ field: `sub_q[${sq.label}].solution`, text: sq.solution_latex });
      }
      for (const h of sq.hints || []) {
        if (h.content_latex) {
          fields.push({ field: `sub_q[${sq.label}].hint[${h.level}]`, text: h.content_latex });
        }
      }
    }

    if (ex.global_solution_latex) {
      fields.push({ field: "global_solution", text: ex.global_solution_latex });
    }

    for (const h of ex.hints || []) {
      if (h.content_latex) {
        fields.push({ field: `hint[${h.level}]`, text: h.content_latex });
      }
    }

    for (const { field, text } of fields) {
      totalFields++;

      // Apply normalizeLatexContent (same as frontend)
      const normalized = normalizeLatexContent(text);

      // 1. Validate KaTeX segments
      const segments = extractMathSegments(normalized);
      for (const seg of segments) {
        const error = validateKatex(seg.math, seg.isDisplay);
        if (error) {
          totalKatexErrors++;
          issues.push({
            type: "KATEX_ERROR",
            file: file.replace(".json", ""),
            exercise: ex.id,
            field,
            math: seg.math.length > 100 ? seg.math.slice(0, 100) + "..." : seg.math,
            error: error.length > 120 ? error.slice(0, 120) + "..." : error,
          });
        }
      }

      // 2. Detect bare LaTeX (only in statement fields - those shown to students)
      if (field.includes("statement")) {
        const bare = detectBareLatex(normalized);
        if (bare.length > 0) {
          totalBareLatex++;
          issues.push({
            type: "BARE_LATEX",
            file: file.replace(".json", ""),
            exercise: ex.id,
            field,
            commands: [...new Set(bare)].slice(0, 10).join(", "),
            normalized_preview: normalized.length > 100 ? normalized.slice(0, 100) + "..." : normalized,
          });
        }
      }
    }
  }
}

// --- Report ---

console.log("=" .repeat(70));
console.log("KATEX VALIDATION REPORT");
console.log("=" .repeat(70));
console.log(`Scanned: ${files.length} files, ${totalExercises} exercises, ${totalFields} fields`);
console.log(`KaTeX errors: ${totalKatexErrors}`);
console.log(`Bare LaTeX in statements: ${totalBareLatex}`);
console.log();

if (issues.length === 0) {
  console.log("No issues found!");
} else {
  // Group by type
  const katexErrors = issues.filter((i) => i.type === "KATEX_ERROR");
  const bareLatex = issues.filter((i) => i.type === "BARE_LATEX");

  if (katexErrors.length > 0) {
    console.log(`--- KATEX ERRORS (${katexErrors.length}) ---`);
    // Group by file
    const byFile = {};
    for (const issue of katexErrors) {
      if (!byFile[issue.file]) byFile[issue.file] = [];
      byFile[issue.file].push(issue);
    }
    for (const [file, fileIssues] of Object.entries(byFile).sort()) {
      console.log(`\n  ${file} (${fileIssues.length} errors):`);
      for (const issue of fileIssues.slice(0, 5)) {
        console.log(`    ${issue.exercise} [${issue.field}]:`);
        console.log(`      math: ${issue.math}`);
        console.log(`      error: ${issue.error}`);
      }
      if (fileIssues.length > 5) {
        console.log(`    ... and ${fileIssues.length - 5} more`);
      }
    }
  }

  if (bareLatex.length > 0) {
    console.log(`\n--- BARE LATEX IN STATEMENTS (${bareLatex.length}) ---`);
    const byFile = {};
    for (const issue of bareLatex) {
      if (!byFile[issue.file]) byFile[issue.file] = [];
      byFile[issue.file].push(issue);
    }
    for (const [file, fileIssues] of Object.entries(byFile).sort()) {
      console.log(`\n  ${file} (${fileIssues.length}):`);
      for (const issue of fileIssues.slice(0, 3)) {
        console.log(`    ${issue.exercise} [${issue.field}]: ${issue.commands}`);
      }
      if (fileIssues.length > 3) {
        console.log(`    ... and ${fileIssues.length - 3} more`);
      }
    }
  }
}

console.log("\n" + "=".repeat(70));
