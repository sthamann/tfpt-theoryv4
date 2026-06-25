import React from "react";
import { AbsoluteFill, useCurrentFrame, interpolate, Easing } from "remotion";
import { Bg } from "../components/Bg";
import { Eyebrow } from "../components/ui";
import { StatusChip } from "../components/StatusChip";
import { SANS, SERIF, MONO } from "../fonts";
import { COLORS } from "../theme";
import { enterUp, fade, fadeInOut } from "../components/anim";

const SM_ITEMS: { title: string; sub: string }[] = [
  { title: "3 forces", sub: "SU(3)×SU(2)×U(1)" },
  { title: "3 generations", sub: "no 4th family" },
  { title: "exactly 1 Higgs", sub: "N_Φ = g_car − |μ₄|" },
  { title: "9 fermion masses", sub: "one φ₀-ladder" },
  { title: "CKM + PMNS", sub: "quark & neutrino mixing" },
  { title: "2 CP phases", sub: "locked together" },
  { title: "strong-CP = 0", sub: "no neutron dipole" },
  { title: "all charges", sub: "hypercharge 41/10" },
];

export const Scene03Readout: React.FC = () => {
  const frame = useCurrentFrame();

  const eyebrow = enterUp(frame, 6, 22);
  const heading = enterUp(frame, 135, 24); // "almost the entire SM" (~62.5s)
  const grid = fadeInOut(frame, 280, 320, 740, 790);
  const gridShift = interpolate(frame, [740, 800], [0, -30], {
    easing: Easing.in(Easing.cubic),
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  const alphaIn = fade(frame, 770, 820);
  const num = enterUp(frame, 790, 28); // α⁻¹ lands (~84s)
  const verdict = enterUp(frame, 960, 24); // forced / <2σ (~90s)
  const footer = enterUp(frame, 1110, 26); // + cosmos + gravity (~95s)

  return (
    <AbsoluteFill>
      <Bg accent={COLORS.blue} tint="#0ea5e9" />
      <AbsoluteFill style={{ flexDirection: "column", alignItems: "center", paddingTop: 84 }}>
        <div style={eyebrow}>
          <Eyebrow>The readout — what comes out</Eyebrow>
        </div>

        <div
          style={{
            ...heading,
            marginTop: 22,
            display: "flex",
            alignItems: "center",
            gap: 18,
          }}
        >
          <div style={{ fontFamily: SERIF, fontSize: 44, fontWeight: 600, color: COLORS.textBright }}>
            Almost the entire Standard Model
          </div>
          <StatusChip grade="E" size={22} />
        </div>

        {/* the SM scope grid (fades out as α reveals) */}
        <div
          style={{
            position: "absolute",
            top: 300,
            opacity: grid,
            transform: `translateY(${gridShift}px)`,
            display: "flex",
            flexWrap: "wrap",
            justifyContent: "center",
            gap: 20,
            width: 1640,
          }}
        >
          {SM_ITEMS.map((it, i) => {
            const e = enterUp(frame, 300 + i * 26, 22, 18);
            return (
              <div
                key={it.title}
                style={{
                  ...e,
                  width: 386,
                  display: "flex",
                  alignItems: "center",
                  gap: 14,
                  padding: "18px 24px",
                  borderRadius: 16,
                  background: "rgba(10,16,30,0.62)",
                  border: `1px solid ${COLORS.exact}40`,
                }}
              >
                <div style={{ color: COLORS.exact, fontSize: 26, fontWeight: 700 }}>✓</div>
                <div style={{ display: "flex", flexDirection: "column" }}>
                  <div style={{ fontFamily: SANS, fontSize: 28, fontWeight: 700, color: COLORS.textBright }}>
                    {it.title}
                  </div>
                  <div style={{ fontFamily: MONO, fontSize: 19, color: COLORS.textDim }}>{it.sub}</div>
                </div>
              </div>
            );
          })}
        </div>

        {/* the α headline */}
        <div
          style={{
            position: "absolute",
            top: 320,
            opacity: alphaIn,
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            gap: 20,
            width: 1600,
          }}
        >
          <div style={{ fontFamily: SANS, fontSize: 30, color: COLORS.textDim, ...enterUp(frame, 790, 24) }}>
            the fine-structure constant — the single positive root of one equation
          </div>
          <div
            style={{
              fontFamily: MONO,
              fontWeight: 700,
              fontSize: 116,
              whiteSpace: "nowrap",
              color: COLORS.textBright,
              textShadow: "0 0 70px rgba(96,165,250,0.4)",
              ...num,
            }}
          >
            α⁻¹ = 137.0359992
          </div>
          <div style={{ ...verdict, fontFamily: SERIF, fontWeight: 600, fontSize: 50 }}>
            <span style={{ color: COLORS.textDim }}>Not chosen. </span>
            <span style={{ color: COLORS.textBright }}>Forced.</span>
            <span style={{ color: COLORS.exact }}> &lt; 2σ from experiment.</span>
          </div>
        </div>

        {/* + cosmos + gravity */}
        <div
          style={{
            position: "absolute",
            bottom: 188,
            ...footer,
            display: "flex",
            gap: 16,
          }}
        >
          {["the cosmos", "gravity"].map((t) => (
            <div
              key={t}
              style={{
                fontFamily: SANS,
                fontSize: 28,
                fontWeight: 600,
                color: COLORS.violet,
                padding: "10px 24px",
                borderRadius: 999,
                background: "rgba(167,139,250,0.12)",
                border: `1px solid ${COLORS.violet}55`,
              }}
            >
              + {t}
            </div>
          ))}
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
