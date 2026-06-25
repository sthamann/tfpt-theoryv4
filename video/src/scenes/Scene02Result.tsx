import React from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig, interpolate } from "remotion";
import { Bg } from "../components/Bg";
import { Eyebrow } from "../components/ui";
import { SANS, SERIF, MONO } from "../fonts";
import { COLORS } from "../theme";
import { pop, CountUp } from "../components/fx";

type Item = { label: string; sub: string; at: number; color: string };

// the cascade of outputs, scheduled to the voice-over waves (scene starts 20s)
const ITEMS: Item[] = [
  { label: "3 forces", sub: "SU(3)×SU(2)×U(1)", at: 170, color: COLORS.blueLight },
  { label: "3 generations", sub: "of matter", at: 208, color: COLORS.blueLight },
  { label: "1 Higgs", sub: "exactly one", at: 246, color: COLORS.blueLight },
  { label: "9 masses", sub: "one ladder", at: 284, color: COLORS.violet },
  { label: "CKM + PMNS", sub: "the mixings", at: 322, color: COLORS.violet },
  { label: "2 CP phases", sub: "locked", at: 360, color: COLORS.violet },
  { label: "strong-CP = 0", sub: "no neutron dipole", at: 398, color: COLORS.violet },
  { label: "Gravity", sub: "Gᵤᵥ = 8π Tᵤᵥ", at: 520, color: COLORS.exact },
  { label: "inflation", sub: "nₛ , r", at: 700, color: COLORS.pink },
  { label: "ordinary matter", sub: "Ω_b", at: 738, color: COLORS.pink },
  { label: "dark energy", sub: "Λ from α", at: 776, color: COLORS.pink },
  { label: "baryon asymmetry", sub: "η_B", at: 814, color: COLORS.pink },
  { label: "α⁻¹ = 137.0359992", sub: "the strength of light", at: 890, color: "#22d3ee" },
  { label: "cosmic birefringence", sub: "β = 0.24°", at: 928, color: "#22d3ee" },
  { label: "Cabibbo angle", sub: "λ_C", at: 962, color: "#22d3ee" },
];

const Chip: React.FC<{ it: Item; frame: number; fps: number }> = ({ it, frame, fps }) => (
  <div
    style={{
      ...pop(frame, fps, it.at, { y: -48, from: 0.8, config: { damping: 13, mass: 0.8, stiffness: 120 } }),
      display: "flex",
      flexDirection: "column",
      gap: 2,
      padding: "14px 22px",
      borderRadius: 14,
      background: "rgba(10,16,30,0.66)",
      border: `1.5px solid ${it.color}66`,
      boxShadow: `0 0 34px -18px ${it.color}`,
    }}
  >
    <div style={{ fontFamily: SANS, fontSize: 27, fontWeight: 700, color: COLORS.textBright, whiteSpace: "nowrap" }}>
      {it.label}
    </div>
    <div style={{ fontFamily: MONO, fontSize: 18, color: it.color }}>{it.sub}</div>
  </div>
);

export const Scene02Result: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const landed = ITEMS.filter((it) => frame >= it.at + 4).length;
  const boardDim = interpolate(frame, [1040, 1090], [1, 0.45], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const band = pop(frame, fps, 1070, { y: 28, from: 0.9 });

  return (
    <AbsoluteFill>
      <Bg accent={COLORS.blue} tint="#0ea5e9" />
      <AbsoluteFill style={{ flexDirection: "column", alignItems: "center", paddingTop: 64 }}>
        <div style={pop(frame, fps, 8)}>
          <Eyebrow>Start at the end — what comes out</Eyebrow>
        </div>

        {/* live tally */}
        <div style={{ ...pop(frame, fps, 140), marginTop: 18, fontFamily: MONO, fontSize: 24, color: COLORS.textDim, letterSpacing: 2 }}>
          outputs locked: <span style={{ color: COLORS.exact, fontWeight: 700 }}>{landed}</span>
        </div>

        {/* the cascade board */}
        <div
          style={{
            marginTop: 26,
            opacity: boardDim,
            display: "flex",
            flexWrap: "wrap",
            justifyContent: "center",
            alignContent: "flex-start",
            gap: 16,
            maxWidth: 1500,
          }}
        >
          {ITEMS.map((it) => (
            <Chip key={it.label} it={it} frame={frame} fps={fps} />
          ))}
        </div>

        {/* the 23-prediction band + the cliffhanger */}
        <div
          style={{
            ...band,
            position: "absolute",
            bottom: 188,
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            gap: 14,
          }}
        >
          <div style={{ display: "flex", alignItems: "baseline", gap: 18 }}>
            <CountUp
              to={23}
              start={1075}
              end={1175}
              style={{ fontFamily: SERIF, fontSize: 86, fontWeight: 700, color: COLORS.textBright }}
            />
            <span style={{ fontFamily: SANS, fontSize: 34, color: COLORS.text }}>concrete, testable predictions</span>
          </div>
          <div style={{ fontFamily: SERIF, fontSize: 38, color: COLORS.textDim }}>
            That's the output. Now — <b style={{ color: COLORS.textBright }}>from how much input?</b>
          </div>
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
