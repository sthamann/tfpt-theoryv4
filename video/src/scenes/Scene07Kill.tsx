import React from "react";
import { AbsoluteFill, useCurrentFrame } from "remotion";
import { Bg } from "../components/Bg";
import { Eyebrow } from "../components/ui";
import { StatusChip } from "../components/StatusChip";
import { SANS, SERIF, MONO } from "../fonts";
import { COLORS, StatusGrade } from "../theme";
import { enterUp, fade } from "../components/anim";

const TALLY: { n: string; label: string; color: string }[] = [
  { n: "9", label: "match", color: COLORS.exact },
  { n: "6", label: "near", color: COLORS.conditional },
  { n: "0", label: "miss", color: COLORS.textBright },
  { n: "8", label: "pending", color: COLORS.textDim },
];

const PREDS: { name: string; value: string; grade: StatusGrade }[] = [
  { name: "sin²θ₁₂", value: "≈ 0.3067", grade: "E" },
  { name: "sin²θ₁₃", value: "≈ 0.0231", grade: "E" },
  { name: "tensor r", value: "0.0033 – 0.0048", grade: "C" },
  { name: "neutrinos", value: "normal order · low floor", grade: "C" },
];

const KILLS = [
  { lab: "DESI", sub: "neutrino mass" },
  { lab: "CMB-S4", sub: "tensor r" },
  { lab: "Hyper-K", sub: "proton decay" },
  { lab: "DESI", sub: "dark energy w" },
];

export const Scene07Kill: React.FC = () => {
  const frame = useCurrentFrame();
  const eyebrow = enterUp(frame, 6, 22);

  const phase1 = 1 - fade(frame, 560, 600);
  const phase2 = fade(frame, 575, 615);

  const head = enterUp(frame, 135, 26); // 23 + tally (~208.5s)
  const note = enterUp(frame, 300, 22); // 13 frozen (~214s)
  const finalLine = enterUp(frame, 760, 24); // one miss → wrong (~234.5s)

  return (
    <AbsoluteFill>
      <Bg accent="#fb7185" tint="#f59e0b" />
      <AbsoluteFill style={{ flexDirection: "column", alignItems: "center", paddingTop: 74 }}>
        <div style={eyebrow}>
          <Eyebrow color={COLORS.open}>23 predictions · how to kill it</Eyebrow>
        </div>

        {/* phase 1 — the 23-prediction scorecard */}
        <div
          style={{
            position: "absolute",
            top: 200,
            opacity: phase1,
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            gap: 22,
            width: "100%",
          }}
        >
          <div style={{ ...head, display: "flex", alignItems: "baseline", gap: 22 }}>
            <span
              style={{
                fontFamily: SERIF,
                fontSize: 110,
                fontWeight: 700,
                color: COLORS.textBright,
                lineHeight: 1,
              }}
            >
              23
            </span>
            <span style={{ fontFamily: SANS, fontSize: 36, color: COLORS.text }}>falsifiable predictions</span>
          </div>

          {/* the data-match tally */}
          <div style={{ ...head, display: "flex", gap: 18 }}>
            {TALLY.map((t) => (
              <div
                key={t.label}
                style={{
                  display: "flex",
                  alignItems: "baseline",
                  gap: 10,
                  padding: "12px 26px",
                  borderRadius: 14,
                  background: "rgba(10,16,30,0.6)",
                  border: `1.5px solid ${t.color}55`,
                }}
              >
                <span style={{ fontFamily: MONO, fontSize: 40, fontWeight: 700, color: t.color }}>{t.n}</span>
                <span style={{ fontFamily: SANS, fontSize: 24, color: COLORS.textDim }}>{t.label}</span>
              </div>
            ))}
          </div>

          <div style={{ ...note, fontFamily: SANS, fontSize: 26, color: COLORS.textDim }}>
            13 of them were <b style={{ color: COLORS.text }}>frozen before the data</b> — sealed, blind, pre-registered.
          </div>

          <div style={{ display: "flex", flexDirection: "column", gap: 10, marginTop: 2 }}>
            {PREDS.map((p, i) => {
              const e = enterUp(frame, 420 + i * 18, 20, 16);
              return (
                <div
                  key={p.name}
                  style={{
                    ...e,
                    display: "flex",
                    alignItems: "center",
                    gap: 24,
                    width: 1000,
                    padding: "10px 26px",
                    borderRadius: 13,
                    background: "rgba(10,16,30,0.55)",
                    border: `1px solid ${COLORS.border}`,
                  }}
                >
                  <div style={{ fontFamily: MONO, fontSize: 30, fontWeight: 700, color: COLORS.textBright, width: 200 }}>
                    {p.name}
                  </div>
                  <div style={{ fontFamily: SANS, fontSize: 27, color: COLORS.text, flex: 1 }}>{p.value}</div>
                  <StatusChip grade={p.grade} size={18} />
                </div>
              );
            })}
          </div>
        </div>

        {/* phase 2 — near-term kill tests */}
        <div
          style={{
            position: "absolute",
            top: 300,
            opacity: phase2,
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            gap: 36,
            width: "100%",
          }}
        >
          <div style={{ fontFamily: MONO, fontSize: 28, letterSpacing: 6, color: COLORS.open, textTransform: "uppercase" }}>
            near-term kill tests
          </div>
          <div style={{ display: "flex", gap: 28 }}>
            {KILLS.map((k, i) => {
              const e = enterUp(frame, 600 + i * 22, 24, 26);
              return (
                <div
                  key={k.lab + k.sub}
                  style={{
                    ...e,
                    display: "flex",
                    flexDirection: "column",
                    alignItems: "center",
                    gap: 10,
                    width: 320,
                    padding: "36px 22px",
                    borderRadius: 20,
                    background: COLORS.openBg,
                    border: `1.5px solid ${COLORS.open}66`,
                    boxShadow: `0 0 50px -22px ${COLORS.open}`,
                  }}
                >
                  <div style={{ fontFamily: SANS, fontSize: 46, fontWeight: 700, color: COLORS.textBright }}>{k.lab}</div>
                  <div style={{ fontFamily: SANS, fontSize: 26, color: COLORS.textDim }}>{k.sub}</div>
                </div>
              );
            })}
          </div>
          <div style={{ ...finalLine, fontFamily: SERIF, fontSize: 40, color: COLORS.text }}>
            Each one is a tripwire. <b style={{ color: COLORS.open }}>One clean miss, and it’s wrong.</b>
          </div>
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
