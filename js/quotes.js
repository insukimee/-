(function () {
  'use strict';

  // ============================ CONFIG ============================
  // KEY-LESS by default: quotes come from Yahoo Finance, routed through
  // public CORS proxies (no API key needed). Public proxies can be slow
  // or briefly unavailable; the script tries several in order.
  //
  // (Optional) Paste a free Finnhub key (https://finnhub.io) to use a
  // dedicated key-based source instead. Leave empty to stay key-less.
  var FINNHUB_KEY = "";
  // ===============================================================

  var els = document.querySelectorAll('[data-quote]');
  if (!els.length) return;

  function fmt(n) {
    if (n === null || n === undefined || isNaN(n)) return null;
    return Number(n).toLocaleString('en-US', {
      minimumFractionDigits: 2, maximumFractionDigits: 2
    });
  }

  function paint(el, price, change, pct) {
    if (price === null || price === undefined) return;
    var cls = change >= 0 ? 'q-up' : 'q-down';
    var sign = change >= 0 ? '+' : '';

    if (el.classList.contains('card-quote')) {
      el.textContent = '$' + fmt(price);
      if (change !== null && change !== undefined) el.classList.add(cls);
      return;
    }

    var priceEl = el.querySelector('.quote-price');
    var chgEl = el.querySelector('.quote-change');
    if (priceEl) priceEl.textContent = '$' + fmt(price);
    if (chgEl && change !== null && change !== undefined) {
      var pctTxt = (pct === null || pct === undefined) ? '' : (' (' + sign + Number(pct).toFixed(2) + '%)');
      chgEl.textContent = sign + fmt(change) + pctTxt;
      chgEl.classList.add(cls);
    }
  }

  function fetchText(url, ms) {
    var ctrl = ('AbortController' in window) ? new AbortController() : null;
    var t = ctrl ? setTimeout(function () { ctrl.abort(); }, ms || 7000) : null;
    var opts = ctrl ? { signal: ctrl.signal } : {};
    return fetch(url, opts).then(function (r) {
      if (t) clearTimeout(t);
      if (!r.ok) throw new Error('HTTP ' + r.status);
      return r.text();
    }, function (e) { if (t) clearTimeout(t); throw e; });
  }

  // ---- key-based (optional) ----
  function viaFinnhub(sym, el) {
    var url = 'https://finnhub.io/api/v1/quote?symbol=' +
      encodeURIComponent(sym) + '&token=' + FINNHUB_KEY;
    return fetchText(url).then(function (txt) {
      var d = JSON.parse(txt);
      if (d && typeof d.c === 'number' && d.c > 0) { paint(el, d.c, d.d, d.dp); return true; }
      return false;
    });
  }

  // ---- key-less (default): Yahoo via CORS proxies ----
  function yahooUrl(sym) {
    return 'https://query1.finance.yahoo.com/v8/finance/chart/' +
      encodeURIComponent(sym.replace('.', '-')) + '?interval=1d&range=1d';
  }

  // Each candidate returns the raw Yahoo JSON text. `wrap` means the
  // proxy returns {contents:"<json>"} that we must unwrap.
  function candidates(u) {
    var e = encodeURIComponent(u);
    return [
      { url: 'https://api.codetabs.com/v1/proxy/?quest=' + e, wrap: false },
      { url: 'https://api.allorigins.win/raw?url=' + e, wrap: false },
      { url: 'https://api.allorigins.win/get?url=' + e, wrap: true },
      { url: 'https://thingproxy.freeboard.io/fetch/' + u, wrap: false },
      { url: u, wrap: false } // direct (works only if CORS allowed)
    ];
  }

  function parseYahoo(text, wrap, el) {
    var d = JSON.parse(text);
    if (wrap) d = JSON.parse(d.contents);
    var res = d && d.chart && d.chart.result && d.chart.result[0];
    var m = res && res.meta;
    if (!m || m.regularMarketPrice === undefined) return false;
    var price = m.regularMarketPrice;
    var prev = (m.chartPreviousClose !== undefined) ? m.chartPreviousClose : m.previousClose;
    var change = (prev !== undefined && prev !== null) ? (price - prev) : null;
    var pct = (prev) ? (change / prev) * 100 : null;
    paint(el, price, change, pct);
    return true;
  }

  function viaYahoo(sym, el) {
    var list = candidates(yahooUrl(sym));
    var i = 0;
    function attempt() {
      if (i >= list.length) return Promise.resolve(false);
      var c = list[i++];
      return fetchText(c.url)
        .then(function (txt) {
          try { return parseYahoo(txt, c.wrap, el) || attempt(); }
          catch (e) { return attempt(); }
        })
        .catch(function () { return attempt(); });
    }
    return attempt();
  }

  els.forEach(function (el) {
    var sym = el.getAttribute('data-quote');
    if (!sym) return;
    var p = FINNHUB_KEY ? viaFinnhub(sym, el) : viaYahoo(sym, el);
    if (p && p.catch) p.catch(function () { /* keep the — placeholder */ });
  });
})();
