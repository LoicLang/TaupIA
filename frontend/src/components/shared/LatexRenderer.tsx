"use client";

import ReactMarkdown from "react-markdown";
import remarkMath from "remark-math";
import rehypeKatex from "rehype-katex";
import "katex/dist/katex.min.css";

interface LatexRendererProps {
  content: string;
  className?: string;
}

const BARE_LATEX_BLOCK =
  /\\(?:begin\{|left|right|frac|sum|prod|int|lim|sqrt|mathbb|mathcal|mathscr|operatorname|overline|underline|vec|cdots|ldots|mapsto|longrightarrow|rightarrow|infty|times|leq|geq|neq|forall|exists|det|sin|cos|tan|ln|exp|partial|zeta|gamma|alpha|beta|theta|phi|psi|omega|subset|cup|cap|in)\b/;
const STRONG_MATH_MARKER = /\\[a-zA-Z]+|[_^{}]/;
const EXISTING_MATH_SEGMENT = /(\$\$[\s\S]*?\$\$|\$[\s\S]*?\$)/g;
const WEAK_MATH_TOKEN = /^[A-Za-z0-9()[\]{}[\],.+\-*/=<>|':]+$/;
const FRENCH_STOPWORDS = new Set([
  "a",
  "au",
  "aux",
  "avec",
  "car",
  "ce",
  "cette",
  "dans",
  "de",
  "des",
  "du",
  "en",
  "et",
  "la",
  "le",
  "les",
  "ou",
  "par",
  "pour",
  "resp",
  "si",
  "sur",
  "tout",
  "toute",
  "toutes",
  "tous",
  "une",
  "un",
]);

function isStrongMathToken(token: string): boolean {
  const stripped = token
    .replace(/^[“"']+/, "")
    .replace(/[.,;:!?]+$/, "")
    .trim();

  if (!stripped) {
    return false;
  }

  return STRONG_MATH_MARKER.test(stripped);
}

function isWeakMathToken(token: string): boolean {
  const stripped = token
    .replace(/^[“"']+/, "")
    .replace(/[.,;:!?]+$/, "")
    .trim();

  if (!stripped || STRONG_MATH_MARKER.test(stripped)) {
    return false;
  }

  if (/[À-ÖØ-öø-ÿ]/.test(stripped) || /[A-Za-z]'[A-Za-z]/.test(stripped)) {
    return false;
  }

  if (FRENCH_STOPWORDS.has(stripped.toLowerCase()) || /^[A-Za-z]{3,}$/.test(stripped)) {
    return false;
  }

  return WEAK_MATH_TOKEN.test(stripped);
}

function splitTrailingPunctuation(token: string): [string, string] {
  let core = token;
  let trailing = "";

  while (/[.,;:!?]$/.test(core)) {
    trailing = core.slice(-1) + trailing;
    core = core.slice(0, -1);
  }

  const opens = (core.match(/\(/g) ?? []).length;
  const closes = (core.match(/\)/g) ?? []).length;
  while (core.endsWith(")")) {
    if (closes <= opens) {
      break;
    }
    trailing = core.slice(-1) + trailing;
    core = core.slice(0, -1);
  }

  return [core, trailing];
}

function wrapInlineLatexRunsInPlainText(segment: string): string {
  if (!segment || !STRONG_MATH_MARKER.test(segment)) {
    return segment;
  }

  const parts = segment.split(/(\s+)/);
  const result: string[] = [];
  let mathBuffer: string[] = [];

  const flushMathBuffer = () => {
    if (!mathBuffer.length) {
      return;
    }

    const joined = mathBuffer.join("");
    mathBuffer = [];
    const leadingWhitespace = joined.match(/^\s*/)?.[0] ?? "";
    const trailingWhitespace = joined.match(/\s*$/)?.[0] ?? "";
    const raw = joined.trim();
    if (!raw) {
      return;
    }

    const [core, trailingPunctuation] = splitTrailingPunctuation(raw);
    if (!core || !STRONG_MATH_MARKER.test(core)) {
      result.push(`${leadingWhitespace}${raw}${trailingWhitespace}`);
      return;
    }

    result.push(`${leadingWhitespace}$${core}$${trailingPunctuation}${trailingWhitespace}`);
  };

  const nextNonSpaceToken = (startIndex: number): string | null => {
    for (let i = startIndex; i < parts.length; i += 1) {
      const candidate = parts[i];
      if (!candidate || /^\s+$/.test(candidate)) {
        continue;
      }
      return candidate;
    }
    return null;
  };

  for (let index = 0; index < parts.length; index += 1) {
    const part = parts[index];
    if (!part) {
      continue;
    }

    if (/^\s+$/.test(part)) {
      if (mathBuffer.length) {
        mathBuffer.push(part);
      } else {
        result.push(part);
      }
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

function wrapInlineLatexRuns(paragraph: string): string {
  if (!paragraph) {
    return paragraph;
  }

  return paragraph
    .split(EXISTING_MATH_SEGMENT)
    .map((segment) => {
      if (!segment || segment.startsWith("$")) {
        return segment;
      }
      return wrapInlineLatexRunsInPlainText(segment);
    })
    .join("");
}

function wrapBareLatexParagraphs(content: string): string {
  return content
    .split(/\n{2,}/)
    .map((paragraph) => {
      const trimmed = wrapInlineLatexRuns(paragraph.trim());
      if (!trimmed || trimmed.includes("$")) {
        return trimmed;
      }

      const candidate = trimmed.replace(/^(?:(?:\d+|[a-z])\)\s*)+/i, "");
      if (!BARE_LATEX_BLOCK.test(candidate)) {
        return trimmed;
      }

      return `$$\n${trimmed}\n$$`;
    })
    .join("\n\n");
}

function extractBraceContent(text: string, startIndex: number): [string, number] | null {
  if (text[startIndex] !== "{") {
    return null;
  }
  let depth = 0;
  for (let i = startIndex; i < text.length; i += 1) {
    if (text[i] === "{") {
      depth += 1;
    } else if (text[i] === "}") {
      depth -= 1;
      if (depth === 0) {
        return [text.slice(startIndex + 1, i), i + 1];
      }
    }
  }
  return null;
}

function getMathSegmentRanges(text: string): Array<[number, number]> {
  const ranges: Array<[number, number]> = [];
  for (const match of text.matchAll(EXISTING_MATH_SEGMENT)) {
    if (match.index === undefined) {
      continue;
    }
    ranges.push([match.index, match.index + match[0].length]);
  }
  return ranges;
}

function isInsideMathSegment(index: number, ranges: Array<[number, number]>): boolean {
  return ranges.some(([start, end]) => index >= start && index < end);
}

function convertTextCommand(
  text: string,
  command: string,
  wrapperStart: string,
  wrapperEnd: string = wrapperStart,
): string {
  const pattern = new RegExp(`\\\\${command}\\{`, "g");
  const mathRanges = getMathSegmentRanges(text);
  let result = "";
  let lastIndex = 0;
  let match: RegExpExecArray | null;

  while ((match = pattern.exec(text)) !== null) {
    if (isInsideMathSegment(match.index, mathRanges)) {
      continue;
    }

    const braceStart = match.index + match[0].length - 1;
    const extracted = extractBraceContent(text, braceStart);
    if (!extracted) {
      continue;
    }
    const [inner, endIndex] = extracted;
    result += text.slice(lastIndex, match.index) + `${wrapperStart}${inner}${wrapperEnd}`;
    lastIndex = endIndex;
    pattern.lastIndex = endIndex;
  }

  result += text.slice(lastIndex);
  return result;
}

function convertLaTeXFormattingToMarkdown(content: string): string {
  let result = content;

  // Convert text-formatting commands outside math mode.
  result = convertTextCommand(result, "textbf", "**");
  result = convertTextCommand(result, "textit", "*");
  result = convertTextCommand(result, "emph", "*");
  result = convertTextCommand(result, "text", "");

  // Convert \begin{itemize}...\end{itemize} → Markdown lists
  result = result.replace(/\\begin\{itemize\}/g, "");
  result = result.replace(/\\end\{itemize\}/g, "");
  result = result.replace(/\\begin\{enumerate\}/g, "");
  result = result.replace(/\\end\{enumerate\}/g, "");
  result = result.replace(/\\item\s*/g, "\n- ");

  // Strip \noindent
  result = result.replace(/\\noindent\s*/g, "");

  return result;
}

function normalizeLatexContent(content: string): string {
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

export default function LatexRenderer({ content, className }: LatexRendererProps) {
  return (
    <div className={`latex-content ${className ?? ""}`.trim()}>
      <ReactMarkdown
        remarkPlugins={[remarkMath]}
        rehypePlugins={[rehypeKatex]}
        components={{
          p: ({ children }) => (
            <p className="mb-3 whitespace-pre-wrap last:mb-0">{children}</p>
          ),
          li: ({ children }) => <li className="mb-1 last:mb-0">{children}</li>,
        }}
      >
        {normalizeLatexContent(content)}
      </ReactMarkdown>
    </div>
  );
}
