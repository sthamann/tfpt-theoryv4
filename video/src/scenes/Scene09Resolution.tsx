import React from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig } from "remotion";
import { Bg } from "../components/Bg";
import { BrandMark } from "../components/ui";
import { SANS, SERIF, MONO } from "../fonts";
import { COLORS, gradientText } from "../theme";
import { pop, E8Petrie, LoopArc } from "../components/fx";
import { fade, fadeInOut } from "../components/anim";

export const Scene09Resolution: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const main = 1 - fade(frame, 430, 480);
  const end = fade(frame, 452, 510);

  const sA = fadeInOut(frame, 20, 45, 150, 175);
  const sB = fadeInOut(frame, 175, 200, 330, 355);
  const sC = fadeInOut(frame, 355, 380, 470, 488);

  return (
    <AbsoluteFill>
      <Bg accent={COLORS.blue} tint="#a78bfa" />

      {/* the whole construct, at rest */}
      <AbsoluteFill style={{ flexDirection: "column", alignItems: "center", justifyContent: "center", gap: 28, opacity: main }}>
        <div style={{ ...pop(frame, fps, 10), fontFamily: SERIF, fontWeight: 600, fontSize: 80, letterSpacing: -1.5, ...gradientText() }}>
          Is reality compiled?
        </div>

        <div style={{ position: "relative", width: 320, height: 320 }}>
          <div style={{ position: "absolute", inset: 0, display: "flex", alignItems: "center", justifyContent: "center" }}>
            <E8Petrie size={250} progress={1} rotateSpeed={0.06} opacity={0.9} />
          </div>
          <div style={{ position: "absolute", inset: 0 }}>
            <LoopArc size={320} progress={1} stroke={COLORS.exact} width={4} />
          </div>
        </div>

        <div style={{ position: "relative", height: 70, width: 1500 }}>
          <div style={{ opacity: sA, position: "absolute", inset: 0, textAlign: "center", fontFamily: SANS, fontSize: 38, color: COLORS.textDim }}>
            We don't know — and that's the honest answer.
          </div>
          <div style={{ opacity: sB, position: "absolute", inset: 0, textAlign: "center", fontFamily: SANS, fontSize: 38, color: COLORS.text }}>
            But here's a version you can <b style={{ color: COLORS.textBright }}>actually test</b>.
          </div>
          <div style={{ opacity: sC, position: "absolute", inset: 0, textAlign: "center", fontFamily: SANS, fontSize: 34, color: COLORS.textDim }}>
            built from almost nothing · every gap marked · every test named
          </div>
        </div>
      </AbsoluteFill>

      {/* end card */}
      <AbsoluteFill style={{ flexDirection: "column", alignItems: "center", justifyContent: "center", gap: 26, opacity: end }}>
        <BrandMark size={64} />
        <div style={{ fontFamily: SERIF, fontSize: 52, fontWeight: 600, color: COLORS.textBright, textAlign: "center", letterSpacing: -1, maxWidth: 1400, lineHeight: 1.2 }}>
          Maybe the constants were never arbitrary —
          <br />
          maybe they simply had to add up.
        </div>
        <div style={{ width: 360, height: 2, background: COLORS.border }} />
        <div style={{ fontFamily: SANS, fontSize: 30, color: COLORS.textDim }}>
          Is reality compiled? — a question you can test.
        </div>
        <div style={{ fontFamily: MONO, fontSize: 32, fontWeight: 600, ...gradientText() }}>fixpoint-theory.com</div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
