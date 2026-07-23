import React from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig } from "remotion";
import { Bg } from "../components/Bg";
import { Eyebrow } from "../components/ui";
import { StatusChip } from "../components/StatusChip";
import { SANS, SERIF, MONO } from "../fonts";
import { COLORS, StatusGrade, gradientText } from "../theme";
import { pop } from "../components/fx";
import { fadeInOut } from "../components/anim";

const CYAN = "#22d3ee";

type Beat = {
  index: string;
  short: string; // bottom-tracker label
  title: string;
  formula: string;
  sub: string;
  grade: StatusGrade;
  fence: string; // the honesty fence, verbatim discipline
  color: string;
};

/**
 * The five results of the 2026-07-22/23 sprint (v519–v529), each with its
 * honesty fence. Numbers verified against the ledger/registry before render:
 * ψ = 64 (v523), T_seam = 4c₃ / β-angle = 2π (v526), 10 side-blind tests
 * (v529), kill-test 2 fires at toy level (v529). No marker moves — the fences
 * ("probe level", "free level", "toy level", "still an input") protect that.
 */
const BEATS: Beat[] = [
  {
    index: "01",
    short: "measure",
    title: "The measure chain — derived",
    formula: "ψ = 64 — computed, not put in",
    sub: "single-valuedness is forced; the normalisation is a fixed-point factor, computed from three independent sources",
    grade: "E",
    fence: "derived at probe level · one global integral still open",
    color: COLORS.blueLight,
  },
  {
    index: "02",
    short: "bridge",
    title: "The Woit bridge stands — through β₂",
    formula: "Θ exists · OS quotient built · clock = time operator",
    sub: "Euclidean → real: the thaw protocol works — the μ₄ clock returns as a positive time operator",
    grade: "C",
    fence: "at the free level · the interacting case stays open",
    color: COLORS.violet,
  },
  {
    index: "03",
    short: "thermal",
    title: "The seam is thermal",
    formula: "T_seam = 4c₃ · β-angle = 2π exact",
    sub: "the founding axiom c₃ = 1/(8π) now carries geometry, anomaly and temperature — a miniature horizon",
    grade: "E",
    fence: "the third leg of c₃",
    color: COLORS.exact,
  },
  {
    index: "04",
    short: "bit",
    title: "The one input bit — now measurable",
    formula: "10 side-blind tests · one order parameter",
    sub: "not derivable in the whole computable class — but physically defined, in principle readable by interferometry",
    grade: "C",
    fence: "one axiom becomes one measurement · still an input",
    color: CYAN,
  },
  {
    index: "05",
    short: "filter",
    title: "The first hard filter",
    formula: "kill test 2 fires — at toy level",
    sub: "the first interacting toy breaks reflection positivity, exactly by the straddle law — a threat, and a selection principle",
    grade: "O",
    fence: "honestly reported · the frontier narrows",
    color: COLORS.open,
  },
];

// scene-local frame windows (scene = 57 s = 1710 frames @ 30 fps), aligned
// with the caption cues in captions.json (scene starts at 245 s absolute)
const INTRO = { in: 10, hold: 132, out: 156 };
const WINDOWS: [number, number][] = [
  [162, 462], // 250.4–260.4 s
  [468, 777], // 260.6–270.9 s
  [783, 1092], // 271.1–281.4 s
  [1098, 1407], // 281.6–291.9 s
  [1413, 1698], // 292.1–301.6 s
];
const FADE = 22;

const BeatCard: React.FC<{ beat: Beat; from: number; to: number }> = ({ beat, from, to }) => {
  const frame = useCurrentFrame();
  const o = fadeInOut(frame, from, from + FADE, to - FADE, to);
  const rise = Math.max(0, 1 - (frame - from) / FADE);
  return (
    <div
      style={{
        position: "absolute",
        inset: 0,
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        gap: 24,
        opacity: o,
        transform: `translateY(${rise * 26}px)`,
        paddingBottom: 130,
      }}
    >
      <div style={{ fontFamily: MONO, fontSize: 26, letterSpacing: 6, color: beat.color, fontWeight: 700 }}>
        {beat.index} / 05
      </div>
      <div style={{ fontFamily: SERIF, fontSize: 62, fontWeight: 600, color: COLORS.textBright, letterSpacing: -1, textAlign: "center", maxWidth: 1500 }}>
        {beat.title}
      </div>
      <div
        style={{
          fontFamily: MONO,
          fontSize: 34,
          fontWeight: 700,
          color: beat.color,
          padding: "14px 30px",
          borderRadius: 14,
          background: "rgba(2,6,18,0.6)",
          border: `1.5px solid ${beat.color}66`,
          boxShadow: `0 0 44px -18px ${beat.color}`,
          whiteSpace: "nowrap",
        }}
      >
        {beat.formula}
      </div>
      <div style={{ fontFamily: SANS, fontSize: 29, color: COLORS.text, textAlign: "center", maxWidth: 1240, lineHeight: 1.45 }}>
        {beat.sub}
      </div>
      <div style={{ display: "flex", alignItems: "center", gap: 16 }}>
        <StatusChip grade={beat.grade} size={20} showLabel={false} />
        <span style={{ fontFamily: MONO, fontSize: 22, color: COLORS.textDim, letterSpacing: 0.5 }}>{beat.fence}</span>
      </div>
    </div>
  );
};

export const Scene08Breakthroughs: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const intro = fadeInOut(frame, INTRO.in, INTRO.in + 27, INTRO.hold, INTRO.out);
  const activeBeat = WINDOWS.filter(([from]) => frame >= from).length - 1;

  return (
    <AbsoluteFill>
      <Bg accent={COLORS.pink} tint="#22d3ee" />
      <AbsoluteFill style={{ flexDirection: "column", alignItems: "center", paddingTop: 56 }}>
        <div style={pop(frame, fps, 8)}>
          <Eyebrow color={COLORS.pink}>It hasn't stopped — five new results</Eyebrow>
        </div>
      </AbsoluteFill>

      {/* intro card */}
      <AbsoluteFill style={{ flexDirection: "column", alignItems: "center", justifyContent: "center", gap: 26, opacity: intro, paddingBottom: 120 }}>
        <div style={{ fontFamily: SERIF, fontSize: 88, fontWeight: 600, letterSpacing: -1.5, ...gradientText() }}>
          Five breakthroughs
        </div>
        <div style={{ fontFamily: SANS, fontSize: 34, color: COLORS.text }}>
          one 48-hour sprint · July 2026 · each machine-checked, each honestly labelled
        </div>
      </AbsoluteFill>

      {/* the five beats */}
      {BEATS.map((b, i) => (
        <BeatCard key={b.index} beat={b} from={WINDOWS[i][0]} to={WINDOWS[i][1]} />
      ))}

      {/* bottom tracker */}
      <AbsoluteFill style={{ alignItems: "center", justifyContent: "flex-end", paddingBottom: 252 }}>
        <div style={{ ...pop(frame, fps, INTRO.out - 10), display: "flex", gap: 18 }}>
          {BEATS.map((b, i) => {
            const lit = i <= activeBeat;
            return (
              <div
                key={b.short}
                style={{
                  display: "flex",
                  alignItems: "center",
                  gap: 10,
                  padding: "8px 18px",
                  borderRadius: 999,
                  background: lit ? `${b.color}1c` : "rgba(15,23,42,0.5)",
                  border: `1px solid ${lit ? `${b.color}88` : COLORS.border}`,
                }}
              >
                <span
                  style={{
                    width: 10,
                    height: 10,
                    borderRadius: "50%",
                    background: lit ? b.color : "rgba(148,163,184,0.35)",
                    boxShadow: lit ? `0 0 10px ${b.color}` : "none",
                  }}
                />
                <span style={{ fontFamily: MONO, fontSize: 20, color: lit ? COLORS.textBright : COLORS.textFaint, letterSpacing: 1 }}>
                  {b.short}
                </span>
              </div>
            );
          })}
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
