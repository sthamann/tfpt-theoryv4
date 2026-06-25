import React from "react";
import { AbsoluteFill, useCurrentFrame, interpolate, Easing } from "remotion";
import { Bg } from "../components/Bg";
import { Eyebrow } from "../components/ui";
import { StatusChip } from "../components/StatusChip";
import { SANS, SERIF, MONO } from "../fonts";
import { COLORS } from "../theme";
import { enterUp, fade, fadeInOut } from "../components/anim";

const CORE = [
  "3 generations of matter",
  "the right electric charges",
  "16 carrier states",
  "the atoms 2 · 3 · 5",
  "Coxeter number 30",
  "240 roots of E₈",
];
const BOUNDARY = [
  "one seed φ₀, from c₃",
  "the Cabibbo angle",
  "the α fixed point",
  "the scale grammar",
];

const ListCard: React.FC<{
  title: string;
  grade: "E" | "C";
  accent: string;
  items: string[];
  baseStart: number;
  frame: number;
}> = ({ title, grade, accent, items, baseStart, frame }) => (
  <div
    style={{
      width: 660,
      padding: 36,
      borderRadius: 24,
      background: "rgba(10,16,30,0.62)",
      border: `1px solid ${accent}40`,
      backdropFilter: "blur(8px)",
    }}
  >
    <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: 24, ...enterUp(frame, baseStart, 20) }}>
      <div style={{ fontFamily: SERIF, fontSize: 42, fontWeight: 600, color: COLORS.textBright }}>
        {title}
      </div>
      <StatusChip grade={grade} size={22} />
    </div>
    <div style={{ display: "flex", flexDirection: "column", gap: 18 }}>
      {items.map((it, i) => {
        const e = enterUp(frame, baseStart + 24 + i * 16, 20, 14);
        return (
          <div key={it} style={{ display: "flex", alignItems: "center", gap: 16, ...e }}>
            <div style={{ width: 12, height: 12, borderRadius: 3, background: accent, flexShrink: 0 }} />
            <div style={{ fontFamily: i < 2 ? SANS : MONO, fontSize: 30, color: COLORS.text, fontWeight: 500 }}>
              {it}
            </div>
          </div>
        );
      })}
    </div>
  </div>
);

export const Scene03Readout: React.FC = () => {
  const frame = useCurrentFrame();

  const eyebrow = enterUp(frame, 6, 22);
  const cols = fadeInOut(frame, 30, 70, 740, 800);
  const colShift = interpolate(frame, [740, 810], [0, -40], {
    easing: Easing.in(Easing.cubic),
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  const alphaIn = fade(frame, 770, 820);
  const num = enterUp(frame, 790, 30); // α⁻¹ lands (~81.5s)
  const sigma = enterUp(frame, 960, 24); // ~86.8s
  const verdict = enterUp(frame, 1085, 24); // ~91s

  return (
    <AbsoluteFill>
      <Bg accent={COLORS.blue} tint="#0ea5e9" />
      <AbsoluteFill style={{ flexDirection: "column", alignItems: "center", paddingTop: 92 }}>
        <div style={eyebrow}>
          <Eyebrow>The readout — what comes out</Eyebrow>
        </div>

        {/* two columns */}
        <div
          style={{
            position: "absolute",
            top: 250,
            display: "flex",
            gap: 56,
            opacity: cols,
            transform: `translateY(${colShift}px)`,
          }}
        >
          <ListCard title="Discrete core" grade="E" accent={COLORS.violet} items={CORE} baseStart={120} frame={frame} />
          <ListCard title="Boundary side" grade="C" accent={COLORS.blueLight} items={BOUNDARY} baseStart={360} frame={frame} />
        </div>

        {/* alpha reveal */}
        <div
          style={{
            position: "absolute",
            top: 252,
            opacity: alphaIn,
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            gap: 22,
            width: 1600,
          }}
        >
          <div style={{ fontFamily: SANS, fontSize: 32, color: COLORS.textDim, ...enterUp(frame, 790, 24) }}>
            the single positive root of one cubic
          </div>
          <div
            style={{
              fontFamily: MONO,
              fontWeight: 700,
              fontSize: 118,
              whiteSpace: "nowrap",
              color: COLORS.textBright,
              textShadow: "0 0 70px rgba(96,165,250,0.4)",
              ...num,
            }}
          >
            α⁻¹ = 137.0359992
          </div>
          <div
            style={{
              fontFamily: SANS,
              fontSize: 34,
              color: COLORS.exact,
              fontWeight: 600,
              ...sigma,
            }}
          >
            1.9σ from CODATA-2022
          </div>
          <div
            style={{
              fontFamily: SERIF,
              fontWeight: 600,
              fontSize: 58,
              ...verdict,
            }}
          >
            <span style={{ color: COLORS.textDim }}>Not a fit. </span>
            <span style={{ color: COLORS.textBright }}>A forced answer.</span>
          </div>
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
