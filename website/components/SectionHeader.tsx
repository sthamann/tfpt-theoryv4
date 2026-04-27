"use client";

import { motion } from "motion/react";
import { cn } from "@/lib/utils";

interface SectionHeaderProps {
  eyebrow?: string;
  title: string;
  description?: string;
  align?: "left" | "center";
  className?: string;
  /**
   * DOM id assigned to the `<h2>`. When set, sibling sections can use
   * `aria-labelledby={id}` to expose this heading as the section's
   * accessible name. Optional; safe to omit when no `<section>` needs to
   * reference it.
   */
  id?: string;
}

export function SectionHeader({
  eyebrow,
  title,
  description,
  align = "left",
  className,
  id,
}: SectionHeaderProps) {
  return (
    <div
      className={cn(
        "flex flex-col gap-3",
        align === "center" && "items-center text-center",
        className,
      )}
    >
      {eyebrow && (
        <motion.span
          initial={{ opacity: 0, y: 6 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, amount: 0.05 }}
          transition={{ duration: 0.5 }}
          className="inline-flex items-center gap-2 rounded-full border border-blue-400/20 bg-blue-500/5 px-3 py-1 text-xs font-medium uppercase tracking-widest text-blue-300"
        >
          <span className="h-1.5 w-1.5 rounded-full bg-blue-400" />
          {eyebrow}
        </motion.span>
      )}
      <motion.h2
        id={id}
        initial={{ opacity: 0, y: 12 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true, amount: 0.05 }}
        transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1] }}
        className="font-serif text-3xl font-semibold leading-tight text-slate-50 sm:text-4xl md:text-5xl"
      >
        {title}
      </motion.h2>
      {description && (
        <motion.p
          initial={{ opacity: 0, y: 12 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, amount: 0.05 }}
          transition={{ duration: 0.7, delay: 0.1, ease: [0.16, 1, 0.3, 1] }}
          className={cn(
            "max-w-2xl text-base text-slate-400 sm:text-lg",
            align === "center" && "mx-auto",
          )}
        >
          {description}
        </motion.p>
      )}
    </div>
  );
}
