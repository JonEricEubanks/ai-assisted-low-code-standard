const state = {
  documents: [],
  category: "All",
  query: "",
  selectedPath: "",
  selectedDocument: null,
  changeMode: "owner",
};

const elements = {
  shell: document.querySelector("#explorer-shell"),
  accessMessage: document.querySelector("#local-access-message"),
  total: document.querySelector("#catalog-total"),
  categoryList: document.querySelector("#category-list"),
  search: document.querySelector("#document-search"),
  activeFilter: document.querySelector("#active-filter"),
  resultCount: document.querySelector("#result-count"),
  documentList: document.querySelector("#document-list"),
  viewerEmpty: document.querySelector("#viewer-empty"),
  viewerContent: document.querySelector("#viewer-content"),
  viewerCategory: document.querySelector("#viewer-category"),
  viewerTitle: document.querySelector("#viewer-title"),
  viewerPath: document.querySelector("#viewer-path"),
  previewTab: document.querySelector("#preview-tab"),
  sourceTab: document.querySelector("#source-tab"),
  previewPanel: document.querySelector("#preview-panel"),
  sourcePanel: document.querySelector("#source-panel"),
  preview: document.querySelector("#document-preview"),
  source: document.querySelector("#document-source"),
  status: document.querySelector("#viewer-status"),
  copyPath: document.querySelector("#copy-path"),
  copySource: document.querySelector("#copy-source"),
  openFullPreview: document.querySelector("#open-full-preview"),
  editWithCopilot: document.querySelector("#edit-with-copilot"),
  suggestChange: document.querySelector("#suggest-change"),
  changeDialog: document.querySelector("#change-dialog"),
  changeDialogMode: document.querySelector("#change-dialog-mode"),
  changeDialogTitle: document.querySelector("#change-dialog-title"),
  closeChangeDialog: document.querySelector("#close-change-dialog"),
  changeTargetTitle: document.querySelector("#change-target-title"),
  changeTargetPath: document.querySelector("#change-target-path"),
  changeType: document.querySelector("#change-type"),
  changeGoal: document.querySelector("#change-goal"),
  includeImpactReview: document.querySelector("#include-impact-review"),
  generatedChangePrompt: document.querySelector("#generated-change-prompt"),
  changeDialogStatus: document.querySelector("#change-dialog-status"),
  copyChangePath: document.querySelector("#copy-change-path"),
  copyChangePrompt: document.querySelector("#copy-change-prompt"),
};

function isLocalAccess() {
  return (
    window.location.hostname === "localhost" ||
    window.location.hostname === "127.0.0.1"
  );
}

function documentUrl(path) {
  return new URL(`../../${path}`, window.location.href);
}

function guideUrl(path) {
  return new URL(`../guide/index.html?doc=${encodeURIComponent(path)}&embed=1`, window.location.href);
}

function filteredDocuments() {
  const query = state.query.toLowerCase();
  return state.documents.filter((document) => {
    const matchesCategory = state.category === "All" || document.category === state.category;
    const searchable = `${document.title} ${document.summary} ${document.path} ${document.source}`.toLowerCase();
    return matchesCategory && (!query || searchable.includes(query));
  });
}

function makeCategoryButton(label, count) {
  const button = document.createElement("button");
  button.type = "button";
  button.className = state.category === label ? "is-active" : "";
  button.dataset.category = label;

  const name = document.createElement("span");
  name.textContent = label;
  const total = document.createElement("strong");
  total.textContent = count;

  button.append(name, total);
  button.addEventListener("click", () => {
    state.category = label;
    renderCategories();
    renderDocuments();
  });
  return button;
}

function renderCategories() {
  const counts = new Map();
  state.documents.forEach((document) => {
    counts.set(document.category, (counts.get(document.category) || 0) + 1);
  });

  elements.categoryList.replaceChildren(
    makeCategoryButton("All", state.documents.length),
    ...Array.from(counts.entries())
      .sort(([left], [right]) => left.localeCompare(right))
      .map(([category, count]) => makeCategoryButton(category, count)),
  );
}

function createDocumentCard(item) {
  const button = window.document.createElement("button");
  button.type = "button";
  button.className = "document-card";
  if (item.path === state.selectedPath) {
    button.classList.add("is-selected");
  }

  const top = window.document.createElement("span");
  top.className = "document-card-top";
  const category = window.document.createElement("small");
  category.textContent = item.category;
  const source = window.document.createElement("small");
  source.textContent = item.source;
  top.append(category, source);

  const title = window.document.createElement("strong");
  title.textContent = item.title;
  const summary = window.document.createElement("span");
  summary.className = "document-summary";
  summary.textContent = item.summary;
  const path = window.document.createElement("code");
  path.textContent = item.path;

  button.append(top, title, summary, path);
  button.addEventListener("click", () => selectDocument(item));
  return button;
}

function renderDocuments() {
  const documents = filteredDocuments();
  elements.activeFilter.textContent = state.category === "All" ? "All resources" : state.category;
  elements.resultCount.textContent = `${documents.length} ${documents.length === 1 ? "resource" : "resources"}`;

  if (!documents.length) {
    const empty = document.createElement("div");
    empty.className = "no-results";
    const title = document.createElement("strong");
    title.textContent = "No matching resources";
    const detail = document.createElement("span");
    detail.textContent = "Try a different category or search term.";
    empty.append(title, detail);
    elements.documentList.replaceChildren(empty);
    return;
  }

  elements.documentList.replaceChildren(...documents.map(createDocumentCard));
}

function setActiveTab(tab) {
  const showPreview = tab === "preview";
  elements.previewTab.classList.toggle("is-active", showPreview);
  elements.sourceTab.classList.toggle("is-active", !showPreview);
  elements.previewTab.setAttribute("aria-selected", String(showPreview));
  elements.sourceTab.setAttribute("aria-selected", String(!showPreview));
  elements.previewPanel.hidden = !showPreview;
  elements.sourcePanel.hidden = showPreview;
}

async function selectDocument(item) {
  state.selectedPath = item.path;
  state.selectedDocument = item;
  elements.viewerEmpty.hidden = true;
  elements.viewerContent.hidden = false;
  elements.viewerCategory.textContent = item.category;
  elements.viewerTitle.textContent = item.title;
  elements.viewerPath.textContent = item.path;
  elements.preview.src = guideUrl(item.path).href;
  elements.openFullPreview.href = guideUrl(item.path).href;
  elements.source.textContent = "Loading source…";
  elements.status.textContent = "";
  setActiveTab("preview");
  renderDocuments();

  const params = new URLSearchParams(window.location.search);
  params.set("doc", item.path);
  window.history.replaceState({}, "", `${window.location.pathname}?${params.toString()}`);

  try {
    const response = await fetch(documentUrl(item.path));
    if (!response.ok) {
      throw new Error(`The source returned HTTP ${response.status}.`);
    }
    elements.source.textContent = await response.text();
  } catch (error) {
    elements.source.textContent = "Source unavailable.";
    elements.status.textContent = `Could not load ${item.path}: ${error.message}`;
  }
}

async function copyText(value, successMessage) {
  try {
    await navigator.clipboard.writeText(value);
    elements.status.textContent = successMessage;
  } catch (error) {
    elements.status.textContent = `Copy failed: ${error.message}`;
  }
}

function buildChangePrompt() {
  if (!state.selectedDocument) {
    return "";
  }

  const isContributor = state.changeMode === "contributor";
  const goal = elements.changeGoal.value.trim() || "[Describe the requested change here]";
  const impactInstruction = elements.includeImpactReview.checked
    ? "- Search for directly related references, documentation, generated catalogs, and tests; update only the surfaces affected by this change."
    : "- Keep the change limited to the selected file unless another file must change for correctness.";

  return [
    "@workspace",
    "",
    isContributor
      ? "Prepare a governed contribution for the selected MGP repository resource."
      : "Implement a governed update to the selected MGP repository resource.",
    "",
    `Target file: ${state.selectedDocument.path}`,
    `Resource: ${state.selectedDocument.title}`,
    `Category: ${state.selectedDocument.category}`,
    `Change type: ${elements.changeType.value}`,
    "",
    "Requested outcome:",
    goal,
    "",
    "Requirements:",
    "- Read the target file and applicable repository instructions before editing.",
    "- Preserve confirmed facts, assumptions, unknowns, approval boundaries, and lifecycle governance.",
    impactInstruction,
    "- Make precise, reviewable changes and preserve existing behavior outside the request.",
    "- Run the smallest relevant validation and report the exact command and result.",
    "- Summarize changed files, behavior, validation, and any remaining human decision.",
    isContributor
      ? "- Work through a feature branch and pull request. Do not merge, push to a protected branch, or change production."
      : "- Do not commit, push, deploy, or change production unless I explicitly request it.",
  ].join("\n");
}

function updateChangePrompt() {
  elements.generatedChangePrompt.textContent = buildChangePrompt();
  elements.changeDialogStatus.textContent = "";
}

function openChangeDialog(mode) {
  if (!state.selectedDocument) {
    elements.status.textContent = "Select a repository resource before starting a change.";
    return;
  }

  state.changeMode = mode;
  const isContributor = mode === "contributor";
  elements.changeDialogMode.textContent = isContributor ? "Contributor workflow" : "Owner workflow";
  elements.changeDialogTitle.textContent = isContributor ? "Suggest a change" : "Edit with Copilot";
  elements.copyChangePrompt.textContent = isContributor
    ? "Copy contribution prompt"
    : "Copy prompt for Copilot";
  elements.changeTargetTitle.textContent = state.selectedDocument.title;
  elements.changeTargetPath.textContent = state.selectedDocument.path;
  elements.changeGoal.value = "";
  elements.changeType.selectedIndex = 0;
  elements.includeImpactReview.checked = true;
  updateChangePrompt();
  elements.changeDialog.showModal();
  elements.changeGoal.focus();
}

async function copyChangePrompt() {
  if (!elements.changeGoal.value.trim()) {
    elements.changeDialogStatus.textContent = "Describe the requested change before copying the prompt.";
    elements.changeGoal.focus();
    return;
  }

  try {
    await navigator.clipboard.writeText(buildChangePrompt());
    elements.changeDialogStatus.textContent =
      "Prompt copied. Return to Copilot Chat in VS Code, select MGP Delivery, and paste it.";
  } catch (error) {
    elements.changeDialogStatus.textContent = `Copy failed: ${error.message}`;
  }
}

async function loadCatalog() {
  if (!isLocalAccess()) {
    elements.shell.hidden = true;
    elements.accessMessage.hidden = false;
    return;
  }

  try {
    const response = await fetch("./catalog.json");
    if (!response.ok) {
      throw new Error(`The catalog returned HTTP ${response.status}.`);
    }

    const catalog = await response.json();
    if (!Array.isArray(catalog.documents)) {
      throw new Error("The catalog format is invalid.");
    }

    state.documents = catalog.documents;
    elements.total.textContent = state.documents.length;
    renderCategories();
    renderDocuments();

    const requestedPath = new URLSearchParams(window.location.search).get("doc");
    const requestedDocument = state.documents.find((document) => document.path === requestedPath);
    if (requestedDocument) {
      selectDocument(requestedDocument);
    }
  } catch (error) {
    elements.resultCount.textContent = "Catalog unavailable";
    const message = document.createElement("div");
    message.className = "no-results";
    const title = document.createElement("strong");
    title.textContent = "Could not load the repository catalog";
    const detail = document.createElement("span");
    detail.textContent = `${error.message} Run scripts\\Build-AdminCatalog.ps1 and refresh this page.`;
    message.append(title, detail);
    elements.documentList.replaceChildren(message);
  }
}

elements.search.addEventListener("input", (event) => {
  state.query = event.target.value.trim();
  renderDocuments();
});
elements.previewTab.addEventListener("click", () => setActiveTab("preview"));
elements.sourceTab.addEventListener("click", () => setActiveTab("source"));
elements.copyPath.addEventListener("click", () => copyText(state.selectedPath, "Repository path copied."));
elements.copySource.addEventListener("click", () => copyText(elements.source.textContent, "Document source copied."));
elements.editWithCopilot.addEventListener("click", () => openChangeDialog("owner"));
elements.suggestChange.addEventListener("click", () => openChangeDialog("contributor"));
elements.closeChangeDialog.addEventListener("click", () => elements.changeDialog.close());
elements.changeType.addEventListener("change", updateChangePrompt);
elements.changeGoal.addEventListener("input", updateChangePrompt);
elements.includeImpactReview.addEventListener("change", updateChangePrompt);
elements.copyChangePath.addEventListener("click", async () => {
  try {
    await navigator.clipboard.writeText(state.selectedPath);
    elements.changeDialogStatus.textContent = "Repository path copied.";
  } catch (error) {
    elements.changeDialogStatus.textContent = `Copy failed: ${error.message}`;
  }
});
elements.copyChangePrompt.addEventListener("click", copyChangePrompt);

loadCatalog();
