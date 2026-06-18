import React from "react";
import { AbsoluteFill, Sequence, useCurrentFrame, useVideoConfig, interpolate } from "remotion";
import { SCENES } from "./script";
import { COLORS } from "./theme";
import { BrandMark } from "./components/ui";
import { Subtitle } from "./components/Subtitle";
import { Scene01ColdOpen } from "./scenes/Scene01ColdOpen";
import { Scene02Machine } from "./scenes/Scene02Machine";
import { Scene03Readout } from "./scenes/Scene03Readout";
import { Scene04Texture } from "./scenes/Scene04Texture";
import { Scene05Kill } from "./scenes/Scene05Kill";
import { Scene06Audit } from "./scenes/Scene06Audit";
import { Scene07OpenKnot } from "./scenes/Scene07OpenKnot";

const SCENE_COMPONENTS: Record<string, React.FC> = {
  "cold-open": Scene01ColdOpen,
  machine: Scene02Machine,
  readout: Scene03Readout,
  texture: Scene04Texture,
  kill: Scene05Kill,
  audit: Scene06Audit,
  "open-knot": Scene07OpenKnot,
};

const ProgressBar: React.FC = () => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();
  const w = interpolate(frame, [0, durationInFrames - 1], [0, 100], {
    extrapolateRight: "clamp",
  });
  return (
    <div style={{ position: "absolute", top: 0, left: 0, right: 0, height: 5, background: "rgba(148,163,184,0.12)" }}>
      <div
        style={{
          height: "100%",
          width: `${w}%`,
          background: "linear-gradient(90deg,#60a5fa,#a78bfa 55%,#f472b6)",
        }}
      />
    </div>
  );
};

export const TfptIntro: React.FC = () => {
  return (
    <AbsoluteFill style={{ backgroundColor: COLORS.bg }}>
      {SCENES.map((s) => {
        const Comp = SCENE_COMPONENTS[s.id];
        return (
          <Sequence key={s.id} from={s.start} durationInFrames={s.durationInFrames} name={s.id}>
            <Comp />
          </Sequence>
        );
      })}

      {/* persistent chrome */}
      <Subtitle />
      <div style={{ position: "absolute", top: 36, left: 48, opacity: 0.85 }}>
        <BrandMark size={26} />
      </div>
      <ProgressBar />
    </AbsoluteFill>
  );
};
