import * as esbuild from 'esbuild';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const appDir = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const repoRoot = path.resolve(appDir, '..');
const wwwDir = path.join(appDir, 'www');

function readJson(file) {
  return JSON.parse(fs.readFileSync(file, 'utf8'));
}

function removeDivsByClass(html, className) {
  const marker = new RegExp(`<div\\b[^>]*class\\s*=\\s*"[^"]*\\b${className}\\b[^"]*"[^>]*>`, 'gi');
  let result = html;
  for (let guard = 0; guard < 200; guard += 1) {
    marker.lastIndex = 0;
    const match = marker.exec(result);
    if (!match) break;
    const start = match.index;
    let depth = 1;
    const token = /<\/?div\b[^>]*>/gi;
    token.lastIndex = start + match[0].length;
    let end = -1;
    let found;
    while ((found = token.exec(result))) {
      if (found[0].startsWith('</')) depth -= 1;
      else depth += 1;
      if (depth === 0) {
        end = found.index + found[0].length;
        break;
      }
    }
    if (end === -1) break;
    result = result.slice(0, start) + result.slice(end);
  }
  return result;
}

export function stripWebAds(html) {
  let next = html.replace(/<script\b[^>]*pagead2\.googlesyndication\.com[\s\S]*?<\/script>/gi, '');
  next = next.replace(/<script\b[^>]*>\s*\(adsbygoogle[\s\S]*?<\/script>/gi, '');
  next = next.replace(/<meta\b[^>]*google-adsense-account[^>]*>/gi, '');
  next = removeDivsByClass(next, 'ad-container');
  return next;
}

const APP_DISPLAY_NAME = 'US Market Insight';

function renameAppChrome(html) {
  return html
    .replace(
      /<a href="index\.html" class="logo">[^<]*<\/a>/g,
      `<a href="index.html" class="logo">${APP_DISPLAY_NAME}</a>`,
    )
    .replace(
      /(<meta name="apple-mobile-web-app-title" content=")[^"]*(")/g,
      `$1${APP_DISPLAY_NAME}$2`,
    )
    .replace(
      /(<meta property="og:site_name" content=")[^"]*(")/g,
      `$1${APP_DISPLAY_NAME}$2`,
    )
    .replace(/ - 마켓인사이트/g, ` - ${APP_DISPLAY_NAME}`)
    .replace(/ - マーケットインサイト/g, ` - ${APP_DISPLAY_NAME}`)
    .replace(/© 2026 마켓인사이트/g, `© 2026 ${APP_DISPLAY_NAME}`)
    .replace(/© 2026 マーケットインサイト/g, `© 2026 ${APP_DISPLAY_NAME}`);
}

function injectShell(html) {
  let next = html;
  if (!/viewport-fit=cover/.test(next)) {
    next = next.replace(
      /<meta\s+name="viewport"\s+content="([^"]*)"/i,
      (_all, content) => `<meta name="viewport" content="${content}, viewport-fit=cover"`,
    );
  }
  if (!next.includes('shell/shell.css')) {
    next = next.replace(
      /<\/head>/i,
      '  <link rel="stylesheet" href="../shell/shell.css">\n<script>window.__MI_APP__=true;</script>\n</head>',
    );
  }
  if (!next.includes('shell/app.js')) {
    next = next.replace(/<\/body>/i, '<script src="../shell/app.js"></script>\n</body>');
  }
  return next;
}

function patchMainJs(source) {
  return source.replace(
    "if ('serviceWorker' in navigator) {",
    "if ('serviceWorker' in navigator && !window.__MI_APP__) {",
  );
}

function copyFile(from, to) {
  fs.mkdirSync(path.dirname(to), { recursive: true });
  fs.copyFileSync(from, to);
}

function walkHtml(dir) {
  const files = [];
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) files.push(...walkHtml(full));
    else if (entry.name.endsWith('.html')) files.push(full);
  }
  return files;
}

function postSlugs(langDir) {
  return fs.readdirSync(langDir)
    .filter((name) => /^post-[a-z0-9-]+\.html$/i.test(name))
    .map((name) => name.replace(/^post-/i, '').replace(/\.html$/i, '').toLowerCase())
    .sort();
}

async function main() {
  const appConfig = readJson(path.join(appDir, 'app.config.json'));
  const capConfig = readJson(path.join(appDir, 'capacitor.config.json'));
  if (appConfig.appId !== capConfig.appId) {
    throw new Error(`appId mismatch: ${appConfig.appId} vs ${capConfig.appId}`);
  }
  if (appConfig.appName !== capConfig.appName) {
    throw new Error(`appName mismatch: ${appConfig.appName} vs ${capConfig.appName}`);
  }
  if (appConfig.appIdConfirmed !== false) {
    console.warn('app.config.json appIdConfirmed is not false. Confirm the id is final before Play upload.');
  }

  fs.rmSync(wwwDir, { recursive: true, force: true });
  fs.mkdirSync(wwwDir, { recursive: true });

  for (const dir of ['ko', 'ja', 'css', 'icons']) {
    const source = path.join(repoRoot, dir);
    if (!fs.existsSync(source)) throw new Error(`missing site directory: ${dir}`);
    fs.cpSync(source, path.join(wwwDir, dir), { recursive: true });
  }

  const mainJs = fs.readFileSync(path.join(repoRoot, 'js', 'main.js'), 'utf8');
  const patched = patchMainJs(mainJs);
  if (patched === mainJs) throw new Error('failed to patch service worker registration in the copied main.js');
  fs.mkdirSync(path.join(wwwDir, 'js'), { recursive: true });
  fs.writeFileSync(path.join(wwwDir, 'js', 'main.js'), patched);

  if (appConfig.stripWebAds !== false) {
    for (const file of walkHtml(path.join(wwwDir, 'ko')).concat(walkHtml(path.join(wwwDir, 'ja')))) {
      const original = fs.readFileSync(file, 'utf8');
      const stripped = injectShell(renameAppChrome(stripWebAds(original)));
      if (stripped.includes('adsbygoogle') || stripped.includes('pagead2.googlesyndication.com')) {
        throw new Error(`web ads remain in ${path.relative(wwwDir, file)}`);
      }
      fs.writeFileSync(file, stripped);
    }
  }

  fs.mkdirSync(path.join(wwwDir, 'shell'), { recursive: true });
  fs.cpSync(path.join(appDir, 'shell', 'shell.css'), path.join(wwwDir, 'shell', 'shell.css'));
  fs.cpSync(path.join(appDir, 'shell', 'feed.sample.json'), path.join(wwwDir, 'shell', 'feed.sample.json'));
  for (const page of ['watchlist.html', 'settings.html', 'legal.html']) {
    copyFile(path.join(appDir, 'shell', 'pages', page), path.join(wwwDir, 'shell', page));
  }

  const runtime = {
    appName: appConfig.appName,
    version: appConfig.version,
    versionCode: appConfig.versionCode,
    disclaimerVersion: appConfig.disclaimerVersion,
    siteBaseUrl: appConfig.siteBaseUrl,
    feedPath: appConfig.feedPath,
    ads: appConfig.ads,
    push: appConfig.push,
    bundledAt: new Date().toISOString(),
    posts: postSlugs(path.join(wwwDir, 'ko')),
  };
  fs.writeFileSync(path.join(wwwDir, 'shell', 'runtime-config.json'), `${JSON.stringify(runtime, null, 2)}\n`);

  fs.writeFileSync(path.join(wwwDir, 'index.html'), `<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <meta name="theme-color" content="#0D0D0D">
  <title>US Market Insight</title>
  <style>html,body{margin:0;background:#0D0D0D;color:#E4E4E4;font-family:sans-serif}</style>
</head>
<body>
  <p style="padding:24px">US Market Insight</p>
  <script src="./shell/app.js"></script>
</body>
</html>
`);

  await esbuild.build({
    entryPoints: [path.join(appDir, 'shell', 'src', 'main.js')],
    bundle: true,
    format: 'iife',
    platform: 'browser',
    target: ['es2020'],
    outfile: path.join(wwwDir, 'shell', 'app.js'),
    legalComments: 'none',
    logLevel: 'silent',
  });

  console.log(`built ${wwwDir} (${runtime.posts.length} tickers, bundle ${runtime.bundledAt})`);
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  main().catch((error) => {
    console.error(error);
    process.exit(1);
  });
}
