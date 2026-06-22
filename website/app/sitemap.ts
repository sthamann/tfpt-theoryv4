import type { MetadataRoute } from "next";
import { papers } from "@/lib/papers";
import { RELEASE_ASSETS } from "@/lib/release";
import { SITE_DATE } from "@/lib/version";
import { SITE_URL } from "@/lib/utils";

/**
 * Sitemap priority by asset path.
 *
 * The introduction (the reading guide) and the four core documents carry the
 * load-bearing arguments and rank highest; the three companions (Appendix H,
 * Origin Theory, research contracts) sit just below.
 */
function priorityForAsset(href: string): number {
  if (href === "/papers/introduction.pdf") return 0.7;
  if (href.startsWith("/papers/")) return 0.65;
  return 0.5;
}

export default function sitemap(): MetadataRoute.Sitemap {
  // Tie lastmod to the released content version (lib/version.ts, generated from
  // tex-artefacts/version.tex) rather than the build timestamp, so crawlers see
  // a meaningful "last changed" date instead of "today" on every deploy.
  const lastModified = new Date(SITE_DATE);

  // Only canonical, crawlable routes — no in-page fragment anchors (#overview,
  // …): search engines drop URL fragments and fold them into the page URL.
  const pages: MetadataRoute.Sitemap = [
    {
      url: SITE_URL,
      lastModified,
      changeFrequency: "weekly",
      priority: 1.0,
    },
    {
      url: `${SITE_URL}/orientation`,
      lastModified,
      changeFrequency: "monthly",
      priority: 0.95,
    },
    {
      url: `${SITE_URL}/compiler`,
      lastModified,
      changeFrequency: "monthly",
      priority: 0.85,
    },
    {
      url: `${SITE_URL}/verification`,
      lastModified,
      changeFrequency: "monthly",
      priority: 0.85,
    },
    {
      url: `${SITE_URL}/falsification`,
      lastModified,
      changeFrequency: "monthly",
      priority: 0.85,
    },
    {
      url: `${SITE_URL}/review`,
      lastModified,
      changeFrequency: "monthly",
      priority: 0.8,
    },
    {
      url: `${SITE_URL}/objections`,
      lastModified,
      changeFrequency: "monthly",
      priority: 0.7,
    },
    {
      url: `${SITE_URL}/replication`,
      lastModified,
      changeFrequency: "monthly",
      priority: 0.7,
    },
    {
      url: `${SITE_URL}/faq`,
      lastModified,
      changeFrequency: "monthly",
      priority: 0.7,
    },
    {
      url: `${SITE_URL}/changelog`,
      lastModified,
      changeFrequency: "weekly",
      priority: 0.6,
    },
  ];

  const paperPages: MetadataRoute.Sitemap = papers.map((p) => ({
    url: `${SITE_URL}/papers/${p.slug}`,
    lastModified,
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
