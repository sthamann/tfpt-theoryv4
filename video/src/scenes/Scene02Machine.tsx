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
      gap: 8,
      padding: "20px 30px",
      borderRadius: 18,
      background: `${color}14`,
      border: `1.5px solid ${color}66`,
      boxShadow: `0 0 40px -16px ${color}`,
      ...style,
    }}
  >
    <div style={{ fontFamily: MONO, fontSize: 40, fontWeight: 700, color: COLORS.textBright }}>{symbol}</div>
    <div style={{ fontFamily: SANS, fontSize: 22, fontWeight: 600, color, letterSpacing: 1 }}>{label}</div>
  </div>
);

const BuildChip: React.FC<{ title: string; sub: string; color: string; style?: React.CSSProperties }> = ({
  title,
  sub,
  color,
  style,
}) => (
  <div
    style={{
      display: "flex",
      flexDirection: "column",
      gap: 2,
      padding: "14px 22px",
      borderRadius: 14,
      background: "rgba(10,16,30,0.6)",
      border: `1px solid ${color}55`,
      minWidth: 300,
      ...style,
    }}
  >
    <div style={{ fontFamily: SANS, fontSize: 26, fontWeight: 700, color: COLORS.textBright }}>{title}</div>
    <div style={{ fontFamily: MONO, fontSize: 20, color }}>{sub}</div>
  </div>
);

const Chevron: React.FC<{ on: number; color?: string }> = ({ on, color = COLORS.textDim }) => (
  <div style={{ display: "flex", gap: 5, opacity: on }}>
    {[0, 1, 2].map((i) => (
      <div
        key={i}
        style={{
          width: 18,
          height: 18,
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

  const eyebrow = enterUp(frame, 6, 22);
  const inA = enterUp(frame, 144, 22); // tempo c₃ (~19.8s)
  const inB = enterUp(frame, 300, 22); // width g_car (~25s)
  const arrow1 = fade(frame, 400, 450);
  const b1 = enterUp(frame, 435, 22); // 3 families (~29.5s)
  const b2 = enterUp(frame, 560, 22); // 16-carrier (~34.5s)
  const b3 = enterUp(frame, 640, 22); // hypercharge
  const arrow2 = fade(frame, 700, 750);
  const e8 = enterUp(frame, 735, 24); // E₈ auditor (~39.5s)
  const e8glow = fade(frame, 735, 820, 0.2, 1);
  const formula = enterUp(frame, 800, 24);

  // swapping callouts: "locks one way" then "pins the inputs"
  const calloutA = fadeInOut(frame, 915, 945, 1075, 1095); // ~45.5–51.5s
  const calloutB = fadeInOut(frame, 1098, 1128, 1270, 1288); // ~51.5–58s

  return (
    <AbsoluteFill>
      <Bg accent={COLORS.blue} tint="#7c3aed" />
      <AbsoluteFill style={{ flexDirection: "column", alignItems: "center", paddingTop: 70 }}>
        <div style={eyebrow}>
          <Eyebrow>The machine — two inputs in</Eyebrow>
        </div>

        {/* the compiler pipeline: inputs → pieces → E₈ auditor */}
        <div style={{ marginTop: 48, display: "flex", alignItems: "center", gap: 30 }}>
          <div style={{ display: "flex", flexDirection: "column", gap: 18 }}>
            <div style={inA}>
              <InputChip symbol="c₃ = 1/(8π)" label="tempo" color={COLORS.blueLight} />
            </div>
            <div style={inB}>
              <InputChip symbol="g_car = 5" label="width (3 + 2)" color={COLORS.violet} />
            </div>
          </div>

          <Chevron on={arrow1} />

          <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
            <div style={b1}>
              <BuildChip title="3 families" sub="A₃ · loops around the edge" color={COLORS.blueLight} />
            </div>
            <div style={b2}>
              <BuildChip title="16-part block" sub="D₅ · one full generation" color={COLORS.exact} />
            </div>
            <div style={b3}>
              <BuildChip title="hypercharges" sub="b₁ = 41/10" color={COLORS.violet} />
            </div>
          </div>

          <Chevron on={arrow2} color={COLORS.exact} />

          <div
            style={{
              ...e8,
              width: 230,
              height: 230,
              borderRadius: "50%",
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              justifyContent: "center",
              gap: 4,
              background: `radial-gradient(circle at 50% 40%, ${COLORS.exact}33, rgba(10,16,30,0.7))`,
              border: `2px solid ${COLORS.exact}aa`,
              boxShadow: `0 0 ${40 + e8glow * 70}px -10px ${COLORS.exact}`,
            }}
          >
            <div style={{ fontFamily: MONO, fontSize: 72, fontWeight: 700, color: COLORS.textBright }}>E₈</div>
            <div style={{ fontFamily: SANS, fontSize: 20, color: COLORS.exact, fontWeight: 700, letterSpacing: 2 }}>
              THE AUDITOR
            </div>
            <div style={{ fontFamily: MONO, fontSize: 20, color: COLORS.textDim }}>det = 1 · 248 = 240 + 8</div>
          </div>
        </div>

        <div style={{ marginTop: 36, ...formula }}>
          <Formula size={40}>
            <Tok color={COLORS.violet}>D₅</Tok> ⊕ <Tok color={COLORS.violet}>A₃</Tok> +{" "}
            <Tok color={COLORS.pink}>μ₄</Tok> ⇒ <Tok color={COLORS.exact}>E₈</Tok>
          </Formula>
        </div>

        {/* swapping reframe callouts */}
        <div style={{ position: "relative", marginTop: 30, height: 120, width: 1640 }}>
          <Callout opacity={calloutA} color={COLORS.exact}>
            E₈ isn’t a force — it’s the <b style={{ color: COLORS.exact }}>auditor</b>: the one rulebook where every
            piece locks together <b style={{ color: COLORS.textBright }}>exactly one way</b>, like a perfect crystal.
          </Callout>
          <Callout opacity={calloutB} color={COLORS.blueLight}>
            It closes for <b style={{ color: COLORS.textBright }}>only that one tempo and width</b> — so E₈ doesn’t
            accept the inputs, it <b style={{ color: COLORS.blueLight }}>pins</b> them. The axioms are outputs.
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
  <div style={{ position: "absolute", inset: 0, display: "flex", alignItems: "center", justifyContent: "center", opacity }}>
    <div
      style={{
        fontFamily: SANS,
        fontSize: 33,
        fontWeight: 500,
        color: COLORS.text,
        textAlign: "center",
        maxWidth: 1540,
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
