import React from "react";
import { AbsoluteFill, useCurrentFrame, interpolate, Easing } from "remotion";
import { Bg } from "../components/Bg";
import { Eyebrow } from "../components/ui";
import { StatusChip } from "../components/StatusChip";
import { SANS, MONO } from "../fonts";
import { COLORS, StatusGrade } from "../theme";
import { enterUp, fade } from "../components/anim";

const PREDS: { name: string; value: string; grade: StatusGrade }[] = [
  { name: "sin²θ₁₂", value: "≈ 0.3067", grade: "E" },
  { name: "sin²θ₁₃", value: "≈ 0.0231", grade: "E" },
  { name: "α⁻¹", value: "fixed point", grade: "E" },
  { name: "tensor r", value: "0.0033 – 0.0048", grade: "C" },
  { name: "neutrinos", value: "normal order · low floor", grade: "C" },
];

const KILLS = [
  { lab: "DESI", sub: "neutrino mass" },
  { lab: "CMB-S4", sub: "tensor r" },
  { lab: "Hyper-K", sub: "proton decay" },
];

export const Scene05Kill: React.FC = () => {
  const frame = useCurrentFrame();
  const eyebrow = enterUp(frame, 6, 22);

  // phase 1: frozen registry + predictions; phase 2: near-term kill tests
  const phase1 = 1 - fade(frame, 700, 760);
  const phase2 = fade(frame, 745, 805);

  const sealScale = interpolate(frame, [50, 96], [0.6, 1], {
    easing: Easing.bezier(0.34, 1.56, 0.64, 1),
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const seal = enterUp(frame, 50, 26);
  const note = enterUp(frame, 560, 24);

  return (
    <AbsoluteFill>
      <Bg accent="#fb7185" tint="#f59e0b" />
      <AbsoluteFill style={{ flexDirection: "column", alignItems: "center", paddingTop: 76 }}>
        <div style={eyebrow}>
          <Eyebrow color={COLORS.open}>How to kill it</Eyebrow>
        </div>

        {/* phase 1 — frozen registry + predictions */}
        <div
          style={{
            position: "absolute",
            top: 220,
            opacity: phase1,
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            gap: 22,
            width: "100%",
          }}
        >
          <div style={{ ...seal, transform: `${seal.transform} scale(${sealScale})` }}>
            <div
              style={{
                display: "inline-flex",
                alignItems: "center",
                gap: 16,
                padding: "14px 30px",
                borderRadius: 999,
                background: "rgba(2,6,18,0.6)",
                border: `2px solid ${COLORS.open}88`,
                fontFamily: MONO,
                fontSize: 28,
                fontWeight: 700,
                letterSpacing: 3,
                color: COLORS.textBright,
              }}
            >
              <span style={{ fontSize: 24 }}>🔒</span> FROZEN · BLIND REGISTRY · PRE-DATA
            </div>
          </div>

          <div style={{ display: "flex", flexDirection: "column", gap: 12, marginTop: 4 }}>
            {PREDS.map((p, i) => {
              const e = enterUp(frame, 130 + i * 22, 20, 16);
              return (
                <div
                  key={p.name}
                  style={{
                    ...e,
                    display: "flex",
                    alignItems: "center",
                    gap: 24,
                    width: 1060,
                    padding: "12px 28px",
                    borderRadius: 14,
                    background: "rgba(10,16,30,0.6)",
                    border: `1px solid ${COLORS.border}`,
                  }}
                >
                  <div style={{ fontFamily: MONO, fontSize: 34, fontWeight: 700, color: COLORS.textBright, width: 220 }}>
                    {p.name}
                  </div>
                  <div style={{ fontFamily: SANS, fontSize: 30, color: COLORS.text, flex: 1 }}>{p.value}</div>
                  <StatusChip grade={p.grade} size={20} />
                </div>
              );
            })}
          </div>

          <div style={{ ...note, fontFamily: SANS, fontSize: 28, color: COLORS.textDim }}>
            Closed core predictions sit within <b style={{ color: COLORS.text }}>~1σ</b> today — every tension tracked in the open.
          </div>
        </div>

        {/* phase 2 — near-term kill tests */}
        <div
          style={{
            position: "absolute",
            top: 320,
            opacity: phase2,
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            gap: 44,
            width: "100%",
          }}
        >
          <div
            style={{
              fontFamily: MONO,
              fontSize: 30,
              letterSpacing: 6,
              color: COLORS.open,
              textTransform: "uppercase",
            }}
          >
            near-term kill tests
          </div>
          <div style={{ display: "flex", gap: 40 }}>
            {KILLS.map((k, i) => {
              const e = enterUp(frame, 790 + i * 24, 24, 26);
              return (
                <div
                  key={k.lab}
                  style={{
                    ...e,
                    display: "flex",
                    flexDirection: "column",
                    alignItems: "center",
                    gap: 12,
                    width: 360,
                    padding: "40px 26px",
                    borderRadius: 22,
                    background: COLORS.openBg,
                    border: `1.5px solid ${COLORS.open}66`,
                    boxShadow: `0 0 50px -20px ${COLORS.open}`,
                  }}
                >
                  <div style={{ fontFamily: SANS, fontSize: 52, fontWeight: 700, color: COLORS.textBright }}>{k.lab}</div>
                  <div style={{ fontFamily: SANS, fontSize: 28, color: COLORS.textDim }}>{k.sub}</div>
                </div>
              );
            })}
          </div>
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
