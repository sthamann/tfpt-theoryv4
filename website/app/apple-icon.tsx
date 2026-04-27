import { ImageResponse } from "next/og";

export const runtime = "edge";
export const size = { width: 180, height: 180 };
export const contentType = "image/png";

export default function AppleIcon() {
  return new ImageResponse(
    (
      <div
        style={{
          width: 180,
          height: 180,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          background:
            "linear-gradient(135deg, #1d4ed8 0%, #6366f1 40%, #a855f7 80%, #ec4899 100%)",
          borderRadius: 38,
        }}
      >
        <svg width="140" height="140" viewBox="0 0 64 64">
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
          <circle
            cx="32"
            cy="32"
            r="6"
            fill="none"
            stroke="#ffffff"
            strokeOpacity="0.5"
            strokeWidth="0.8"
          />
        </svg>
      </div>
    ),
    { ...size },
  );
}
