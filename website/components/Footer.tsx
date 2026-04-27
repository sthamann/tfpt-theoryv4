import Link from "next/link";
import { Logo } from "./Logo";

export function Footer() {
  return (
    <footer className="relative mt-24 border-t border-slate-800/80 bg-slate-950/60">
      <div className="absolute inset-x-0 -top-px h-px bg-gradient-to-r from-transparent via-blue-500/40 to-transparent" />
      <div className="mx-auto grid max-w-7xl gap-10 px-4 py-14 sm:px-6 lg:grid-cols-3 lg:px-8">
        <div>
          <Logo size={40} />
          <p className="mt-4 max-w-md text-sm leading-relaxed text-slate-400">
            Topological Fixed-Point Theory. A boundary-polarized spectral framework
            that derives the Standard-Model packet, predicts α⁻¹(0), the Cabibbo
            angle, the PMNS matrix, and downstream cosmology — from a one-sided
            boundary datum, with no fitted constants.
          </p>
          <p className="mt-4 text-xs text-slate-500">
            By <span className="text-slate-300">Stefan Hamann</span> &amp;{" "}
            <span className="text-slate-300">Alessandro Rizzo</span>.
          </p>
        </div>

        <div>
          <h3 className="font-serif text-sm font-semibold uppercase tracking-wider text-slate-200">
            Theory
          </h3>
          <ul className="mt-4 space-y-2 text-sm">
            <li>
              <Link href="/#chain" className="text-slate-400 hover:text-white">
                Reconstruction chain
              </Link>
            </li>
            <li>
              <Link href="/#papers" className="text-slate-400 hover:text-white">
                Paper series
              </Link>
            </li>
            <li>
              <Link
                href="/#predictions"
                className="text-slate-400 hover:text-white"
              >
                Prediction surface
              </Link>
            </li>
            <li>
              <Link
                href="/papers/theory_map.pdf"
                target="_blank"
                rel="noopener"
                className="text-slate-400 hover:text-white"
              >
                Theory status map (PDF)
              </Link>
            </li>
          </ul>
        </div>

        <div>
          <h3 className="font-serif text-sm font-semibold uppercase tracking-wider text-slate-200">
            Downloads
          </h3>
          <ul className="mt-4 space-y-2 text-sm">
            <li>
              <Link
                href="/orientation"
                className="text-slate-400 hover:text-white"
              >
                Orientation note
              </Link>
            </li>
            <li>
              <Link
                href="/papers/series_index.pdf"
                target="_blank"
                rel="noopener"
                className="text-slate-400 hover:text-white"
              >
                Series index
              </Link>
            </li>
            <li>
              <Link
                href="/papers/technical_companion.pdf"
                target="_blank"
                rel="noopener"
                className="text-slate-400 hover:text-white"
              >
                Technical companion
              </Link>
            </li>
            <li>
              <Link
                href="/predictions/tfpt_two_page_summary.pdf"
                target="_blank"
                rel="noopener"
                className="text-slate-400 hover:text-white"
              >
                Two-page summary
              </Link>
            </li>
          </ul>
        </div>
      </div>

      <div className="border-t border-slate-800/80 px-4 py-6 sm:px-6 lg:px-8">
        <div className="mx-auto flex max-w-7xl flex-col items-start justify-between gap-3 text-xs text-slate-500 sm:flex-row sm:items-center">
          <p>
            © {new Date().getFullYear()} Stefan Hamann &amp; Alessandro Rizzo.
            All papers and predictions distributed for academic use.
          </p>
          <p className="text-slate-600">
            TFPT 4.5 series — boundary polarization · carrier rigidity · observable closure
          </p>
        </div>
      </div>
    </footer>
  );
}
