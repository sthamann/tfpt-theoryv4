"use client";

import { cn } from "@/lib/utils";

interface LogoProps {
  size?: number;
  className?: string;
  animated?: boolean;
  showWordmark?: boolean;
  ariaLabel?: string;
}

export function LogoMark({
  size = 40,
  className,
  animated = true,
  ariaLabel = "TFPT logo",
}: LogoProps) {
  const id = "tfpt";
  return (
    <svg
      viewBox="0 0 64 64"
      width={size}
      height={size}
      className={cn(
        "logo-mark relative shrink-0",
        animated && "logo-animated",
        className,
      )}
      role="img"
      aria-label={ariaLabel}
      xmlns="http://www.w3.org/2000/svg"
    >
      <defs>
        <linearGradient
          id={`${id}-grad`}
          x1="0%"
          y1="0%"
          x2="100%"
          y2="100%"
          gradientUnits="objectBoundingBox"
        >
          <stop offset="0%" stopColor="#1d4ed8" />
          <stop offset="40%" stopColor="#6366f1" />
          <stop offset="80%" stopColor="#a855f7" />
          <stop offset="100%" stopColor="#ec4899" />
        </linearGradient>
        <radialGradient id={`${id}-glow`} cx="50%" cy="50%" r="55%">
          <stop offset="0%" stopColor="#ffffff" stopOpacity="0.95" />
          <stop offset="55%" stopColor="#ffffff" stopOpacity="0.18" />
          <stop offset="100%" stopColor="#ffffff" stopOpacity="0" />
        </radialGradient>
        <linearGradient id={`${id}-edge`} x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stopColor="#ffffff" stopOpacity="0.55" />
          <stop offset="100%" stopColor="#ffffff" stopOpacity="0" />
        </linearGradient>
      </defs>

      <rect
        x="0.5"
        y="0.5"
        width="63"
        height="63"
        rx="14.5"
        fill={`url(#${id}-grad)`}
      />
      <rect
        x="0.5"
        y="0.5"
        width="63"
        height="63"
        rx="14.5"
        fill="none"
        stroke={`url(#${id}-edge)`}
        strokeWidth="1"
      />

      <g className="logo-glow">
        <circle cx="32" cy="32" r="14" fill={`url(#${id}-glow)`} />
      </g>

      <g className="logo-arcs" stroke="#ffffff" fill="none" strokeLinecap="round">
        <path
          d="M 14 32 A 18 18 0 0 1 50 32"
          strokeWidth="1.4"
          strokeOpacity="0.55"
        />
        <path
          d="M 14 32 A 18 18 0 0 0 50 32"
          strokeWidth="1.2"
          strokeOpacity="0.4"
          strokeDasharray="2 3"
        />
      </g>

      <line
        x1="11"
        y1="32"
        x2="53"
        y2="32"
        stroke="#ffffff"
        strokeOpacity="0.55"
        strokeWidth="1"
        strokeLinecap="round"
      />

      <g className="logo-dots-top" fill="#ffffff">
        <circle cx="22" cy="22" r="2" opacity="0.95" />
        <circle cx="32" cy="19" r="2" opacity="0.95" />
        <circle cx="42" cy="22" r="2" opacity="0.95" />
      </g>

      <g className="logo-dots-bottom" fill="#ffffff">
        <circle cx="26" cy="45" r="2" opacity="0.95" />
        <circle cx="38" cy="45" r="2" opacity="0.95" />
      </g>

      <g className="logo-fixedpoint">
        <circle cx="32" cy="32" r="3" fill="#ffffff" />
        <circle
          className="logo-ring"
          cx="32"
          cy="32"
          r="6"
          fill="none"
          stroke="#ffffff"
          strokeWidth="0.8"
          strokeOpacity="0.5"
        />
      </g>
    </svg>
  );
}

export function Logo({
  size = 40,
  className,
  animated = true,
  showWordmark = true,
}: LogoProps) {
  return (
    <span className={cn("inline-flex items-center gap-2.5", className)}>
      <LogoMark size={size} animated={animated} />
      {showWordmark && (
        <span className="leading-tight">
          <span className="block font-serif text-base font-semibold tracking-tight text-slate-100">
            TFPT
          </span>
          <span className="hidden text-[10px] uppercase tracking-[0.18em] text-slate-400 sm:block">
            Fixed-Point Theory
          </span>
        </span>
      )}
    </span>
  );
}
