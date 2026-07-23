import React from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig } from "remotion";
import { Bg } from "../components/Bg";
import { Eyebrow } from "../components/ui";
import { StatusChip } from "../components/StatusChip";
import { SANS, SERIF } from "../fonts";
import { COLORS, StatusGrade } from "../theme";
import { pop } from "../components/fx";

/**
 * The honest remainder, post-breakthroughs (2026-07-23 ledger state):
 * SEAM.EQUIV and WOIT.OS.TWISTOR.01 stay open, the global BCOV integral is
 * the measure-chain residual, the unit is still ungiveable, and the bit is
 * defined but remains input.
 */
const GAPS: { title: string; sub: string; grade: StatusGrade; color: string; at: number }[] = [
  { title: "The interacting seam", sub: "one construction site — now with its first hard filter", grade: "O", color: COLORS.open, at: 60 },
  { title: "One global integral", sub: "the last step of the measure chain", grade: "O", color: COLORS.violet, at: 90 },
  { title: "One unit", sub: "no pure number can give it", grade: "O", color: COLORS.conditional, at: 120 },
  { title: "One bit", sub: "defined as a measurement — still an input", grade: "C", color: "#22d3ee", at: 150 },
];

const KILLS = ["neutrino mass", "proton decay", "dark energy"];

export const Scene09Open: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  return (
    <AbsoluteFill>
      <Bg accent={COLORS.conditional} tint="#fb7185" />
      <AbsoluteFill style={{ flexDirection: "column", alignItems: "center", justifyContent: "center", gap: 26, paddingBottom: 150 }}>
        <div style={pop(frame, fps, 8)}>
          <Eyebrow color={COLORS.conditional}>Honest about the gaps</Eyebrow>
        </div>

        <div style={{ ...pop(frame, fps, 22), fontFamily: SERIF, fontSize: 44, fontWeight: 600, color: COLORS.textBright }}>
          Closer — and still not finished.
        </div>

        <div style={{ display: "flex", gap: 20 }}>
          {GAPS.map((g) => (
            <div
              key={g.title}
              style={{
                ...pop(frame, fps, g.at),
                width: 356,
                display: "flex",
                flexDirection: "column",
                gap: 12,
                padding: 26,
                borderRadius: 20,
                background: "rgba(10,16,30,0.64)",
                border: `1.5px solid ${g.color}55`,
              }}
            >
              <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", gap: 10 }}>
                <div style={{ fontFamily: SERIF, fontSize: 29, fontWeight: 600, color: COLORS.textBright }}>{g.title}</div>
                <StatusChip grade={g.grade} size={17} showLabel={false} />
              </div>
              <div style={{ fontFamily: SANS, fontSize: 23, color: COLORS.text, lineHeight: 1.35 }}>{g.sub}</div>
            </div>
          ))}
        </div>

        <div style={{ ...pop(frame, fps, 235), display: "flex", alignItems: "center", gap: 16, marginTop: 4 }}>
          <span style={{ fontFamily: SANS, fontSize: 28, color: COLORS.textDim }}>every gap labelled — and still killable:</span>
          {KILLS.map((k, i) => (
            <div key={k} style={{ ...pop(frame, fps, 250 + i * 16), fontFamily: SANS, fontSize: 26, fontWeight: 700, color: COLORS.textBright, padding: "8px 20px", borderRadius: 12, background: COLORS.openBg, border: `1.5px solid ${COLORS.open}66` }}>
              {k}
            </div>
          ))}
        </div>

        <div style={{ ...pop(frame, fps, 320), fontFamily: SERIF, fontSize: 34, color: COLORS.open, fontWeight: 600 }}>
          One clean miss — and it's wrong.
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
