import React from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig, interpolate } from "remotion";
import { Bg } from "../components/Bg";
import { Eyebrow } from "../components/ui";
import { SANS, SERIF, MONO } from "../fonts";
import { COLORS } from "../theme";
import { pop, popScale } from "../components/fx";
import { fade } from "../components/anim";

/** Dots streaming inward into the two input chips. */
const Converge: React.FC<{ from: number; to: number }> = ({ from, to }) => {
  const frame = useCurrentFrame();
  const p = interpolate(frame, [from, to], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const golden = 2.399963;
  return (
    <>
      {Array.from({ length: 46 }).map((_, i) => {
        const a = i * golden;
        const startR = 560 + (i % 6) * 30;
        const r = startR * (1 - p);
        const x = Math.cos(a) * r;
        const y = Math.sin(a) * r * 0.6;
        const op = interpolate(p, [0, 0.15, 0.8, 1], [0, 0.8, 0.7, 0]);
        const col = [COLORS.blueLight, COLORS.violet, COLORS.pink][i % 3];
        return (
          <div
            key={i}
            style={{
              position: "absolute",
              left: `calc(50% + ${x}px)`,
              top: `calc(50% + ${y}px)`,
              width: 5,
              height: 5,
              borderRadius: "50%",
              background: col,
              opacity: op,
              boxShadow: `0 0 7px ${col}`,
            }}
          />
        );
      })}
    </>
  );
};

const InputChip: React.FC<{ sym: string; label: string; color: string; style?: React.CSSProperties }> = ({
  sym,
  label,
  color,
  style,
}) => (
  <div
    style={{
      display: "flex",
      flexDirection: "column",
      alignItems: "center",
      gap: 8,
      padding: "22px 34px",
      borderRadius: 18,
      background: `${color}14`,
      border: `1.5px solid ${color}88`,
      boxShadow: `0 0 50px -18px ${color}`,
      ...style,
    }}
  >
    <div style={{ fontFamily: MONO, fontSize: 44, fontWeight: 700, color: COLORS.textBright }}>{sym}</div>
    <div style={{ fontFamily: SANS, fontSize: 22, fontWeight: 600, color }}>{label}</div>
  </div>
);

export const Scene03Input: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const chipsOut = fade(frame, 320, 380, 1, 0); // chips compress away
  const chips = { opacity: chipsOut };
  const contrast = pop(frame, fps, 500, { y: 26 });

  return (
    <AbsoluteFill>
      <Bg accent={COLORS.violet} tint="#0ea5e9" />
      <AbsoluteFill style={{ flexDirection: "column", alignItems: "center", paddingTop: 70 }}>
        <div style={pop(frame, fps, 8)}>
          <Eyebrow color={COLORS.violet}>Almost nothing goes in</Eyebrow>
        </div>
      </AbsoluteFill>

      {/* converging dots */}
      <AbsoluteFill style={{ alignItems: "center", justifyContent: "center", marginTop: 30 }}>
        <Converge from={30} to={250} />
      </AbsoluteFill>

      {/* the two inputs, then their reduction to π */}
      <AbsoluteFill style={{ alignItems: "center", justifyContent: "center", marginTop: 30 }}>
        <div style={{ ...chips, display: "flex", gap: 40 }}>
          <div style={pop(frame, fps, 120)}>
            <InputChip sym="c₃ = 1/(8π)" label="a tempo · edge of space" color={COLORS.blueLight} />
          </div>
          <div style={pop(frame, fps, 150)}>
            <InputChip sym="g_car = 5" label="a width · 5 slots" color={COLORS.violet} />
          </div>
        </div>

        {/* reduce → π */}
        <div style={{ position: "absolute", display: "flex", flexDirection: "column", alignItems: "center", gap: 14, opacity: fade(frame, 360, 420) }}>
          <div style={{ fontFamily: SANS, fontSize: 26, color: COLORS.textDim }}>strip it down — and they aren't even free:</div>
          <div style={{ display: "flex", alignItems: "center", gap: 22 }}>
            <div style={{ ...popScale(frame, fps, 380), fontFamily: SERIF, fontSize: 130, fontWeight: 700, color: COLORS.textBright, textShadow: `0 0 60px ${COLORS.blueLight}66` }}>
              π
            </div>
            <div style={{ ...pop(frame, fps, 430), display: "flex", flexDirection: "column", gap: 4 }}>
              <div style={{ fontFamily: MONO, fontSize: 30, color: COLORS.violet }}>+ one pattern</div>
              <div style={{ fontFamily: MONO, fontSize: 30, color: COLORS.textDim }}>a = (1, 1, 2)</div>
            </div>
          </div>
          <div style={{ fontFamily: SANS, fontSize: 24, color: COLORS.textFaint }}>only π has no cheaper origin</div>
        </div>
      </AbsoluteFill>

      {/* the contrast — tiny source vs. everything */}
      <AbsoluteFill style={{ alignItems: "center", justifyContent: "flex-end", paddingBottom: 230 }}>
        <div style={{ ...contrast, display: "flex", alignItems: "center", gap: 30 }}>
          <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 6 }}>
            <div style={{ width: 18, height: 18, borderRadius: "50%", background: COLORS.blueLight, boxShadow: `0 0 18px ${COLORS.blueLight}` }} />
            <div style={{ fontFamily: SANS, fontSize: 22, color: COLORS.textDim }}>a tiny source</div>
          </div>
          <div style={{ fontFamily: MONO, fontSize: 40, color: COLORS.textDim }}>⟶</div>
          <div style={{ position: "relative", width: 360, height: 90 }}>
            {Array.from({ length: 34 }).map((_, i) => {
              const golden = 2.399963;
              const a = i * golden;
              const rr = 24 + (i % 5) * 26;
              const col = [COLORS.blueLight, COLORS.violet, COLORS.pink][i % 3];
              return (
                <div key={i} style={{ position: "absolute", left: 180 + Math.cos(a) * rr, top: 45 + Math.sin(a) * rr * 0.7, width: 5, height: 5, borderRadius: "50%", background: col, opacity: 0.7, boxShadow: `0 0 6px ${col}` }} />
              );
            })}
          </div>
          <div style={{ fontFamily: SERIF, fontSize: 34, color: COLORS.textBright, maxWidth: 360 }}>
            …all of this. <span style={{ color: COLORS.textDim }}>That gap is the whole story.</span>
          </div>
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
