import React from "react";
import { interpolate, spring, useCurrentFrame, useVideoConfig, Easing } from "remotion";
import { COLORS } from "../theme";

/* ----------------------------------------------------------------------------
 * Motion primitives — spring physics + a few self-animating SVG components.
 * Everything is deterministic in `frame`, so it renders identically every time.
 * ------------------------------------------------------------------------- */

type SpringCfg = { damping?: number; mass?: number; stiffness?: number };

/** A 0→1 spring that starts at `delay` frames (clamped, never runs early). */
export const springIn = (
  frame: number,
  fps: number,
  delay = 0,
  config: SpringCfg = { damping: 18, mass: 0.9, stiffness: 120 },
): number => spring({ frame: Math.max(0, frame - delay), fps, config });

/** Pop-in: opacity + rise + subtle scale, driven by a spring. */
export const pop = (
  frame: number,
  fps: number,
  delay = 0,
  opts: { y?: number; from?: number; config?: SpringCfg } = {},
): React.CSSProperties => {
  const { y = 26, from = 0.92, config } = opts;
  const s = springIn(frame, fps, delay, config);
  return {
    opacity: Math.min(1, s * 1.1),
    transform: `translateY(${(1 - s) * y}px) scale(${from + (1 - from) * s})`,
  };
};

/** A bouncy scale-in for badges / hero numbers. */
export const popScale = (frame: number, fps: number, delay = 0): React.CSSProperties => {
  const s = springIn(frame, fps, delay, { damping: 11, mass: 0.8, stiffness: 130 });
  return { opacity: Math.min(1, s * 1.2), transform: `scale(${0.6 + 0.4 * s})` };
};

/** Count a number up from `from`→`to` over [start,end] frames. */
export const CountUp: React.FC<{
  to: number;
  from?: number;
  start: number;
  end: number;
  decimals?: number;
  style?: React.CSSProperties;
  suffix?: string;
}> = ({ to, from = 0, start, end, decimals = 0, style, suffix = "" }) => {
  const frame = useCurrentFrame();
  const v = interpolate(frame, [start, end], [from, to], {
    easing: Easing.out(Easing.cubic),
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  return <span style={style}>{v.toFixed(decimals)}{suffix}</span>;
};

/** A path that draws itself in over [start,end] (stroke-dashoffset). */
export const DrawnPath: React.FC<{
  d: string;
  start: number;
  end: number;
  length?: number;
  stroke?: string;
  width?: number;
  opacity?: number;
  glow?: boolean;
}> = ({ d, start, end, length = 4000, stroke = COLORS.blueLight, width = 3, opacity = 1, glow = true }) => {
  const frame = useCurrentFrame();
  const o = interpolate(frame, [start, end], [length, 0], {
    easing: Easing.bezier(0.16, 1, 0.3, 1),
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  return (
    <path
      d={d}
      fill="none"
      stroke={stroke}
      strokeWidth={width}
      strokeLinecap="round"
      strokeDasharray={length}
      strokeDashoffset={o}
      opacity={opacity}
      style={glow ? { filter: `drop-shadow(0 0 6px ${stroke})` } : undefined}
    />
  );
};

/* ----------------------------------------------------------------------------
 * E8Petrie — the iconic 240-root Petrie projection: 8 concentric rings of 30.
 * Vertices fly out from the centre (spring + stagger), the star chords draw,
 * and the whole figure rotates slowly. `progress` (0→1) controls assembly.
 * ------------------------------------------------------------------------- */

const RING_RADII = [0.2, 0.31, 0.42, 0.53, 0.64, 0.75, 0.87, 1.0];
const RING_COLORS = [
  COLORS.blueLight,
  "#7cc4ff",
  COLORS.blue,
  COLORS.violet,
  "#b794ff",
  COLORS.pink,
  "#f0a6cf",
  COLORS.exact,
];

export const E8Petrie: React.FC<{
  size: number;
  progress: number;
  rotateSpeed?: number;
  showChords?: boolean;
  opacity?: number;
}> = ({ size, progress, rotateSpeed = 0.12, showChords = true, opacity = 1 }) => {
  const frame = useCurrentFrame();
  const R = size / 2;
  const cx = R;
  const cy = R;
  const rot = frame * rotateSpeed;
  const N = 30;

  const rings = RING_RADII.map((rr, k) => {
    const radius = rr * R * 0.92;
    const offset = k * 6; // degrees, gives the swirl
    const pts = Array.from({ length: N }, (_, i) => {
      const a = ((i * 360) / N + offset) * (Math.PI / 180);
      // staggered fly-out: each vertex eases out to its radius
      const idx = k * N + i;
      const local = interpolate(progress, [0, 1], [0, 1]);
      const start = (idx / (8 * N)) * 0.55;
      const vp = interpolate(local, [start, start + 0.4], [0, 1], {
        easing: Easing.out(Easing.cubic),
        extrapolateLeft: "clamp",
        extrapolateRight: "clamp",
      });
      const rad = radius * vp;
      return { x: cx + rad * Math.cos(a), y: cy + rad * Math.sin(a), vp };
    });
    return { pts, color: RING_COLORS[k] };
  });

  const chordOpacity = interpolate(progress, [0.55, 0.95], [0, 0.5], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <svg
      width={size}
      height={size}
      viewBox={`0 0 ${size} ${size}`}
      style={{ opacity, transform: `rotate(${rot}deg)`, overflow: "visible" }}
    >
      {/* star-polygon chords per ring (skip 11 → the dense E8 look) */}
      {showChords &&
        rings.map((ring, k) =>
          ring.pts.map((p, i) => {
            const q = ring.pts[(i + 11) % N];
            if (p.vp < 0.6 || q.vp < 0.6) return null;
            return (
              <line
                key={`c${k}-${i}`}
                x1={p.x}
                y1={p.y}
                x2={q.x}
                y2={q.y}
                stroke={ring.color}
                strokeWidth={1}
                opacity={chordOpacity}
              />
            );
          }),
        )}
      {/* vertices */}
      {rings.map((ring, k) =>
        ring.pts.map((p, i) => (
          <circle
            key={`v${k}-${i}`}
            cx={p.x}
            cy={p.y}
            r={interpolate(p.vp, [0, 1], [0, k < 4 ? 3.2 : 4]) }
            fill={ring.color}
            opacity={p.vp}
            style={{ filter: `drop-shadow(0 0 5px ${ring.color})` }}
          />
        )),
      )}
    </svg>
  );
};

/* ----------------------------------------------------------------------------
 * LoopArc — a circular arrow that draws itself; used for the fixed-point loop.
 * ------------------------------------------------------------------------- */

export const LoopArc: React.FC<{
  size: number;
  progress: number; // 0→1 draw
  stroke?: string;
  width?: number;
}> = ({ size, progress, stroke = COLORS.exact, width = 6 }) => {
  const R = size / 2;
  const r = R - width * 2;
  const cx = R;
  const cy = R;
  // near-full circle, leaving a gap for the arrowhead
  const startA = -90;
  const sweep = 312 * Math.min(1, Math.max(0, progress));
  const endA = startA + sweep;
  const rad = (d: number) => (d * Math.PI) / 180;
  const x1 = cx + r * Math.cos(rad(startA));
  const y1 = cy + r * Math.sin(rad(startA));
  const x2 = cx + r * Math.cos(rad(endA));
  const y2 = cy + r * Math.sin(rad(endA));
  const large = sweep > 180 ? 1 : 0;
  const d = `M ${x1} ${y1} A ${r} ${r} 0 ${large} 1 ${x2} ${y2}`;
  // arrowhead at the leading end
  const ah = 14;
  const tA = rad(endA);
  const tx = cx + r * Math.cos(tA);
  const ty = cy + r * Math.sin(tA);
  const dir = tA + Math.PI / 2; // tangent
  const headOpacity = progress > 0.12 ? 1 : 0;

  return (
    <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`} style={{ overflow: "visible" }}>
      <path d={d} fill="none" stroke={stroke} strokeWidth={width} strokeLinecap="round" style={{ filter: `drop-shadow(0 0 10px ${stroke})` }} />
      <polygon
        points={`${tx + ah * Math.cos(dir)},${ty + ah * Math.sin(dir)} ${tx + ah * Math.cos(dir + 2.4)},${ty + ah * Math.sin(dir + 2.4)} ${tx + ah * Math.cos(dir - 2.4)},${ty + ah * Math.sin(dir - 2.4)}`}
        fill={stroke}
        opacity={headOpacity}
        style={{ filter: `drop-shadow(0 0 8px ${stroke})` }}
      />
    </svg>
  );
};

/** A reusable hook to grab fps without importing everywhere. */
export const useFps = (): number => useVideoConfig().fps;
