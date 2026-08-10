/*!
 * Load NDT4 icon sprite (academic-mark, mobile-mark, icons)
 */
(function (window, document) {
  "use strict";
  if (
    !document.createElementNS ||
    !document.createElementNS("http://www.w3.org/2000/svg", "svg").createSVGRect
  ) {
    return;
  }

  var rev = "ndt4-icons-1";
  var storageKey = "inlineSVGdata";
  var revKey = "inlineSVGrev";
  var spriteUrl = "/static/svg/icons-nd-base.svg";
  var hasStorage = "localStorage" in window && window.localStorage !== null;
  var svgText;

  function inject() {
    document.body.insertAdjacentHTML("afterbegin", svgText);
  }

  function whenReady() {
    if (document.body) {
      inject();
    } else {
      document.addEventListener("DOMContentLoaded", inject);
    }
  }

  if (hasStorage && localStorage.getItem(revKey) === rev) {
    svgText = localStorage.getItem(storageKey);
    if (svgText) {
      whenReady();
      return;
    }
  }

  try {
    var xhr = new XMLHttpRequest();
    xhr.open("GET", spriteUrl, true);
    xhr.onload = function () {
      if (xhr.status >= 200 && xhr.status < 400) {
        svgText = xhr.responseText;
        whenReady();
        if (hasStorage) {
          localStorage.setItem(storageKey, svgText);
          localStorage.setItem(revKey, rev);
        }
      }
    };
    xhr.send();
  } catch (e) {
    /* sprite optional for text-only fallback */
  }
})(window, document);

/*!
 * Person page contact fields — show rows with content
 */
(function () {
  document.addEventListener("DOMContentLoaded", function () {
    ["office", "phone", "email"].forEach(function (key) {
      var display = document.getElementById(key + "-display");
      var title = document.getElementById(key + "-title");
      if (!display || !title) return;
      if (display.textContent.trim().length > 0) {
        title.classList.remove("person-contact-hidden");
        display.classList.remove("person-contact-hidden");
      }
    });
  });
})();

/*!
 * NDT4 tabs — progressive enhancement for .nav-tabs / .tab-panel markup
 */
(function () {
  document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".nav-tabs").forEach(function (nav) {
      var tabs = nav.querySelectorAll(".tab");
      var panels = nav.parentElement.querySelectorAll(".tab-panel");
      if (!tabs.length || !panels.length) return;

      tabs.forEach(function (tab, index) {
        tab.addEventListener("click", function (event) {
          event.preventDefault();
          tabs.forEach(function (item) {
            item.classList.remove("active");
            item.setAttribute("aria-selected", "false");
          });
          panels.forEach(function (panel) {
            panel.hidden = true;
          });
          tab.classList.add("active");
          tab.setAttribute("aria-selected", "true");
          if (panels[index]) {
            panels[index].hidden = false;
          }
        });
      });
    });
  });
})();
