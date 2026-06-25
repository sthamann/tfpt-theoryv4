import React from "react";
import { AbsoluteFill, useCurrentFrame } from "remotion";
import { Bg } from "../components/Bg";
import { Eyebrow } from "../components/ui";
import { SANS, SERIF, MONO } from "../fonts";
import { COLORS } from "../theme";
import { enterUp } from "../components/anim";

/**
 * The "is this just numerology?" trust beat. Each stat card appears in step with
 * the narration (frame offsets from the scene start at 146s). Numbers mirror the
 * Safeguards companion (S) / website Safeguards band.
 */
const STATS: { big: string; small: string; color: string; at: number }[] = [
  {
    big: "13 / 13",
    small: "TFPT hits all 13 frozen predictions — 200,000 random look-alikes reach ≤ 5",
    color: COLORS.exact,
    at: 435, // ~160.5s
  },
  {
    big: "1 in 94,500",
    small: "α variants — exactly one lands in the measured window",
    color: COLORS.blueLight,
    at: 570, // ~165s
  },
  {
    big: "7 grammars",
    small: "seven disjoint number systems rebuild the same skeleton",
    color: COLORS.violet,
    at: 750, // ~171s
  },
  {
    big: "3 of 8",
    small: "E₈ pieces feed a prediction — the other 5 are published overhead",
    color: "#22d3ee",
    at: 930, // ~177s
  },
];

export const Scene06Safeguards: React.FC = () => {
  const frame = useCurrentFrame();

  const eyebrow = enterUp(frame, 6, 22);
  const headline = enterUp(frame, 150, 26); // "we tried to break it" (~151s)
  const band = enterUp(frame, 1095, 26); // ≤10⁻³⁰ + two paths (~182.5s)

  return (
    <AbsoluteFill>
      <Bg accent={COLORS.exact} tint="#7c3aed" />
      <AbsoluteFill style={{ flexDirection: "column", alignItems: "center", paddingTop: 70, gap: 24 }}>
        <div style={eyebrow}>
          <Eyebrow color={COLORS.exact}>Why this isn’t numerology</Eyebrow>
        </div>

        <div
          style={{
            ...headline,
            fontFamily: SERIF,
            fontSize: 50,
            fontWeight: 600,
            color: COLORS.textBright,
            textAlign: "center",
          }}
        >
          A theory of small numbers could be luck. <span style={{ color: COLORS.exact }}>So we tried to break it.</span>
        </div>

        {/* four punchy stat cards, revealed in step with the voice-over */}
        <div style={{ display: "flex", gap: 22, marginTop: 14 }}>
          {STATS.map((s) => {
            const e = enterUp(frame, s.at, 24, 26);
            return (
              <div
                key={s.big}
                style={{
                  ...e,
                  width: 410,
                  minHeight: 240,
                  display: "flex",
                  flexDirection: "column",
                  gap: 16,
                  padding: "30px 30px",
                  borderRadius: 22,
                  background: "rgba(10,16,30,0.66)",
                  border: `1.5px solid ${s.color}55`,
                  boxShadow: `0 0 50px -24px ${s.color}`,
                  backdropFilter: "blur(8px)",
                }}
              >
                <div
                  style={{
                    fontFamily: SERIF,
                    fontSize: 64,
                    fontWeight: 700,
                    color: s.color,
                    lineHeight: 1,
                  }}
                >
                  {s.big}
                </div>
                <div style={{ fontFamily: SANS, fontSize: 26, color: COLORS.text, lineHeight: 1.35 }}>
                  {s.small}
                </div>
              </div>
            );
          })}
        </div>

        {/* the bottom-line odds + two independent paths */}
        <div
          style={{
            ...band,
            display: "flex",
            alignItems: "center",
            gap: 30,
            marginTop: 22,
            padding: "22px 40px",
            borderRadius: 20,
            background: "rgba(2,6,18,0.55)",
            border: `1px solid ${COLORS.exact}44`,
          }}
        >
          <div style={{ display: "flex", flexDirection: "column" }}>
            <div style={{ fontFamily: MONO, fontSize: 46, fontWeight: 700, color: COLORS.exact }}>
              ≤ 10⁻³⁰
            </div>
            <div style={{ fontFamily: SANS, fontSize: 24, color: COLORS.textDim }}>
              that a look-alike matches the full scorecard
            </div>
          </div>
          <div style={{ width: 1, alignSelf: "stretch", background: COLORS.border }} />
          <div style={{ fontFamily: SANS, fontSize: 26, color: COLORS.text }}>
            checked twice — independently in{" "}
            <b style={{ color: COLORS.textBright }}>Wolfram</b> and{" "}
            <b style={{ color: COLORS.textBright }}>Lean</b>
          </div>
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
