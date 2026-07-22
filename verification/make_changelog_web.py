#!/usr/bin/env python3
"""Generate the website changelog mirror from the canonical changelog.tex.

Source : changelog.tex             (repo root; THE canonical dated changelog)
Target : website/lib/changelog.ts  (typed data the /changelog page renders)

The target is GENERATED -- never edit it by hand.  To change the changelog,
edit changelog.tex (newest first, plain LaTeX) and re-run:

    python3 verification/make_changelog_web.py           # rewrite the target
    python3 verification/make_changelog_web.py --check    # exit 1 if stale

It is run automatically by `bash build.sh gen`, and its freshness is enforced
by verification/audit_sync.py (section A.generated) so the public /changelog
page can never drift from changelog.tex -- the single source of truth.

The parser turns the small, fixed LaTeX subset used in the changelog
(\\subsection*ed dated entries, itemized \\item lines, and the inline markup
\\textbf \\emph \\texttt \\vref \\veri, the status markers \\mE/\\mC/\\mO/\\mX,
inline math $...$, accents and dashes) into a typed node tree that the page
renders -- math via KaTeX (using the convenience macros mirrored from the
changelog.tex preamble).

stdlib only -- runnable without the venv (build.sh calls it with python3).
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHANGELOG_TEX = ROOT / "changelog.tex"
WEBSITE_DIR = ROOT / "website"
TS_TARGET = WEBSITE_DIR / "lib" / "changelog.ts"

# Status-marker macros -> public four-class letter (incl. the legacy aliases
# kept in the changelog.tex preamble so old entries still render their class).
MARKERS = {
    "mE": "E", "mC": "C", "mO": "O", "mX": "X",
    "tI": "E", "tL": "E", "tF": "E", "tN": "E", "tIalg": "E", "tInum": "E",
    "tP": "C", "tB": "C", "tR": "C", "tA": "O", "tX": "X",
}

# Inline math macros whose bodies are read from the changelog.tex preamble and
# handed to KaTeX at render time (single source: the \providecommand block).
MATH_MACRO_NAMES = [
    "cthree", "phiz", "gcar", "Nfam", "Oadm", "ainv", "Mbar", "Z", "PP",
]

# LaTeX accent command -> precomposed-character lookup (only the accents that
# actually occur in the changelog text, e.g. M\"obius, Calder\'on, Pl\"ucker).
ACCENTS = {
    '"': {"a": "ä", "o": "ö", "u": "ü", "e": "ë", "i": "ï",
          "A": "Ä", "O": "Ö", "U": "Ü"},
    "'": {"a": "á", "e": "é", "i": "í", "o": "ó", "u": "ú",
          "c": "ć", "n": "ń", "y": "ý", "s": "ś", "z": "ź",
          "A": "Á", "E": "É", "O": "Ó"},
    "`": {"a": "à", "e": "è", "i": "ì", "o": "ò", "u": "ù"},
    "^": {"a": "â", "e": "ê", "i": "î", "o": "ô", "u": "û"},
    "~": {"a": "ã", "n": "ñ", "o": "õ"},
    "=": {"a": "ā", "e": "ē", "o": "ō", "u": "ū"},
    ".": {"z": "ż"},
}

# Commands whose braced argument is rendered verbatim as a monospace code span.
CODE_CMDS = {"texttt", "vref", "veri", "path", "code", "verb"}
# Commands that are transparent (their content is rendered inline as-is).
TRANSPARENT_CMDS = {"textrm", "textnormal", "text", "mbox", "textsc", "ensuremath"}


# --------------------------------------------------------------------------
# LaTeX scanning helpers (escape-aware so $\{...\}$ etc. do not miscount)
# --------------------------------------------------------------------------

def read_group(s: str, i: int) -> tuple[str, int]:
    """s[i] must be '{'. Return (inner_text, index_after_closing_brace)."""
    assert s[i] == "{", f"expected '{{' at {i}: {s[i:i + 30]!r}"
    depth = 0
    j = i
    while j < len(s):
        c = s[j]
        if c == "\\":           # escaped char: skip the next char wholesale
            j += 2
            continue
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return s[i + 1:j], j + 1
        j += 1
    raise ValueError(f"unbalanced braces from {i}: {s[i:i + 40]!r}")


def clean_code(s: str) -> str:
    """Normalise the content of a \\texttt/\\vref/\\veri argument to plain text."""
    s = s.replace("\\allowbreak", "")
    s = re.sub(r"\\([_&#%{}$*])", r"\1", s)        # \_ \& \# \% \{ \} \$ \* -> literal
    s = re.sub(r"\\textbackslash\s*", "\\\\", s)   # \textbackslash subsection -> \subsection
    s = s.replace("\\,", " ").replace("~", "\u00a0")
    s = re.sub(r"[ \t\r\n]+", " ", s)
    return s.strip()


def apply_text_subs(t: str) -> str:
    """Collapse ASCII whitespace (keeping NBSP) and apply LaTeX dash/quote subs."""
    t = re.sub(r"[ \t\r\n]+", " ", t)
    t = t.replace("``", "\u201c").replace("''", "\u201d")
    t = t.replace("---", "\u2014").replace("--", "\u2013")
    return t


# --------------------------------------------------------------------------
# Inline parser: LaTeX subset -> list of node dicts
#   {"k":"t","v":..}   text          {"k":"b","c":[..]}  bold
#   {"k":"m","v":..}   inline math    {"k":"i","c":[..]}  italic
#   {"k":"c","v":..}   code / ref     {"k":"s","v":"E"}   status marker
# --------------------------------------------------------------------------

def parse_inline(s: str) -> list[dict]:
    nodes: list[dict] = []
    buf: list[str] = []

    def flush() -> None:
        if not buf:
            return
        text = apply_text_subs("".join(buf))
        buf.clear()
        if text != "":
            nodes.append({"k": "t", "v": text})

    i, n = 0, len(s)
    while i < n:
        c = s[i]

        if c == "$":                                   # inline math
            flush()
            j = i + 1
            while j < n and s[j] != "$":
                j += 2 if s[j] == "\\" else 1
            nodes.append({"k": "m", "v": s[i + 1:j].strip()})
            i = j + 1
            continue

        if c == "~":                                   # non-breaking space
            buf.append("\u00a0")
            i += 1
            continue

        if c == "\\":
            m = re.match(r"\\([a-zA-Z]+)", s[i:])
            if not m:                                  # escaped punctuation / accent
                nxt = s[i + 1] if i + 1 < n else ""
                if nxt in ACCENTS:
                    k = i + 2
                    if k < n and s[k] == "{":
                        grp, k = read_group(s, k)
                        letter = grp[:1]
                    else:
                        letter = s[k] if k < n else ""
                        k += 1
                    buf.append(ACCENTS[nxt].get(letter, letter))
                    i = k
                elif nxt == " ":
                    buf.append(" ")
                    i += 2
                elif nxt == ",":
                    buf.append("\u202f")               # thin space
                    i += 2
                else:
                    buf.append(nxt)
                    i += 2
                continue

            name = m.group(1)
            i += m.end()

            if name in MARKERS:
                flush()
                nodes.append({"k": "s", "v": MARKERS[name]})
                if i + 1 < n and s[i] == "\\" and s[i + 1] == " ":  # swallow "\ "
                    i += 2
                continue
            if name == "allowbreak":
                continue
            if name in ("ldots", "dots"):
                buf.append("\u2026")
                continue
            if i < n and s[i] == "{":
                content, i = read_group(s, i)
                if name in CODE_CMDS:
                    flush()
                    nodes.append({"k": "c", "v": clean_code(content)})
                elif name == "textbf":
                    flush()
                    nodes.append({"k": "b", "c": parse_inline(content)})
                elif name in ("emph", "textit", "textsl"):
                    flush()
                    nodes.append({"k": "i", "c": parse_inline(content)})
                else:                                  # transparent / unknown w/ arg
                    sub = parse_inline(content)
                    flush()
                    nodes.extend(sub)
                continue
            # bare command with no argument (e.g. spacing) -> drop
            continue

        buf.append(c)
        i += 1

    flush()
    return strip_edge_space(nodes)


def strip_edge_space(nodes: list[dict]) -> list[dict]:
    """Drop leading/trailing text nodes that are pure whitespace."""
    def blank(nd: dict) -> bool:
        return nd["k"] == "t" and nd["v"].strip() == ""
    while nodes and blank(nodes[0]):
        nodes.pop(0)
    while nodes and blank(nodes[-1]):
        nodes.pop()
    return nodes


# --------------------------------------------------------------------------
# Block parser: changelog.tex -> list of dated entries
# --------------------------------------------------------------------------

def load_math_macros(tex: str) -> dict[str, str]:
    macros: dict[str, str] = {}
    for name in MATH_MACRO_NAMES:
        m = re.search(r"\\providecommand\{\\" + name + r"\}\s*", tex)
        if not m:
            continue
        brace = tex.index("{", m.end() - 1)
        body, _ = read_group(tex, brace)
        macros["\\" + name] = body
    return macros


def parse_items(body: str) -> list[list[dict]]:
    m = re.search(r"\\begin\{itemize\}(.*?)\\end\{itemize\}", body, re.S)
    if not m:
        return []
    inner = m.group(1).lstrip()
    # drop the enumitem optional argument (e.g. [leftmargin=1.5em]) so it is
    # not rendered as a bogus first bullet
    if inner.startswith("["):
        close = inner.find("]")
        if close != -1:
            inner = inner[close + 1:]
    parts = re.split(r"\\item\b", inner)
    items = []
    for part in parts:
        part = part.strip()
        if not part:
            continue
        nodes = parse_inline(part)
        if nodes:
            items.append(nodes)
    return items


def strip_outer_parens(s: str) -> str:
    """Drop one balanced outer '(...)' wrapper; leave the string untouched if the
    parentheses are not a single outermost balanced pair (safe no-op fallback)."""
    s = s.strip()
    if not (s.startswith("(") and s.endswith(")")):
        return s
    depth = 0
    for idx, ch in enumerate(s):
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth == 0:                    # first '(' closes here
                return s[1:-1].strip() if idx == len(s) - 1 else s
    return s


def parse_title(title_raw: str) -> tuple[str, str, list[dict]]:
    title_raw = title_raw.strip()
    dm = re.match(
        r"\s*(20\d\d-\d\d-\d\d(?:\s*/\s*20\d\d-\d\d-\d\d)*)\s*",
        title_raw, re.S,
    )
    if dm:
        date_label = re.sub(r"\s+", " ", dm.group(1)).strip()
        rest = title_raw[dm.end():].strip()
    else:
        date_label, rest = "", title_raw

    # Multi-entry days tag each entry with a roman-numeral enumerator that is its
    # own leading parenthetical, e.g. "(XXIII) (the real summary ...)". Pull the
    # enumerator into the date label so the heading is only the summary and never
    # renders as the bogus "XXIII) (" prefix on the site.
    enum = ""
    em = re.match(r"\(([IVXLCDM]+)\)\s*(\(.*)$", rest, re.S)
    if em:
        enum = em.group(1)
        rest = em.group(2).strip()

    heading_raw = strip_outer_parens(rest)
    if enum:
        date_label = f"{date_label} \u00b7 {enum}" if date_label else enum

    dates = re.findall(r"20\d\d-\d\d-\d\d", date_label or title_raw)
    sort_date = max(dates) if dates else "0000-00-00"
    return sort_date, date_label, parse_inline(heading_raw)


def parse_entries(tex: str) -> list[dict]:
    starts = [m.start() for m in re.finditer(r"\\subsection\*\{", tex)]
    entries = []
    for idx, start in enumerate(starts):
        brace = tex.index("{", start)
        title_raw, after = read_group(tex, brace)
        end = starts[idx + 1] if idx + 1 < len(starts) else len(tex)
        body = tex[after:end]
        body = re.split(r"\\ifdefined\\ChangelogImported\\else", body)[0]
        sort_date, date_label, heading = parse_title(title_raw)
        entries.append({
            "date": sort_date,
            "dateLabel": date_label,
            "heading": heading,
            "items": parse_items(body),
        })
    return entries


# --------------------------------------------------------------------------
# TypeScript emitter
# --------------------------------------------------------------------------

TS_HEADER = """\
// GENERATED FILE -- DO NOT EDIT BY HAND.
// Mirror of the canonical changelog.tex (repo root). Single source of truth.
// Regenerate with:  python3 verification/make_changelog_web.py
// (run automatically by `bash build.sh gen`; freshness enforced by
//  verification/audit_sync.py, so this page can never drift from changelog.tex).

/**
 * One inline node of a changelog entry.
 *   k = "t" text · "m" inline math (KaTeX) · "c" code / script ref ·
 *       "s" status marker (v is "E" | "C" | "O" | "X") · "b" bold · "i" italic
 */
export interface ChangelogNode {
  k: "t" | "m" | "c" | "s" | "b" | "i";
  v?: string;
  c?: ChangelogNode[];
}

export interface ChangelogEntry {
  /** Sort key (YYYY-MM-DD, newest first) -- the latest date in the heading. */
  date: string;
  /** Literal date label as written, e.g. "2026-06-07 / 2026-06-08". */
  dateLabel: string;
  /** Parsed heading (the parenthetical after the date); empty for bare dates. */
  heading: ChangelogNode[];
  /** The entry's bullet points, each a list of inline nodes. */
  items: ChangelogNode[][];
}

/** KaTeX macros mirrored from the changelog.tex standalone preamble. */
export const CHANGELOG_MACROS: Record<string, string> =
"""

TS_FOOTER = """
export const CHANGELOG_COUNT = CHANGELOG.length;
"""


def build() -> dict[Path, str]:
    tex = CHANGELOG_TEX.read_text()
    macros = load_math_macros(tex)
    entries = parse_entries(tex)
    body = (
        TS_HEADER
        + json.dumps(macros, ensure_ascii=False, indent=2)
        + ";\n\nexport const CHANGELOG: ChangelogEntry[] = "
        + json.dumps(entries, ensure_ascii=False, indent=2)
        + ";\n"
        + TS_FOOTER
    )
    return {TS_TARGET: body}


def main() -> None:
    check_only = "--check" in sys.argv
    stale = []
    for target, content in build().items():
        # Shadow-export trees ship no website/ -- skip the mirror there instead
        # of crashing on a missing parent directory (mirrors make_script_index).
        if WEBSITE_DIR in target.parents and not WEBSITE_DIR.exists():
            if not check_only:
                print(f"skipped (no website/ in this tree): {target.relative_to(ROOT)}")
            continue
        if not target.exists() or target.read_text() != content:
            if check_only:
                stale.append(target)
            else:
                target.write_text(content)
                print(f"wrote {target.relative_to(ROOT)}")
    if check_only:
        if stale:
            for t in stale:
                print(f"STALE (re-run make_changelog_web.py): {t.relative_to(ROOT)}")
            sys.exit(1)
        print("changelog mirror up to date")


if __name__ == "__main__":
    main()
