/* Custom Markdown Live Editor & Reader for Django Admin BuildNote */
document.addEventListener("DOMContentLoaded", function () {
  var textarea = document.getElementById("id_body_markdown");
  if (!textarea) return;

  // Build Container Elements
  var container = document.createElement("div");
  container.className = "markdown-editor-container";

  // 1. Toolbar
  var toolbar = document.createElement("div");
  toolbar.className = "markdown-toolbar";
  toolbar.innerHTML = `
    <span class="markdown-toolbar-label">Markdown Tools</span>
    <button type="button" data-action="h2">H2</button>
    <button type="button" data-action="h3">H3</button>
    <button type="button" data-action="h4">H4</button>
    <button type="button" data-action="bold"><strong>B</strong></button>
    <button type="button" data-action="code"><code>Code</code></button>
    <button type="button" data-action="codeblock">CodeBlock</button>
    <button type="button" data-action="checklist">Checklist [-]</button>
    <button type="button" data-action="quote">Quote [&gt;]</button>
    <button type="button" data-action="hr">Divider [---]</button>
    <button type="button" data-action="link">Link [url]</button>
  `;

  // 2. Panes
  var panes = document.createElement("div");
  panes.className = "markdown-panes";

  var editorPane = document.createElement("div");
  editorPane.className = "markdown-pane-editor";

  var previewPane = document.createElement("div");
  previewPane.className = "markdown-pane-preview";
  previewPane.innerHTML = `
    <div class="markdown-preview-header">
      <span>Live Reader (사이트 100% 동일 미리보기)</span>
      <span style="font-size: 10px; color: #94a3b8;">실시간 반영 중</span>
    </div>
    <div class="markdown-preview-body subpage-article-body" id="markdown-live-preview"></div>
  `;

  // Mount DOM
  var parent = textarea.parentNode;
  parent.insertBefore(container, textarea);
  container.appendChild(toolbar);
  container.appendChild(panes);
  panes.appendChild(editorPane);
  panes.appendChild(previewPane);
  editorPane.appendChild(textarea);

  var previewBody = document.getElementById("markdown-live-preview");

  // Inline Escape Helper
  function escapeHtml(text) {
    return text
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }

  // Inline Markdown Renderer
  function renderInline(text) {
    var escaped = escapeHtml(text);
    // Inline code
    escaped = escaped.replace(/`([^`]+)`/g, "<code>$1</code>");
    // Bold
    escaped = escaped.replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");
    // Markdown link
    escaped = escaped.replace(
      /\[([^\]]+)\]\(([^)]+)\)/g,
      '<a href="$2" target="_blank" rel="noopener noreferrer">$1</a>'
    );
    return escaped;
  }

  // Full Parser (Exact match with views.py _render_limited_markdown)
  function parseMarkdown(md) {
    if (!md) return '<p style="color: #94a3b8;">작성된 본문이 없습니다.</p>';

    var lines = md.split("\n");
    var blocks = [];
    var paragraphLines = [];
    var listItems = [];
    var orderedItems = [];
    var quoteLines = [];
    var inCodeBlock = false;
    var codeLang = "";
    var codeLines = [];

    function flushParagraph() {
      if (paragraphLines.length > 0) {
        blocks.push("<p>" + renderInline(paragraphLines.join(" ")) + "</p>");
        paragraphLines = [];
      }
    }

    function flushList() {
      if (listItems.length > 0) {
        blocks.push("<ul>" + listItems.map(function (it) { return "<li>" + it + "</li>"; }).join("") + "</ul>");
        listItems = [];
      }
    }

    function flushOrderedList() {
      if (orderedItems.length > 0) {
        blocks.push("<ol>" + orderedItems.map(function (it) { return "<li>" + it + "</li>"; }).join("") + "</ol>");
        orderedItems = [];
      }
    }

    function flushQuote() {
      if (quoteLines.length > 0) {
        blocks.push("<blockquote>" + quoteLines.map(renderInline).join("<br>") + "</blockquote>");
        quoteLines = [];
      }
    }

    function flushCode() {
      if (codeLines.length > 0) {
        var langAttr = codeLang ? ' class="language-' + escapeHtml(codeLang) + '"' : "";
        blocks.push("<pre><code" + langAttr + ">" + escapeHtml(codeLines.join("\n")) + "</code></pre>");
        codeLines = [];
      }
    }

    function flushAllPending() {
      flushParagraph();
      flushList();
      flushOrderedList();
      flushQuote();
    }

    for (var i = 0; i < lines.length; i++) {
      var rawLine = lines[i];
      var stripped = rawLine.trim();

      // Code Block Fence
      if (stripped.startsWith("```")) {
        if (inCodeBlock) {
          flushCode();
          inCodeBlock = false;
          codeLang = "";
        } else {
          flushAllPending();
          inCodeBlock = true;
          codeLang = stripped.substring(3).trim();
        }
        continue;
      }

      if (inCodeBlock) {
        codeLines.push(rawLine);
        continue;
      }

      // Blank Line
      if (!stripped) {
        flushAllPending();
        continue;
      }

      // Horizontal Rule
      if (stripped === "---" || stripped === "***" || stripped === "___") {
        flushAllPending();
        blocks.push("<hr>");
        continue;
      }

      // Blockquote
      if (stripped.startsWith("> ")) {
        flushParagraph();
        flushList();
        flushOrderedList();
        quoteLines.push(stripped.substring(2).trim());
        continue;
      } else if (quoteLines.length > 0) {
        flushQuote();
      }

      // Headings
      if (stripped.startsWith("#### ")) {
        flushAllPending();
        blocks.push("<h4>" + renderInline(stripped.substring(5).trim()) + "</h4>");
        continue;
      }
      if (stripped.startsWith("### ")) {
        flushAllPending();
        blocks.push("<h3>" + renderInline(stripped.substring(4).trim()) + "</h3>");
        continue;
      }
      if (stripped.startsWith("## ")) {
        flushAllPending();
        blocks.push("<h2>" + renderInline(stripped.substring(3).trim()) + "</h2>");
        continue;
      }
      if (stripped.startsWith("# ")) {
        flushAllPending();
        blocks.push("<h1>" + renderInline(stripped.substring(2).trim()) + "</h1>");
        continue;
      }

      // Unordered List & Checklists
      if (stripped.startsWith("- ") || stripped.startsWith("* ")) {
        flushParagraph();
        flushOrderedList();
        var bulletText = stripped.substring(2).trim();
        var isCheckbox = false;
        var isChecked = false;
        if (bulletText.startsWith("[ ] ")) {
          isCheckbox = true;
          bulletText = bulletText.substring(4);
        } else if (bulletText.startsWith("[x] ") || bulletText.startsWith("[X] ")) {
          isCheckbox = true;
          isChecked = true;
          bulletText = bulletText.substring(4);
        }

        var renderedItem = renderInline(bulletText);
        if (isCheckbox) {
          var chkAttr = isChecked ? " checked" : "";
          renderedItem = '<label class="subpage-checklist-item"><input type="checkbox"' + chkAttr + ' disabled> ' + renderedItem + '</label>';
        }
        listItems.push(renderedItem);
        continue;
      } else if (listItems.length > 0) {
        flushList();
      }

      // Ordered List
      var mOl = stripped.match(/^(\d+)\.\s+(.*)$/);
      if (mOl) {
        flushParagraph();
        flushList();
        orderedItems.push(renderInline(mOl[2].trim()));
        continue;
      } else if (orderedItems.length > 0) {
        flushOrderedList();
      }

      paragraphLines.push(stripped);
    }

    flushAllPending();
    flushCode();
    return blocks.join("\n");
  }

  // Update Preview
  function updatePreview() {
    previewBody.innerHTML = parseMarkdown(textarea.value);
  }

  textarea.addEventListener("input", updatePreview);
  updatePreview(); // Initial render

  // Toolbar Insert Action
  function insertSnippet(before, after) {
    var start = textarea.selectionStart;
    var end = textarea.selectionEnd;
    var text = textarea.value;
    var selected = text.substring(start, end) || "내용";
    var replacement = before + selected + after;

    textarea.value = text.substring(0, start) + replacement + text.substring(end);
    textarea.focus();
    textarea.selectionStart = start + before.length;
    textarea.selectionEnd = start + before.length + selected.length;
    updatePreview();
  }

  toolbar.addEventListener("click", function (e) {
    var btn = e.target.closest("button");
    if (!btn) return;
    var action = btn.getAttribute("data-action");

    switch (action) {
      case "h2":
        insertSnippet("\n## ", "\n");
        break;
      case "h3":
        insertSnippet("\n### ", "\n");
        break;
      case "h4":
        insertSnippet("\n#### ", "\n");
        break;
      case "bold":
        insertSnippet("**", "**");
        break;
      case "code":
        insertSnippet("`", "`");
        break;
      case "codeblock":
        insertSnippet("\n```python\n", "\n```\n");
        break;
      case "checklist":
        insertSnippet("\n- [ ] ", "\n");
        break;
      case "quote":
        insertSnippet("\n> ", "\n");
        break;
      case "hr":
        insertSnippet("\n\n---\n\n", "");
        break;
      case "link":
        insertSnippet("[", "](https://)");
        break;
    }
  });
});
