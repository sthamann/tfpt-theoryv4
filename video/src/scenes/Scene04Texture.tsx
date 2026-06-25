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
  const sub = enterUp(frame, 480, 22); // "drop out of the same geometry" (~111s)
  const bridge = enterUp(frame, 630, 26); // the one honest unit (~116s)

  return (
    <AbsoluteFill>
      <Bg accent="#22d3ee" tint="#7c3aed" />
      <AbsoluteFill style={{ flexDirection: "column", alignItems: "center", paddingTop: 96, gap: 40 }}>
        <div style={eyebrow}>
          <Eyebrow color="#22d3ee">One pattern — not free knobs</Eyebrow>
        </div>

        <div style={{ ...formula, marginTop: 24 }}>
          <Formula size={40}>
            <Tok color={COLORS.textBright}>mass &amp; mixing</Tok> ={" "}
            <Tok color={COLORS.blueLight}>one seed φ₀</Tok> ⊗{" "}
            <Tok color={COLORS.violet}>fixed matrix R</Tok> ⊗{" "}
            <Tok color={COLORS.pink}>whole-number steps</Tok>
          </Formula>
        </div>

        {/* CKM / angles dropping out */}
        <div style={{ display: "flex", gap: 20, marginTop: 10 }}>
          {DROPS.map((d, i) => {
            const e = enterUp(frame, 320 + i * 20, 20, 22);
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
          …all drop out of the <b style={{ color: COLORS.text }}>same geometry</b>; θ₁₃ comes straight from the seed.
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
            Absolute masses still need <b style={{ color: COLORS.textBright }}>one honest unit, v_geo</b>.
            <span style={{ color: COLORS.textDim }}> We flag it — we don’t hide it.</span>
          </div>
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
