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

export type PdfInteraction = "download" | "view";

export interface TrackPdfArgs {
  file: string;
  source: DownloadSource;
  kind: DownloadKind;
  interaction: PdfInteraction;
  title?: string;
}

/**
 * Fire a Vercel Web Analytics custom event for a PDF interaction.
 *
 * - Event names: "pdf_download", "pdf_view"
 * - Properties: file (path without leading slash), source, kind, interaction, title?
 *
 * Vercel Web Analytics is cookie-free and does not store IP addresses,
 * so no consent banner is required for this event.
 *
 * The browser navigates to the PDF after the click. `track()` uses
 * `navigator.sendBeacon` under the hood, so the event is reliably
 * delivered even when the link opens in a new tab.
 */
export function trackPdfInteraction({
  file,
  source,
  kind,
  interaction,
  title,
}: TrackPdfArgs) {
  const fileLabel = file.replace(/^\//, "");
  const props: Record<string, string> = {
    file: fileLabel,
    source,
    kind,
    interaction,
  };
  if (title) {
    props.title = title.length > 120 ? `${title.slice(0, 117)}...` : title;
  }
  track(interaction === "view" ? "pdf_view" : "pdf_download", props);
}
