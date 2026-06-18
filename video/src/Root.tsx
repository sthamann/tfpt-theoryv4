import "./index.css";
import { Composition, Still } from "remotion";
import { TfptIntro } from "./TfptIntro";
import { Poster } from "./Poster";
import { FPS, WIDTH, HEIGHT, TOTAL_FRAMES } from "./script";

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="TfptIntro"
        component={TfptIntro}
        durationInFrames={TOTAL_FRAMES}
        fps={FPS}
        width={WIDTH}
        height={HEIGHT}
      />
      <Still id="Poster" component={Poster} width={WIDTH} height={HEIGHT} />
    </>
  );
};
