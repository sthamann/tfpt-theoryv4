import React from "react";
import { AbsoluteFill, useCurrentFrame, interpolate, Easing } from "remotion";
import { Bg } from "../components/Bg";
import { Eyebrow } from "../components/ui";
import { MONO, SERIF } from "../fonts";
import { COLORS } from "../theme";
import { enterUp, fadeInOut } from "../components/anim";

export const Scene01ColdOpen: React.FC = () => {
  const frame = useCurrentFrame();

  const eyebrow = enterUp(frame, 6, 24);
  // left-to-right reveal of the number
  const reveal = interpolate(frame, [24, 110], [100, 0], {
    easing: Easing.bezier(0.16, 1, 0.3, 1),
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const numScale = interpolate(frame, [24, 130], [0.96, 1], {
    easing: Easing.out(Easing.cubic),
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const underline = interpolate(frame, [110, 150], [0, 1], {
    easing: Easing.bezier(0.16, 1, 0.3, 1),
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // sub-line swaps, aligned to the caption beats:
  // "measured" -> "one answer, two inputs" -> "where it could break"
  const s1 = fadeInOut(frame, 120, 145, 240, 258);
  const s2 = fadeInOut(frame, 250, 274, 338, 354);
  const s3 = fadeInOut(frame, 345, 366, 442, 450);

  return (
    <AbsoluteFill>
      <Bg accent={COLORS.blue} tint="#7c3aed" />
      <AbsoluteFill
        style={{
          alignItems: "center",
          justifyContent: "center",
          paddingBottom: 150,
          flexDirection: "column",
          gap: 44,
        }}
      >
        <div style={{ ...eyebrow }}>
          <Eyebrow>α⁻¹ · fine-structure constant</Eyebrow>
        </div>

        <div style={{ position: "relative", transform: `scale(${numScale})` }}>
          <div
            style={{
              fontFamily: MONO,
              fontWeight: 700,
              fontSize: 170,
              letterSpacing: 2,
              color: COLORS.textBright,
              clipPath: `inset(0 ${reveal}% 0 0)`,
              textShadow: "0 0 60px rgba(96,165,250,0.35)",
            }}
          >
            137.0359992
          </div>
          <div
            style={{
              height: 8,
              marginTop: 14,
              borderRadius: 4,
              transformOrigin: "left center",
              transform: `scaleX(${underline})`,
              background: "linear-gradient(90deg,#60a5fa,#a78bfa 55%,#f472b6)",
              boxShadow: "0 0 30px -4px rgba(167,139,250,0.7)",
            }}
          />
        </div>

        <div style={{ position: "relative", height: 90, width: 1500 }}>
          <SubLine opacity={s1} color={COLORS.textDim}>
            Physics measures it.
          </SubLine>
          <SubLine opacity={s2} color={COLORS.textBright}>
            TFPT computes it — the one answer a short equation allows. Two inputs, nothing else.
          </SubLine>
          <SubLine opacity={s3} color={COLORS.open}>
            …and here is exactly where it could break.
          </SubLine>
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

const SubLine: React.FC<{
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
      fontFamily: SERIF,
      fontWeight: 500,
      fontSize: 50,
      color,
      textAlign: "center",
    }}
  >
    {children}
  </div>
);
