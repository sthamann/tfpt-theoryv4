import type { MetadataRoute } from "next";
import { papers } from "@/lib/papers";
import { RELEASE_ASSETS } from "@/lib/release";

const SITE_URL =
  process.env.NEXT_PUBLIC_SITE_URL || "https://tfpt-theory.vercel.app";

/**
 * Sitemap priority by asset path.
 *
 * The numbered core papers (00–06) carry the load-bearing arguments and rank
 * highest. Auxiliary papers (theory map, technical companion, series index,
 * coverage audit) and the two-page summary are still first-class downloads
 * but slightly lower. Individual prediction PDFs sit just below since they
 * are leaf nodes of the closed branch.
 */
function priorityForAsset(href: string): number {
  if (/^\/papers\/0\d_/.test(href)) return 0.7;
  if (href === "/predictions/tfpt_two_page_summary.pdf") return 0.65;
  if (href.startsWith("/papers/")) return 0.6;
  if (href.startsWith("/predictions/")) return 0.55;
  return 0.5;
}

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
    {
      url: `${SITE_URL}/falsification`,
      lastModified: now,
      changeFrequency: "monthly",
      priority: 0.85,
    },
  ];

  const paperPages: MetadataRoute.Sitemap = papers.map((p) => ({
    url: `${SITE_URL}/papers/${p.slug}`,
    lastModified: now,
    changeFrequency: "monthly",
    priority: 0.85,
  }));

  // Single source of truth for every released PDF asset (papers + predictions
  // + auxiliary documents). New entries only need to be added in
  // `lib/release.ts` — they appear in the sitemap automatically.
  const releaseFiles: MetadataRoute.Sitemap = Object.values(RELEASE_ASSETS).map(
    (asset) => ({
      url: `${SITE_URL}${asset.href}`,
      lastModified: new Date(asset.releaseDate),
      changeFrequency: "monthly",
      priority: priorityForAsset(asset.href),
    }),
  );

  return [...pages, ...paperPages, ...releaseFiles];
}
