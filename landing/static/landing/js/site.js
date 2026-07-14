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
      if (range.count_for_career === false) return sum;
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
      toggle.setAttribute(
        "aria-expanded",
        menu.classList.contains("hidden") ? "false" : "true",
      );
    });

    menu.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", function () {
        menu.classList.add("hidden");
        toggle.setAttribute("aria-expanded", "false");
      });
    });

    document.addEventListener("keydown", function (event) {
      if (event.key !== "Escape" || menu.classList.contains("hidden")) return;
      menu.classList.add("hidden");
      toggle.setAttribute("aria-expanded", "false");
      toggle.focus();
    });
  }

  function bindInquiryLinks() {
    document.querySelectorAll("[data-inquiry-type]").forEach(function (link) {
      link.addEventListener("click", function (event) {
        var field = document.querySelector("#id_inquiry_type");
        var inquiryType = link.dataset.inquiryType || "";
        if (!field || !inquiryType) return;
        var hasChoice = Array.prototype.some.call(field.options, function (option) {
          return option.value === inquiryType;
        });
        if (!hasChoice) return;
        var contact = document.querySelector("#contact");
        if (!contact) return;
        event.preventDefault();
        field.value = inquiryType;
        contact.scrollIntoView({ behavior: "smooth" });
      });
    });
  }

  function bindConsentToggle(root) {
    var scope = root || document;
    var all = scope.querySelector("#id_agree_all");
    var required = scope.querySelector("#id_agree_privacy");
    var optional = scope.querySelector("#id_agree_marketing");
    if (!all || !required || !optional) return;
    if (all.dataset.bound === "1") return;

    function syncAll() {
      all.checked = required.checked && optional.checked;
    }

    all.addEventListener("change", function () {
      required.checked = all.checked;
      optional.checked = all.checked;
    });

    required.addEventListener("change", syncAll);
    optional.addEventListener("change", syncAll);
    all.dataset.bound = "1";
    syncAll();
  }

  var ANALYTICS_FIELD_ALLOWLIST = [
    "page_key",
    "lead_source",
    "inquiry_type",
    "ad_source",
    "ad_campaign",
    "ad_group",
    "ad_intent",
    "ad_creative",
    "ad_keyword",
    "landing_variant",
    "utm_source",
    "utm_medium",
    "utm_campaign",
    "utm_term",
    "utm_content",
  ];
  var ATTRIBUTION_FIELD_NAMES = [
    "ad_source",
    "ad_campaign",
    "ad_group",
    "ad_intent",
    "ad_creative",
    "ad_keyword",
    "landing_variant",
    "utm_source",
    "utm_medium",
    "utm_campaign",
    "utm_term",
    "utm_content",
  ];
  var URL_ATTRIBUTION_PARAM_MAP = {
    src: "ad_source",
    campaign: "ad_campaign",
    group: "ad_group",
    intent: "ad_intent",
    creative: "ad_creative",
    kw: "ad_keyword",
    landing_variant: "landing_variant",
    utm_source: "utm_source",
    utm_medium: "utm_medium",
    utm_campaign: "utm_campaign",
    utm_term: "utm_term",
    utm_content: "utm_content",
  };
  var ATTRIBUTION_STORAGE_KEY = "quroom_attribution_context";

  function safeAnalyticsValue(value) {
    var cleaned = (value || "").trim();
    if (!cleaned || cleaned.indexOf("@") !== -1 || cleaned.indexOf("%40") !== -1) {
      return "";
    }
    return cleaned.slice(0, 120);
  }

  function readStoredAttribution() {
    try {
      var raw = window.sessionStorage.getItem(ATTRIBUTION_STORAGE_KEY);
      return raw ? JSON.parse(raw) || {} : {};
    } catch (_err) {
      return {};
    }
  }

  function writeStoredAttribution(context) {
    try {
      window.sessionStorage.setItem(
        ATTRIBUTION_STORAGE_KEY,
        JSON.stringify(context),
      );
    } catch (_err) {
      return;
    }
  }

  function currentUrlAttribution() {
    if (typeof URLSearchParams === "undefined") {
      return {};
    }
    var params = new URLSearchParams(window.location.search || "");
    var context = {};
    Object.keys(URL_ATTRIBUTION_PARAM_MAP).forEach(function (paramName) {
      var fieldName = URL_ATTRIBUTION_PARAM_MAP[paramName];
      var value = safeAnalyticsValue(params.get(paramName) || "");
      if (value) {
        context[fieldName] = value;
      }
    });
    return context;
  }

  function attributionContext() {
    var stored = readStoredAttribution();
    var current = currentUrlAttribution();
    var merged = Object.assign({}, stored, current);
    if (Object.keys(current).length) {
      writeStoredAttribution(merged);
    }
    return merged;
  }

  function applyAttributionToForms(root) {
    var context = attributionContext();
    var scope = root || document;
    scope.querySelectorAll("form").forEach(function (form) {
      ATTRIBUTION_FIELD_NAMES.forEach(function (name) {
        var field = form.querySelector("[name='" + name + "']");
        var value = safeAnalyticsValue(context[name] || "");
        if (field && !field.value && value) {
          field.value = value;
        }
      });
    });
  }

  function fieldValue(form, name) {
    var field = form.querySelector("[name='" + name + "']");
    if (!field) return "";
    if (field.type === "checkbox") {
      return field.checked ? "true" : "false";
    }
    return (field.value || "").trim();
  }

  function analyticsPayload(form) {
    var payload = {};
    var context = attributionContext();
    ANALYTICS_FIELD_ALLOWLIST.forEach(function (name) {
      var value = safeAnalyticsValue(fieldValue(form, name) || context[name] || "");
      if (value) {
        payload[name] = value;
      }
    });
    return payload;
  }

  function sendAnalyticsEvent(eventName, payload) {
    if (!eventName) return;

    var eventPayload = payload || {};
    window.dataLayer = window.dataLayer || [];
    window.dataLayer.push(
      Object.assign(
        {
          event: eventName,
        },
        eventPayload,
      ),
    );

    if (typeof window.gtag === "function") {
      window.gtag("event", eventName, eventPayload);
    }
  }

  function handleHtmxAfterRequest(event) {
    var detail = event && event.detail ? event.detail : {};
    var form = detail.elt;
    if (!form || !form.matches || !form.matches("form[data-analytics-event]")) {
      return;
    }

    var xhr = detail.xhr;
    var status = xhr && typeof xhr.status === "number" ? xhr.status : 0;
    if (status < 200 || status >= 300) {
      return;
    }

    sendAnalyticsEvent(form.dataset.analyticsEvent, analyticsPayload(form));
  }

  document.addEventListener("DOMContentLoaded", function () {
    bindMobileMenu();
    bindInquiryLinks();
    updateCareerDuration();
    bindConsentToggle(document);
    applyAttributionToForms(document);
  });

  document.body.addEventListener("htmx:afterSwap", function (event) {
    var target = event && event.detail ? event.detail.target : null;
    if (!target) return;
    if (target.id === "contact-form-wrap" || target.querySelector("#id_agree_all")) {
      bindConsentToggle(target);
    }
    applyAttributionToForms(target);
  });

  document.body.addEventListener("htmx:afterRequest", handleHtmxAfterRequest);
})();
