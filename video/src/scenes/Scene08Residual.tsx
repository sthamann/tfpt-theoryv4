import React from "react";
import { AbsoluteFill, useCurrentFrame } from "remotion";
import { Bg } from "../components/Bg";
import { Eyebrow, BrandMark } from "../components/ui";
import { StatusChip } from "../components/StatusChip";
import { SANS, SERIF, MONO } from "../fonts";
import { COLORS, StatusGrade } from "../theme";
import { enterUp, fade } from "../components/anim";

/** The three named, typed handoffs — the entire honest residual. */
const HANDOFFS: {
  title: string;
  id: string;
  body: string;
  grade: StatusGrade;
  accent: string;
  at: number;
}[] = [
  {
    title: "The central seam",
    id: "G_net",
    body: "closed — one published theorem away",
    grade: "C",
    accent: COLORS.conditional,
    at: 285, // ~228.5s
  },
  {
    title: "External physics",
    id: "F_transfer",
    body: "Koide · η_B · axion · mₚ/mₑ — labelled bridges",
    grade: "C",
    accent: COLORS.violet,
    at: 450, // ~234s
  },
  {
    title: "One honest unit",
    id: "v_geo",
    body: "a theorem forbids a scale from pure numbers",
    grade: "O",
    accent: COLORS.open,
    at: 600, // ~239s
  },
];

export const Scene08Residual: React.FC = () => {
  const frame = useCurrentFrame();

  const residual = 1 - fade(frame, 770, 812);
  const eyebrow = enterUp(frame, 6, 22);
  const intro = enterUp(frame, 135, 24); // "three named handoffs" (~223.5s)

  const end = fade(frame, 782, 836);
  const endRise = enterUp(frame, 782, 34);

  return (
    <AbsoluteFill>
      <Bg accent={COLORS.conditional} tint="#a78bfa" />

      {/* residual layer */}
      <AbsoluteFill
        style={{ flexDirection: "column", alignItems: "center", paddingTop: 96, gap: 28, opacity: residual }}
      >
        <div style={eyebrow}>
          <Eyebrow color={COLORS.conditional}>What is actually open</Eyebrow>
        </div>

        <div
          style={{
            ...intro,
            fontFamily: SERIF,
            fontSize: 46,
            fontWeight: 600,
            color: COLORS.textBright,
            textAlign: "center",
            maxWidth: 1400,
          }}
        >
          Not a vague pile — <span style={{ color: COLORS.conditional }}>three named handoffs</span>, and{" "}
          <b style={{ color: COLORS.textBright }}>zero hidden mechanisms</b>.
        </div>

        <div style={{ display: "flex", gap: 28, marginTop: 18 }}>
          {HANDOFFS.map((h) => {
            const e = enterUp(frame, h.at, 24, 26);
            return (
              <div
                key={h.id}
                style={{
                  ...e,
                  width: 540,
                  minHeight: 260,
                  display: "flex",
                  flexDirection: "column",
                  gap: 18,
                  padding: 34,
                  borderRadius: 24,
                  background: "rgba(10,16,30,0.64)",
                  border: `1.5px solid ${h.accent}55`,
                  backdropFilter: "blur(8px)",
                }}
              >
                <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
                  <div style={{ fontFamily: SERIF, fontSize: 38, fontWeight: 600, color: COLORS.textBright }}>
                    {h.title}
                  </div>
                  <StatusChip grade={h.grade} size={20} />
                </div>
                <div
                  style={{
                    fontFamily: MONO,
                    fontSize: 34,
                    fontWeight: 700,
                    color: h.accent,
                    letterSpacing: 1,
                  }}
                >
                  {h.id}
                </div>
                <div style={{ fontFamily: SANS, fontSize: 28, color: COLORS.text, lineHeight: 1.35 }}>
                  {h.body}
                </div>
              </div>
            );
          })}
        </div>
      </AbsoluteFill>

      {/* end card */}
      <AbsoluteFill
        style={{
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center",
          gap: 28,
          opacity: end * endRise.opacity,
          transform: endRise.transform,
        }}
      >
        <BrandMark size={72} />
        <div
          style={{
            fontFamily: SERIF,
            fontSize: 66,
            fontWeight: 600,
            color: COLORS.textBright,
            textAlign: "center",
            letterSpacing: -1,
          }}
        >
          Two inputs. One compiler.
          <br />
          Fully audited.
        </div>
        <div style={{ fontFamily: SANS, fontSize: 32, color: COLORS.textDim }}>
          ledger-typed · reproducible · falsifiable
        </div>
        <div
          style={{
            fontFamily: MONO,
            fontSize: 34,
            fontWeight: 600,
            backgroundImage: "linear-gradient(135deg,#60a5fa,#a78bfa 55%,#f472b6)",
            WebkitBackgroundClip: "text",
            backgroundClip: "text",
            WebkitTextFillColor: "transparent",
            marginTop: 8,
          }}
        >
          fixpoint-theory.com
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
