import React from "react";
import { AbsoluteFill, useCurrentFrame, interpolate } from "remotion";
import { COLORS } from "../theme";

/**
 * The shared backdrop: deep navy, a faint engineering grid (masked at the top
 * like the site hero) and two slowly drifting colour blobs. Tuned to stay
 * behind content — never competes with the type.
 */
export const Bg: React.FC<{ accent?: string; tint?: string }> = ({
  accent = COLORS.blue,
  tint = "#7c3aed",
}) => {
  const frame = useCurrentFrame();
  const drift = Math.sin(frame / 110) * 40;
  const drift2 = Math.cos(frame / 130) * 50;
  const pulse = interpolate(Math.sin(frame / 90), [-1, 1], [0.28, 0.45]);

  return (
    <AbsoluteFill style={{ backgroundColor: COLORS.bg, overflow: "hidden" }}>
      <AbsoluteFill
        style={{
          background: `radial-gradient(circle at 18% 4%, ${accent}22, transparent 45%), radial-gradient(circle at 84% 96%, ${tint}1f, transparent 45%)`,
        }}
      />
      {/* drifting glow */}
      <div
        style={{
          position: "absolute",
          top: -260 + drift,
          left: 960 - 550 + drift2,
          width: 1100,
          height: 620,
          borderRadius: "50%",
          filter: "blur(120px)",
          opacity: pulse,
          background: `radial-gradient(closest-side, ${accent}66, ${tint}33, transparent)`,
        }}
      />
      {/* engineering grid, masked top-down */}
      <AbsoluteFill
        style={{
          backgroundImage:
            "linear-gradient(to right, rgba(148,163,184,0.06) 1px, transparent 1px), linear-gradient(to bottom, rgba(148,163,184,0.06) 1px, transparent 1px)",
          backgroundSize: "72px 72px",
          maskImage:
            "radial-gradient(ellipse 85% 65% at 50% 0%, black, transparent)",
          WebkitMaskImage:
            "radial-gradient(ellipse 85% 65% at 50% 0%, black, transparent)",
        }}
      />
      {/* vignette */}
      <AbsoluteFill
        style={{
          boxShadow: "inset 0 0 360px 80px rgba(2,4,12,0.85)",
        }}
      />
    </AbsoluteFill>
  );
};
