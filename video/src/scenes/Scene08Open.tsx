import React from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig } from "remotion";
import { Bg } from "../components/Bg";
import { Eyebrow } from "../components/ui";
import { StatusChip } from "../components/StatusChip";
import { SANS, SERIF } from "../fonts";
import { COLORS, StatusGrade } from "../theme";
import { pop } from "../components/fx";

const GAPS: { title: string; sub: string; grade: StatusGrade; color: string; at: number }[] = [
  { title: "Seal the core", sub: "one more theorem", grade: "C", color: COLORS.conditional, at: 150 },
  { title: "Bridges to known physics", sub: "a few links, not yet proofs", grade: "C", color: COLORS.violet, at: 190 },
  { title: "One unit", sub: "no pure number can give it", grade: "O", color: COLORS.open, at: 230 },
];

const KILLS = ["neutrino mass", "proton decay", "dark energy"];

export const Scene08Open: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  return (
    <AbsoluteFill>
      <Bg accent={COLORS.conditional} tint="#fb7185" />
      <AbsoluteFill style={{ flexDirection: "column", alignItems: "center", justifyContent: "center", gap: 28, paddingBottom: 150 }}>
        <div style={pop(frame, fps, 8)}>
          <Eyebrow color={COLORS.conditional}>Honest about the gaps</Eyebrow>
        </div>

        <div style={{ ...pop(frame, fps, 24), fontFamily: SERIF, fontSize: 46, fontWeight: 600, color: COLORS.textBright }}>
          It isn't finished — and we don't pretend it is.
        </div>

        <div style={{ display: "flex", gap: 24 }}>
          {GAPS.map((g) => (
            <div
              key={g.title}
              style={{
                ...pop(frame, fps, g.at),
                width: 420,
                display: "flex",
                flexDirection: "column",
                gap: 12,
                padding: 28,
                borderRadius: 20,
                background: "rgba(10,16,30,0.64)",
                border: `1.5px solid ${g.color}55`,
              }}
            >
              <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
                <div style={{ fontFamily: SERIF, fontSize: 32, fontWeight: 600, color: COLORS.textBright }}>{g.title}</div>
                <StatusChip grade={g.grade} size={18} showLabel={false} />
              </div>
              <div style={{ fontFamily: SANS, fontSize: 26, color: COLORS.text }}>{g.sub}</div>
            </div>
          ))}
        </div>

        <div style={{ ...pop(frame, fps, 390), display: "flex", alignItems: "center", gap: 18, marginTop: 6 }}>
          <span style={{ fontFamily: SANS, fontSize: 30, color: COLORS.textDim }}>every gap labelled — and it's killable:</span>
          {KILLS.map((k, i) => (
            <div key={k} style={{ ...pop(frame, fps, 410 + i * 22), fontFamily: SANS, fontSize: 28, fontWeight: 700, color: COLORS.textBright, padding: "10px 22px", borderRadius: 12, background: COLORS.openBg, border: `1.5px solid ${COLORS.open}66` }}>
              {k}
            </div>
          ))}
        </div>

        <div style={{ ...pop(frame, fps, 490), fontFamily: SERIF, fontSize: 36, color: COLORS.open, fontWeight: 600 }}>
          One clean miss — and it's wrong.
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
