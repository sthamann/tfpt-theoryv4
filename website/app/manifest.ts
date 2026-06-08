import type { MetadataRoute } from "next";

export default function manifest(): MetadataRoute.Manifest {
  return {
    name: "TFPT — Topological Fixed-Point Theory",
    short_name: "TFPT",
    description:
      "A discrete compiler that builds E₈ from two axioms {c₃ = 1/(8π), g_car = 5} and reads off the Standard Model, α, the flavor sector, and the scale grammar.",
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
