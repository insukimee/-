(function () {
  'use strict';

  // ============================ CONFIG ============================
  // For RELIABLE live quotes, get a FREE API key at https://finnhub.io
  // and paste it between the quotes below. Finnhub allows browser (CORS)
  // requests, so it works on a static site like this.
  //
  // If left empty, the script falls back to a key-less source (Yahoo),
  // which may be blocked by the browser's CORS policy on some networks.
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

    // Compact card variant: element itself holds the price.
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

  function viaFinnhub(sym, el) {
    var url = 'https://finnhub.io/api/v1/quote?symbol=' +
      encodeURIComponent(sym) + '&token=' + FINNHUB_KEY;
    return fetch(url).then(function (r) { return r.json(); }).then(function (d) {
      if (d && typeof d.c === 'number' && d.c > 0) paint(el, d.c, d.d, d.dp);
    });
  }

  function viaYahoo(sym, el) {
    // Yahoo uses a dash for class shares (e.g. MOG-A).
    var ysym = sym.replace('.', '-');
    var url = 'https://query1.finance.yahoo.com/v8/finance/chart/' +
      encodeURIComponent(ysym) + '?interval=1d&range=1d';
    return fetch(url).then(function (r) { return r.json(); }).then(function (d) {
      var res = d && d.chart && d.chart.result && d.chart.result[0];
      var m = res && res.meta;
      if (!m || m.regularMarketPrice === undefined) return;
      var price = m.regularMarketPrice;
      var prev = (m.chartPreviousClose !== undefined) ? m.chartPreviousClose : m.previousClose;
      var change = (prev !== undefined && prev !== null) ? (price - prev) : null;
      var pct = (prev) ? (change / prev) * 100 : null;
      paint(el, price, change, pct);
    });
  }

  els.forEach(function (el) {
    var sym = el.getAttribute('data-quote');
    if (!sym) return;
    var p = FINNHUB_KEY ? viaFinnhub(sym, el) : viaYahoo(sym, el);
    if (p && p.catch) p.catch(function () { /* keep the — placeholder */ });
  });
})();
