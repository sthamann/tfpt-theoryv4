import React from "react";
import { useCurrentFrame, useVideoConfig, interpolate } from "remotion";
import captions from "../captions.json";
import { Caption } from "../script";
import { SANS } from "../fonts";
import { COLORS } from "../theme";

const CUES = captions as Caption[];
const FADE = 0.18; // seconds

/**
 * The global caption track, burned in at the bottom. It reads the same
 * captions.json that generates the .vtt file shipped to the website, so the
 * on-screen text and the accessible subtitle track are guaranteed identical.
 */
export const Subtitle: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = frame / fps;

  const cue = CUES.find((c) => t >= c.from && t < c.to);
  if (!cue) return null;

  const opacity = interpolate(
    t,
    [cue.from, cue.from + FADE, cue.to - FADE, cue.to],
    [0, 1, 1, 0],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" },
  );

  return (
    <div
      style={{
        position: "absolute",
        left: 0,
        right: 0,
        bottom: 96,
        display: "flex",
        justifyContent: "center",
        padding: "0 220px",
      }}
    >
      <div
        style={{
          opacity,
          maxWidth: 1320,
          textAlign: "center",
          fontFamily: SANS,
          fontWeight: 500,
          fontSize: 38,
          lineHeight: 1.4,
          color: COLORS.textBright,
          background: "rgba(2,6,18,0.66)",
          border: `1px solid ${COLORS.border}`,
          borderRadius: 16,
          padding: "18px 34px",
          backdropFilter: "blur(8px)",
          textShadow: "0 2px 18px rgba(0,0,0,0.6)",
        }}
      >
        {cue.text}
      </div>
    </div>
  );
};
