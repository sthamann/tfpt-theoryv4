import { ImageResponse } from "next/og";

export const runtime = "edge";
export const alt =
  "TFPT in One Map — Orientation Note (Paper 0). The public entry document of the TFPT 4.5 paper series.";
export const size = { width: 1200, height: 630 };
export const contentType = "image/png";

export default function OrientationOgImage() {
  return new ImageResponse(
    (
      <div
        style={{
          width: "100%",
          height: "100%",
          display: "flex",
          flexDirection: "column",
          background:
            "radial-gradient(ellipse at 18% 0%, rgba(59,130,246,0.5), transparent 55%), radial-gradient(ellipse at 82% 100%, rgba(168,85,247,0.35), transparent 55%), #060912",
          color: "#e2e8f0",
          fontFamily: "Inter, sans-serif",
          padding: 72,
          position: "relative",
        }}
      >
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: 16,
          }}
        >
          <div
            style={{
              width: 64,
              height: 64,
              borderRadius: 16,
              background:
                "linear-gradient(135deg, #1d4ed8 0%, #6366f1 40%, #a855f7 80%, #ec4899 100%)",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              boxShadow: "0 12px 40px -8px rgba(99,102,241,0.5)",
            }}
          >
            <svg width="48" height="48" viewBox="0 0 64 64">
              <path
                d="M 14 32 A 18 18 0 0 1 50 32"
                stroke="#ffffff"
                strokeOpacity="0.55"
                strokeWidth="1.5"
                fill="none"
                strokeLinecap="round"
              />
              <path
                d="M 14 32 A 18 18 0 0 0 50 32"
                stroke="#ffffff"
                strokeOpacity="0.4"
                strokeWidth="1.2"
                fill="none"
                strokeLinecap="round"
                strokeDasharray="2 3"
              />
              <line
                x1="11"
                y1="32"
                x2="53"
                y2="32"
                stroke="#ffffff"
                strokeOpacity="0.55"
                strokeWidth="1"
              />
              <circle cx="22" cy="22" r="2" fill="#ffffff" />
              <circle cx="32" cy="19" r="2" fill="#ffffff" />
              <circle cx="42" cy="22" r="2" fill="#ffffff" />
              <circle cx="26" cy="45" r="2" fill="#ffffff" />
              <circle cx="38" cy="45" r="2" fill="#ffffff" />
              <circle cx="32" cy="32" r="3" fill="#ffffff" />
            </svg>
          </div>
          <div style={{ display: "flex", flexDirection: "column" }}>
            <div
              style={{
                fontFamily: "serif",
                fontSize: 28,
                fontWeight: 700,
                color: "#f1f5f9",
              }}
            >
              TFPT
            </div>
            <div
              style={{
                fontSize: 12,
                color: "#94a3b8",
                letterSpacing: 4,
                textTransform: "uppercase",
                marginTop: 2,
              }}
            >
              Orientation note · Paper 0
            </div>
          </div>
        </div>

        <div
          style={{
            display: "flex",
            flexDirection: "column",
            marginTop: "auto",
          }}
        >
          <div
            style={{
              display: "flex",
              fontFamily: "serif",
              fontSize: 96,
              fontWeight: 600,
              color: "#f8fafc",
              lineHeight: 1.0,
              letterSpacing: -2.5,
            }}
          >
            TFPT in
          </div>
          <div
            style={{
              display: "flex",
              fontFamily: "serif",
              fontSize: 96,
              fontWeight: 600,
              color: "#f8fafc",
              lineHeight: 1.0,
              letterSpacing: -2.5,
              marginTop: 8,
            }}
          >
            <span
              style={{
                display: "flex",
                background:
                  "linear-gradient(90deg, #60a5fa, #a78bfa, #f472b6)",
                backgroundClip: "text",
                color: "transparent",
              }}
            >
              one map.
            </span>
          </div>
          <div
            style={{
              fontSize: 26,
              color: "#cbd5e1",
              marginTop: 22,
              lineHeight: 1.45,
              maxWidth: 960,
              display: "flex",
            }}
          >
            Boundary polarization, carrier rigidity, and observable closure — what TFPT claims, what it doesn't, and the dependency map between Papers 1 to 6.
          </div>
          <div
            style={{
              display: "flex",
              alignItems: "center",
              gap: 18,
              color: "#64748b",
              fontSize: 18,
              marginTop: 22,
            }}
          >
            <span style={{ display: "flex" }}>Stefan Hamann</span>
            <span
              style={{
                width: 4,
                height: 4,
                borderRadius: 2,
                background: "#475569",
              }}
            />
            <span style={{ display: "flex" }}>Alessandro Rizzo</span>
          </div>
        </div>
      </div>
    ),
    {
      ...size,
    },
  );
}
