import React from "react";
import { AbsoluteFill, Sequence, useCurrentFrame, useVideoConfig, interpolate } from "remotion";
import { SCENES } from "./script";
import { COLORS } from "./theme";
import { BrandMark } from "./components/ui";
import { Subtitle } from "./components/Subtitle";
import { Scene01Question } from "./scenes/Scene01Question";
import { Scene02Result } from "./scenes/Scene02Result";
import { Scene03Input } from "./scenes/Scene03Input";
import { Scene04Proof } from "./scenes/Scene04Proof";
import { Scene05FixedPoint } from "./scenes/Scene05FixedPoint";
import { Scene06Beauty } from "./scenes/Scene06Beauty";
import { Scene07Numerology } from "./scenes/Scene07Numerology";
import { Scene08Open } from "./scenes/Scene08Open";
import { Scene09Resolution } from "./scenes/Scene09Resolution";

const SCENE_COMPONENTS: Record<string, React.FC> = {
  question: Scene01Question,
  result: Scene02Result,
  input: Scene03Input,
  proof: Scene04Proof,
  "fixed-point": Scene05FixedPoint,
  beauty: Scene06Beauty,
  numerology: Scene07Numerology,
  open: Scene08Open,
  resolution: Scene09Resolution,
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
