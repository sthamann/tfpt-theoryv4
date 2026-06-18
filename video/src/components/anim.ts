import { Easing, interpolate } from "remotion";

const EASE_OUT = Easing.bezier(0.16, 1, 0.3, 1);

/** Fade + rise on enter; optional fade on exit near the end of a window. */
export const enterUp = (
  frame: number,
  start: number,
  dur = 22,
  rise = 26,
): { opacity: number; transform: string } => {
  const t = interpolate(frame, [start, start + dur], [0, 1], {
    easing: EASE_OUT,
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  return { opacity: t, transform: `translateY(${(1 - t) * rise}px)` };
};

/** Simple clamped fade between two frames. */
export const fade = (
  frame: number,
  start: number,
  end: number,
  from = 0,
  to = 1,
): number =>
  interpolate(frame, [start, end], [from, to], {
    easing: EASE_OUT,
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

/** A hold-then-fadeout opacity for elements that should leave before a cut. */
export const fadeInOut = (
  frame: number,
  inStart: number,
  inEnd: number,
  outStart: number,
  outEnd: number,
): number => {
  const i = fade(frame, inStart, inEnd, 0, 1);
  const o = fade(frame, outStart, outEnd, 0, 1);
  return Math.max(0, i - o);
};

export { EASE_OUT };
