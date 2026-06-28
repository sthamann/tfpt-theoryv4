import type { MetadataRoute } from "next";
import { SITE_URL } from "@/lib/utils";

/**
 * robots.txt — everything is crawlable. The wildcard rule already allows every
 * bot; the explicit AI-/search-engine entries below make the intent
 * unambiguous and signal that TFPT *wants* to be indexed and cited by both
 * classic search engines (Google, Bing) and answer engines (ChatGPT,
 * Perplexity, Claude, Gemini, Copilot). Training crawlers are allowed too, so
 * the theory can enter model weights and be cited long-term.
 */
const AI_AND_SEARCH_BOTS = [
  "Googlebot",
  "Google-Extended",
  "Bingbot",
  "DuckDuckBot",
  "Applebot",
  "Applebot-Extended",
  "GPTBot",
  "ChatGPT-User",
  "OAI-SearchBot",
  "PerplexityBot",
  "Perplexity-User",
  "ClaudeBot",
  "Claude-User",
  "anthropic-ai",
  "Google-CloudVertexBot",
  "Amazonbot",
  "Bytespider",
  "CCBot",
];

export default function robots(): MetadataRoute.Robots {
  return {
    rules: [
      { userAgent: "*", allow: "/" },
      ...AI_AND_SEARCH_BOTS.map((userAgent) => ({ userAgent, allow: "/" })),
    ],
    sitemap: `${SITE_URL}/sitemap.xml`,
    host: SITE_URL,
  };
}
