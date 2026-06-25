import React from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig, interpolate } from "remotion";
import { Bg } from "../components/Bg";
import { Eyebrow } from "../components/ui";
import { SANS, SERIF, MONO } from "../fonts";
import { COLORS } from "../theme";
import { pop, E8Petrie } from "../components/fx";

/** A small candidate universe whose lattice fails to lock — it shatters. */
const FailedTile: React.FC<{ label: string; at: number }> = ({ label, at }) => {
  const frame = useCurrentFrame();
  const f = frame - at;
  const shatter = interpolate(f, [22, 70], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const form = interpolate(f, [0, 16], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const xMark = interpolate(f, [26, 40], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return (
    <div style={{ position: "relative", width: 200, height: 150, opacity: form }}>
      {Array.from({ length: 12 }).map((_, i) => {
        const a = (i * 360) / 12 * (Math.PI / 180);
        const r = 34 * form + shatter * (90 + (i % 4) * 40);
        const op = interpolate(shatter, [0, 0.5, 1], [0.9, 0.7, 0]);
        return (
          <div
            key={i}
            style={{
              position: "absolute",
              left: 100 + Math.cos(a) * r,
              top: 60 + Math.sin(a) * r,
              width: 6,
              height: 6,
              borderRadius: "50%",
              background: COLORS.open,
              opacity: op,
              boxShadow: `0 0 6px ${COLORS.open}`,
            }}
          />
        );
      })}
      <div style={{ position: "absolute", left: 0, right: 0, top: 36, textAlign: "center", fontSize: 54, color: COLORS.open, opacity: xMark, fontWeight: 800 }}>✗</div>
      <div style={{ position: "absolute", left: 0, right: 0, bottom: 0, textAlign: "center", fontFamily: MONO, fontSize: 22, color: COLORS.textDim }}>{label}</div>
    </div>
  );
};

export const Scene04Proof: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const progress = interpolate(frame, [40, 520], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const labelIn = interpolate(frame, [150, 220], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });

  return (
    <AbsoluteFill>
      <Bg accent={COLORS.exact} tint="#5b8cff" />
      <AbsoluteFill style={{ flexDirection: "column", alignItems: "center", paddingTop: 56 }}>
        <div style={pop(frame, fps, 8)}>
          <Eyebrow color={COLORS.exact}>Why it's rigorous — the proof layer</Eyebrow>
        </div>

        {/* the E8 Petrie projection assembling */}
        <div style={{ position: "relative", width: 450, height: 450, marginTop: 4 }}>
          <div style={{ position: "absolute", inset: 0, display: "flex", alignItems: "center", justifyContent: "center" }}>
            <E8Petrie size={450} progress={progress} rotateSpeed={0.1} />
          </div>
          {/* dark backing for legibility */}
          <div style={{ position: "absolute", inset: 0, display: "flex", alignItems: "center", justifyContent: "center", opacity: labelIn }}>
            <div style={{ width: 230, height: 230, borderRadius: "50%", background: "radial-gradient(circle, rgba(2,6,18,0.82) 40%, transparent 72%)" }} />
          </div>
          {/* centre label */}
          <div style={{ position: "absolute", inset: 0, display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", opacity: labelIn, gap: 2 }}>
            <div style={{ fontFamily: MONO, fontSize: 70, fontWeight: 700, color: COLORS.textBright, textShadow: `0 0 30px ${COLORS.exact}` }}>E₈</div>
            <div style={{ fontFamily: SANS, fontSize: 19, fontWeight: 700, letterSpacing: 2, color: COLORS.exact }}>THE PROOF LAYER</div>
            <div style={{ fontFamily: MONO, fontSize: 18, color: COLORS.textDim }}>240 roots · det = 1</div>
          </div>
        </div>

        {/* caption */}
        <div style={{ ...pop(frame, fps, 360), marginTop: 8, fontFamily: SERIF, fontSize: 34, color: COLORS.text, textAlign: "center", maxWidth: 1300 }}>
          The referee: the parts can fit together <b style={{ color: COLORS.textBright }}>only one way</b>.
        </div>

        {/* failed universes */}
        <div style={{ ...pop(frame, fps, 855), display: "flex", alignItems: "center", gap: 26, marginTop: 14 }}>
          <div style={{ fontFamily: SANS, fontSize: 24, color: COLORS.textDim, maxWidth: 220 }}>
            change the tempo or width and it <b style={{ color: COLORS.open }}>doesn't compile</b>:
          </div>
          <FailedTile label="width 4" at={870} />
          <FailedTile label="width 6" at={900} />
          <FailedTile label="tempo ≠ 8" at={930} />
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
