"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";

/**
 * Home used to host archive sections under hash anchors. Those sections moved
 * to dedicated routes; this client redirect keeps old bookmarks / README links
 * from landing on a missing fragment.
 */
const MAP: Record<string, string> = {
  papers: "/papers",
  predictions: "/predictions",
  "open-gates": "/verification#open-gates",
  chain: "/architecture#chain",
  gravity: "/architecture#gravity",
  rosetta: "/orientation#rosetta",
  ecosystem: "/#downloads",
};

export function LegacyAnchorRedirect() {
  const router = useRouter();

  useEffect(() => {
    const hash = window.location.hash.replace(/^#/, "");
    if (!hash) return;
    const target = MAP[hash];
    if (target) router.replace(target);
  }, [router]);

  return null;
}
