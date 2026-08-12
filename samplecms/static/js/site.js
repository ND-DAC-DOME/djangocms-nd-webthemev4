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
 * Direct-file Video widgets — play opens an NDT dialog--video modal when the
 * widget is in a page-header hero (controls are clipped by .page-image frames).
 * Elsewhere, play inline with the overlay control.
 */
(function () {
  document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll("[data-video-file]").forEach(function (root) {
      var playButton = root.querySelector(".video-file__play");
      var dialog = root.querySelector("dialog.dialog--video");
      var modalVideo = dialog && dialog.querySelector(".dialog-content video");
      var previewVideo = root.querySelector(".video-file__preview video");
      var inHero = !!root.closest(".page-header");

      if (!playButton) return;

      function openModal() {
        if (!dialog || !modalVideo || typeof dialog.showModal !== "function") {
          return false;
        }
        dialog.showModal();
        document.body.classList.add("has-open-dialog");
        var playPromise = modalVideo.play();
        if (playPromise && typeof playPromise.catch === "function") {
          playPromise.catch(function () {
            /* Controls remain available if autoplay is blocked. */
          });
        }
        return true;
      }

      function closeModalPlayback() {
        document.body.classList.remove("has-open-dialog");
        if (!modalVideo) return;
        modalVideo.pause();
        modalVideo.currentTime = 0;
      }

      function playInline() {
        var video = previewVideo || root.querySelector("video");
        if (!video) return;
        root.classList.add("is-playing");
        video.removeAttribute("muted");
        video.setAttribute("controls", "");
        var playPromise = video.play();
        if (playPromise && typeof playPromise.catch === "function") {
          playPromise.catch(function () {});
        }
      }

      playButton.addEventListener("click", function (event) {
        event.preventDefault();
        if (inHero && openModal()) {
          return;
        }
        playInline();
      });

      if (dialog) {
        dialog.addEventListener("close", closeModalPlayback);
        dialog.addEventListener("click", function (event) {
          if (event.target === dialog) {
            dialog.close();
          }
        });
      }

      if (previewVideo) {
        previewVideo.addEventListener("ended", function () {
          root.classList.remove("is-playing");
          previewVideo.removeAttribute("controls");
          previewVideo.setAttribute("muted", "");
          previewVideo.currentTime = 0;
        });
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
