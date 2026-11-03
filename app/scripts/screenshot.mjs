import fs from 'node:fs';
import http from 'node:http';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import puppeteer from 'puppeteer-core';

const appDir = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const wwwDir = path.join(appDir, 'www');
const outDir = process.env.SCREENSHOT_DIR || '/opt/cursor/artifacts/screenshots';

function contentType(file) {
  const ext = path.extname(file);
  if (ext === '.html') return 'text/html; charset=utf-8';
  if (ext === '.js') return 'text/javascript; charset=utf-8';
  if (ext === '.css') return 'text/css; charset=utf-8';
  if (ext === '.json') return 'application/json; charset=utf-8';
  if (ext === '.png') return 'image/png';
  return 'application/octet-stream';
}

function startServer(root) {
  const server = http.createServer((request, response) => {
    const url = decodeURIComponent((request.url || '/').split('?')[0]);
    const relative = url === '/' ? 'index.html' : url.replace(/^\/+/, '');
    const file = path.resolve(root, relative);
    if (!file.startsWith(root)) {
      response.writeHead(403);
      response.end();
      return;
    }
    const target = fs.existsSync(file) && fs.statSync(file).isDirectory()
      ? path.join(file, 'index.html')
      : file;
    if (!fs.existsSync(target) || !fs.statSync(target).isFile()) {
      response.writeHead(404);
      response.end('not found');
      return;
    }
    response.writeHead(200, { 'content-type': contentType(target) });
    fs.createReadStream(target).pipe(response);
  });
  return new Promise((resolve) => {
    server.listen(0, '127.0.0.1', () => resolve(server));
  });
}

async function shot(page, name) {
  const file = path.join(outDir, `${name}.png`);
  await page.screenshot({ path: file, fullPage: false });
  console.log('screenshot', file);
}

async function main() {
  if (!fs.existsSync(path.join(wwwDir, 'shell', 'app.js'))) {
    throw new Error('www is missing. Run npm run build:www first.');
  }
  fs.mkdirSync(outDir, { recursive: true });
  const server = await startServer(wwwDir);
  const { port } = server.address();
  const base = `http://127.0.0.1:${port}`;
  const browser = await puppeteer.launch({
    executablePath: process.env.CHROME_PATH || '/usr/local/bin/google-chrome',
    headless: true,
    args: ['--no-sandbox', '--disable-dev-shm-usage', '--window-size=390,844'],
  });
  try {
    const page = await browser.newPage();
    await page.setViewport({ width: 390, height: 844, deviceScaleFactor: 2 });
    await page.goto(`${base}/`, { waitUntil: 'domcontentloaded' });
    await page.waitForSelector('#mi-consent-accept');
    const consentText = await page.$eval('#mi-consent', (node) => node.innerText);
    if (!consentText.includes('투자 권유가 아닙니다')) throw new Error('consent copy missing');
    await shot(page, '01-consent');
    await page.click('#mi-consent-accept');
    await page.waitForSelector('.mi-tabs');
    await page.waitForSelector('h1');
    const homeText = await page.evaluate(() => document.body.innerText);
    if (homeText.includes('adsbygoogle')) throw new Error('AdSense markup still visible');
    if (!documentTitleSafe(homeText)) throw new Error('home shell missing disclaimer');
    await shot(page, '02-home');

    await page.goto(`${base}/ko/post-nvda.html`, { waitUntil: 'domcontentloaded' });
    await page.waitForSelector('#mi-star');
    await page.click('#mi-star');
    const pressed = await page.$eval('#mi-star', (node) => node.getAttribute('aria-pressed'));
    if (pressed !== 'true') throw new Error('star did not toggle on');
    await shot(page, '03-post-watched');

    await page.goto(`${base}/shell/watchlist.html`, { waitUntil: 'domcontentloaded' });
    await page.waitForSelector('.mi-card');
    const watchText = await page.evaluate(() => document.body.innerText);
    if (!watchText.includes('NVDA')) throw new Error('watchlist missing NVDA');
    await shot(page, '04-watchlist');

    await page.goto(`${base}/shell/settings.html`, { waitUntil: 'domcontentloaded' });
    const settingsText = await page.evaluate(() => document.body.innerText);
    if (!settingsText.includes('1.0.0')) throw new Error('version missing');
    if (!settingsText.includes('증권사가 아니며')) throw new Error('disclaimer missing on settings');
    await shot(page, '05-settings');

    await page.goto(`${base}/ja/index.html`, { waitUntil: 'domcontentloaded' });
    const jaText = await page.evaluate(() => document.body.innerText);
    if (!jaText.includes('投資勧誘ではありません')) throw new Error('Japanese shell missing');
    await shot(page, '06-ja-home');

    await page.evaluate(() => window.dispatchEvent(new Event('offline')));
    await page.waitForSelector('#mi-offline:not([hidden])', { timeout: 3000 });
    await shot(page, '07-offline');
    console.log('shell checks passed');
  } finally {
    await browser.close();
    server.close();
  }
}

function documentTitleSafe(text) {
  return text.includes('투자 권유 아님');
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
