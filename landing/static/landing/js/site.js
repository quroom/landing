(function () {
  function parseCareerRanges() {
    var node = document.getElementById("career-data");
    if (!node) return [];
    try {
      return JSON.parse(node.textContent || "[]");
    } catch (_err) {
      return [];
    }
  }

  function parseDate(dateString) {
    var parts = (dateString || "").split("-");
    if (parts.length !== 3) return null;
    return new Date(Number(parts[0]), Number(parts[1]) - 1, Number(parts[2]));
  }

  function monthsBetween(start, end) {
    var months = (end.getFullYear() - start.getFullYear()) * 12;
    months += end.getMonth() - start.getMonth();
    if (end.getDate() < start.getDate()) {
      months -= 1;
    }
    return Math.max(months, 0);
  }

  function formatCareer(totalMonths) {
    var years = Math.floor(totalMonths / 12);
    var months = totalMonths % 12;
    return years + "년 " + months + "개월";
  }

  function updateCareerDuration() {
    var ranges = parseCareerRanges();
    if (!ranges.length) return;

    var now = new Date();
    var totalMonths = ranges.reduce(function (sum, range) {
      var start = parseDate(range.start);
      var end = range.end ? parseDate(range.end) : now;
      if (!start || !end) return sum;
      return sum + monthsBetween(start, end);
    }, 0);

    var text = formatCareer(totalMonths);
    var heroNode = document.getElementById("career-duration");
    if (heroNode) {
      heroNode.textContent = text;
    }

    var metricNodes = document.querySelectorAll("[data-dynamic-career='true']");
    metricNodes.forEach(function (node) {
      node.textContent = text;
    });
  }

  function bindMobileMenu() {
    var toggle = document.getElementById("menu-toggle");
    var menu = document.getElementById("mobile-menu");
    if (!toggle || !menu) return;

    toggle.addEventListener("click", function () {
      menu.classList.toggle("hidden");
    });

    menu.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", function () {
        menu.classList.add("hidden");
      });
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    bindMobileMenu();
    updateCareerDuration();
  });
})();
