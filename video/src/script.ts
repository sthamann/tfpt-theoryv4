export const FPS = 30;
export const WIDTH = 1920;
export const HEIGHT = 1080;

const sec = (s: number) => Math.round(s * FPS);

/**
 * The 7-beat timeline. `start`/`durationInFrames` are absolute on the master
 * track; the caption cues in captions.json are authored against the same
 * seconds, so the burned-in subtitle and the exported .vtt never drift.
 */
export const SCENES = [
  { id: "cold-open", start: sec(0), durationInFrames: sec(15) },
  { id: "machine", start: sec(15), durationInFrames: sec(41) },
  { id: "readout", start: sec(56), durationInFrames: sec(41) },
  { id: "texture", start: sec(97), durationInFrames: sec(26) },
  { id: "kill", start: sec(123), durationInFrames: sec(31) },
  { id: "audit", start: sec(154), durationInFrames: sec(19) },
  { id: "open-knot", start: sec(173), durationInFrames: sec(25) },
] as const;

export const TOTAL_FRAMES = sec(198);

export type Caption = { from: number; to: number; text: string };
