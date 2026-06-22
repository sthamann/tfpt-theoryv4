"use client";

import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useRef,
  useState,
} from "react";
import { createPortal } from "react-dom";
import {
  Check,
  Copy,
  Github,
  Loader2,
  Play,
  RotateCw,
  X,
  XCircle,
} from "lucide-react";
import { runScript, pyodideVersion, type RunResult } from "@/lib/pyodide";
import { RichText } from "@/lib/richtext";
import { cn, REPO_URL } from "@/lib/utils";

interface ReproducerCtx {
  open: (file: string) => void;
}

const Ctx = createContext<ReproducerCtx | null>(null);

export function useReproducer(): ReproducerCtx {
  const ctx = useContext(Ctx);
  if (!ctx) throw new Error("useReproducer must be used within ReproducerProvider");
  return ctx;
}

type Phase = "loading" | "running" | "done" | "error";

interface ScriptDoc {
  title: string;
  body: string;
}

/** Pull the module docstring out of a Python source file's leading triple-quote. */
function extractDoc(src: string): ScriptDoc {
  const m = src.match(/^\uFEFF?\s*[rubRUB]?("""|''')([\s\S]*?)\1/);
  if (!m) return { title: "", body: "" };
  const doc = m[2].trim();
  const lines = doc.split("\n");
  const title = (lines[0] ?? "").replace(/^v\d+\s*--?\s*/i, "").trim();
  const body = lines.slice(1).join("\n").trim();
  return { title, body };
}

export function ReproducerProvider({ children }: { children: React.ReactNode }) {
  const [file, setFile] = useState<string | null>(null);
  const open = useCallback((f: string) => setFile(f), []);

  return (
    <Ctx.Provider value={{ open }}>
      {children}
      {file && <ReproducerModal file={file} onClose={() => setFile(null)} />}
    </Ctx.Provider>
  );
}

function ReproducerModal({ file, onClose }: { file: string; onClose: () => void }) {
  const [mounted, setMounted] = useState(false);
  const [phase, setPhase] = useState<Phase>("loading");
  const [status, setStatus] = useState("Starting…");
  const [result, setResult] = useState<RunResult | null>(null);
  const [revealed, setRevealed] = useState(0);
  const [showSource, setShowSource] = useState(false);
  const [source, setSource] = useState<string | null>(null);
  const [doc, setDoc] = useState<ScriptDoc>({ title: "", body: "" });
  const [docOpen, setDocOpen] = useState(false);
  const [copied, setCopied] = useState(false);
  const runId = useRef(0);

  const id = file.replace(/\.py$/, "").split("_")[0];
  const githubUrl = `${REPO_URL}/blob/main/verification/${file}`;
  const localCmd = `python verification/${file}`;

  useEffect(() => setMounted(true), []);

  // Eagerly load the source so we can show the script's header and the
  // (instant) source view.
  useEffect(() => {
    let cancelled = false;
    setSource(null);
    setDoc({ title: "", body: "" });
    setDocOpen(false);
    fetch(`/verification/${file}`)
      .then((r) => r.text())
      .then((text) => {
        if (cancelled) return;
        setSource(text);
        setDoc(extractDoc(text));
      })
      .catch(() => {});
    return () => {
      cancelled = true;
    };
  }, [file]);

  const run = useCallback(async () => {
    const myRun = ++runId.current;
    setPhase("loading");
    setStatus("Starting…");
    setResult(null);
    setRevealed(0);
    try {
      const res = await runScript(file, (s) => {
        if (runId.current === myRun) setStatus(s);
      });
      if (runId.current !== myRun) return;
      setResult(res);
      setPhase(res.error ? "error" : "done");
    } catch (e) {
      if (runId.current !== myRun) return;
      setResult({
        header: "",
        checks: [],
        passed: 0,
        failed: 0,
        ok: false,
        raw: "",
        error: e instanceof Error ? e.message : String(e),
      });
      setPhase("error");
    }
  }, [file]);

  // Auto-run on open / file change.
  useEffect(() => {
    run();
  }, [run]);

  // Step-by-step reveal of the checks once we have a result.
  useEffect(() => {
    if (phase !== "done" || !result) return;
    if (result.checks.length === 0) {
      setRevealed(0);
      return;
    }
    const total = result.checks.length;
    const step = Math.max(45, Math.min(110, Math.floor(2400 / total)));
    let i = 0;
    setRevealed(0);
    const t = window.setInterval(() => {
      i += 1;
      setRevealed(i);
      if (i >= total) window.clearInterval(t);
    }, step);
    return () => window.clearInterval(t);
  }, [phase, result]);

  // Esc closes; lock body scroll while open.
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => e.key === "Escape" && onClose();
    document.addEventListener("keydown", onKey);
    const prev = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    return () => {
      document.removeEventListener("keydown", onKey);
      document.body.style.overflow = prev;
    };
  }, [onClose]);

  const toggleSource = useCallback(async () => {
    setShowSource((v) => !v);
    if (source === null) {
      try {
        const text = await fetch(`/verification/${file}`).then((r) => r.text());
        setSource(text);
      } catch {
        setSource("# Could not load the source. View it on GitHub instead.");
      }
    }
  }, [file, source]);

  const copyCmd = useCallback(async () => {
    try {
      await navigator.clipboard.writeText(localCmd);
      setCopied(true);
      window.setTimeout(() => setCopied(false), 1600);
    } catch {
      /* clipboard unavailable on insecure origins */
    }
  }, [localCmd]);

  if (!mounted) return null;

  const checks = result?.checks ?? [];
  const shown = checks.slice(0, revealed);

  return createPortal(
    <div
      className="fixed inset-0 z-[60] flex items-end justify-center bg-slate-950/70 p-0 backdrop-blur-sm sm:items-center sm:p-4"
      role="dialog"
      aria-modal="true"
      aria-label={`Reproducer for ${file}`}
      onClick={(e) => {
        if (e.target === e.currentTarget) onClose();
      }}
    >
      <div className="glass-strong flex max-h-[92vh] w-full max-w-3xl flex-col overflow-hidden rounded-t-2xl border border-slate-700/50 sm:rounded-2xl">
        {/* Header */}
        <div className="flex items-start justify-between gap-3 border-b border-slate-800/60 px-5 py-4">
          <div className="min-w-0">
            <div className="flex flex-wrap items-center gap-2">
              <span className="rounded-md bg-blue-500/15 px-2 py-0.5 font-mono text-xs font-semibold text-blue-200 ring-1 ring-blue-400/30">
                {id}
              </span>
              <h2 className="truncate font-mono text-sm font-semibold text-slate-100">
                {file}
              </h2>
            </div>
            <p className="mt-1 text-[11px] leading-snug text-slate-400">
              Runs entirely in your browser via Pyodide {pyodideVersion()}{" "}
              (WebAssembly). Nothing is sent to a server.
            </p>
          </div>
          <button
            type="button"
            onClick={onClose}
            aria-label="Close reproducer"
            className="flex-none rounded-md p-1.5 text-slate-400 transition-colors hover:bg-white/5 hover:text-white"
          >
            <X size={18} />
          </button>
        </div>

        {/* Body */}
        <div className="flex-1 overflow-y-auto px-5 py-4">
          {/* What the script checks — pulled from the file's docstring */}
          {doc.title && (
            <div className="mb-4 rounded-xl border border-slate-700/40 bg-slate-950/40 px-4 py-3">
              <div className="text-[10px] font-semibold uppercase tracking-widest text-blue-300/80">
                What this script checks
              </div>
              <p className="mt-1 text-[13px] font-medium leading-snug text-slate-100">
                <RichText text={doc.title} />
              </p>
              {doc.body && (
                <>
                  <div
                    className={cn(
                      "mt-2 overflow-hidden whitespace-pre-wrap break-words text-[11px] leading-relaxed text-slate-400",
                      docOpen ? "" : "max-h-[3.9rem]",
                    )}
                  >
                    <RichText text={doc.body} />
                  </div>
                  <button
                    type="button"
                    onClick={() => setDocOpen((v) => !v)}
                    className="mt-1.5 text-[11px] font-semibold text-blue-300 transition-colors hover:text-blue-200"
                  >
                    {docOpen ? "Show less" : "Show more"}
                  </button>
                </>
              )}
            </div>
          )}

          {(phase === "loading" || phase === "running") && (
            <div className="flex items-center gap-3 rounded-xl border border-slate-700/40 bg-slate-950/40 px-4 py-4 text-sm text-slate-300">
              <Loader2 size={16} className="animate-spin text-blue-300" aria-hidden />
              <span>{status}</span>
            </div>
          )}

          {phase === "error" && result && (
            <div className="rounded-xl border border-rose-400/30 bg-rose-500/5 px-4 py-4">
              <div className="flex items-center gap-2 text-sm font-semibold text-rose-200">
                <XCircle size={16} aria-hidden />
                This script did not complete in the browser sandbox
              </div>
              <p className="mt-2 text-xs leading-relaxed text-slate-300">
                Some heavier scripts (large SciPy solves) are best run locally.
                You can still read the source, open it on GitHub, or run it with
                the command below.
              </p>
              {result.error && (
                <pre className="mt-3 max-h-48 overflow-auto whitespace-pre-wrap break-words rounded-md border border-slate-800/60 bg-slate-950/70 p-3 text-[11px] leading-relaxed text-rose-200/90">
                  {result.error}
                </pre>
              )}
            </div>
          )}

          {phase === "done" && result && (
            <div>
              {/* Overall verdict */}
              <div
                className={cn(
                  "flex flex-wrap items-center justify-between gap-2 rounded-xl border px-4 py-3",
                  result.ok
                    ? "border-emerald-400/30 bg-emerald-500/10"
                    : "border-rose-400/30 bg-rose-500/10",
                )}
              >
                <div className="flex items-center gap-2">
                  {result.ok ? (
                    <Check size={16} className="text-emerald-300" aria-hidden />
                  ) : (
                    <XCircle size={16} className="text-rose-300" aria-hidden />
                  )}
                  <span
                    className={cn(
                      "text-sm font-semibold",
                      result.ok ? "text-emerald-200" : "text-rose-200",
                    )}
                  >
                    {result.ok ? "ALL CHECKS PASSED" : "Some checks failed"}
                  </span>
                </div>
                <span className="font-mono text-xs text-slate-300">
                  {result.passed} passed
                  {result.failed > 0 ? ` · ${result.failed} failed` : ""}
                </span>
              </div>

              {result.header && (
                <p className="mt-3 font-mono text-[11px] text-slate-400">
                  {result.header}
                </p>
              )}

              {/* Step-by-step checks */}
              <ol className="mt-3 space-y-1.5">
                {shown.map((c, i) => (
                  <li
                    key={i}
                    className="flex items-start gap-2 rounded-md border border-slate-800/50 bg-slate-950/40 px-3 py-1.5"
                  >
                    {c.ok ? (
                      <Check
                        size={13}
                        className="mt-0.5 flex-none text-emerald-400"
                        aria-hidden
                      />
                    ) : (
                      <XCircle
                        size={13}
                        className="mt-0.5 flex-none text-rose-400"
                        aria-hidden
                      />
                    )}
                    <span className="text-[12px] leading-snug text-slate-300">
                      <RichText text={c.label} />
                    </span>
                  </li>
                ))}
                {revealed < checks.length && (
                  <li className="flex items-center gap-2 px-3 py-1 text-[11px] text-slate-500">
                    <Loader2 size={12} className="animate-spin" aria-hidden />
                    {checks.length - revealed} more…
                  </li>
                )}
              </ol>

              {checks.length === 0 && result.raw && (
                <pre className="mt-3 max-h-72 overflow-auto whitespace-pre-wrap break-words rounded-md border border-slate-800/60 bg-slate-950/70 p-3 text-[11px] leading-relaxed text-slate-300">
                  {result.raw}
                </pre>
              )}
            </div>
          )}

          {/* Collapsible source */}
          <div className="mt-4">
            <button
              type="button"
              onClick={toggleSource}
              className="text-xs font-semibold text-blue-300 transition-colors hover:text-blue-200"
            >
              {showSource ? "Hide" : "Show"} the script source
            </button>
            {showSource && (
              <pre className="mt-2 max-h-80 overflow-auto whitespace-pre-wrap break-words rounded-md border border-slate-800/60 bg-slate-950/80 p-3 text-[11px] leading-relaxed text-slate-300">
                <code className="font-mono">{source ?? "Loading…"}</code>
              </pre>
            )}
          </div>
        </div>

        {/* Footer */}
        <div className="flex flex-wrap items-center gap-2 border-t border-slate-800/60 px-5 py-3">
          <button
            type="button"
            onClick={run}
            disabled={phase === "loading" || phase === "running"}
            className="inline-flex items-center gap-1.5 rounded-full bg-gradient-to-r from-blue-500 to-violet-500 px-4 py-2 text-xs font-semibold text-white shadow-md shadow-blue-500/20 transition-transform hover:scale-105 disabled:opacity-50 disabled:hover:scale-100"
          >
            {phase === "loading" || phase === "running" ? (
              <Loader2 size={13} className="animate-spin" aria-hidden />
            ) : phase === "done" || phase === "error" ? (
              <RotateCw size={13} aria-hidden />
            ) : (
              <Play size={13} aria-hidden />
            )}
            {phase === "done" || phase === "error" ? "Run again" : "Running…"}
          </button>
          <button
            type="button"
            onClick={copyCmd}
            className="inline-flex items-center gap-1.5 rounded-full border border-slate-600/60 bg-slate-900/60 px-3 py-2 font-mono text-[11px] text-slate-200 transition-colors hover:bg-slate-800/80"
            title="Copy the command to run it locally"
          >
            {copied ? <Check size={12} aria-hidden /> : <Copy size={12} aria-hidden />}
            {localCmd}
          </button>
          <a
            href={githubUrl}
            target="_blank"
            rel="noopener noreferrer"
            className="ml-auto inline-flex items-center gap-1.5 rounded-full border border-slate-600/60 bg-slate-900/60 px-3 py-2 text-xs font-semibold text-slate-200 transition-colors hover:bg-slate-800/80"
          >
            <Github size={13} aria-hidden />
            GitHub
          </a>
        </div>
      </div>
    </div>,
    document.body,
  );
}
