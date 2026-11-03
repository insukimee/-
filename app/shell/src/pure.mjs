/** Pure helpers. No Capacitor imports so Node tests can load this file. */

export function slugFromPath(pathname) {
  const pathOnly = String(pathname || '').split('?')[0].split('#')[0];
  const match = pathOnly.match(/\/post-([a-z0-9-]+)\.html$/i);
  return match ? match[1].toLowerCase() : null;
}

export function tickerFromSlug(slug) {
  if (!slug) return null;
  const normalized = String(slug).toLowerCase();
  if (/^[a-z0-9]+-[a-z]$/.test(normalized)) {
    const index = normalized.lastIndexOf('-');
    return `${normalized.slice(0, index)}.${normalized.slice(index + 1)}`.toUpperCase();
  }
  return normalized.toUpperCase();
}

export function topicForSlug(slug, prefix = 'ticker-') {
  if (!slug) return null;
  const topic = `${prefix}${String(slug).toLowerCase()}`;
  if (!/^[a-zA-Z0-9-_.~%]{1,900}$/.test(topic)) return null;
  return topic;
}

export function digestTopic(lang, prefix = 'digest-') {
  if (lang !== 'ko' && lang !== 'ja') return null;
  return `${prefix}${lang}`;
}

export function resolveInitialLang(saved, navigatorLang) {
  if (saved === 'ko' || saved === 'ja') return saved;
  const lang = String(navigatorLang || '').toLowerCase();
  if (lang.startsWith('ja')) return 'ja';
  return 'ko';
}

export function langFromPath(pathname) {
  const match = String(pathname || '').match(/\/(ko|ja)\//);
  return match ? match[1] : null;
}

export function swapLangPath(pathname, target) {
  if (target !== 'ko' && target !== 'ja') return pathname;
  if (/\/(ko|ja)\//.test(pathname)) {
    return pathname.replace(/\/(ko|ja)\//, `/${target}/`);
  }
  return pathname;
}

export function isBootstrapPath(pathname) {
  const pathOnly = String(pathname || '/');
  if (pathOnly === '/' || pathOnly === '') return true;
  if (/\/(ko|ja)\//.test(pathOnly)) return false;
  return /\/index\.html$/.test(pathOnly);
}

export function pageKind(pathname) {
  const pathOnly = String(pathname || '');
  if (/\/post-[a-z0-9-]+\.html$/i.test(pathOnly)) return 'post';
  if (/\/stock-analysis\.html$/i.test(pathOnly)) return 'stocks';
  if (/\/economy-trends\.html$/i.test(pathOnly)) return 'economy';
  if (/\/watchlist\.html$/i.test(pathOnly)) return 'watchlist';
  if (/\/settings\.html$/i.test(pathOnly)) return 'settings';
  if (/\/legal\.html$/i.test(pathOnly)) return 'legal';
  if (/\/(ko|ja)\/index\.html$/i.test(pathOnly)) return 'home';
  if (isBootstrapPath(pathOnly)) return 'boot';
  return 'other';
}

export function tabForKind(kind) {
  if (kind === 'home') return 'home';
  if (kind === 'stocks' || kind === 'post') return 'stocks';
  if (kind === 'economy') return 'economy';
  if (kind === 'watchlist') return 'watchlist';
  if (kind === 'settings' || kind === 'legal') return 'settings';
  return null;
}

export function localPostPath(lang, slug) {
  return `/${lang}/post-${slug}.html`;
}

export function publicPostUrl(siteBaseUrl, lang, slug) {
  const base = String(siteBaseUrl || '').replace(/\/$/, '');
  return `${base}/${lang}/post-${slug}.html`;
}

export function legalUrl(siteBaseUrl, lang, page) {
  const base = String(siteBaseUrl || '').replace(/\/$/, '');
  const file = page === 'terms' ? 'terms.html' : 'privacy-policy.html';
  return `${base}/${lang}/${file}`;
}

export function parseWatchlist(raw) {
  if (!raw) return [];
  try {
    const data = typeof raw === 'string' ? JSON.parse(raw) : raw;
    if (!Array.isArray(data)) return [];
    return data.filter((item) => item && typeof item.slug === 'string' && item.slug);
  } catch {
    return [];
  }
}

export function toggleWatch(list, entry) {
  const exists = list.some((item) => item.slug === entry.slug);
  if (exists) return list.filter((item) => item.slug !== entry.slug);
  return [entry, ...list.filter((item) => item.slug !== entry.slug)];
}

export function isWatched(list, slug) {
  return list.some((item) => item.slug === slug);
}

export function findWatchlistUpdates(feed, watchlist, seenIds, lang) {
  const slugs = new Set((watchlist || []).map((item) => item.slug));
  const seen = new Set(seenIds || []);
  const items = feed && Array.isArray(feed.items) ? feed.items : [];
  return items.filter((item) => {
    if (!item || !item.id || !item.slug) return false;
    if (!slugs.has(item.slug)) return false;
    if (lang && item.lang && item.lang !== lang) return false;
    if (seen.has(item.id)) return false;
    return true;
  });
}

export function desiredTopics(options) {
  const notify = options && options.notify;
  if (!notify) return [];
  const tickerPrefix = (options && options.tickerPrefix) || 'ticker-';
  const digestPrefix = (options && options.digestPrefix) || 'digest-';
  const topics = [];
  for (const item of (options && options.watchlist) || []) {
    const topic = topicForSlug(item.slug, tickerPrefix);
    if (topic) topics.push(topic);
  }
  if (options && options.digest) {
    const digest = digestTopic(options.lang, digestPrefix);
    if (digest) topics.push(digest);
  }
  return [...new Set(topics)];
}

export function topicDiff(previous, next) {
  const prev = new Set(previous || []);
  const nxt = new Set(next || []);
  return {
    subscribe: [...nxt].filter((topic) => !prev.has(topic)),
    unsubscribe: [...prev].filter((topic) => !nxt.has(topic)),
  };
}

export function adUnitForRequest(ads) {
  const testBanner = 'ca-app-pub-3940256099942544/6300978111';
  const testApp = 'ca-app-pub-3940256099942544~3347511713';
  if (!ads || ads.useTestAds) {
    return {
      adId: (ads && ads.androidTestBannerAdUnitId) || testBanner,
      isTesting: true,
      appId: (ads && ads.androidTestAppId) || testApp,
    };
  }
  const adId = ads.bannerAdUnitId || '';
  const appId = ads.androidAppId || '';
  if (/REPLACE|^$/.test(adId) || /REPLACE|^$/.test(appId)) {
    return { blocked: true, reason: 'missing-production-id' };
  }
  return { adId, isTesting: false, appId };
}
