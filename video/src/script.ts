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
  { id: "machine", start: sec(15), durationInFrames: sec(43) },
  { id: "readout", start: sec(58), durationInFrames: sec(44) },
  { id: "clocks", start: sec(102), durationInFrames: sec(32) },
  { id: "gravity", start: sec(134), durationInFrames: sec(26) },
  { id: "safeguards", start: sec(160), durationInFrames: sec(44) },
  { id: "kill", start: sec(204), durationInFrames: sec(40) },
  { id: "residual", start: sec(244), durationInFrames: sec(32) },
] as const;

export const TOTAL_FRAMES = sec(276);

export type Caption = { from: number; to: number; text: string };
