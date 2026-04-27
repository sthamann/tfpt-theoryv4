import type { MetadataRoute } from "next";
import { papers } from "@/lib/papers";
import { predictions } from "@/lib/predictions";

const SITE_URL =
  process.env.NEXT_PUBLIC_SITE_URL || "https://tfpt-theory.vercel.app";

export default function sitemap(): MetadataRoute.Sitemap {
  const now = new Date();

  const pages: MetadataRoute.Sitemap = [
    {
      url: SITE_URL,
      lastModified: now,
      changeFrequency: "weekly",
      priority: 1.0,
    },
    {
      url: `${SITE_URL}/orientation`,
      lastModified: now,
      changeFrequency: "monthly",
      priority: 0.95,
    },
    {
      url: `${SITE_URL}/#overview`,
      lastModified: now,
      changeFrequency: "monthly",
      priority: 0.7,
    },
    {
      url: `${SITE_URL}/#chain`,
      lastModified: now,
      changeFrequency: "monthly",
      priority: 0.7,
    },
    {
      url: `${SITE_URL}/#papers`,
      lastModified: now,
      changeFrequency: "monthly",
      priority: 0.85,
    },
    {
      url: `${SITE_URL}/#predictions`,
      lastModified: now,
      changeFrequency: "monthly",
      priority: 0.9,
    },
    {
      url: `${SITE_URL}/#downloads`,
      lastModified: now,
      changeFrequency: "monthly",
      priority: 0.7,
    },
  ];

  const paperFiles: MetadataRoute.Sitemap = papers.map((p) => ({
    url: `${SITE_URL}${p.pdf}`,
    lastModified: now,
    changeFrequency: "yearly",
    priority: 0.6,
  }));

  const predictionFiles: MetadataRoute.Sitemap = predictions.map((p) => ({
    url: `${SITE_URL}${p.pdf}`,
    lastModified: now,
    changeFrequency: "yearly",
    priority: 0.55,
  }));

  return [...pages, ...paperFiles, ...predictionFiles];
}
