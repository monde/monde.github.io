#!/usr/bin/env node
// Runs PurgeCSS against _site HTML output and reports what would be removed.
// Usage: npm run purgecss:diff
//
// Writes purged CSS to assets/style.purged.css and prints a size comparison.

const { PurgeCSS } = require("purgecss");
const fs = require("fs");
const path = require("path");

const ROOT = path.join(__dirname, "..");
const INPUT_CSS = path.join(ROOT, "assets/style.css");
const OUTPUT_CSS = path.join(ROOT, "assets/style.purged.css");

async function main() {
  const result = await new PurgeCSS().purge({
    css: [INPUT_CSS],
    content: ["_site/**/*.html"],
    // Safelist selectors that are injected dynamically or come from plugins
    safelist: {
      standard: [],
      deep: [],
      greedy: [],
    },
  });

  const purged = result[0].css;
  fs.writeFileSync(OUTPUT_CSS, purged);

  const originalSize = fs.statSync(INPUT_CSS).size;
  const purgedSize = Buffer.byteLength(purged, "utf8");
  const saved = originalSize - purgedSize;
  const pct = ((saved / originalSize) * 100).toFixed(1);

  console.log(`Original:  ${(originalSize / 1024).toFixed(1)} KB  (${INPUT_CSS})`);
  console.log(`Purged:    ${(purgedSize / 1024).toFixed(1)} KB  (${OUTPUT_CSS})`);
  console.log(`Removed:   ${(saved / 1024).toFixed(1)} KB  (${pct}%)`);
  console.log();
  console.log("Review assets/style.purged.css, then copy it over assets/style.css when satisfied.");
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
