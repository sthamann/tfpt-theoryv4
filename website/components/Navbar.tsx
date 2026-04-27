"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { Menu, X } from "lucide-react";
import { cn } from "@/lib/utils";
import { Logo } from "./Logo";

const links = [
  { href: "/#overview", label: "Overview" },
  { href: "/#chain", label: "Chain" },
  { href: "/#papers", label: "Papers" },
  { href: "/#predictions", label: "Predictions" },
  { href: "/#downloads", label: "Downloads" },
];

export function Navbar() {
  const [scrolled, setScrolled] = useState(false);
  const [open, setOpen] = useState(false);

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 12);
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  return (
    <header
      className={cn(
        "fixed top-0 left-0 right-0 z-40 transition-all duration-300",
        scrolled
          ? "glass-strong backdrop-saturate-200 border-b border-slate-700/40"
          : "bg-transparent",
      )}
    >
      <nav
        aria-label="Primary"
        className="mx-auto flex h-16 max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8"
      >
        <Link
          href="/"
          className="group flex items-center"
          aria-label="TFPT home"
        >
          <Logo size={36} />
        </Link>

        <ul className="hidden items-center gap-1 md:flex">
          {links.map((l) => (
            <li key={l.href}>
              <Link
                href={l.href}
                className="rounded-md px-3 py-2 text-sm font-medium text-slate-300 transition-colors hover:bg-white/5 hover:text-white"
              >
                {l.label}
              </Link>
            </li>
          ))}
          <li>
            <Link
              href="/orientation"
              className="ml-2 rounded-full bg-gradient-to-r from-blue-500 to-violet-500 px-4 py-2 text-sm font-semibold text-white shadow-lg shadow-blue-500/20 transition-transform hover:scale-105 focus:scale-105"
            >
              Read the orientation
            </Link>
          </li>
        </ul>

        <button
          type="button"
          onClick={() => setOpen((v) => !v)}
          className="md:hidden inline-flex h-10 w-10 items-center justify-center rounded-md text-slate-300 hover:bg-white/5 hover:text-white"
          aria-label={open ? "Close menu" : "Open menu"}
          aria-expanded={open}
        >
          {open ? <X size={20} /> : <Menu size={20} />}
        </button>
      </nav>

      {open && (
        <div
          id="mobile-menu"
          className="md:hidden glass-strong border-t border-slate-700/40 px-4 pb-4 pt-2"
        >
          <ul className="flex flex-col gap-1">
            {links.map((l) => (
              <li key={l.href}>
                <Link
                  href={l.href}
                  onClick={() => setOpen(false)}
                  className="block rounded-md px-3 py-2 text-base text-slate-200 hover:bg-white/5"
                >
                  {l.label}
                </Link>
              </li>
            ))}
            <li>
              <Link
                href="/orientation"
                onClick={() => setOpen(false)}
                className="mt-2 block rounded-full bg-gradient-to-r from-blue-500 to-violet-500 px-4 py-2 text-center text-sm font-semibold text-white"
              >
                Read the orientation
              </Link>
            </li>
          </ul>
        </div>
      )}
    </header>
  );
}
