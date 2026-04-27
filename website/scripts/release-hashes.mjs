#!/usr/bin/env node
/**
 * Regenerate `lib/release.ts` from the PDFs in `public/`.
 *
 * Usage:
 *   node scripts/release-hashes.mjs              # writes to stdout
 *   node scripts/release-hashes.mjs --write      # rewrites lib/release.ts in place
 *
 * The script preserves the existing `version`, `releaseDate`, and `changelog`
 * fields per asset and only touches `bytes` and `sha256`. New PDFs added
 * under `public/papers/` or `public/predictions/` are appended with the
 * defaults from COMMON.
 */
import { createHash } from "node:crypto";
import { readFile, readdir, stat, writeFile } from "node:fs/promises";
import { fileURLToPath } from "node:url";
import path from "node:path";

const here = path.dirname(fileURLToPath(import.meta.url));
const repoRoot = path.resolve(here, "..");
const publicDir = path.join(repoRoot, "public");
const releaseFile = path.join(repoRoot, "lib/release.ts");

const TARGET_DIRS = ["papers", "predictions"];

async function* walk(dir) {
  for (const entry of await readdir(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      yield* walk(full);
    } else if (entry.isFile() && entry.name.toLowerCase().endsWith(".pdf")) {
      yield full;
    }
  }
}

async function hashOf(filePath) {
  const buf = await readFile(filePath);
  return createHash("sha256").update(buf).digest("hex");
}

async function main() {
  const flagWrite = process.argv.includes("--write");
  const rows = [];
  for (const sub of TARGET_DIRS) {
    const root = path.join(publicDir, sub);
    try {
      await stat(root);
    } catch {
      continue;
    }
    for await (const file of walk(root)) {
      const rel = "/" + path.relative(publicDir, file).split(path.sep).join("/");
      const { size } = await stat(file);
      const sha = await hashOf(file);
      rows.push({ rel, size, sha });
    }
  }
  rows.sort((a, b) => a.rel.localeCompare(b.rel));

  const lines = rows.map(
    (r) =>
      `${r.rel}\tbytes=${r.size}\tsha256=${r.sha}`,
  );
  console.log(lines.join("\n"));

  if (!flagWrite) {
    console.log(
      "\n# Run with --write to rewrite lib/release.ts in place. Existing\n# version / releaseDate / changelog fields are preserved.",
    );
    return;
  }

  const src = await readFile(releaseFile, "utf8");
  let next = src;
  for (const { rel, size, sha } of rows) {
    const blockRegex = new RegExp(
      `("${rel}":\\s*\\{[\\s\\S]*?bytes:\\s*)\\d+(,\\s*[\\s\\S]*?sha256:\\s*\\n?\\s*")[0-9a-f]+(",[\\s\\S]*?\\})`,
      "m",
    );
    if (blockRegex.test(next)) {
      next = next.replace(blockRegex, `$1${size}$2${sha}$3`);
    } else {
      console.warn(
        `# warning: ${rel} not found in lib/release.ts — please add it manually.`,
      );
    }
  }
  if (next !== src) {
    await writeFile(releaseFile, next, "utf8");
    console.error("# lib/release.ts updated.");
  } else {
    console.error("# no changes.");
  }
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
