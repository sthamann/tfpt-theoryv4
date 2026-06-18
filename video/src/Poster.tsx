import React from "react";
import { AbsoluteFill } from "remotion";
import { Bg } from "./components/Bg";
import { BrandMark } from "./components/ui";
import { SANS, SERIF, MONO } from "./fonts";
import { COLORS } from "./theme";

/** Static thumbnail used as the website <video> poster. */
export const Poster: React.FC = () => {
  return (
    <AbsoluteFill>
      <Bg accent={COLORS.blue} tint="#7c3aed" />
      <AbsoluteFill style={{ flexDirection: "column", alignItems: "center", justifyContent: "center", gap: 34 }}>
        <BrandMark size={40} />
        <div
          style={{
            fontFamily: MONO,
            fontWeight: 700,
            fontSize: 150,
            color: COLORS.textBright,
            textShadow: "0 0 70px rgba(96,165,250,0.4)",
          }}
        >
          α⁻¹ = 137.0359992
        </div>
        <div
          style={{
            width: 520,
            height: 8,
            borderRadius: 4,
            background: "linear-gradient(90deg,#60a5fa,#a78bfa 55%,#f472b6)",
            boxShadow: "0 0 30px -4px rgba(167,139,250,0.7)",
          }}
        />
        <div
          style={{
            fontFamily: SERIF,
            fontSize: 56,
            fontWeight: 600,
            color: COLORS.textBright,
            textAlign: "center",
            letterSpacing: -1,
          }}
        >
          Two axioms. One compiler.
          <br />A testable Standard-Model skeleton.
        </div>
        <div style={{ fontFamily: SANS, fontSize: 30, color: COLORS.textDim }}>
          a 3-minute introduction
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
