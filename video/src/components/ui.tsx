import React from "react";
import { SANS, SERIF, MONO } from "../fonts";
import { COLORS, gradientText } from "../theme";

/** A small uppercase eyebrow / section label. */
export const Eyebrow: React.FC<{
  children: React.ReactNode;
  color?: string;
  style?: React.CSSProperties;
}> = ({ children, color = COLORS.blueLight, style }) => (
  <div
    style={{
      fontFamily: MONO,
      fontSize: 24,
      fontWeight: 600,
      letterSpacing: 6,
      textTransform: "uppercase",
      color,
      display: "inline-flex",
      alignItems: "center",
      gap: 14,
      padding: "10px 22px",
      borderRadius: 999,
      border: `1px solid ${color}3a`,
      background: `${color}14`,
      ...style,
    }}
  >
    {children}
  </div>
);

export const Headline: React.FC<{
  children: React.ReactNode;
  size?: number;
  gradient?: boolean;
  style?: React.CSSProperties;
}> = ({ children, size = 86, gradient = false, style }) => (
  <h1
    style={{
      fontFamily: SERIF,
      fontWeight: 600,
      fontSize: size,
      lineHeight: 1.05,
      letterSpacing: -1.5,
      margin: 0,
      color: COLORS.textBright,
      textAlign: "center",
      ...(gradient ? gradientText() : {}),
      ...style,
    }}
  >
    {children}
  </h1>
);

export const Chip: React.FC<{
  children: React.ReactNode;
  color?: string;
  size?: number;
  style?: React.CSSProperties;
}> = ({ children, color = COLORS.textDim, size = 30, style }) => (
  <span
    style={{
      fontFamily: SANS,
      fontSize: size,
      fontWeight: 600,
      color,
      padding: `${size * 0.42}px ${size * 0.7}px`,
      borderRadius: 14,
      background: "rgba(15,23,42,0.6)",
      border: `1px solid ${COLORS.border}`,
      whiteSpace: "nowrap",
      ...style,
    }}
  >
    {children}
  </span>
);

export const Card: React.FC<{
  children: React.ReactNode;
  accent?: string;
  style?: React.CSSProperties;
}> = ({ children, accent = COLORS.border, style }) => (
  <div
    style={{
      background: "rgba(10,16,30,0.62)",
      border: `1px solid ${accent}`,
      borderRadius: 22,
      padding: 34,
      backdropFilter: "blur(8px)",
      ...style,
    }}
  >
    {children}
  </div>
);

/** The TFPT wordmark used in the corner and on the end card. */
export const BrandMark: React.FC<{ size?: number; style?: React.CSSProperties }> = ({
  size = 30,
  style,
}) => (
  <div
    style={{
      display: "inline-flex",
      alignItems: "center",
      gap: size * 0.5,
      fontFamily: MONO,
      fontWeight: 700,
      fontSize: size,
      letterSpacing: 3,
      color: COLORS.textBright,
      ...style,
    }}
  >
    <span
      style={{
        width: size * 0.9,
        height: size * 0.9,
        borderRadius: 8,
        background: "linear-gradient(135deg,#60a5fa,#a78bfa 55%,#f472b6)",
        boxShadow: "0 0 22px -4px rgba(96,165,250,0.7)",
        display: "inline-block",
      }}
    />
    <span>TFPT</span>
  </div>
);
