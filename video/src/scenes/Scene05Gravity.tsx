import React from "react";
import { AbsoluteFill, useCurrentFrame } from "remotion";
import { Bg } from "../components/Bg";
import { Eyebrow } from "../components/ui";
import { Formula, Tok } from "../components/Formula";
import { SANS, SERIF } from "../fonts";
import { COLORS } from "../theme";
import { enterUp, fade } from "../components/anim";

const OVERDET = [
  { label: "anchor", sub: "a = (1, 1, 2)" },
  { label: "geometry", sub: "|μ₄| = 4" },
  { label: "thermodynamics", sub: "horizon heat" },
];

export const Scene05Gravity: React.FC = () => {
  const frame = useCurrentFrame();

  const eyebrow = enterUp(frame, 6, 22);
  const bridge = enterUp(frame, 120, 24); // c₃ = 1/(8π) → c₃⁻¹ = 8π (~124.5s)
  const einstein = enterUp(frame, 160, 26);
  const glow = fade(frame, 160, 240, 0.25, 1);
  const sub = enterUp(frame, 300, 24); // "full law of gravity" (~130s)
  const lambda = enterUp(frame, 470, 24); // Λ from α (~135.5s)
  const triadLabel = enterUp(frame, 600, 22); // three ways (~140s)

  return (
    <AbsoluteFill>
      <Bg accent={COLORS.exact} tint="#f59e0b" />
      <AbsoluteFill style={{ flexDirection: "column", alignItems: "center", paddingTop: 80, gap: 30 }}>
        <div style={eyebrow}>
          <Eyebrow color={COLORS.exact}>Gravity comes free</Eyebrow>
        </div>

        {/* the input IS the 8π */}
        <div style={{ ...bridge, marginTop: 6 }}>
          <Formula size={34} plate>
            <Tok color={COLORS.blueLight}>c₃ = 1/(8π)</Tok>
            <span style={{ color: COLORS.textDim, margin: "0 6px" }}>⇒</span>
            <Tok color={COLORS.exact}>c₃⁻¹ = 8π</Tok>
          </Formula>
        </div>

        {/* the full covariant Einstein equation, 8π highlighted */}
        <div
          style={{
            ...einstein,
            padding: "32px 56px",
            borderRadius: 24,
            background: "rgba(2,6,18,0.55)",
            border: `1px solid ${COLORS.exact}55`,
            boxShadow: `0 0 ${30 + glow * 70}px -16px ${COLORS.exact}`,
          }}
        >
          <Formula size={66} plate={false}>
            <Tok color={COLORS.textBright}>G</Tok>
            <span style={{ color: COLORS.textDim }}>ₐᵦ + Λ</span>
            <Tok color={COLORS.textBright}>g</Tok>
            <span style={{ color: COLORS.textDim }}>ₐᵦ =</span>
            <Tok color={COLORS.exact}>8π</Tok>
            <Tok color={COLORS.textBright}>T</Tok>
            <span style={{ color: COLORS.textDim }}>ₐᵦ</span>
          </Formula>
        </div>

        <div style={{ ...sub, fontFamily: SANS, fontSize: 30, color: COLORS.textDim, textAlign: "center", maxWidth: 1280 }}>
          the full law of gravity — <b style={{ color: COLORS.text }}>both constants fixed</b>, nothing tuned.
        </div>

        {/* Λ from α */}
        <div
          style={{
            ...lambda,
            display: "flex",
            alignItems: "center",
            gap: 18,
            padding: "16px 30px",
            borderRadius: 16,
            background: COLORS.conditionalBg,
            border: `1px solid ${COLORS.conditional}55`,
          }}
        >
          <span style={{ fontFamily: SANS, fontSize: 26, color: COLORS.conditional, fontWeight: 600 }}>
            even the cosmological constant
          </span>
          <Formula size={30} plate={false}>
            <span style={{ color: COLORS.textDim }}>Λ ∼</span> <Tok color={COLORS.textBright}>e</Tok>
            <span style={{ color: COLORS.textBright }}>⁻²ᵃ⁻¹</span>
          </Formula>
        </div>

        {/* triple over-determination — the punchline */}
        <div style={{ ...triadLabel, display: "flex", flexDirection: "column", alignItems: "center", gap: 16, marginTop: 6 }}>
          <div style={{ fontFamily: SANS, fontSize: 26, color: COLORS.textDim }}>
            the same <b style={{ color: COLORS.exact }}>1/(8π)</b> shows up three independent ways
          </div>
          <div style={{ display: "flex", gap: 20 }}>
            {OVERDET.map((o, i) => {
              const e = enterUp(frame, 620 + i * 22, 22, 22);
              return (
                <div
                  key={o.label}
                  style={{
                    ...e,
                    display: "flex",
                    flexDirection: "column",
                    alignItems: "center",
                    gap: 6,
                    width: 300,
                    padding: "20px 24px",
                    borderRadius: 18,
                    background: "rgba(10,16,30,0.6)",
                    border: `1.5px solid ${COLORS.exact}44`,
                  }}
                >
                  <div style={{ fontFamily: SERIF, fontSize: 32, fontWeight: 600, color: COLORS.textBright }}>
                    {o.label}
                  </div>
                  <div style={{ fontFamily: SANS, fontSize: 22, color: COLORS.textDim }}>{o.sub}</div>
                </div>
              );
            })}
          </div>
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
