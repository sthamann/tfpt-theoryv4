import { ImageResponse } from "next/og";

export const runtime = "edge";
export const alt =
  "TFPT — Topological Fixed-Point Theory: Boundary polarization, carrier rigidity, and observable closure.";
export const size = { width: 1200, height: 630 };
export const contentType = "image/png";

export default function OpengraphImage() {
  return new ImageResponse(
    (
      <div
        style={{
          width: "100%",
          height: "100%",
          display: "flex",
          flexDirection: "column",
          background:
            "radial-gradient(ellipse at 18% 0%, rgba(99,102,241,0.55), transparent 55%), radial-gradient(ellipse at 82% 100%, rgba(236,72,153,0.35), transparent 55%), #060912",
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
              width: 72,
              height: 72,
              borderRadius: 18,
              background:
                "linear-gradient(135deg, #1d4ed8 0%, #6366f1 40%, #a855f7 80%, #ec4899 100%)",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              position: "relative",
              boxShadow: "0 12px 40px -8px rgba(99,102,241,0.5)",
            }}
          >
            <svg width="56" height="56" viewBox="0 0 64 64">
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
              <circle cx="22" cy="22" r="2.2" fill="#ffffff" />
              <circle cx="32" cy="19" r="2.2" fill="#ffffff" />
              <circle cx="42" cy="22" r="2.2" fill="#ffffff" />
              <circle cx="26" cy="45" r="2.2" fill="#ffffff" />
              <circle cx="38" cy="45" r="2.2" fill="#ffffff" />
              <circle cx="32" cy="32" r="3.2" fill="#ffffff" />
              <circle
                cx="32"
                cy="32"
                r="6"
                fill="none"
                stroke="#ffffff"
                strokeOpacity="0.55"
                strokeWidth="1"
              />
            </svg>
          </div>
          <div style={{ display: "flex", flexDirection: "column" }}>
            <div
              style={{
                fontFamily: "serif",
                fontSize: 32,
                fontWeight: 700,
                color: "#f1f5f9",
                letterSpacing: -0.5,
              }}
            >
              TFPT
            </div>
            <div
              style={{
                fontSize: 13,
                color: "#94a3b8",
                letterSpacing: 4,
                textTransform: "uppercase",
                marginTop: 2,
              }}
            >
              Fixed-Point Theory
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
              fontSize: 26,
              color: "#a78bfa",
              letterSpacing: 4,
              textTransform: "uppercase",
              marginBottom: 24,
              fontWeight: 600,
              display: "flex",
              alignItems: "center",
              gap: 12,
            }}
          >
            <span
              style={{
                width: 28,
                height: 1,
                background: "#a78bfa",
                opacity: 0.8,
              }}
            />
            TFPT 4.5 paper series · 2026
          </div>
          <div
            style={{
              display: "flex",
              flexDirection: "row",
              flexWrap: "wrap",
              alignItems: "baseline",
              fontFamily: "serif",
              fontSize: 92,
              fontWeight: 600,
              color: "#f8fafc",
              lineHeight: 1.0,
              letterSpacing: -2.5,
              maxWidth: 1080,
              gap: 22,
            }}
          >
            <span style={{ display: "flex" }}>One</span>
            <span
              style={{
                display: "flex",
                background:
                  "linear-gradient(90deg, #60a5fa, #a78bfa, #f472b6)",
                backgroundClip: "text",
                color: "transparent",
              }}
            >
              boundary datum.
            </span>
          </div>
          <div
            style={{
              display: "flex",
              fontFamily: "serif",
              fontSize: 92,
              fontWeight: 600,
              color: "#f8fafc",
              lineHeight: 1.0,
              letterSpacing: -2.5,
              marginTop: 8,
            }}
          >
            The whole Standard Model.
          </div>
          <div
            style={{
              fontSize: 24,
              color: "#cbd5e1",
              marginTop: 24,
              lineHeight: 1.4,
              maxWidth: 920,
              display: "flex",
            }}
          >
            Derives the Standard-Model packet, the fine-structure constant 1/137.0360, the Cabibbo angle, the PMNS matrix, and strong-CP closure — with no fitted constants.
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
