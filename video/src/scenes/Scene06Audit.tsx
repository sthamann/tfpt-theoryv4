import React from "react";
import { AbsoluteFill, useCurrentFrame } from "remotion";
import { Bg } from "../components/Bg";
import { Eyebrow } from "../components/ui";
import { SANS, MONO, SERIF } from "../fonts";
import { COLORS } from "../theme";
import { enterUp } from "../components/anim";

const MARKERS = [
  { m: "[E]", label: "Exact", color: COLORS.exact, bg: COLORS.exactBg },
  { m: "[C]", label: "Conditional", color: COLORS.conditional, bg: COLORS.conditionalBg },
  { m: "[O]", label: "Open", color: COLORS.open, bg: COLORS.openBg },
  { m: "[X]", label: "Kill test", color: COLORS.blueLight, bg: "rgba(59,130,246,0.12)" },
];

export const Scene06Audit: React.FC = () => {
  const frame = useCurrentFrame();
  const eyebrow = enterUp(frame, 6, 22);
  const ledger = enterUp(frame, 220, 26);
  const red = enterUp(frame, 380, 26);

  return (
    <AbsoluteFill>
      <Bg accent={COLORS.exact} tint="#0ea5e9" />
      <AbsoluteFill style={{ flexDirection: "column", alignItems: "center", justifyContent: "center", paddingBottom: 150, gap: 44 }}>
        <div style={eyebrow}>
          <Eyebrow color={COLORS.exact}>How it stays honest</Eyebrow>
        </div>

        {/* four-class markers */}
        <div style={{ display: "flex", gap: 22 }}>
          {MARKERS.map((mk, i) => {
            const e = enterUp(frame, 70 + i * 22, 22, 22);
            return (
              <div
                key={mk.m}
                style={{
                  ...e,
                  display: "flex",
                  flexDirection: "column",
                  alignItems: "center",
                  gap: 10,
                  padding: "22px 38px",
                  borderRadius: 18,
                  background: mk.bg,
                  border: `1.5px solid ${mk.color}66`,
                }}
              >
                <div style={{ fontFamily: MONO, fontSize: 52, fontWeight: 700, color: mk.color }}>{mk.m}</div>
                <div style={{ fontFamily: SANS, fontSize: 24, fontWeight: 600, color: COLORS.text }}>{mk.label}</div>
              </div>
            );
          })}
        </div>

        <div
          style={{
            ...ledger,
            fontFamily: SERIF,
            fontSize: 44,
            color: COLORS.text,
            textAlign: "center",
            maxWidth: 1300,
          }}
        >
          One <b style={{ color: COLORS.textBright }}>machine-readable ledger</b> — the single source of truth.
          A <b style={{ color: COLORS.textBright }}>no-free-pattern</b> rule on every load-bearing number.
        </div>

        <div
          style={{
            ...red,
            display: "flex",
            alignItems: "center",
            gap: 22,
            padding: "26px 42px",
            borderRadius: 20,
            background: "rgba(2,6,18,0.5)",
            border: `1px solid ${COLORS.open}44`,
            maxWidth: 1300,
          }}
        >
          <span style={{ fontSize: 40 }}>🛠️</span>
          <div style={{ fontFamily: SANS, fontSize: 36, color: COLORS.text }}>
            A <b style={{ color: COLORS.open }}>red team</b> whose job is to <b style={{ color: COLORS.textBright }}>break</b> the theory — not confirm it.
          </div>
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
