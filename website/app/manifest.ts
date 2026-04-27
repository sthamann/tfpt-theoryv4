import type { MetadataRoute } from "next";

export default function manifest(): MetadataRoute.Manifest {
  return {
    name: "TFPT — Topological Fixed-Point Theory",
    short_name: "TFPT",
    description:
      "A boundary-polarized spectral framework that derives the Standard-Model packet, α, CKM, PMNS, and downstream cosmology from a one-sided boundary datum.",
    start_url: "/",
    display: "standalone",
    background_color: "#06091a",
    theme_color: "#1e3a8a",
    icons: [
      {
        src: "/icon",
        sizes: "64x64",
        type: "image/png",
      },
      {
        src: "/apple-icon",
        sizes: "180x180",
        type: "image/png",
      },
    ],
    lang: "en",
    categories: ["education", "science", "physics"],
    orientation: "any",
  };
}
