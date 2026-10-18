const allowedRoots = new Set([
  "standards",
  "qa",
  "governance",
  "docs",
  "templates",
  "skills",
]);
const allowedRootFiles = new Set(["README.md", "AGENT_WORKFLOW.md", "CONTRIBUTING.md"]);
const params = new URLSearchParams(window.location.search);
const documentPath = params.get("doc") || "";
const content = document.querySelector("#guide-content");
const repoRoot = new URL("../../", window.location.href);
const quickPathLink = document.querySelector("#quick-path-link");
const quickPathByDocument = {
  "standards/power-apps.md": "../platform/index.html?type=power-apps",
  "standards/power-automate.md": "../platform/index.html?type=power-automate",
  "standards/sharepoint.md": "../platform/index.html?type=sharepoint",
  "standards/integrated-solutions.md": "../platform/index.html?type=integrated",
  "skills/azure-resource-boundary/SKILL.md": "../azure/index.html",
};

if (quickPathByDocument[documentPath]) {
  quickPathLink.href = quickPathByDocument[documentPath];
  quickPathLink.hidden = false;
}

function isAllowedDocument(path) {
  if (!/^[a-zA-Z0-9._/-]+\.md$/.test(path) || path.includes("..")) {
    return false;
  }

  const [root] = path.split("/");
  return allowedRoots.has(root) || allowedRootFiles.has(path);
}

function escapeHtml(value) {
  return value
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function slugify(value) {
  return value
    .toLowerCase()
    .replace(/<[^>]+>/g, "")
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/(^-|-$)/g, "");
}

function sourceUrl() {
  return new URL(`../../${documentPath}`, window.location.href);
}

function resolveLink(target) {
  if (target.startsWith("#")) {
    return target;
  }

  let resolved;
  try {
    resolved = new URL(target, sourceUrl());
  } catch {
    return "#";
  }

  if (!["http:", "https:", "mailto:"].includes(resolved.protocol)) {
    return "#";
  }

  if (resolved.origin !== window.location.origin || !resolved.pathname.endsWith(".md")) {
    return resolved.href;
  }

  const relativePath = decodeURIComponent(resolved.pathname.slice(repoRoot.pathname.length));
  if (!isAllowedDocument(relativePath)) {
    return resolved.href;
  }

  return `./index.html?doc=${encodeURIComponent(relativePath)}${resolved.hash}`;
}

function resolveImage(target) {
  try {
    const resolved = new URL(target, sourceUrl());
    return ["http:", "https:"].includes(resolved.protocol) ? resolved.href : "";
  } catch {
    return "";
  }
}

function renderInline(value) {
  const codeTokens = [];
  let html = escapeHtml(value).replace(/`([^`]+)`/g, (_, code) => {
    const token = `%%CODE${codeTokens.length}%%`;
    codeTokens.push(`<code>${code}</code>`);
    return token;
  });

  html = html.replace(/!\[([^\]]*)\]\(([^)\s]+)(?:\s+&quot;[^&]*&quot;)?\)/g, (_, alt, url) => {
    const source = resolveImage(url);
    return source ? `<img src="${escapeHtml(source)}" alt="${alt}" loading="lazy" />` : alt;
  });
  html = html.replace(/\[([^\]]+)\]\(([^)\s]+)(?:\s+&quot;[^&]*&quot;)?\)/g, (_, label, url) => {
    const href = resolveLink(url);
    const external = href.startsWith("http") && new URL(href).origin !== window.location.origin;
    return `<a href="${escapeHtml(href)}"${external ? ' target="_blank" rel="noreferrer"' : ""}>${label}</a>`;
  });
  html = html
    .replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>")
    .replace(/__([^_]+)__/g, "<strong>$1</strong>")
    .replace(/(?<!\*)\*([^*]+)\*(?!\*)/g, "<em>$1</em>");

  codeTokens.forEach((token, index) => {
    html = html.replace(`%%CODE${index}%%`, token);
  });
  return html;
}

function splitTableRow(line) {
  return line
    .trim()
    .replace(/^\||\|$/g, "")
    .split("|")
    .map((cell) => cell.trim());
}

function isTableSeparator(line) {
  return /^\s*\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|?\s*$/.test(line);
}

function renderMarkdown(markdown) {
  const lines = markdown.replace(/\r\n/g, "\n").split("\n");
  const output = [];
  let index = 0;
  let paragraph = [];

  function flushParagraph() {
    if (!paragraph.length) {
      return;
    }
    output.push(`<p>${renderInline(paragraph.join(" "))}</p>`);
    paragraph = [];
  }

  while (index < lines.length) {
    const line = lines[index];

    if (line.startsWith("```")) {
      flushParagraph();
      const language = line.slice(3).trim();
      const code = [];
      index += 1;
      while (index < lines.length && !lines[index].startsWith("```")) {
        code.push(lines[index]);
        index += 1;
      }
      output.push(
        `<pre><code${language ? ` class="language-${escapeHtml(language)}"` : ""}>${escapeHtml(code.join("\n"))}</code></pre>`,
      );
      index += 1;
      continue;
    }

    const heading = line.match(/^(#{1,6})\s+(.+)$/);
    if (heading) {
      flushParagraph();
      const level = heading[1].length;
      const text = renderInline(heading[2]);
      output.push(`<h${level} id="${slugify(heading[2])}">${text}</h${level}>`);
      index += 1;
      continue;
    }

    if (line.includes("|") && index + 1 < lines.length && isTableSeparator(lines[index + 1])) {
      flushParagraph();
      const headers = splitTableRow(line);
      const rows = [];
      index += 2;
      while (index < lines.length && lines[index].includes("|") && lines[index].trim()) {
        rows.push(splitTableRow(lines[index]));
        index += 1;
      }
      output.push(
        `<div class="table-wrap"><table><thead><tr>${headers
          .map((header) => `<th>${renderInline(header)}</th>`)
          .join("")}</tr></thead><tbody>${rows
          .map(
            (row) =>
              `<tr>${headers
                .map((_, cellIndex) => `<td>${renderInline(row[cellIndex] || "")}</td>`)
                .join("")}</tr>`,
          )
          .join("")}</tbody></table></div>`,
      );
      continue;
    }

    const task = line.match(/^\s*[-*]\s+\[([ xX])\]\s+(.+)$/);
    if (task) {
      flushParagraph();
      const items = [];
      while (index < lines.length) {
        const current = lines[index].match(/^\s*[-*]\s+\[([ xX])\]\s+(.+)$/);
        if (!current) {
          break;
        }
        items.push(
          `<li class="${current[1].toLowerCase() === "x" ? "is-complete" : ""}">${renderInline(current[2])}</li>`,
        );
        index += 1;
      }
      output.push(`<ul class="task-list">${items.join("")}</ul>`);
      continue;
    }

    const unordered = line.match(/^\s*[-*]\s+(.+)$/);
    if (unordered) {
      flushParagraph();
      const items = [];
      while (index < lines.length) {
        const current = lines[index].match(/^\s*[-*]\s+(.+)$/);
        if (!current) {
          break;
        }
        items.push(`<li>${renderInline(current[1])}</li>`);
        index += 1;
      }
      output.push(`<ul>${items.join("")}</ul>`);
      continue;
    }

    const ordered = line.match(/^\s*(\d+)\.\s+(.+)$/);
    if (ordered) {
      flushParagraph();
      const items = [];
      const start = Number(ordered[1]);
      while (index < lines.length) {
        const current = lines[index].match(/^\s*\d+\.\s+(.+)$/);
        if (!current) {
          break;
        }
        items.push(`<li>${renderInline(current[1])}</li>`);
        index += 1;
      }
      output.push(`<ol${start > 1 ? ` start="${start}"` : ""}>${items.join("")}</ol>`);
      continue;
    }

    if (line.startsWith("> ")) {
      flushParagraph();
      const quote = [];
      while (index < lines.length && lines[index].startsWith("> ")) {
        quote.push(lines[index].slice(2));
        index += 1;
      }
      output.push(`<blockquote><p>${renderInline(quote.join(" "))}</p></blockquote>`);
      continue;
    }

    if (/^\s*---+\s*$/.test(line)) {
      flushParagraph();
      output.push("<hr />");
      index += 1;
      continue;
    }

    if (!line.trim()) {
      flushParagraph();
      index += 1;
      continue;
    }

    paragraph.push(line.trim());
    index += 1;
  }

  flushParagraph();
  return output.join("\n");
}

function categoryFor(path) {
  const categories = {
    standards: "Delivery standard",
    qa: "Quality and evidence",
    governance: "Governance",
    templates: "Delivery template",
    skills: "Agent capability",
    docs: "Developer guidance",
  };
  return categories[path.split("/")[0]] || "Repository guidance";
}

function buildTableOfContents() {
  const headings = [...content.querySelectorAll("h2, h3")];
  const toc = document.querySelector("#table-of-contents");

  headings.forEach((heading) => {
    const link = document.createElement("a");
    link.href = `#${heading.id}`;
    link.textContent = heading.textContent;
    if (heading.tagName === "H3") {
      link.style.paddingLeft = "18px";
    }
    toc.appendChild(link);
  });

  if (!headings.length) {
    document.querySelector(".reader-sidebar").hidden = true;
  }
}

function showError(message) {
  document.querySelector("#guide-title").textContent = "Guide unavailable";
  document.querySelector("#guide-summary").textContent =
    "Return to the delivery guide and choose another resource.";
  content.innerHTML = `<div class="reader-error"><div><strong>We could not open this guide.</strong><span>${escapeHtml(message)}</span></div></div>`;
}

async function loadDocument() {
  if (!isAllowedDocument(documentPath)) {
    showError("The requested document path is not allowed.");
    return;
  }

  const response = await fetch(sourceUrl());
  if (!response.ok) {
    showError(`The source returned HTTP ${response.status}.`);
    return;
  }

  const markdown = await response.text();
  const titleMatch = markdown.match(/^#\s+(.+)$/m);
  const firstParagraph = markdown
    .split(/\n\s*\n/)
    .find((block) => block.trim() && !block.trim().startsWith("#") && !block.trim().startsWith("|"));
  const title = titleMatch ? titleMatch[1].trim() : "MGP Guide";

  document.title = `MGP | ${title}`;
  document.querySelector("#guide-title").textContent = title;
  document.querySelector("#guide-category").textContent = categoryFor(documentPath);
  document.querySelector("#guide-summary").textContent = firstParagraph
    ? firstParagraph.replace(/[*_`#]/g, "").trim()
    : "MGP delivery guidance and standards.";
  document.querySelector("#download-source").href = sourceUrl().href;
  document.querySelector("#download-source").download = documentPath.split("/").pop();
  content.innerHTML = renderMarkdown(markdown);
  buildTableOfContents();
}

document.querySelector("#back-button").addEventListener("click", () => {
  if (window.history.length > 1) {
    window.history.back();
  } else {
    window.location.href = "../index.html";
  }
});

loadDocument().catch((error) => {
  showError(error.message);
});
