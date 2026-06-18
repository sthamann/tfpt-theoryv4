import React from "react";
import { MONO } from "../fonts";
import { COLORS } from "../theme";

/**
 * A monospace formula plate. Math is written with Unicode (subscripts,
 * superscripts, ⊕ ⇒ π φ τ) rather than a TeX engine — crisp, animatable and
 * dependency-light, while staying on-brand with the site's mono formulas.
 */
export const Formula: React.FC<{
  children: React.ReactNode;
  size?: number;
  plate?: boolean;
  color?: string;
  style?: React.CSSProperties;
}> = ({ children, size = 56, plate = true, color = COLORS.textBright, style }) => {
  return (
    <div
      style={{
        fontFamily: MONO,
        fontSize: size,
        fontWeight: 500,
        color,
        letterSpacing: 0.5,
        lineHeight: 1.25,
        display: "inline-flex",
        alignItems: "center",
        gap: size * 0.28,
        padding: plate ? `${size * 0.42}px ${size * 0.72}px` : 0,
        borderRadius: plate ? 18 : 0,
        background: plate ? "rgba(2,6,18,0.55)" : "transparent",
        border: plate ? `1px solid ${COLORS.border}` : "none",
        backdropFilter: plate ? "blur(6px)" : undefined,
        ...style,
      }}
    >
      {children}
    </div>
  );
};

/** A coloured token inside a formula (e.g. an input or a result). */
export const Tok: React.FC<{
  children: React.ReactNode;
  color?: string;
  bold?: boolean;
}> = ({ children, color = COLORS.blueLight, bold = true }) => (
  <span style={{ color, fontWeight: bold ? 700 : 500 }}>{children}</span>
);
