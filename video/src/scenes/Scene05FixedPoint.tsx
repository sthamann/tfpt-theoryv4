import React from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig, interpolate } from "remotion";
import { Bg } from "../components/Bg";
import { Eyebrow } from "../components/ui";
import { SANS, SERIF, MONO } from "../fonts";
import { COLORS } from "../theme";
import { pop, popScale, springIn, LoopArc, DrawnPath } from "../components/fx";

export const Scene05FixedPoint: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const buildDraw = { start: 30, end: 330 }; // inputs → E8
  const loopProgress = interpolate(frame, [330, 520], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const closed = loopProgress > 0.96;
  const lock = springIn(frame, fps, 515, { damping: 9, mass: 0.7, stiffness: 140 });
  const inputsGlow = interpolate(lock, [0, 1], [0.5, 1]);

  const S = 470; // ring box
  const cx = S / 2;

  return (
    <AbsoluteFill>
      <Bg accent={COLORS.exact} tint="#a78bfa" />
      <AbsoluteFill style={{ flexDirection: "column", alignItems: "center", paddingTop: 52 }}>
        <div style={pop(frame, fps, 8)}>
          <Eyebrow color={COLORS.exact}>The twist — it computes itself</Eyebrow>
        </div>

        <div style={{ position: "relative", width: S, height: S, marginTop: 18 }}>
          {/* the closing loop */}
          <div style={{ position: "absolute", inset: 0 }}>
            <LoopArc size={S} progress={loopProgress} stroke={COLORS.exact} width={6} />
          </div>

          {/* the forward "build" arrow inputs → E8 */}
          <svg width={S} height={S} viewBox={`0 0 ${S} ${S}`} style={{ position: "absolute", inset: 0 }}>
            <DrawnPath d={`M ${cx} 96 L ${cx} ${S - 96}`} start={buildDraw.start} end={buildDraw.end} stroke={COLORS.blueLight} width={3} length={320} />
            {frame > buildDraw.end - 30 && (
              <polygon points={`${cx - 9},${S - 104} ${cx + 9},${S - 104} ${cx},${S - 88}`} fill={COLORS.blueLight} opacity={interpolate(frame, [buildDraw.end - 30, buildDraw.end], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" })} />
            )}
          </svg>

          {/* inputs node (top) — snaps + locks when the loop closes */}
          <div
            style={{
              position: "absolute",
              top: 32,
              left: "50%",
              transform: `translateX(-50%) scale(${1 + (closed ? lock * 0.04 : 0)})`,
              display: "flex",
              alignItems: "center",
              gap: 12,
              padding: "12px 22px",
              borderRadius: 999,
              background: "rgba(2,6,18,0.7)",
              border: `2px solid ${COLORS.blueLight}`,
              opacity: inputsGlow,
              boxShadow: `0 0 ${20 + lock * 40}px -8px ${COLORS.blueLight}`,
            }}
          >
            <span style={{ fontFamily: MONO, fontSize: 26, fontWeight: 700, color: COLORS.textBright }}>c₃ = 1/(8π) · g_car = 5</span>
            <span style={{ fontSize: 24, opacity: lock }}>🔒</span>
          </div>

          {/* E8 node (bottom) */}
          <div
            style={{
              position: "absolute",
              bottom: 30,
              left: "50%",
              transform: "translateX(-50%)",
              width: 110,
              height: 110,
              borderRadius: "50%",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              background: `radial-gradient(circle at 50% 40%, ${COLORS.exact}44, rgba(10,16,30,0.8))`,
              border: `2px solid ${COLORS.exact}`,
              boxShadow: `0 0 40px -12px ${COLORS.exact}`,
            }}
          >
            <span style={{ fontFamily: MONO, fontSize: 46, fontWeight: 700, color: COLORS.textBright }}>E₈</span>
          </div>

          {/* centre label */}
          <div style={{ position: "absolute", inset: 0, display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", gap: 4 }}>
            <div style={{ ...popScale(frame, fps, 530), fontFamily: SERIF, fontSize: 46, fontWeight: 700, color: COLORS.exact, letterSpacing: 1 }}>
              FIXED POINT
            </div>
            <div style={{ ...pop(frame, fps, 560), fontFamily: SANS, fontSize: 22, color: COLORS.textDim }}>
              it works out its own inputs
            </div>
          </div>
        </div>

        <div style={{ ...pop(frame, fps, 700), marginTop: 14, fontFamily: SERIF, fontSize: 36, color: COLORS.text, textAlign: "center", maxWidth: 1280 }}>
          Not a model you tune until it fits — <b style={{ color: COLORS.textBright }}>a structure that has to be what it is</b>.
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
