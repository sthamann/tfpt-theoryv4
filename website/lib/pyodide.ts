/**
 * In-browser Python runtime for the live reproducer.
 *
 * Every verification script is the project's own deterministic code; it is run
 * client-side inside the Pyodide WebAssembly sandbox (no server, no machine
 * access, no user input is executed). This keeps the site fully static — it
 * works on Vercel exactly because nothing runs server-side.
 */

const PYODIDE_VERSION = "0.29.4";
const INDEX_URL = `https://cdn.jsdelivr.net/pyodide/v${PYODIDE_VERSION}/full/`;
const WORK_DIR = "/home/pyodide";

// eslint-disable-next-line @typescript-eslint/no-explicit-any
type Pyodide = any;

declare global {
  interface Window {
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    loadPyodide?: (opts: { indexURL: string }) => Promise<Pyodide>;
  }
}

let pyodidePromise: Promise<Pyodide> | null = null;
const scriptCache = new Map<string, string>();

function loadScriptOnce(src: string): Promise<void> {
  return new Promise((resolve, reject) => {
    if (document.querySelector(`script[data-pyodide]`)) {
      resolve();
      return;
    }
    const s = document.createElement("script");
    s.src = src;
    s.async = true;
    s.dataset.pyodide = "true";
    s.onload = () => resolve();
    s.onerror = () => reject(new Error("Failed to load the Pyodide runtime."));
    document.head.appendChild(s);
  });
}

async function fetchText(path: string): Promise<string> {
  const cached = scriptCache.get(path);
  if (cached) return cached;
  const res = await fetch(path);
  if (!res.ok) throw new Error(`Could not fetch ${path} (${res.status}).`);
  const text = await res.text();
  scriptCache.set(path, text);
  return text;
}

type StatusFn = (s: string) => void;

/** Lazily boot Pyodide once and pre-load the shared constants module. */
async function getPyodide(onStatus?: StatusFn): Promise<Pyodide> {
  if (!pyodidePromise) {
    pyodidePromise = (async () => {
      onStatus?.("Loading the Python runtime (Pyodide, ~once)…");
      await loadScriptOnce(`${INDEX_URL}pyodide.js`);
      if (!window.loadPyodide) throw new Error("Pyodide failed to initialise.");
      const py = await window.loadPyodide({ indexURL: INDEX_URL });

      onStatus?.("Loading the shared constants (tfpt_constants.py)…");
      const consts = await fetchText("/verification/tfpt_constants.py");
      py.FS.writeFile(`${WORK_DIR}/tfpt_constants.py`, consts);
      // tfpt_constants imports mpmath at module level → make sure it is present.
      await py.loadPackagesFromImports(consts);
      py.runPython(`import sys\nif ${JSON.stringify(WORK_DIR)} not in sys.path: sys.path.insert(0, ${JSON.stringify(WORK_DIR)})`);
      return py;
    })();
  }
  return pyodidePromise;
}

export interface CheckRow {
  ok: boolean;
  label: string;
}

export interface RunResult {
  header: string;
  checks: CheckRow[];
  passed: number;
  failed: number;
  ok: boolean;
  raw: string;
  error?: string;
}

function parseOutput(raw: string): Omit<RunResult, "raw" | "error"> {
  const lines = raw.split("\n");
  const checks: CheckRow[] = [];
  let header = "";
  let passed = 0;
  let failed = 0;
  for (const line of lines) {
    const m = line.match(/^\s*\[(PASS|FAIL)\]\s+(.*)$/);
    if (m) {
      checks.push({ ok: m[1] === "PASS", label: m[2].trim() });
      continue;
    }
    const sum = line.match(/---\s+.*?:\s+(\d+)\s+passed,\s+(\d+)\s+failed\s+---/);
    if (sum) {
      passed = parseInt(sum[1], 10);
      failed = parseInt(sum[2], 10);
      continue;
    }
    if (!header && line.trim() && !line.includes("[")) header = line.trim();
  }
  if (passed === 0 && failed === 0) {
    passed = checks.filter((c) => c.ok).length;
    failed = checks.filter((c) => !c.ok).length;
  }
  return { header, checks, passed, failed, ok: failed === 0 && checks.length > 0 };
}

/**
 * Run one verification script (e.g. "v3_em_alpha.py") in the browser and
 * return its parsed [PASS]/[FAIL] output. Throws only on unexpected I/O.
 */
/** Extra data files a script reads from its own directory at runtime. */
const SCRIPT_ASSETS: Record<string, string[]> = {
  "v84_frozen_registry.py": ["predictions_frozen.json"],
};

export async function runScript(
  file: string,
  onStatus?: StatusFn,
): Promise<RunResult> {
  const py = await getPyodide(onStatus);
  onStatus?.(`Fetching ${file}…`);
  const src = await fetchText(`/verification/${file}`);
  py.FS.writeFile(`${WORK_DIR}/${file}`, src);
  for (const asset of SCRIPT_ASSETS[file] ?? []) {
    const data = await fetchText(`/verification/${asset}`);
    py.FS.writeFile(`${WORK_DIR}/${asset}`, data);
  }

  onStatus?.("Resolving packages (numpy, sympy, mpmath, scipy…)…");
  await py.loadPackagesFromImports(src);

  onStatus?.("Running the script…");
  const modname = file.replace(/\.py$/, "");
  // Capture stdout/stderr deterministically into a StringIO (newlines intact),
  // instead of relying on the per-line `batched` callback.
  const code = [
    "import importlib, sys, io, contextlib, traceback",
    "import tfpt_constants as _tc",
    "_tc.reset()",
    `sys.modules.pop(${JSON.stringify(modname)}, None)`,
    "_buf = io.StringIO()",
    "_err = ''",
    "with contextlib.redirect_stdout(_buf), contextlib.redirect_stderr(_buf):",
    "    try:",
    `        _m = importlib.import_module(${JSON.stringify(modname)})`,
    "        if hasattr(_m, 'run'):",
    "            _m.run()",
    "    except Exception:",
    "        _err = traceback.format_exc()",
    "_out = _buf.getvalue()",
  ].join("\n");

  let raw = "";
  let error: string | undefined;
  try {
    py.runPython(code);
    raw = String(py.globals.get("_out") ?? "");
    const err = String(py.globals.get("_err") ?? "");
    if (err.trim()) error = err;
  } catch (e) {
    error = e instanceof Error ? e.message : String(e);
  }

  const parsed = parseOutput(raw);
  return { ...parsed, raw, ok: error ? false : parsed.ok, error };
}

export function pyodideVersion() {
  return PYODIDE_VERSION;
}
