// News-image entry for Thursday 26 November 2026 (Node 22, stdlib only).
// The front page is drawn by gen_image.py and saved here as entry.png;
// this program just copies it to the output directory, deterministically,
// with no network access.
//
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync } from "node:fs";
import { join } from "node:path";

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
copyFileSync(new URL("./entry.png", import.meta.url),
             join(outDir, "entry.png"));
