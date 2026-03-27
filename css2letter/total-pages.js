(function () {
  function updateTotalPages(rootSelector = "#print-root") {
    const root = document.querySelector(rootSelector);
    if (!root) return;

    const total = root.querySelectorAll(".page").length || 1;
    root.querySelectorAll(".pageno").forEach((el) => {
      el.dataset.total = String(total);
    });
  }

  window.updateTotalPages = updateTotalPages;

  window.addEventListener("DOMContentLoaded", () => updateTotalPages());
  window.addEventListener("beforeprint", () => updateTotalPages());
})();
