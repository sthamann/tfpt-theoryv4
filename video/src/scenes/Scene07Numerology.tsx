import React from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig, interpolate } from "remotion";
import { Bg } from "../components/Bg";
import { Eyebrow } from "../components/ui";
import { SANS, SERIF } from "../fonts";
import { COLORS } from "../theme";
import { pop, CountUp } from "../components/fx";
import { fade, fadeInOut } from "../components/anim";

const GRID = 18 * 7; // 126 illustrative pips for "hundreds of checks"

export const Scene07Numerology: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const question = fadeInOut(frame, 12, 40, 285, 315);
  const swarm = fadeInOut(frame, 300, 340, 700, 745);
  const badges = fadeInOut(frame, 700, 740, 1055, 1095);
  const nullm = fade(frame, 1095, 1140);

  const lit = Math.max(0, Math.min(GRID, Math.floor((frame - 320) / 2.6)));

  return (
    <AbsoluteFill>
      <Bg accent="#fb7185" tint="#7c3aed" />
      <AbsoluteFill style={{ flexDirection: "column", alignItems: "center", paddingTop: 56 }}>
        <div style={pop(frame, fps, 8)}>
          <Eyebrow color={COLORS.open}>Is this just numerology?</Eyebrow>
        </div>

        {/* Phase A — the fair objection */}
        <div style={{ position: "absolute", top: 230, left: 0, right: 0, textAlign: "center", opacity: question, padding: "0 200px" }}>
          <div style={{ fontFamily: SERIF, fontSize: 50, color: COLORS.textBright }}>
            Small whole numbers that fit reality —
          </div>
          <div style={{ fontFamily: SERIF, fontSize: 50, color: COLORS.open, marginTop: 8 }}>
            isn't that like seeing faces in clouds?
          </div>
        </div>

        {/* Phase B — hundreds of machine-checks assembling */}
        <div style={{ position: "absolute", top: 170, left: 0, right: 0, opacity: swarm, display: "flex", flexDirection: "column", alignItems: "center", gap: 22 }}>
          <div style={{ display: "flex", flexWrap: "wrap", gap: 7, width: 900, justifyContent: "center" }}>
            {Array.from({ length: GRID }).map((_, i) => {
              const on = i < lit;
              return (
                <div
                  key={i}
                  style={{
                    width: 26,
                    height: 26,
                    borderRadius: 6,
                    background: on ? COLORS.exact : "rgba(148,163,184,0.14)",
                    boxShadow: on ? `0 0 8px ${COLORS.exact}` : "none",
                    transform: on ? "scale(1)" : "scale(0.8)",
                  }}
                />
              );
            })}
          </div>
          <div style={{ display: "flex", alignItems: "baseline", gap: 14 }}>
            <CountUp to={422} start={320} end={690} style={{ fontFamily: SERIF, fontSize: 62, fontWeight: 700, color: COLORS.textBright }} />
            <span style={{ fontFamily: SANS, fontSize: 30, color: COLORS.text }}>independent checks — each verified by computer</span>
          </div>
          <div style={{ fontFamily: SANS, fontSize: 26, color: COLORS.textDim }}>
            nobody drew this top-down — it <b style={{ color: COLORS.textBright }}>assembled itself</b> into one whole.
          </div>
        </div>

        {/* Phase C — verified twice + red team */}
        <div style={{ position: "absolute", top: 280, left: 0, right: 0, opacity: badges, display: "flex", flexDirection: "column", alignItems: "center", gap: 26 }}>
          <div style={{ fontFamily: SERIF, fontSize: 38, color: COLORS.text }}>
            Every load-bearing claim, <b style={{ color: COLORS.textBright }}>checked twice</b> — and a team paid to break it.
          </div>
          <div style={{ display: "flex", gap: 24 }}>
            {[
              { t: "Wolfram", s: "independent engine", c: COLORS.blueLight },
              { t: "Lean", s: "kernel proof", c: COLORS.violet },
              { t: "Red team", s: "tries to kill it", c: COLORS.open },
            ].map((b) => (
              <div key={b.t} style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 6, width: 300, padding: "26px 20px", borderRadius: 18, background: "rgba(10,16,30,0.64)", border: `1.5px solid ${b.c}66`, boxShadow: `0 0 40px -20px ${b.c}` }}>
                <div style={{ fontFamily: SANS, fontSize: 38, fontWeight: 700, color: COLORS.textBright }}>{b.t}</div>
                <div style={{ fontFamily: SANS, fontSize: 22, color: b.c }}>{b.s}</div>
              </div>
            ))}
          </div>
        </div>

        {/* Phase D — the null model */}
        <div style={{ position: "absolute", top: 250, left: 0, right: 0, opacity: nullm, display: "flex", flexDirection: "column", alignItems: "center", gap: 26 }}>
          <div style={{ fontFamily: SERIF, fontSize: 36, color: COLORS.text }}>
            Froze 13 predictions <b style={{ color: COLORS.textBright }}>before the data</b>. Then 200,000 random look-alikes.
          </div>
          <div style={{ display: "flex", alignItems: "flex-end", gap: 60, height: 200 }}>
            {/* random cluster */}
            <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 10 }}>
              <div style={{ display: "flex", alignItems: "flex-end", gap: 6, height: 170 }}>
                {Array.from({ length: 9 }).map((_, i) => {
                  const score = 1 + ((i * 7) % 5); // 1..5
                  const h = interpolate(frame, [1160, 1230], [0, (score / 13) * 170], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
                  return <div key={i} style={{ width: 22, height: h, borderRadius: 4, background: COLORS.open, opacity: 0.7 }} />;
                })}
              </div>
              <div style={{ fontFamily: SANS, fontSize: 24, color: COLORS.textDim }}>random theories — <b style={{ color: COLORS.open }}>≤ 5 / 13</b></div>
            </div>
            {/* TFPT */}
            <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 10 }}>
              <div style={{ width: 64, height: interpolate(frame, [1180, 1260], [0, 170], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }), borderRadius: 6, background: COLORS.exact, boxShadow: `0 0 40px -10px ${COLORS.exact}` }} />
              <div style={{ fontFamily: SANS, fontSize: 24, color: COLORS.textBright }}>TFPT — <b style={{ color: COLORS.exact }}>13 / 13</b></div>
            </div>
          </div>
          <div style={{ ...pop(frame, fps, 1320), fontFamily: SERIF, fontSize: 40, color: COLORS.textBright }}>
            by luck? <b style={{ color: COLORS.exact }}>below 1 in 10³⁰</b> — effectively zero.
          </div>
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
