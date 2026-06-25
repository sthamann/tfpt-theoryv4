import React from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig, interpolate } from "remotion";
import { Bg } from "../components/Bg";
import { SANS, SERIF, MONO } from "../fonts";
import { COLORS, gradientText } from "../theme";
import { pop } from "../components/fx";
import { fadeInOut } from "../components/anim";

const CODE = "> seam     c₃ = 1/(8π)\n> carrier  g_car = 5\n> compile( reality )";

/** Particles that burst out of the code block — "unfolds into something huge". */
const Burst: React.FC<{ from: number; to: number }> = ({ from, to }) => {
  const frame = useCurrentFrame();
  const p = interpolate(frame, [from, to], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const golden = 2.399963;
  return (
    <>
      {Array.from({ length: 80 }).map((_, i) => {
        const a = i * golden;
        const spread = 360 + (i % 7) * 70;
        const r = p * spread;
        const x = Math.cos(a) * r;
        const y = Math.sin(a) * r * 0.62;
        const op = interpolate(p, [0, 0.2, 0.85, 1], [0, 1, 0.8, 0]) * (0.4 + (i % 5) / 7);
        const col = [COLORS.blueLight, COLORS.violet, COLORS.pink][i % 3];
        return (
          <div
            key={i}
            style={{
              position: "absolute",
              left: `calc(50% + ${x}px)`,
              top: `calc(50% + ${y}px)`,
              width: 6,
              height: 6,
              borderRadius: "50%",
              background: col,
              opacity: op,
              boxShadow: `0 0 8px ${col}`,
            }}
          />
        );
      })}
    </>
  );
};

export const Scene01Question: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const revealed = Math.floor(
    interpolate(frame, [18, 120], [0, CODE.length], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }),
  );
  const codeFade = interpolate(frame, [130, 260], [1, 0.12], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const caret = Math.floor(frame / 14) % 2 === 0 ? "▮" : " ";

  const sA = fadeInOut(frame, 150, 175, 250, 268); // "honest question"
  const sB = fadeInOut(frame, 300, 322, 430, 448); // "compiled, not chosen"
  const sC = fadeInOut(frame, 445, 468, 585, 599); // "where it leads / how it fails"

  return (
    <AbsoluteFill>
      <Bg accent={COLORS.blue} tint="#7c3aed" />

      {/* code block that types, then dims as it "compiles" */}
      <AbsoluteFill style={{ alignItems: "center", justifyContent: "center", opacity: codeFade }}>
        <pre
          style={{
            fontFamily: MONO,
            fontSize: 40,
            lineHeight: 1.6,
            color: COLORS.text,
            background: "rgba(2,6,18,0.55)",
            border: `1px solid ${COLORS.border}`,
            borderRadius: 18,
            padding: "30px 44px",
            margin: 0,
          }}
        >
          {CODE.slice(0, revealed)}
          <span style={{ color: COLORS.blueLight }}>{revealed >= CODE.length - 1 ? caret : ""}</span>
        </pre>
      </AbsoluteFill>

      <AbsoluteFill style={{ alignItems: "center", justifyContent: "center" }}>
        <Burst from={120} to={300} />
      </AbsoluteFill>

      {/* the question */}
      <AbsoluteFill style={{ flexDirection: "column", alignItems: "center", justifyContent: "center", gap: 30 }}>
        <div style={{ height: 90 }}>
          <div style={{ opacity: sA, position: "absolute", left: 0, right: 0, textAlign: "center", fontFamily: SANS, fontSize: 38, color: COLORS.textDim }}>
            An honest question — not a claim.
          </div>
        </div>
        <div
          style={{
            ...pop(frame, fps, 258, { y: 30, from: 0.8 }),
            fontFamily: SERIF,
            fontWeight: 600,
            fontSize: 104,
            letterSpacing: -2,
            ...gradientText(),
          }}
        >
          Is reality compiled?
        </div>
        <div style={{ position: "relative", height: 70, width: 1400 }}>
          <div style={{ opacity: sB, position: "absolute", inset: 0, textAlign: "center", fontFamily: SANS, fontSize: 40, color: COLORS.text }}>
            Could the rules be the <b style={{ color: COLORS.textBright }}>output</b> of something tiny — compiled, not chosen?
          </div>
          <div style={{ opacity: sC, position: "absolute", inset: 0, textAlign: "center", fontFamily: SANS, fontSize: 36, color: COLORS.textDim }}>
            Let's see where that leads — and <b style={{ color: COLORS.open }}>how it could fail</b>.
          </div>
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
