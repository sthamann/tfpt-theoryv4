import React from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig, interpolate, Easing } from "remotion";
import { Bg } from "../components/Bg";
import { Eyebrow } from "../components/ui";
import { SANS, SERIF, MONO } from "../fonts";
import { COLORS } from "../theme";
import { pop, DrawnPath } from "../components/fx";

const FACES = [
  { label: "3 families", color: COLORS.blueLight, at: 110 },
  { label: "5 slots", color: COLORS.violet, at: 150 },
  { label: "E₈ clock · 30", color: COLORS.exact, at: 190 },
];

// point on the quadratic Bézier well P0(40,60) P1(300,250) P2(560,60)
const wellPoint = (t: number) => {
  const u = 1 - t;
  const x = u * u * 40 + 2 * u * t * 300 + t * t * 560;
  const y = u * u * 60 + 2 * u * t * 250 + t * t * 60;
  return { x, y };
};

const Gear: React.FC<{ n: number; size: number; color: string; speed: number }> = ({ n, size, color, speed }) => {
  const frame = useCurrentFrame();
  return (
    <div style={{ position: "relative", width: size, height: size }}>
      <div style={{ position: "absolute", inset: 0, borderRadius: "50%", border: `7px dashed ${color}`, transform: `rotate(${frame * speed}deg)`, boxShadow: `0 0 26px -10px ${color}` }} />
      <div style={{ position: "absolute", inset: 0, display: "flex", alignItems: "center", justifyContent: "center", fontFamily: MONO, fontSize: size * 0.4, fontWeight: 700, color: COLORS.textBright }}>{n}</div>
    </div>
  );
};

export const Scene06Beauty: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // ball rolling to the single resting state
  const t = interpolate(frame, [420, 520], [0.02, 0.5], { easing: Easing.out(Easing.cubic), extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const wobble = interpolate(frame, [520, 640], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }) * 0.06 * Math.sin((frame - 520) / 6);
  const ball = wellPoint(Math.min(0.6, t + wobble));

  return (
    <AbsoluteFill>
      <Bg accent={COLORS.violet} tint="#22d3ee" />
      <AbsoluteFill style={{ flexDirection: "column", alignItems: "center", paddingTop: 56 }}>
        <div style={pop(frame, fps, 8)}>
          <Eyebrow color={COLORS.violet}>The beauty — one connected object</Eyebrow>
        </div>

        {/* 2·3·5 hub → faces */}
        <div style={{ display: "flex", alignItems: "center", gap: 40, marginTop: 30 }}>
          <div style={{ ...pop(frame, fps, 60), fontFamily: SERIF, fontSize: 70, fontWeight: 700, color: COLORS.textBright, padding: "16px 30px", borderRadius: 20, background: "rgba(2,6,18,0.55)", border: `1.5px solid ${COLORS.violet}66`, boxShadow: `0 0 50px -18px ${COLORS.violet}` }}>
            2 · 3 · 5
          </div>
          <svg width={120} height={120} viewBox="0 0 120 120">
            <DrawnPath d="M0 60 L120 18" start={90} end={150} length={140} stroke={COLORS.blueLight} width={2} />
            <DrawnPath d="M0 60 L120 60" start={130} end={190} length={120} stroke={COLORS.violet} width={2} />
            <DrawnPath d="M0 60 L120 102" start={170} end={230} length={140} stroke={COLORS.exact} width={2} />
          </svg>
          <div style={{ display: "flex", flexDirection: "column", gap: 14 }}>
            {FACES.map((f) => (
              <div key={f.label} style={{ ...pop(frame, fps, f.at), fontFamily: SANS, fontSize: 28, fontWeight: 700, color: COLORS.textBright, padding: "10px 20px", borderRadius: 12, background: "rgba(10,16,30,0.6)", border: `1px solid ${f.color}66` }}>
                {f.label}
              </div>
            ))}
          </div>
        </div>
        <div style={{ ...pop(frame, fps, 240), marginTop: 16, fontFamily: SERIF, fontSize: 32, color: COLORS.textDim }}>
          the same atoms in every part — <b style={{ color: COLORS.textBright }}>one object, seen many ways</b>.
        </div>

        {/* the single resting state */}
        <div style={{ display: "flex", alignItems: "center", gap: 50, marginTop: 26 }}>
          <div style={{ display: "flex", alignItems: "center" }}>
            <Gear n={5} size={84} color={COLORS.violet} speed={1.6} />
            <div style={{ marginLeft: -10 }}>
              <Gear n={6} size={70} color={COLORS.blueLight} speed={-2.0} />
            </div>
          </div>
          <div style={{ position: "relative", width: 600, height: 130 }}>
            <svg width={600} height={130} viewBox="0 0 600 130" style={{ position: "absolute", inset: 0 }}>
              <path d="M40 60 Q300 250 560 60" fill="none" stroke={COLORS.border} strokeWidth={4} />
              <circle cx={ball.x} cy={ball.y} r={14} fill={COLORS.exact} style={{ filter: `drop-shadow(0 0 12px ${COLORS.exact})` }} />
            </svg>
            <div style={{ position: "absolute", bottom: -6, left: 0, right: 0, textAlign: "center", fontFamily: SANS, fontSize: 24, color: COLORS.textDim }}>
              one resting state — <b style={{ color: COLORS.exact }}>selected, not tuned</b>
            </div>
          </div>
        </div>

        <div style={{ ...pop(frame, fps, 600), marginTop: 8, fontFamily: SANS, fontSize: 30, color: COLORS.text }}>
          almost no free choices · one connected picture
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
