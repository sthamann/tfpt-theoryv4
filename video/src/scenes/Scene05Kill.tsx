import React from "react";
import { AbsoluteFill, useCurrentFrame, interpolate, Easing } from "remotion";
import { Bg } from "../components/Bg";
import { Eyebrow } from "../components/ui";
import { StatusChip } from "../components/StatusChip";
import { SANS, MONO } from "../fonts";
import { COLORS, StatusGrade } from "../theme";
import { enterUp } from "../components/anim";

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
  const sealScale = interpolate(frame, [50, 96], [0.6, 1], {
    easing: Easing.bezier(0.34, 1.56, 0.64, 1),
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const seal = enterUp(frame, 50, 26);
  const note = enterUp(frame, 440, 24);
  const killHead = enterUp(frame, 590, 22);

  return (
    <AbsoluteFill>
      <Bg accent="#fb7185" tint="#f59e0b" />
      <AbsoluteFill style={{ flexDirection: "column", alignItems: "center", paddingTop: 84, gap: 26 }}>
        <div style={eyebrow}>
          <Eyebrow color={COLORS.open}>How to kill it</Eyebrow>
        </div>

        {/* frozen seal */}
        <div style={{ ...seal, transform: `${seal.transform} scale(${sealScale})` }}>
          <div
            style={{
              display: "inline-flex",
              alignItems: "center",
              gap: 16,
              padding: "16px 32px",
              borderRadius: 999,
              background: "rgba(2,6,18,0.6)",
              border: `2px solid ${COLORS.open}88`,
              fontFamily: MONO,
              fontSize: 30,
              fontWeight: 700,
              letterSpacing: 3,
              color: COLORS.textBright,
            }}
          >
            <span style={{ fontSize: 26 }}>🔒</span> FROZEN · BLIND REGISTRY · PRE-DATA
          </div>
        </div>

        {/* prediction list */}
        <div style={{ display: "flex", flexDirection: "column", gap: 16, marginTop: 8 }}>
          {PREDS.map((p, i) => {
            const e = enterUp(frame, 150 + i * 24, 20, 18);
            return (
              <div
                key={p.name}
                style={{
                  ...e,
                  display: "flex",
                  alignItems: "center",
                  gap: 24,
                  width: 1120,
                  padding: "16px 30px",
                  borderRadius: 16,
                  background: "rgba(10,16,30,0.6)",
                  border: `1px solid ${COLORS.border}`,
                }}
              >
                <div style={{ fontFamily: MONO, fontSize: 38, fontWeight: 700, color: COLORS.textBright, width: 240 }}>
                  {p.name}
                </div>
                <div style={{ fontFamily: SANS, fontSize: 34, color: COLORS.text, flex: 1 }}>
                  {p.value}
                </div>
                <StatusChip grade={p.grade} size={22} />
              </div>
            );
          })}
        </div>

        <div style={{ ...note, fontFamily: SANS, fontSize: 30, color: COLORS.textDim, marginTop: 4 }}>
          Closed core predictions sit within <b style={{ color: COLORS.text }}>~1σ</b> today — every tension tracked in the open.
        </div>

        {/* near-term kill tests */}
        <div style={{ ...killHead, display: "flex", alignItems: "center", gap: 20, marginTop: 10 }}>
          <div style={{ fontFamily: MONO, fontSize: 24, letterSpacing: 4, color: COLORS.open, textTransform: "uppercase" }}>
            near-term kill tests
          </div>
          {KILLS.map((k, i) => {
            const e = enterUp(frame, 640 + i * 20, 20, 18);
            return (
              <div
                key={k.lab}
                style={{
                  ...e,
                  display: "flex",
                  flexDirection: "column",
                  alignItems: "center",
                  gap: 4,
                  padding: "14px 26px",
                  borderRadius: 14,
                  background: COLORS.openBg,
                  border: `1px solid ${COLORS.open}55`,
                }}
              >
                <div style={{ fontFamily: SANS, fontSize: 30, fontWeight: 700, color: COLORS.textBright }}>{k.lab}</div>
                <div style={{ fontFamily: SANS, fontSize: 20, color: COLORS.textDim }}>{k.sub}</div>
              </div>
            );
          })}
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
