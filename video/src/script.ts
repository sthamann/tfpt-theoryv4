export const FPS = 30;
export const WIDTH = 1920;
export const HEIGHT = 1080;

const sec = (s: number) => Math.round(s * FPS);

/**
 * The 9-beat "Is reality compiled?" timeline. `start`/`durationInFrames` are
 * absolute on the master track; the caption cues in captions.json are authored
 * against the same seconds, so the burned-in subtitle and the exported .vtt
 * never drift.
 */
export const SCENES = [
  { id: "question", start: sec(0), durationInFrames: sec(20) },
  { id: "result", start: sec(20), durationInFrames: sec(45) },
  { id: "input", start: sec(65), durationInFrames: sec(30) },
  { id: "proof", start: sec(95), durationInFrames: sec(40) },
  { id: "fixed-point", start: sec(135), durationInFrames: sec(30) },
  { id: "beauty", start: sec(165), durationInFrames: sec(30) },
  { id: "numerology", start: sec(195), durationInFrames: sec(50) },
  { id: "open", start: sec(245), durationInFrames: sec(20) },
  { id: "resolution", start: sec(265), durationInFrames: sec(20) },
] as const;

export const TOTAL_FRAMES = sec(285);

export type Caption = { from: number; to: number; text: string };
