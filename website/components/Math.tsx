"use client";

import { useMemo } from "react";
import katex from "katex";
import { cn } from "@/lib/utils";

interface MathProps {
  children: string;
  block?: boolean;
  className?: string;
}

export function Math({ children, block = false, className }: MathProps) {
  const html = useMemo(() => {
    try {
      return katex.renderToString(children, {
        displayMode: block,
        throwOnError: false,
        strict: "ignore",
        output: "html",
      });
    } catch {
      return children;
    }
  }, [children, block]);

  if (block) {
    return (
      <div
        className={cn("my-2 overflow-x-auto", className)}
        dangerouslySetInnerHTML={{ __html: html }}
      />
    );
  }

  return (
    <span
      className={className}
      dangerouslySetInnerHTML={{ __html: html }}
    />
  );
}
