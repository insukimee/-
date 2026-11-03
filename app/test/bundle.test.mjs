import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const www = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../www');

function walk(dir) {
  const files = [];
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) files.push(...walk(full));
    else files.push(full);
  }
  return files;
}

test('bundled site has no AdSense and includes the app shell', () => {
  assert.equal(fs.existsSync(path.join(www, 'shell', 'app.js')), true);
  assert.equal(fs.existsSync(path.join(www, 'ko', 'index.html')), true);
  assert.equal(fs.existsSync(path.join(www, 'ja', 'post-nvda.html')), true);
  assert.equal(fs.existsSync(path.join(www, 'sw.js')), false);
  const html = walk(www).filter((file) => file.endsWith('.html'));
  assert.ok(html.length > 40);
  for (const file of html) {
    const text = fs.readFileSync(file, 'utf8');
    assert.equal(text.includes('adsbygoogle'), false, file);
    assert.equal(text.includes('pagead2.googlesyndication.com'), false, file);
  }
  const home = fs.readFileSync(path.join(www, 'ko', 'index.html'), 'utf8');
  assert.match(home, /shell\/app\.js/);
  assert.match(home, /__MI_APP__/);
  const config = JSON.parse(fs.readFileSync(path.join(www, 'shell', 'runtime-config.json'), 'utf8'));
  assert.equal(config.appName, 'US Market Insight');
  assert.equal(config.ads.useTestAds, true);
  assert.ok(config.posts.includes('nvda'));
  assert.ok(config.posts.includes('mog-a'));
  const js = fs.readFileSync(path.join(www, 'js', 'main.js'), 'utf8');
  assert.match(js, /__MI_APP__/);
});
