// Run: python3 tools/key_art.py && node tools/key_art.mjs. Renders the key art SVG to PNG with real system fonts.
import { chromium } from 'playwright';
import { fileURLToPath } from 'node:url';
import { copyFile } from 'node:fs/promises';

const svg = fileURLToPath(new URL('../docs/img/key-art.svg', import.meta.url));
const png = fileURLToPath(new URL('../docs/img/key-art.png', import.meta.url));
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1600, height: 900 }, deviceScaleFactor: 2 });
await page.goto(`file://${svg}`);
await page.screenshot({ path: png });
await browser.close();
await copyFile(png, fileURLToPath(new URL('../site/img/key-art.png', import.meta.url)));
console.log(png);
