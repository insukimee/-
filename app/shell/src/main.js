import { App } from '@capacitor/app';
import { Capacitor, registerPlugin } from '@capacitor/core';
import { Network } from '@capacitor/network';
import { Preferences } from '@capacitor/preferences';
import { PushNotifications } from '@capacitor/push-notifications';
import { Share } from '@capacitor/share';
import { SplashScreen } from '@capacitor/splash-screen';
import { StatusBar, Style } from '@capacitor/status-bar';
import { t } from './i18n.js';
import {
  adUnitForRequest,
  desiredTopics,
  findWatchlistUpdates,
  isBootstrapPath,
  isWatched,
  langFromPath,
  legalUrl,
  localPostPath,
  pageKind,
  parseWatchlist,
  publicPostUrl,
  resolveInitialLang,
  slugFromPath,
  swapLangPath,
  tabForKind,
  tickerFromSlug,
  toggleWatch,
  topicDiff,
} from './pure.mjs';

const KEYS = {
  lang: 'mi.lang',
  disclaimer: 'mi.disclaimerVersion',
  watchlist: 'mi.watchlist',
  notify: 'mi.notify',
  digest: 'mi.digest',
  topics: 'mi.topics',
  seen: 'mi.seenFeed',
  token: 'mi.pushToken',
};

const MiTopics = registerPlugin('MiTopics');
const state = {
  config: null,
  lang: 'ko',
  watchlist: [],
  notify: false,
  digest: false,
  topics: [],
  seen: [],
  online: true,
};

function strings() {
  return t(state.lang);
}

async function prefGet(key) {
  const { value } = await Preferences.get({ key });
  return value;
}

async function prefSet(key, value) {
  await Preferences.set({ key, value: String(value) });
}

function el(tag, attrs, children) {
  const node = document.createElement(tag);
  for (const [key, value] of Object.entries(attrs || {})) {
    if (key === 'text') node.textContent = value;
    else if (key === 'html') node.innerHTML = value;
    else if (value === false || value == null) continue;
    else node.setAttribute(key, value === true ? '' : String(value));
  }
  for (const child of children || []) {
    if (child) node.append(child);
  }
  return node;
}

function icon(name) {
  const paths = {
    home: '<path d="M4 11.5 12 4l8 7.5"/><path d="M6 10.5V20h12v-9.5"/>',
    stocks: '<path d="M4 16l4-5 3 3 5-7"/><path d="M4 20h16"/>',
    economy: '<circle cx="12" cy="12" r="8"/><path d="M4 12h16M12 4c2.5 2.4 2.5 13.6 0 16M12 4c-2.5 2.4-2.5 13.6 0 16"/>',
    watchlist: '<path d="m12 4 2.2 4.6 5 .7-3.6 3.5.9 5.1L12 15.8 7.5 17.9l.9-5.1L4.8 9.3l5-.7L12 4z"/>',
    settings: '<circle cx="12" cy="12" r="3"/><path d="M12 3.5v2.2M12 18.3v2.2M3.5 12h2.2M18.3 12h2.2M6 6l1.6 1.6M16.4 16.4 18 18M18 6l-1.6 1.6M7.6 16.4 6 18"/>',
  };
  const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
  svg.setAttribute('viewBox', '0 0 24 24');
  svg.setAttribute('aria-hidden', 'true');
  svg.innerHTML = paths[name] || '';
  return svg;
}

function toast(message) {
  document.querySelectorAll('.mi-toast').forEach((node) => node.remove());
  const node = el('div', { class: 'mi-toast', role: 'status', text: message });
  document.body.append(node);
  setTimeout(() => node.remove(), 2400);
}

function mountChrome() {
  const s = strings();
  document.querySelectorAll('.mi-boot,.mi-disclaimer,.mi-offline,.mi-tabs,.mi-admock,.mi-consent').forEach((node) => node.remove());
  const boot = el('div', { class: 'mi-boot', id: 'mi-boot' }, [
    el('div', { class: 'mi-kicker', text: 'US Market Insight' }),
    el('p', { text: s.boot }),
  ]);
  const bar = el('button', { class: 'mi-disclaimer', type: 'button', text: s.disclaimerBar });
  bar.addEventListener('click', () => { location.href = '/shell/legal.html'; });
  const offline = el('div', { class: 'mi-offline', id: 'mi-offline', hidden: state.online ? '' : null, text: s.offline });
  if (state.online) offline.setAttribute('hidden', '');
  const ad = el('div', { class: 'mi-admock', id: 'mi-admock', hidden: '', text: s.adMock });
  const tabs = el('nav', { class: 'mi-tabs', id: 'mi-tabs' });
  const kind = pageKind(location.pathname);
  const active = tabForKind(kind);
  const items = [
    ['home', `/${state.lang}/index.html`, s.tabs.home],
    ['stocks', `/${state.lang}/stock-analysis.html`, s.tabs.stocks],
    ['economy', `/${state.lang}/economy-trends.html`, s.tabs.economy],
    ['watchlist', '/shell/watchlist.html', s.tabs.watchlist],
    ['settings', '/shell/settings.html', s.tabs.settings],
  ];
  for (const [name, href, label] of items) {
    const link = el('a', { href, text: label });
    if (name === active) link.setAttribute('aria-current', 'page');
    link.prepend(icon(name));
    tabs.append(link);
  }
  document.body.append(boot, bar, offline, ad, tabs);
  document.body.classList.add('mi-app');
  document.documentElement.lang = state.lang;
}

function hideBoot() {
  document.getElementById('mi-boot')?.remove();
}

function showConsent() {
  const s = strings();
  hideBoot();
  const list = el('ul');
  for (const line of s.consentBullets) list.append(el('li', { text: line }));
  const button = el('button', { class: 'mi-btn', id: 'mi-consent-accept', type: 'button', text: s.consentButton });
  const more = el('button', { class: 'mi-linkish', type: 'button', text: s.consentMore });
  more.addEventListener('click', () => { location.href = '/shell/legal.html?from=consent'; });
  const panel = el('section', { class: 'mi-consent', id: 'mi-consent', role: 'dialog', 'aria-modal': 'true' }, [
    el('div', { class: 'mi-kicker', text: s.consentKicker }),
    el('h1', { text: s.consentTitle }),
    el('p', { text: s.consentLead }),
    list,
    button,
    more,
  ]);
  button.addEventListener('click', async () => {
    await prefSet(KEYS.disclaimer, state.config.disclaimerVersion);
    panel.remove();
    await afterAccepted();
  });
  document.body.append(panel);
}

async function loadConfig() {
  const response = await fetch('/shell/runtime-config.json', { cache: 'no-store' });
  if (!response.ok) throw new Error('runtime config missing');
  return response.json();
}

async function loadState() {
  state.lang = resolveInitialLang(await prefGet(KEYS.lang), navigator.language);
  const pathLang = langFromPath(location.pathname);
  if (pathLang && pathLang !== state.lang && !isBootstrapPath(location.pathname)) {
    state.lang = pathLang;
    await prefSet(KEYS.lang, pathLang);
  }
  state.watchlist = parseWatchlist(await prefGet(KEYS.watchlist));
  state.notify = (await prefGet(KEYS.notify)) === '1';
  state.digest = (await prefGet(KEYS.digest)) === '1';
  state.topics = safeJson(await prefGet(KEYS.topics), []);
  if (!Array.isArray(state.topics)) state.topics = [];
  state.seen = safeJson(await prefGet(KEYS.seen), []);
  if (!Array.isArray(state.seen)) state.seen = [];
}

function safeJson(raw, fallback) {
  if (!raw) return fallback;
  try {
    return JSON.parse(raw);
  } catch {
    return fallback;
  }
}

async function saveWatchlist(list) {
  state.watchlist = list;
  await prefSet(KEYS.watchlist, JSON.stringify(list));
  if (state.notify) await syncTopics();
}

function setOfflineVisible(online) {
  state.online = online;
  document.body.classList.toggle('mi-is-offline', !online);
  const node = document.getElementById('mi-offline');
  if (!node) return;
  if (online) node.setAttribute('hidden', '');
  else node.removeAttribute('hidden');
}

async function initNetwork() {
  try {
    const status = await Network.getStatus();
    setOfflineVisible(!!status.connected);
    await Network.addListener('networkStatusChange', (next) => setOfflineVisible(!!next.connected));
  } catch {
    setOfflineVisible(navigator.onLine);
    window.addEventListener('online', () => setOfflineVisible(true));
    window.addEventListener('offline', () => setOfflineVisible(false));
  }
}

async function initNativeChrome() {
  if (!Capacitor.isNativePlatform()) return;
  try {
    await StatusBar.setOverlaysWebView({ overlay: false });
    await StatusBar.setBackgroundColor({ color: '#0D0D0D' });
    await StatusBar.setStyle({ style: Style.Dark });
  } catch {
    /* Status bar plugin is unavailable outside a native shell. */
  }
  try {
    await SplashScreen.hide();
  } catch {
    /* Splash may already be hidden. */
  }
  await App.addListener('backButton', ({ canGoBack }) => {
    if (document.getElementById('mi-consent')) return;
    if (canGoBack) {
      window.history.back();
      return;
    }
    const kind = pageKind(location.pathname);
    if (kind !== 'home') {
      location.assign(`/${state.lang}/index.html`);
      return;
    }
    App.exitApp();
  });
  await App.addListener('appStateChange', ({ isActive }) => {
    if (isActive) checkFeed(false);
  });
}

function wireLanguageLinks() {
  document.querySelectorAll('a.lang-switch').forEach((anchor) => {
    anchor.addEventListener('click', async () => {
      const href = anchor.getAttribute('href') || '';
      const next = /(^|\/)ja\//.test(href) ? 'ja' : /(^|\/)ko\//.test(href) ? 'ko' : null;
      if (next) await prefSet(KEYS.lang, next);
    });
  });
}

async function sharePost(slug, title) {
  const s = strings();
  const url = publicPostUrl(state.config.siteBaseUrl, state.lang, slug);
  const text = `${title}\n${s.shareDisclaimer}`;
  try {
    await Share.share({ title: 'US Market Insight', text, url, dialogTitle: s.share });
  } catch (error) {
    if (error && error.message && /cancel/i.test(error.message)) return;
    try {
      await navigator.clipboard.writeText(`${text}\n${url}`);
      toast(s.shareCopied);
    } catch {
      toast(url);
    }
  }
}

async function renderPostActions() {
  if (pageKind(location.pathname) !== 'post') return;
  const slug = slugFromPath(location.pathname);
  if (!slug) return;
  const header = document.querySelector('.post-header') || document.querySelector('main');
  if (!header || document.getElementById('mi-post-actions')) return;
  const s = strings();
  const title = (document.querySelector('.post-header h1, h1') || {}).textContent || tickerFromSlug(slug);
  const star = el('button', {
    class: 'mi-textbtn mi-star',
    type: 'button',
    id: 'mi-star',
    text: isWatched(state.watchlist, slug) ? s.starRemove : s.starAdd,
  });
  star.setAttribute('aria-pressed', isWatched(state.watchlist, slug) ? 'true' : 'false');
  star.addEventListener('click', async () => {
    const entry = {
      slug,
      ticker: tickerFromSlug(slug),
      title: title.trim(),
      addedAt: new Date().toISOString(),
    };
    const next = toggleWatch(state.watchlist, entry);
    await saveWatchlist(next);
    const on = isWatched(next, slug);
    star.textContent = on ? s.starRemove : s.starAdd;
    star.setAttribute('aria-pressed', on ? 'true' : 'false');
  });
  const share = el('button', { class: 'mi-textbtn', type: 'button', id: 'mi-share', text: s.share });
  share.addEventListener('click', () => sharePost(slug, title.trim()));
  const row = el('div', { class: 'mi-post-actions', id: 'mi-post-actions' }, [star, share]);
  header.append(row);
}

function renderWatchlist() {
  const root = document.getElementById('mi-page');
  if (!root) return;
  const s = strings();
  root.replaceChildren();
  root.append(el('h1', { text: s.watchTitle }));
  root.append(el('p', { class: 'mi-note', text: s.watchNote }));
  root.append(el('div', { id: 'mi-update-slot' }));
  if (!state.watchlist.length) {
    root.append(el('p', { text: s.watchEmpty }));
    return;
  }
  for (const item of state.watchlist) {
    const card = el('div', { class: 'mi-card' });
    const link = el('a', { href: localPostPath(state.lang, item.slug) });
    link.append(el('strong', { text: `${item.ticker || tickerFromSlug(item.slug)}` }));
    link.append(el('span', { text: item.title || item.slug }));
    const remove = el('button', { class: 'mi-textbtn', type: 'button', text: s.watchRemove });
    remove.addEventListener('click', async () => {
      await saveWatchlist(state.watchlist.filter((row) => row.slug !== item.slug));
      renderWatchlist();
    });
    card.append(link, remove);
    root.append(card);
  }
}

function renderLegal() {
  const root = document.getElementById('mi-page');
  if (!root) return;
  const s = strings();
  const privacy = legalUrl(state.config.siteBaseUrl, state.lang, 'privacy');
  const terms = legalUrl(state.config.siteBaseUrl, state.lang, 'terms');
  root.replaceChildren();
  root.append(el('h1', { text: s.consentTitle }));
  root.append(el('p', { text: s.aboutBody }));
  const list = el('ul');
  for (const line of s.consentBullets) list.append(el('li', { text: line }));
  root.append(list);
  root.append(el('p', {}, [
    el('a', { href: privacy, text: s.privacy }),
  ]));
  root.append(el('p', {}, [
    el('a', { href: terms, text: s.terms }),
  ]));
  root.append(el('p', { class: 'mi-note', text: state.config.siteBaseUrl }));
}

function renderSettings(pushStatus) {
  const root = document.getElementById('mi-page');
  if (!root) return;
  const s = strings();
  root.replaceChildren();
  root.append(el('h1', { text: s.settingsTitle }));
  root.append(el('h2', { text: s.language }));
  const langRow = el('div', { class: 'mi-lang' });
  for (const [code, label] of [['ko', s.langKo], ['ja', s.langJa]]) {
    const button = el('button', { class: 'mi-textbtn', type: 'button', text: label });
    button.setAttribute('aria-pressed', state.lang === code ? 'true' : 'false');
    button.addEventListener('click', async () => {
      await prefSet(KEYS.lang, code);
      const nextPath = swapLangPath(location.pathname, code);
      if (nextPath !== location.pathname) location.assign(nextPath);
      else location.reload();
    });
    langRow.append(button);
  }
  root.append(langRow);

  root.append(el('h2', { text: s.notifications }));
  root.append(el('p', { class: 'mi-note', text: s.notifyLead }));
  root.append(toggleRow(s.notifyOn, state.notify, async (checked) => {
    state.notify = checked;
    await prefSet(KEYS.notify, checked ? '1' : '0');
    const status = checked ? await enablePush() : await syncTopics();
    renderSettings(status || strings().notifyOff);
  }));
  root.append(toggleRow(s.digestOn, state.digest, async (checked) => {
    state.digest = checked;
    await prefSet(KEYS.digest, checked ? '1' : '0');
    if (state.notify) await syncTopics();
  }));
  root.append(el('p', { class: 'mi-note', text: s.digestHelp }));
  root.append(el('p', { class: 'mi-status', id: 'mi-push-status', text: pushStatus || s.notifyOff }));

  const check = el('button', { class: 'mi-textbtn', id: 'mi-feed-check', type: 'button', text: s.feedCheck });
  check.addEventListener('click', () => checkFeed(true));
  root.append(check);
  root.append(el('div', { id: 'mi-feed-result' }));

  root.append(el('h2', { text: s.legal }));
  root.append(el('p', {}, [el('a', { href: '/shell/legal.html', text: s.aboutTitle })]));
  root.append(el('p', {}, [el('a', { href: legalUrl(state.config.siteBaseUrl, state.lang, 'privacy'), text: s.privacy })]));
  root.append(el('p', {}, [el('a', { href: legalUrl(state.config.siteBaseUrl, state.lang, 'terms'), text: s.terms })]));
  root.append(el('h2', { text: s.aboutTitle }));
  root.append(el('p', { text: s.aboutBody }));
  root.append(el('p', { class: 'mi-note', text: `${s.version} ${state.config.version}` }));
  root.append(el('p', { class: 'mi-note', text: `${s.bundle} ${state.config.bundledAt || ''}` }));
}

function toggleRow(label, checked, onChange) {
  const input = el('input', { type: 'checkbox' });
  input.checked = checked;
  input.addEventListener('change', () => onChange(input.checked));
  const row = el('label', { class: 'mi-row mi-switch' }, [
    el('span', { text: label }),
    input,
  ]);
  return row;
}

async function loadFeed() {
  const remoteUrl = `${String(state.config.siteBaseUrl).replace(/\/$/, '')}${state.config.feedPath || '/feed.json'}`;
  try {
    const response = await fetch(remoteUrl, { cache: 'no-store' });
    if (response.ok) {
      const feed = await response.json();
      if (feed && Array.isArray(feed.items)) return { source: 'remote', feed };
    }
  } catch {
    /* Remote feed is optional until the site publishes feed.json. */
  }
  const local = await fetch('/shell/feed.sample.json');
  return { source: 'sample', feed: await local.json() };
}

async function checkFeed(interactive) {
  const s = strings();
  let result;
  try {
    result = await loadFeed();
  } catch {
    return;
  }
  const updates = findWatchlistUpdates(result.feed, state.watchlist, state.seen, state.lang);
  const box = document.getElementById('mi-feed-result');
  if (box) {
    box.replaceChildren();
    const source = result.source === 'remote' ? s.feedRemote : s.feedSample;
    box.append(el('p', { class: 'mi-note', text: source }));
    if (!updates.length) box.append(el('p', { text: s.feedNone }));
    for (const item of updates) {
      const link = el('a', { class: 'mi-card', href: localPostPath(item.lang || state.lang, item.slug), text: item.title || item.ticker });
      box.append(link);
    }
  } else if (updates.length) {
    let host = document.getElementById('mi-updates');
    if (!host) {
      host = el('section', { class: 'mi-updates', id: 'mi-updates' });
      const slot = document.getElementById('mi-update-slot');
      const main = document.querySelector('main');
      if (slot) slot.append(host);
      else if (main) main.prepend(host);
    }
    host.replaceChildren(el('h2', { text: s.updatesTitle }));
    for (const item of updates) {
      host.append(el('a', { class: 'mi-card', href: localPostPath(item.lang || state.lang, item.slug), text: item.title || item.ticker }));
    }
  }
  if (interactive) {
    state.seen = [...new Set([...state.seen, ...updates.map((item) => item.id)])].slice(-200);
    await prefSet(KEYS.seen, JSON.stringify(state.seen));
  }
}

function setPushStatus(text) {
  const node = document.getElementById('mi-push-status');
  if (node) node.textContent = text;
}

async function enablePush() {
  const s = strings();
  if (!Capacitor.isNativePlatform()) {
    setPushStatus(s.notifyWeb);
    await syncTopics();
    return s.notifyWeb;
  }
  let perm;
  try {
    perm = await PushNotifications.requestPermissions();
  } catch {
    setPushStatus(s.notifyUnavailable);
    return s.notifyUnavailable;
  }
  if (!perm || perm.receive !== 'granted') {
    state.notify = false;
    await prefSet(KEYS.notify, '0');
    setPushStatus(s.notifyDenied);
    return s.notifyDenied;
  }
  try {
    await PushNotifications.register();
  } catch {
    setPushStatus(s.notifyUnavailable);
    return s.notifyUnavailable;
  }
  const topicStatus = await syncTopics();
  const status = topicStatus || s.notifyReady;
  setPushStatus(status);
  return status;
}

async function topicCall(method, topic) {
  try {
    await MiTopics[method]({ topic });
    return true;
  } catch {
    return false;
  }
}

async function syncTopics() {
  const s = strings();
  const next = desiredTopics({
    notify: state.notify,
    digest: state.digest,
    lang: state.lang,
    watchlist: state.watchlist,
    tickerPrefix: state.config.push.tickerTopicPrefix,
    digestPrefix: state.config.push.digestTopicPrefix,
  });
  const diff = topicDiff(state.topics, next);
  if (!Capacitor.isNativePlatform()) {
    state.topics = next;
    await prefSet(KEYS.topics, JSON.stringify(next));
    return null;
  }
  let ok = true;
  for (const topic of diff.subscribe) ok = (await topicCall('subscribe', topic)) && ok;
  for (const topic of diff.unsubscribe) ok = (await topicCall('unsubscribe', topic)) && ok;
  if (!ok) return s.notifyUnavailable;
  state.topics = next;
  await prefSet(KEYS.topics, JSON.stringify(next));
  return null;
}

function registerPushListeners() {
  if (!Capacitor.isNativePlatform()) return;
  PushNotifications.addListener('registration', async (token) => {
    const value = token && token.value ? token.value : '';
    if (value) await prefSet(KEYS.token, value);
    setPushStatus(strings().notifyReady);
  });
  PushNotifications.addListener('registrationError', () => {
    setPushStatus(strings().notifyUnavailable);
  });
}

async function startAds() {
  const slot = document.getElementById('mi-admock');
  const platform = Capacitor.getPlatform();
  const request = adUnitForRequest(state.config.ads, platform);
  if (request.blocked) {
    if (slot) {
      slot.removeAttribute('hidden');
      slot.textContent = strings().adFailed;
    }
    return;
  }
  if (!Capacitor.isNativePlatform()) {
    if (slot) slot.removeAttribute('hidden');
    return;
  }
  try {
    const { AdMob, AdmobConsentStatus, BannerAdSize, BannerAdPosition, MaxAdContentRating } = await import('@capacitor-community/admob');
    let consent = await AdMob.requestConsentInfo();
    if (consent.isConsentFormAvailable && consent.status === AdmobConsentStatus.REQUIRED) {
      consent = await AdMob.showConsentForm();
    }
    if (!consent.canRequestAds) {
      if (slot) slot.setAttribute('hidden', '');
      return;
    }
    if (platform === 'ios') {
      try {
        await AdMob.requestTrackingAuthorization();
      } catch {
        /* ATT can be denied. Ads may still load without the advertising identifier. */
      }
    }
    await AdMob.initialize({
      initializeForTesting: request.isTesting === true,
      tagForChildDirectedTreatment: false,
      tagForUnderAgeOfConsent: false,
      maxAdContentRating: MaxAdContentRating.Teen,
    });
    await AdMob.showBanner({
      adId: request.adId,
      adSize: BannerAdSize.ADAPTIVE_BANNER,
      position: BannerAdPosition.BOTTOM_CENTER,
      margin: 72,
      isTesting: request.isTesting === true,
    });
    if (slot) slot.setAttribute('hidden', '');
  } catch {
    if (slot) {
      slot.removeAttribute('hidden');
      slot.textContent = strings().adFailed;
    }
  }
}

async function afterAccepted() {
  hideBoot();
  await renderPostActions();
  if (document.body.dataset.miPage === 'watchlist') renderWatchlist();
  if (document.body.dataset.miPage === 'settings') renderSettings();
  if (document.body.dataset.miPage === 'legal') renderLegal();
  wireLanguageLinks();
  await initNetwork();
  await initNativeChrome();
  registerPushListeners();
  if (state.notify) await enablePush();
  await startAds();
  await checkFeed(false);
}

async function boot() {
  try {
    state.config = await loadConfig();
  } catch {
    return;
  }
  await loadState();
  if (isBootstrapPath(location.pathname)) {
    location.replace(`/${state.lang}/index.html`);
    return;
  }
  mountChrome();
  const accepted = (await prefGet(KEYS.disclaimer)) === state.config.disclaimerVersion;
  const legalDuringConsent = document.body.dataset.miPage === 'legal' && new URLSearchParams(location.search).get('from') === 'consent';
  if (!accepted && !legalDuringConsent) {
    showConsent();
    return;
  }
  await afterAccepted();
}

boot();
