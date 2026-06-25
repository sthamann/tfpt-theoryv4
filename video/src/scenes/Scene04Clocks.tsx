import React from "react";
import { AbsoluteFill, useCurrentFrame } from "remotion";
import { Bg } from "../components/Bg";
import { Eyebrow } from "../components/ui";
import { SANS, SERIF, MONO } from "../fonts";
import { COLORS } from "../theme";
import { enterUp } from "../components/anim";

/** A meshing "gear/clock": a rotating dashed ring with a number in the centre. */
const Gear: React.FC<{ n: number; label: string; size: number; color: string; speed: number }> = ({
  n,
  label,
  size,
  color,
  speed,
}) => {
  const frame = useCurrentFrame();
  const rot = frame * speed;
  return (
    <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 10 }}>
      <div style={{ position: "relative", width: size, height: size }}>
        <div
          style={{
            position: "absolute",
            inset: 0,
            borderRadius: "50%",
            border: `9px dashed ${color}`,
            transform: `rotate(${rot}deg)`,
            boxShadow: `0 0 40px -14px ${color}`,
          }}
        />
        <div
          style={{
            position: "absolute",
            inset: 0,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            fontFamily: MONO,
            fontSize: size * 0.42,
            fontWeight: 700,
            color: COLORS.textBright,
          }}
        >
          {n}
        </div>
      </div>
      <div style={{ fontFamily: SANS, fontSize: 22, fontWeight: 600, color }}>{label}</div>
    </div>
  );
};

export const Scene04Clocks: React.FC = () => {
  const frame = useCurrentFrame();

  const eyebrow = enterUp(frame, 6, 22);
  const question = enterUp(frame, 20, 24);
  const gears = enterUp(frame, 135, 24); // two gears (~106.5s)
  const ring = enterUp(frame, 240, 22); // order-30 (~112s)
  const spectrum = enterUp(frame, 360, 24); // gap (~117.5s)
  const attractor = enterUp(frame, 560, 24); // unique attractor (~123s)
  const bridge = enterUp(frame, 760, 24); // discrete→dynamic (~129s)

  return (
    <AbsoluteFill>
      <Bg accent="#22d3ee" tint="#a78bfa" />
      <AbsoluteFill style={{ flexDirection: "column", alignItems: "center", paddingTop: 70, gap: 20 }}>
        <div style={eyebrow}>
          <Eyebrow color="#22d3ee">The clocks — discrete → dynamic</Eyebrow>
        </div>

        <div style={{ ...question, fontFamily: SERIF, fontSize: 38, color: COLORS.text, textAlign: "center" }}>
          A list of numbers isn’t physics yet — what makes it <b style={{ color: COLORS.textBright }}>move</b>?
        </div>

        {/* two meshing gears → an order-30 clock */}
        <div style={{ ...gears, display: "flex", alignItems: "center", gap: 16, marginTop: 6 }}>
          <Gear n={5} label="carrier" size={150} color={COLORS.violet} speed={1.6} />
          <div style={{ fontFamily: MONO, fontSize: 40, color: COLORS.textDim }}>×</div>
          <Gear n={6} label="families (2·3)" size={130} color={COLORS.blueLight} speed={-2.0} />
          <div style={{ fontFamily: MONO, fontSize: 40, color: COLORS.textDim }}>=</div>
          <div style={{ ...ring, display: "flex", flexDirection: "column", alignItems: "center", gap: 4 }}>
            <div style={{ fontFamily: MONO, fontSize: 72, fontWeight: 700, color: "#22d3ee" }}>30</div>
            <div style={{ fontFamily: SANS, fontSize: 22, color: COLORS.textDim }}>order-30 clock · 2 · 3 · 5</div>
          </div>
        </div>

        {/* the gapped spectrum */}
        <div
          style={{
            ...spectrum,
            display: "flex",
            alignItems: "center",
            gap: 18,
            padding: "16px 30px",
            borderRadius: 16,
            background: "rgba(2,6,18,0.5)",
            border: `1px solid ${COLORS.border}`,
          }}
        >
          <span style={{ fontFamily: MONO, fontSize: 30, color: COLORS.text }}>
            spectrum {"{"} 1, (2/3)⁶, (1/3)⁶ {"}"}
          </span>
          <span style={{ fontFamily: SANS, fontSize: 26, color: "#22d3ee", fontWeight: 600 }}>
            gap Δ = 6 ln(3/2) &gt; 0
          </span>
        </div>

        {/* unique attractor */}
        <div style={{ ...attractor, display: "flex", alignItems: "center", gap: 22, marginTop: 2 }}>
          <div style={{ display: "flex", alignItems: "center", gap: 6 }}>
            {[0.25, 0.4, 0.6].map((o, i) => (
              <div key={i} style={{ width: 12, height: 12, borderRadius: "50%", background: COLORS.textDim, opacity: o }} />
            ))}
            <div style={{ fontFamily: MONO, fontSize: 34, color: COLORS.textDim, margin: "0 8px" }}>→</div>
            <div
              style={{
                width: 26,
                height: 26,
                borderRadius: "50%",
                background: COLORS.exact,
                boxShadow: `0 0 26px -4px ${COLORS.exact}`,
              }}
            />
          </div>
          <div style={{ fontFamily: SANS, fontSize: 30, color: COLORS.text }}>
            one <b style={{ color: COLORS.exact }}>unique attractor</b> (Perron–Frobenius) — the constants are{" "}
            <b style={{ color: COLORS.textBright }}>selected, not tuned</b>.
          </div>
        </div>

        <div
          style={{
            ...bridge,
            fontFamily: SERIF,
            fontSize: 34,
            color: COLORS.textDim,
            textAlign: "center",
            marginTop: 4,
          }}
        >
          the bridge: <b style={{ color: COLORS.textBright }}>frozen arithmetic → living dynamics</b>.
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
