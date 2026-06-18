import React from "react";
import { MONO } from "../fonts";
import { STATUS_META, StatusGrade } from "../theme";

/** A ledger-style status badge: [E] exact · [C] conditional · [O] open. */
export const StatusChip: React.FC<{
  grade: StatusGrade;
  size?: number;
  showLabel?: boolean;
}> = ({ grade, size = 26, showLabel = true }) => {
  const m = STATUS_META[grade];
  return (
    <span
      style={{
        display: "inline-flex",
        alignItems: "center",
        gap: 10,
        padding: `${size * 0.28}px ${size * 0.55}px`,
        borderRadius: 999,
        background: m.bg,
        border: `1px solid ${m.color}55`,
        color: m.color,
        fontFamily: MONO,
        fontWeight: 700,
        fontSize: size,
        lineHeight: 1,
        whiteSpace: "nowrap",
      }}
    >
      <span>[{grade}]</span>
      {showLabel && (
        <span style={{ fontWeight: 500, letterSpacing: 0.4 }}>{m.label}</span>
      )}
    </span>
  );
};
