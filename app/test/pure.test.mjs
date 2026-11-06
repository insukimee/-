import test from 'node:test';
import assert from 'node:assert/strict';
import {
  adUnitForRequest,
  desiredTopics,
  findWatchlistUpdates,
  isBootstrapPath,
  pageKind,
  resolveInitialLang,
  tickerFromSlug,
  toggleWatch,
  topicDiff,
  topicForSlug,
} from '../shell/src/pure.mjs';

test('ticker from slug keeps class suffix', () => {
  assert.equal(tickerFromSlug('nvda'), 'NVDA');
  assert.equal(tickerFromSlug('mog-a'), 'MOG.A');
  assert.equal(tickerFromSlug('ttwo'), 'TTWO');
});

test('topic names stay within FCM rules', () => {
  assert.equal(topicForSlug('mog-a'), 'ticker-mog-a');
  assert.equal(topicForSlug(''), null);
});

test('language follows a saved choice, otherwise the device language', () => {
  assert.equal(resolveInitialLang('ja', 'ko-KR'), 'ja');
  assert.equal(resolveInitialLang(null, 'ja-JP'), 'ja');
  assert.equal(resolveInitialLang('', 'ko-KR'), 'ko');
  assert.equal(resolveInitialLang(null, 'en-US'), 'ko');
});

test('page kind and bootstrap path', () => {
  assert.equal(pageKind('/ko/post-nvda.html'), 'post');
  assert.equal(pageKind('/ja/stock-analysis.html'), 'stocks');
  assert.equal(pageKind('/shell/settings.html'), 'settings');
  assert.equal(isBootstrapPath('/index.html'), true);
  assert.equal(isBootstrapPath('/ko/index.html'), false);
});

test('watchlist toggle and feed diff', () => {
  const added = toggleWatch([], { slug: 'nvda', ticker: 'NVDA', title: 'NVDA' });
  assert.equal(added.length, 1);
  assert.equal(toggleWatch(added, { slug: 'nvda' }).length, 0);
  const updates = findWatchlistUpdates(
    { items: [{ id: 'a', slug: 'nvda', lang: 'ko', title: 't' }, { id: 'b', slug: 'aapl', lang: 'ko' }] },
    [{ slug: 'nvda' }],
    [],
    'ko',
  );
  assert.deepEqual(updates.map((item) => item.id), ['a']);
});

test('topics follow the watchlist and can be cleared', () => {
  const next = desiredTopics({
    notify: true,
    digest: true,
    lang: 'ja',
    watchlist: [{ slug: 'nvda' }],
  });
  assert.deepEqual(next, ['ticker-nvda', 'digest-ja']);
  const diff = topicDiff(['ticker-aapl'], next);
  assert.deepEqual(diff.subscribe, ['ticker-nvda', 'digest-ja']);
  assert.deepEqual(diff.unsubscribe, ['ticker-aapl']);
  assert.deepEqual(desiredTopics({ notify: false, watchlist: [{ slug: 'nvda' }] }), []);
});

test('production ad ids are not requested while they are placeholders', () => {
  const testAds = adUnitForRequest({ useTestAds: true });
  assert.equal(testAds.isTesting, true);
  assert.match(testAds.adId, /3940256099942544/);
  const blocked = adUnitForRequest({
    useTestAds: false,
    bannerAdUnitId: 'REPLACE_WITH_BANNER_AD_UNIT_ID',
    androidAppId: 'REPLACE_WITH_ADMOB_APP_ID',
  });
  assert.equal(blocked.blocked, true);
});
