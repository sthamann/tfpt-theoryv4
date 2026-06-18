import React from "react";
import { AbsoluteFill, useCurrentFrame } from "remotion";
import { Bg } from "../components/Bg";
import { Eyebrow } from "../components/ui";
import { Formula, Tok } from "../components/Formula";
import { SANS, MONO } from "../fonts";
import { COLORS } from "../theme";
import { enterUp, fade, fadeInOut } from "../components/anim";

const InputChip: React.FC<{
  symbol: React.ReactNode;
  label: string;
  color: string;
  style?: React.CSSProperties;
}> = ({ symbol, label, color, style }) => (
  <div
    style={{
      display: "flex",
      flexDirection: "column",
      alignItems: "center",
      gap: 12,
      padding: "26px 38px",
      borderRadius: 20,
      background: `${color}14`,
      border: `1.5px solid ${color}66`,
      boxShadow: `0 0 40px -16px ${color}`,
      ...style,
    }}
  >
    <div style={{ fontFamily: MONO, fontSize: 50, fontWeight: 700, color: COLORS.textBright }}>
      {symbol}
    </div>
    <div style={{ fontFamily: SANS, fontSize: 24, fontWeight: 600, color, letterSpacing: 1 }}>
      {label}
    </div>
  </div>
);

const Chevron: React.FC<{ on: number; color?: string }> = ({ on, color = COLORS.textDim }) => (
  <div style={{ display: "flex", gap: 6, opacity: on }}>
    {[0, 1, 2].map((i) => (
      <div
        key={i}
        style={{
          width: 22,
          height: 22,
          borderTop: `5px solid ${color}`,
          borderRight: `5px solid ${color}`,
          transform: "rotate(45deg)",
          opacity: 0.4 + i * 0.3,
        }}
      />
    ))}
  </div>
);

export const Scene02Machine: React.FC = () => {
  const frame = useCurrentFrame();

  // Internal beats are aligned to the caption timeline (scene starts at 15s).
  const eyebrow = enterUp(frame, 6, 22);
  const inA = enterUp(frame, 110, 22);
  const inB = enterUp(frame, 250, 22);
  const arrow1 = fade(frame, 330, 380);
  const mid = enterUp(frame, 360, 24);
  const arrow2 = fade(frame, 600, 650);
  const e8 = enterUp(frame, 630, 26);
  const formula = enterUp(frame, 670, 26);

  // E8 glow ramps when the glue closes it into E8
  const e8glow = fade(frame, 620, 700, 0.2, 1);

  // lower callouts swap — "audit hull" then "readout after projection"
  const calloutA = fadeInOut(frame, 800, 832, 1040, 1070);
  const calloutB = fadeInOut(frame, 1080, 1112, 1200, 1225);

  return (
    <AbsoluteFill>
      <Bg accent={COLORS.blue} tint="#7c3aed" />
      <AbsoluteFill style={{ flexDirection: "column", alignItems: "center", paddingTop: 76 }}>
        <div style={eyebrow}>
          <Eyebrow>The machine</Eyebrow>
        </div>

        {/* the compiler row */}
        <div
          style={{
            marginTop: 52,
            display: "flex",
            alignItems: "center",
            gap: 42,
          }}
        >
          <div style={{ display: "flex", flexDirection: "column", gap: 22, ...inA }}>
            <div style={inB}>
              <InputChip symbol="c₃ = 1/(8π)" label="seam constant" color={COLORS.blueLight} />
            </div>
            <InputChip symbol="g_car = 5" label="carrier rank" color={COLORS.violet} />
          </div>

          <Chevron on={arrow1} />

          <div
            style={{
              ...mid,
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              gap: 14,
              padding: "30px 46px",
              borderRadius: 22,
              background: "rgba(10,16,30,0.6)",
              border: `1px solid ${COLORS.border}`,
            }}
          >
            <div style={{ fontFamily: MONO, fontSize: 56, fontWeight: 700, color: COLORS.textBright }}>
              D₅ ⊕ A₃
            </div>
            <div style={{ fontFamily: MONO, fontSize: 30, color: COLORS.pink, fontWeight: 600 }}>
              ⋊ μ₄ glue
            </div>
            <div style={{ fontFamily: SANS, fontSize: 22, color: COLORS.textDim }}>
              SO(10) half-spinor · family geometry
            </div>
          </div>

          <Chevron on={arrow2} color={COLORS.exact} />

          <div
            style={{
              ...e8,
              width: 200,
              height: 200,
              borderRadius: "50%",
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              justifyContent: "center",
              gap: 6,
              background: `radial-gradient(circle at 50% 40%, ${COLORS.exact}33, rgba(10,16,30,0.7))`,
              border: `2px solid ${COLORS.exact}aa`,
              boxShadow: `0 0 ${40 + e8glow * 60}px -10px ${COLORS.exact}`,
            }}
          >
            <div style={{ fontFamily: MONO, fontSize: 76, fontWeight: 700, color: COLORS.textBright }}>
              E₈
            </div>
            <div style={{ fontFamily: SANS, fontSize: 22, color: COLORS.exact, fontWeight: 600 }}>
              240 roots
            </div>
          </div>
        </div>

        <div style={{ marginTop: 40, ...formula }}>
          <Formula size={44}>
            <Tok color={COLORS.violet}>D₅</Tok> ⊕ <Tok color={COLORS.violet}>A₃</Tok> +{" "}
            <Tok color={COLORS.pink}>μ₄</Tok> ⇒ <Tok color={COLORS.exact}>E₈</Tok>
          </Formula>
        </div>

        {/* swapping reframe callouts */}
        <div style={{ position: "relative", marginTop: 34, height: 120, width: 1620 }}>
          <Callout opacity={calloutA} color={COLORS.open}>
            E₈ is <b style={{ color: COLORS.textBright }}>not</b> a gauge group of nature — it is the{" "}
            <b style={{ color: COLORS.open }}>audit hull</b>, the consistency container.
          </Callout>
          <Callout opacity={calloutB} color={COLORS.exact}>
            The Standard Model is a <b style={{ color: COLORS.textBright }}>readout after projection</b> —
            not “everything is E₈”.
          </Callout>
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

const Callout: React.FC<{
  children: React.ReactNode;
  opacity: number;
  color: string;
}> = ({ children, opacity, color }) => (
  <div
    style={{
      position: "absolute",
      inset: 0,
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      opacity,
    }}
  >
    <div
      style={{
        fontFamily: SANS,
        fontSize: 34,
        fontWeight: 500,
        color: COLORS.text,
        textAlign: "center",
        maxWidth: 1520,
        padding: "16px 30px",
        borderRadius: 16,
        background: "rgba(2,6,18,0.5)",
        border: `1px solid ${color}44`,
      }}
    >
      {children}
    </div>
  </div>
);
