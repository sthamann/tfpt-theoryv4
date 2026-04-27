import { track } from "@vercel/analytics";

/**
 * Where on the site the PDF was opened from. Used as the "source" property
 * in the Vercel Web Analytics dashboard so the same file can be segmented
 * by entry point (hero CTA vs. paper detail vs. footer, etc.).
 */
export type DownloadSource =
  | "hero"
  | "papers-detail"
  | "predictions-card"
  | "predictions-summary-cta"
  | "downloads-papers"
  | "downloads-companions"
  | "footer"
  | "orientation-hero"
  | "orientation-download"
  | "orientation-sidebar"
  | "series-map";

/**
 * Coarse classification of the artifact behind the link, so the dashboard
 * can group by document type independently of the source location.
 */
export type DownloadKind =
  | "paper"
  | "prediction"
  | "companion"
  | "summary"
  | "series-index"
  | "theory-map"
  | "coverage-audit";

export interface TrackPdfArgs {
  file: string;
  source: DownloadSource;
  kind: DownloadKind;
  title?: string;
}

/**
 * Fire a Vercel Web Analytics custom event for a PDF open / download click.
 *
 * - Event name: "pdf_download"
 * - Properties: file (path without leading slash), source, kind, title?
 *
 * Vercel Web Analytics is cookie-free and does not store IP addresses,
 * so no consent banner is required for this event.
 *
 * The browser navigates to the PDF after the click. `track()` uses
 * `navigator.sendBeacon` under the hood, so the event is reliably
 * delivered even when the link opens in a new tab.
 */
export function trackPdfDownload({ file, source, kind, title }: TrackPdfArgs) {
  const fileLabel = file.replace(/^\//, "");
  const props: Record<string, string> = {
    file: fileLabel,
    source,
    kind,
  };
  if (title) {
    props.title = title.length > 120 ? `${title.slice(0, 117)}...` : title;
  }
  track("pdf_download", props);
}
