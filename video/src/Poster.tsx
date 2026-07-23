import React from "react";
import { AbsoluteFill } from "remotion";
import { Bg } from "./components/Bg";
import { BrandMark } from "./components/ui";
import { E8Petrie } from "./components/fx";
import { SANS, SERIF, MONO } from "./fonts";
import { COLORS, gradientText } from "./theme";

/** Static thumbnail used as the website <video> poster. */
export const Poster: React.FC = () => {
  return (
    <AbsoluteFill>
      <Bg accent={COLORS.blue} tint="#7c3aed" />
      <AbsoluteFill style={{ flexDirection: "column", alignItems: "center", justifyContent: "center", gap: 30 }}>
        <BrandMark size={40} />
        <div style={{ position: "relative", width: 360, height: 360 }}>
          <div style={{ position: "absolute", inset: 0, display: "flex", alignItems: "center", justifyContent: "center" }}>
            <E8Petrie size={360} progress={1} rotateSpeed={0} />
          </div>
        </div>
        <div
          style={{
            fontFamily: SERIF,
            fontWeight: 600,
            fontSize: 92,
            letterSpacing: -2,
            ...gradientText(),
          }}
        >
          Is reality compiled?
        </div>
        <div
          style={{
            fontFamily: SANS,
            fontSize: 34,
            color: COLORS.text,
            textAlign: "center",
          }}
        >
          The whole Standard Model, gravity and 27 predictions — from almost nothing.
        </div>
        <div style={{ fontFamily: MONO, fontSize: 26, color: COLORS.textDim }}>a 5½-minute introduction</div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
