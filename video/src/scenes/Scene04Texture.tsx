import React from "react";
import { AbsoluteFill, useCurrentFrame } from "remotion";
import { Bg } from "../components/Bg";
import { Eyebrow, Chip } from "../components/ui";
import { Formula, Tok } from "../components/Formula";
import { StatusChip } from "../components/StatusChip";
import { SANS, SERIF } from "../fonts";
import { COLORS } from "../theme";
import { enterUp } from "../components/anim";

const DROPS = ["Vus", "Vcb", "Vub", "δ_CP (lead)", "θ₁₃"];

export const Scene04Texture: React.FC = () => {
  const frame = useCurrentFrame();

  const eyebrow = enterUp(frame, 6, 22);
  const formula = enterUp(frame, 60, 26);
  const sub = enterUp(frame, 360, 22);
  const bridge = enterUp(frame, 520, 26);

  return (
    <AbsoluteFill>
      <Bg accent="#22d3ee" tint="#7c3aed" />
      <AbsoluteFill style={{ flexDirection: "column", alignItems: "center", paddingTop: 96, gap: 40 }}>
        <div style={eyebrow}>
          <Eyebrow color="#22d3ee">One texture — not free knobs</Eyebrow>
        </div>

        <div style={{ ...formula, marginTop: 24 }}>
          <Formula size={40}>
            <Tok color={COLORS.textBright}>mass &amp; mixing</Tok> ={" "}
            <Tok color={COLORS.blueLight}>seed φ₀</Tok> ⊗{" "}
            <Tok color={COLORS.violet}>fixed flavor matrix R</Tok> ⊗{" "}
            <Tok color={COLORS.pink}>integer word-lengths</Tok>
          </Formula>
        </div>

        {/* CKM / angles dropping out */}
        <div style={{ display: "flex", gap: 20, marginTop: 10 }}>
          {DROPS.map((d, i) => {
            const e = enterUp(frame, 170 + i * 22, 20, 22);
            return (
              <div key={d} style={e}>
                <Chip color={COLORS.textBright} size={30}>
                  {d}
                </Chip>
              </div>
            );
          })}
        </div>
        <div style={{ ...sub, fontFamily: SANS, fontSize: 30, color: COLORS.textDim }}>
          …all fall out of the <b style={{ color: COLORS.text }}>same holonomy</b>; θ₁₃ comes straight from the seed.
        </div>

        {/* the honest bridge */}
        <div
          style={{
            ...bridge,
            marginTop: 26,
            display: "flex",
            alignItems: "center",
            gap: 26,
            padding: "30px 44px",
            borderRadius: 22,
            background: COLORS.openBg,
            border: `1px solid ${COLORS.open}55`,
            maxWidth: 1380,
          }}
        >
          <StatusChip grade="O" size={24} showLabel={false} />
          <div style={{ fontFamily: SERIF, fontSize: 38, color: COLORS.text, lineHeight: 1.25 }}>
            Absolute masses aren’t “magically done” — they run through{" "}
            <b style={{ color: COLORS.textBright }}>one typed bridge, v_geo</b>, and standard RG.
            <span style={{ color: COLORS.textDim }}> Dimensional analysis with a seatbelt.</span>
          </div>
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
