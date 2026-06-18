// Generate a WebVTT subtitle track from the same captions.json that drives the
// burned-in subtitle, so the accessible track and the on-screen text never drift.
//
//   node scripts/make-vtt.mjs
//
// Writes ../website/public/intro/tfpt-intro.en.vtt (relative to the video/ dir).
import { readFileSync, writeFileSync, mkdirSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const cues = JSON.parse(readFileSync(resolve(here, "../src/captions.json"), "utf8"));

const pad = (n, w = 2) => String(n).padStart(w, "0");
const stamp = (sec) => {
  const ms = Math.round((sec - Math.floor(sec)) * 1000);
  const s = Math.floor(sec) % 60;
  const m = Math.floor(sec / 60) % 60;
  const h = Math.floor(sec / 3600);
  return `${pad(h)}:${pad(m)}:${pad(s)}.${pad(ms, 3)}`;
};

let out = "WEBVTT\n\n";
cues.forEach((c, i) => {
  out += `${i + 1}\n${stamp(c.from)} --> ${stamp(c.to)}\n${c.text}\n\n`;
});

const dest = resolve(here, "../../website/public/intro/tfpt-intro.en.vtt");
mkdirSync(dirname(dest), { recursive: true });
writeFileSync(dest, out, "utf8");
console.log(`Wrote ${cues.length} cues -> ${dest}`);
