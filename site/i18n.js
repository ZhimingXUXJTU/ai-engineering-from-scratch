/**
 * i18n.js — Lightweight internationalization for AI Engineering from Scratch
 * Supports English (en) and Chinese (zh). Language saved in localStorage.
 */
(function () {
  var STORAGE_KEY = 'aifs-lang';
  var currentLang = 'zh'; // default to Chinese for beginners

  function initLang() {
    var stored = localStorage.getItem(STORAGE_KEY);
    if (stored === 'en' || stored === 'zh') {
      currentLang = stored;
    }
    applyLang();
  }

  function setLang(lang) {
    if (lang !== 'en' && lang !== 'zh') return;
    currentLang = lang;
    localStorage.setItem(STORAGE_KEY, lang);
    applyLang();
  }

  function getLang() {
    return currentLang;
  }

  function t(key) {
    if (currentLang === 'en') return null; // no translation needed
    if (!window.ZH || !window.ZH.ui) return null;
    return window.ZH.ui[key] || null;
  }

  function applyLang() {
    var root = document.documentElement;
    root.setAttribute('lang', currentLang === 'zh' ? 'zh-CN' : 'en');
    root.classList.remove('lang-en', 'lang-zh');
    root.classList.add('lang-' + currentLang);

    // Update all [data-i18n] elements
    var els = document.querySelectorAll('[data-i18n]');
    for (var i = 0; i < els.length; i++) {
      var el = els[i];
      var key = el.getAttribute('data-i18n');
      var zhText = t(key);
      if (zhText) {
        if (!el.getAttribute('data-en-text')) {
          el.setAttribute('data-en-text', el.textContent);
        }
        el.textContent = zhText;
      } else {
        var enText = el.getAttribute('data-en-text');
        if (enText) el.textContent = enText;
      }
    }

    // Update all [data-i18n-placeholder] elements
    var placeholders = document.querySelectorAll('[data-i18n-placeholder]');
    for (var j = 0; j < placeholders.length; j++) {
      var el2 = placeholders[j];
      var key2 = el2.getAttribute('data-i18n-placeholder');
      var zhText2 = t(key2);
      if (zhText2) {
        if (!el2.getAttribute('data-en-placeholder')) {
          el2.setAttribute('data-en-placeholder', el2.getAttribute('placeholder'));
        }
        el2.setAttribute('placeholder', zhText2);
      } else {
        var enPh = el2.getAttribute('data-en-placeholder');
        if (enPh) el2.setAttribute('placeholder', enPh);
      }
    }

    // Update all [data-i18n-title] elements
    var titles = document.querySelectorAll('[data-i18n-title]');
    for (var k = 0; k < titles.length; k++) {
      var el3 = titles[k];
      var key3 = el3.getAttribute('data-i18n-title');
      var zhText3 = t(key3);
      if (zhText3) {
        if (!el3.getAttribute('data-en-title')) {
          el3.setAttribute('data-en-title', el3.getAttribute('title') || '');
        }
        el3.setAttribute('title', zhText3);
      } else {
        var enTitle = el3.getAttribute('data-en-title');
        if (enTitle) el3.setAttribute('title', enTitle);
      }
    }

    // Update all [data-i18n-aria] elements
    var arias = document.querySelectorAll('[data-i18n-aria]');
    for (var m = 0; m < arias.length; m++) {
      var el4 = arias[m];
      var key4 = el4.getAttribute('data-i18n-aria');
      var zhText4 = t(key4);
      if (zhText4) {
        if (!el4.getAttribute('data-en-aria')) {
          el4.setAttribute('data-en-aria', el4.getAttribute('aria-label') || '');
        }
        el4.setAttribute('aria-label', zhText4);
      } else {
        var enAria = el4.getAttribute('data-en-aria');
        if (enAria) el4.setAttribute('aria-label', enAria);
      }
    }

    // Update lang toggle button
    var toggleBtns = document.querySelectorAll('.lang-toggle');
    for (var n = 0; n < toggleBtns.length; n++) {
      toggleBtns[n].textContent = currentLang === 'zh' ? 'EN' : '中';
      toggleBtns[n].setAttribute('title', currentLang === 'zh' ? 'Switch to English' : '切换到中文');
    }

    // Dispatch event for other scripts to react
    document.dispatchEvent(new CustomEvent('langchange', { detail: { lang: currentLang } }));
  }

  // Get Chinese translation for a phase
  function phaseZh(phaseId) {
    if (currentLang === 'en' || !window.ZH || !window.ZH.phases) return null;
    return window.ZH.phases[phaseId] || null;
  }

  // Get Chinese translation for a glossary term
  function glossaryZh(term) {
    if (currentLang === 'en' || !window.ZH || !window.ZH.glossary) return null;
    return window.ZH.glossary[term] || null;
  }

  // Get Chinese translation for an artifact
  function artifactZh(name) {
    if (currentLang === 'en' || !window.ZH || !window.ZH.artifacts) return null;
    return window.ZH.artifacts[name] || null;
  }

  // Expose API
  window.AIFS_I18N = {
    init: initLang,
    setLang: setLang,
    getLang: getLang,
    t: t,
    apply: applyLang,
    phaseZh: phaseZh,
    glossaryZh: glossaryZh,
    artifactZh: artifactZh,
    isZh: function () { return currentLang === 'zh'; }
  };

  // Auto-init when DOM ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initLang);
  } else {
    initLang();
  }
})();
