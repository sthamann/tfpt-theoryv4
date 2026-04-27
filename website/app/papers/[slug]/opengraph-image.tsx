import { ImageResponse } from "next/og";
import { papers, STATUS_META } from "@/lib/papers";

export const runtime = "edge";
export const alt = "TFPT 4.5 paper preview";
export const size = { width: 1200, height: 630 };
export const contentType = "image/png";

interface PaperOgImageProps {
  params: { slug: string };
}

export default async function PaperOgImage(
  props: PaperOgImageProps,
): Promise<ImageResponse> {
  const { slug } = await Promise.resolve(props.params);
  const paper = papers.find((p) => p.slug === slug) ?? papers[0];
  const meta = STATUS_META[paper.status];

  // Pick a per-status accent gradient for the OG card.
  const accentByStatus: Record<string, [string, string]> = {
    orientation: ["#94a3b8", "#475569"],
    core: ["#60a5fa", "#a855f7"],
    bridge: ["#34d399", "#14b8a6"],
    conditional: ["#fb923c", "#ef4444"],
    downstream: ["#f472b6", "#ec4899"],
  };
  const [accentA, accentB] = accentByStatus[paper.status] ?? [
    "#60a5fa",
    "#a855f7",
  ];

  return new ImageResponse(
    (
      <div
        style={{
          width: "100%",
          height: "100%",
          display: "flex",
          flexDirection: "column",
          background: `radial-gradient(ellipse at 18% 0%, ${accentA}55, transparent 55%), radial-gradient(ellipse at 82% 100%, ${accentB}40, transparent 55%), #060912`,
          color: "#e2e8f0",
          fontFamily: "Inter, sans-serif",
          padding: 72,
        }}
      >
        <div
          style={{ display: "flex", alignItems: "center", gap: 16 }}
        >
          <div
            style={{
              width: 56,
              height: 56,
              borderRadius: 14,
              background: `linear-gradient(135deg, ${accentA}, ${accentB})`,
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              color: "#ffffff",
              fontFamily: "serif",
              fontSize: 28,
              fontWeight: 700,
            }}
          >
            {paper.number}
          </div>
          <div style={{ display: "flex", flexDirection: "column" }}>
            <div
              style={{
                fontFamily: "serif",
                fontSize: 22,
                fontWeight: 700,
                color: "#f1f5f9",
              }}
            >
              TFPT 4.5 paper series
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
              {meta.label}
            </div>
          </div>
        </div>

        <div
          style={{
            display: "flex",
            flexDirection: "column",
            marginTop: "auto",
            gap: 18,
          }}
        >
          <div
            style={{
              display: "flex",
              fontFamily: "serif",
              fontSize: 64,
              fontWeight: 600,
              color: "#f8fafc",
              lineHeight: 1.05,
              letterSpacing: -1.5,
              maxWidth: 1056,
            }}
          >
            {paper.title}
          </div>
          <div
            style={{
              display: "flex",
              fontSize: 24,
              color: "#cbd5e1",
              lineHeight: 1.4,
              maxWidth: 1000,
            }}
          >
            {paper.subtitle}
          </div>
          <div
            style={{
              display: "flex",
              alignItems: "center",
              gap: 18,
              color: "#64748b",
              fontSize: 18,
              marginTop: 6,
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
            <span
              style={{
                width: 4,
                height: 4,
                borderRadius: 2,
                background: "#475569",
              }}
            />
            <span style={{ display: "flex" }}>tfpt-theory.vercel.app</span>
          </div>
        </div>
      </div>
    ),
    { ...size },
  );
}
