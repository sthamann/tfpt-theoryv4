import React from "react";
import { AbsoluteFill, useCurrentFrame, interpolate, Easing } from "remotion";
import { Bg } from "../components/Bg";
import { Eyebrow, BrandMark } from "../components/ui";
import { Formula, Tok } from "../components/Formula";
import { SANS, SERIF, MONO } from "../fonts";
import { COLORS } from "../theme";
import { enterUp, fade, fadeInOut } from "../components/anim";

const FEEDS = ["metric inclusion G_net", "carrier P2", "boundary QFT", "Dirac · cutoff · glue"];

export const Scene07OpenKnot: React.FC = () => {
  const frame = useCurrentFrame();

  const knot = fadeInOut(frame, 20, 60, 520, 600);
  const eyebrow = enterUp(frame, 6, 22);
  const statement = enterUp(frame, 210, 28);
  const tag = enterUp(frame, 310, 24);
  const flat = enterUp(frame, 390, 24);

  // feeds collapse: fade out after appearing
  const feedsCollapse = interpolate(frame, [170, 220], [1, 0.18], {
    easing: Easing.in(Easing.cubic),
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  const end = fade(frame, 545, 620);
  const endRise = enterUp(frame, 545, 34);

  return (
    <AbsoluteFill>
      <Bg accent={COLORS.conditional} tint="#a78bfa" />

      {/* knot layer */}
      <AbsoluteFill style={{ flexDirection: "column", alignItems: "center", paddingTop: 90, gap: 30, opacity: knot }}>
        <div style={eyebrow}>
          <Eyebrow color={COLORS.conditional}>The one open knot</Eyebrow>
        </div>

        <div style={{ display: "flex", alignItems: "center", gap: 30, marginTop: 16, opacity: feedsCollapse }}>
          <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
            {FEEDS.map((f, i) => (
              <div
                key={f}
                style={{
                  ...enterUp(frame, 60 + i * 16, 18, 14),
                  fontFamily: MONO,
                  fontSize: 24,
                  color: COLORS.textDim,
                  padding: "10px 18px",
                  borderRadius: 12,
                  background: "rgba(10,16,30,0.6)",
                  border: `1px solid ${COLORS.border}`,
                }}
              >
                {f}
              </div>
            ))}
          </div>
          <div style={{ fontFamily: MONO, fontSize: 60, color: COLORS.conditional }}>→</div>
          <div style={{ fontFamily: SANS, fontSize: 26, color: COLORS.textDim, maxWidth: 220 }}>
            collapse to <b style={{ color: COLORS.textBright }}>one</b> condition
          </div>
        </div>

        <div style={{ ...statement, marginTop: 14 }}>
          <Formula size={46}>
            <Tok color={COLORS.open}>raw RP seam</Tok> ⇒{" "}
            <Tok color={COLORS.exact}>(E₈)₁ net</Tok> <Tok color={COLORS.textBright}>at τ = i</Tok>
          </Formula>
        </div>

        <div style={{ ...tag, display: "flex", alignItems: "center", gap: 18 }}>
          <span
            style={{
              fontFamily: MONO,
              fontSize: 24,
              fontWeight: 700,
              letterSpacing: 2,
              color: COLORS.conditional,
              padding: "8px 18px",
              borderRadius: 999,
              border: `1px solid ${COLORS.conditional}66`,
              background: COLORS.conditionalBg,
            }}
          >
            SEAM.EQUIV.01
          </span>
          <span style={{ fontFamily: SANS, fontSize: 30, color: COLORS.textDim }}>
            both proof routes meet here
          </span>
        </div>

        <div
          style={{
            ...flat,
            fontFamily: SERIF,
            fontSize: 40,
            color: COLORS.text,
            textAlign: "center",
            maxWidth: 1240,
            marginTop: 6,
          }}
        >
          The sharpest remaining link has a name —{" "}
          <b style={{ color: COLORS.textBright }}>Flat-Away</b>. Close it, and the structural core is done.
        </div>
      </AbsoluteFill>

      {/* end card */}
      <AbsoluteFill
        style={{
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center",
          gap: 30,
          opacity: end * endRise.opacity,
          transform: endRise.transform,
        }}
      >
        <BrandMark size={72} />
        <div
          style={{
            fontFamily: SERIF,
            fontSize: 64,
            fontWeight: 600,
            color: COLORS.textBright,
            textAlign: "center",
            letterSpacing: -1,
          }}
        >
          Two axioms. One compiler.
          <br />
          One open theorem.
        </div>
        <div style={{ fontFamily: SANS, fontSize: 32, color: COLORS.textDim }}>
          ledger-typed · reproducible · falsifiable
        </div>
        <div
          style={{
            fontFamily: MONO,
            fontSize: 34,
            fontWeight: 600,
            ...{
              backgroundImage: "linear-gradient(135deg,#60a5fa,#a78bfa 55%,#f472b6)",
              WebkitBackgroundClip: "text",
              backgroundClip: "text",
              WebkitTextFillColor: "transparent",
            },
            marginTop: 8,
          }}
        >
          fixpoint-theory.com
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
