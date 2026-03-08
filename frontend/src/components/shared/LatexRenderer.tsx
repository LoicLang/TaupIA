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
  /\\(?:begin\{|left|right|frac|sum|prod|int|lim|sqrt|mathbb|mathcal|operatorname|overline|underline|vec|cdots|ldots|mapsto|longrightarrow|rightarrow|infty|times|leq|geq|neq|forall|exists|det|sin|cos|tan|ln|exp)\b/;

function wrapBareLatexParagraphs(content: string): string {
  return content
    .split(/\n{2,}/)
    .map((paragraph) => {
      const trimmed = paragraph.trim();
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

function normalizeLatexContent(content: string): string {
  let normalized = content.trim().replace(/\r\n?/g, "\n");

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
