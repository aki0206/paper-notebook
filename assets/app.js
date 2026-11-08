// 首頁篩選與數學式渲染。沒有 JavaScript 時，所有卡片照常顯示。
(function () {
  const cards = document.getElementById("cards");
  if (cards) {
    const items = Array.from(cards.querySelectorAll(".card"));
    const chips = Array.from(document.querySelectorAll("[data-filter-theme]"));
    const year = document.getElementById("year");
    const q = document.getElementById("q");
    const shown = document.getElementById("shown");
    const empty = document.getElementById("empty");
    let theme = "";

    function apply() {
      const words = q.value.trim().toLowerCase().split(/\s+/).filter(Boolean);
      let n = 0;
      items.forEach(function (card) {
        const ok = (!theme || card.dataset.theme === theme) &&
          (!year.value || card.dataset.year === year.value) &&
          words.every(function (w) { return card.dataset.search.includes(w); });
        card.hidden = !ok;
        if (ok) n++;
      });
      shown.textContent = n;
      empty.hidden = n > 0;
    }

    chips.forEach(function (chip) {
      chip.addEventListener("click", function () {
        theme = chip.dataset.filterTheme;
        chips.forEach(function (c) { c.setAttribute("aria-pressed", String(c === chip)); });
        apply();
      });
    });
    year.addEventListener("change", apply);
    q.addEventListener("input", apply);
  }

  window.addEventListener("load", function () {
    if (window.renderMathInElement) {
      document.querySelectorAll(".math").forEach(function (el) {
        window.renderMathInElement(el, {
          delimiters: [
            { left: "$$", right: "$$", display: true },
            { left: "$", right: "$", display: false }
          ],
          throwOnError: false
        });
      });
    }
  });
})();
