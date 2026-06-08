import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

/**
 * Canonical source repository: the full theory documents plus the independent
 * verification stack (Python suite, Wolfram mirror, Lean carrier proof) and the
 * versioned status ledger.
 */
export const REPO_URL = "https://github.com/sthamann/tfpt-theoryv4";
