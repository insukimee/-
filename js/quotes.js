(function () {
  'use strict';

  // ============================ CONFIG ============================
  // KEY-LESS by default: quotes are fetched from Yahoo Finance, with
  // public CORS proxies as automatic fallbacks when the browser blocks
  // the direct request. No API key required.
  //
  // (Optional) For a dedicated key-based source, paste a free Finnhub
  // key here; if set, it takes priority. Leave empty to stay key-less.
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

  // ---- key-based (optional) ----
  function viaFinnhub(sym, el) {
    var url = 'https://finnhub.io/api/v1/quote?symbol=' +
      encodeURIComponent(sym) + '&token=' + FINNHUB_KEY;
    return fetch(url).then(function (r) { return r.json(); }).then(function (d) {
      if (d && typeof d.c === 'number' && d.c > 0) { paint(el, d.c, d.d, d.dp); return true; }
      return false;
    });
  }

  // ---- key-less (default): Yahoo, with CORS-proxy fallbacks ----
  function yahooUrl(sym) {
    // Yahoo uses a dash for class shares (e.g. MOG-A).
    return 'https://query1.finance.yahoo.com/v8/finance/chart/' +
      encodeURIComponent(sym.replace('.', '-')) + '?interval=1d&range=1d';
  }

  function candidates(url) {
    return [
      url,
      'https://corsproxy.io/?url=' + encodeURIComponent(url),
      'https://api.allorigins.win/raw?url=' + encodeURIComponent(url)
    ];
  }

  function parseYahoo(d, el) {
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
    var urls = candidates(yahooUrl(sym));
    var i = 0;
    function attempt() {
      if (i >= urls.length) return Promise.resolve(false);
      return fetch(urls[i++])
        .then(function (r) { return r.json(); })
        .then(function (d) { return parseYahoo(d, el) || attempt(); })
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
