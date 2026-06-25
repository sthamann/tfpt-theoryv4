export const FPS = 30;
export const WIDTH = 1920;
export const HEIGHT = 1080;

const sec = (s: number) => Math.round(s * FPS);

/**
 * The 8-beat timeline. `start`/`durationInFrames` are absolute on the master
 * track; the caption cues in captions.json are authored against the same
 * seconds, so the burned-in subtitle and the exported .vtt never drift.
 */
export const SCENES = [
  { id: "cold-open", start: sec(0), durationInFrames: sec(15) },
  { id: "machine", start: sec(15), durationInFrames: sec(40) },
  { id: "readout", start: sec(55), durationInFrames: sec(40) },
  { id: "texture", start: sec(95), durationInFrames: sec(25) },
  { id: "gravity", start: sec(120), durationInFrames: sec(26) },
  { id: "safeguards", start: sec(146), durationInFrames: sec(43) },
  { id: "kill", start: sec(189), durationInFrames: sec(30) },
  { id: "residual", start: sec(219), durationInFrames: sec(31) },
] as const;

export const TOTAL_FRAMES = sec(250);

export type Caption = { from: number; to: number; text: string };
