/**
 * browser-smoke.mjs -- load a URL in headless Chromium, screenshot it,
 * and report anything the page complained about.
 *
 *   node scripts/browser-smoke.mjs <url> <out.png>
 *
 * Exits non-zero on a failed load, a page error, or an HTTP error
 * response, so it works as a smoke test in CI.
 */
import { chromium } from 'playwright';
import { mkdir, readdir } from 'node:fs/promises';
import { dirname, join } from 'node:path';
import { existsSync } from 'node:fs';

/**
 * This environment ships Chromium under PLAYWRIGHT_BROWSERS_PATH, but the
 * npm playwright package pins its own build number and will refuse to run
 * if that exact build is absent. Rather than downloading a second copy,
 * find whatever chromium is already installed and point at it.
 */
async function installedChromium() {
  const root = process.env.PLAYWRIGHT_BROWSERS_PATH;
  if (!root || !existsSync(root)) return undefined;
  const candidates = [];
  for (const dir of await readdir(root)) {
    if (!dir.startsWith('chromium')) continue;
    for (const rel of ['chrome-linux/chrome', 'chrome-linux/headless_shell']) {
      const full = join(root, dir, rel);
      if (existsSync(full)) candidates.push(full);
    }
  }
  candidates.sort();                    // prefer full chrome over headless_shell
  return candidates.find(c => c.endsWith('/chrome')) ?? candidates[0];
}

const [url, out] = process.argv.slice(2);
if (!url || !out) {
  console.error('usage: node scripts/browser-smoke.mjs <url> <out.png>');
  process.exit(2);
}

await mkdir(dirname(out), { recursive: true });

const executablePath = await installedChromium();
if (executablePath) console.log(`using installed chromium: ${executablePath}`);
const browser = await chromium.launch(executablePath ? { executablePath } : {});
const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });

const consoleErrors = [];
const pageErrors = [];
const badResponses = [];

const IGNORABLE = /favicon\.ico/;
page.on('console', m => {
  if (m.type() === 'error' && !IGNORABLE.test(m.text() + m.location()?.url)) consoleErrors.push(m.text());
});
page.on('pageerror', e => pageErrors.push(e.message));
page.on('response', r => {
  if (r.status() >= 400 && !IGNORABLE.test(r.url())) badResponses.push(`${r.status()} ${r.url()}`);
});

let status = 0;
try {
  const resp = await page.goto(url, { waitUntil: 'networkidle', timeout: 30000 });
  console.log(`loaded ${url} -> HTTP ${resp ? resp.status() : 'n/a'}`);
  console.log(`title: ${JSON.stringify(await page.title())}`);
  await page.screenshot({ path: out, fullPage: true });
  console.log(`screenshot: ${out}`);
  if (resp && resp.status() >= 400) status = 1;
} catch (err) {
  console.error(`LOAD FAILED: ${err.message}`);
  status = 1;
}

for (const [label, list] of [['page error', pageErrors],
                             ['console error', consoleErrors],
                             ['http >=400', badResponses]]) {
  if (list.length) {
    status = 1;
    console.error(`\n${list.length} ${label}(s):`);
    list.slice(0, 10).forEach(x => console.error(`  ${x}`));
  }
}
if (!status) console.log('\nsmoke OK: no page errors, no console errors, no 4xx/5xx');
await browser.close();
process.exit(status);
