const artifactTypes = {
  intake: {
    title: "Solution Intake",
    eyebrow: "Frame the work",
    description:
      "Turn the CSM handoff into a clear, testable starting point before architecture or build begins.",
    source: "../../templates/solution-intake.md",
    fileName: "solution-intake.md",
    workflow: ["Capture the outcome", "Confirm scope and constraints", "Record the decision"],
    ruleLabel: "Intake rule",
    rule: "Do not begin architecture without an owner, outcome, and testable scope.",
    returnUrl: "../training/index.html#start-solution",
    sections: [
      {
        title: "Frame the request",
        description: "Establish accountability and the measurable business outcome.",
        fields: [
          ["Intake ID", "INT-001", true],
          ["Request date", "", false, "date"],
          ["Sponsor", "Name or role"],
          ["Solution owner", "Name or role", true],
          ["Problem", "What problem needs to be solved?", true, "textarea"],
          ["Desired measurable outcome", "How will success be measured?", true, "textarea"],
        ],
      },
      {
        title: "Define people and scope",
        description: "Make the boundaries visible before choosing a platform.",
        fields: [
          ["Users/personas", "Who will use or support the solution?", true, "textarea"],
          ["In scope", "What must this delivery include?", true, "textarea"],
          ["Out of scope", "What is explicitly excluded?", false, "textarea"],
          ["Current process", "How is the work completed today?", false, "textarea"],
          ["Deadline/constraints", "Dates, dependencies, or fixed constraints", false, "textarea"],
        ],
      },
      {
        title: "Identify technical constraints",
        description: "Capture the information that shapes architecture, risk, and governance.",
        fields: [
          ["Systems/data sources", "SharePoint, Dataverse, SQL, APIs…", false, "textarea"],
          ["Data classification", "Public, internal, confidential…"],
          ["Expected volume", "Users, records, transactions, or frequency"],
          ["Integrations", "Upstream and downstream systems", false, "textarea"],
          ["Accessibility needs", "Personas or standards to support", false, "textarea"],
          ["Security/permission needs", "Roles, access boundaries, or elevated actions", false, "textarea"],
          ["Records/retention needs", "Retention, disposal, legal, or audit needs", false, "textarea"],
          ["Licensing considerations", "Premium connectors, capacity, or user licenses", false, "textarea"],
          ["Support owner", "Team or named owner"],
        ],
      },
      {
        title: "Make it testable",
        description: "Define the proof required to call the outcome complete.",
        fields: [
          ["Acceptance criteria", "One criterion per line with an evidence expectation", true, "textarea"],
          ["Facts", "Confirmed information", false, "textarea"],
          ["Assumptions", "Beliefs that still require confirmation", false, "textarea"],
          ["Unknowns", "Open questions, owners, and target dates", false, "textarea"],
        ],
      },
      {
        title: "Record the recommendation",
        description: "Leave a clear decision for the next person in the lifecycle.",
        fields: [
          ["Risk class", "Low, medium, high, or critical"],
          ["Ready for architecture", "Yes, no, or conditional"],
          ["Required approvers", "Named roles or people"],
          ["Recommended next action", "What should happen next?", true, "textarea"],
        ],
      },
    ],
  },
  release: {
    title: "Release Checklist",
    eyebrow: "Release gate",
    description:
      "Confirm the solution, evidence, operating model, and approvals are ready before deployment.",
    source: "../../templates/release-checklist.md",
    fileName: "release-checklist.md",
    workflow: ["Verify the release", "Resolve every exception", "Capture the decision"],
    ruleLabel: "Release rule",
    rule: "No release proceeds without evidence, rollback readiness, and named approval.",
    returnUrl: "../training/index.html#validate-release",
    checklist: [
      "Approved version and release notes identified",
      "Requirements and critical regression pass",
      "No unresolved Severity 1 or 2 defects",
      "Environment variables and connection references verified",
      "Identities, owners, backups, and permissions verified",
      "Security, accessibility, records, and licensing decisions retained",
      "Monitoring, alerting, support, and escalation ready",
      "Deployment order and prerequisites verified",
      "Rollback procedure tested or explicitly approved",
      "User communication and training ready",
      "Evidence package complete",
      "Named solution owner approval",
      "Named technical/QA approval",
    ],
    decisionFields: [
      ["Release", "Approved, rejected, or conditional", true],
      ["Approvers", "Named approvers", true],
      ["Residual risk", "Accepted risks or exceptions", false, "textarea"],
      ["Rollback trigger", "Observable condition that starts rollback", true, "textarea"],
      ["Evidence package", "Link or evidence package ID", true],
    ],
  },
  handoff: {
    title: "Handoff Checklist",
    eyebrow: "Transfer ownership",
    description:
      "Give the next owner enough context, access, and practice to operate the solution confidently.",
    source: "../../templates/handoff-checklist.md",
    fileName: "handoff-checklist.md",
    workflow: ["Package the context", "Walk through operations", "Confirm ownership"],
    ruleLabel: "Handoff rule",
    rule: "Handoff is complete only when the successor can operate and recover the solution.",
    returnUrl: "../training/index.html#validate-release",
    checklist: [
      "Business purpose, owner, sponsor, and support contacts",
      "Environments and direct links",
      "Component inventory and dependencies",
      "Architecture and data dictionary",
      "Connectors, identities, connections, and licenses",
      "Permissions and security model",
      "Records, retention, sensitivity, and disposal decisions",
      "Deployment and rollback procedure",
      "Monitoring, common failures, recovery, and escalation",
      "Regression pack and test data",
      "Known defects, limitations, risks, and backlog",
      "Change history and release notes",
      "Successor walkthrough completed",
      "Successor independently ran a regression",
      "Successor diagnosed a staged failure",
      "Ongoing owner accepted responsibility",
    ],
  },
};

const params = new URLSearchParams(window.location.search);
const type = params.get("type");
const artifact = artifactTypes[type];
const form = document.querySelector("#artifact-form");
const actionStatus = document.querySelector("#action-status");

function toId(label) {
  return label.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/(^-|-$)/g, "");
}

function escapeMarkdown(value) {
  return value.trim();
}

function createWorkflow() {
  artifact.workflow.forEach((step, index) => {
    const item = document.createElement("li");
    item.innerHTML = `<b>${String(index + 1).padStart(2, "0")}</b>${step}`;
    document.querySelector("#workflow-steps").appendChild(item);
  });
}

function createField(field) {
  const [labelText, placeholder, required = false, type = "text"] = field;
  const label = document.createElement("label");
  const id = toId(labelText);
  const labelContent = document.createElement("span");
  const control =
    type === "textarea" ? document.createElement("textarea") : document.createElement("input");

  labelContent.innerHTML = `${labelText}${required ? ' <b aria-hidden="true">*</b>' : ""}`;
  control.id = id;
  control.name = id;
  control.required = required;
  control.placeholder = placeholder;
  control.dataset.label = labelText;

  if (type === "textarea") {
    control.rows = 4;
  } else {
    control.type = type;
  }

  label.append(labelContent, control);
  return label;
}

function createFormSections() {
  artifact.sections.forEach((section, index) => {
    const heading = document.createElement("div");
    const fields = document.createElement("div");

    heading.className = "form-heading";
    heading.innerHTML = `
      <div>
        <span class="section-number">${String(index + 1).padStart(2, "0")}</span>
        <h2>${section.title}</h2>
        <p>${section.description}</p>
      </div>
    `;
    fields.className = "field-grid field-grid-two artifact-fields";
    section.fields.forEach((field) => fields.appendChild(createField(field)));

    if (index > 0) {
      const divider = document.createElement("div");
      divider.className = "form-divider";
      form.appendChild(divider);
    }

    form.append(heading, fields);
  });
}

function createChecklist() {
  const heading = document.createElement("div");
  const list = document.createElement("div");

  heading.className = "form-heading";
  heading.innerHTML = `
    <div>
      <span class="section-number">01</span>
      <h2>Complete the gate</h2>
      <p>Check each item only after the evidence has been confirmed.</p>
    </div>
  `;
  list.className = "interactive-checklist";

  artifact.checklist.forEach((item, index) => {
    const label = document.createElement("label");
    const checkbox = document.createElement("input");
    const marker = document.createElement("span");
    const text = document.createElement("span");

    checkbox.type = "checkbox";
    checkbox.name = `item-${index}`;
    checkbox.dataset.label = item;
    marker.className = "check-marker";
    text.className = "check-copy";
    text.innerHTML = `<b>${String(index + 1).padStart(2, "0")}</b><strong>${item}</strong>`;
    label.append(checkbox, marker, text);
    list.appendChild(label);
  });

  form.append(heading, list);

  if (artifact.decisionFields) {
    const divider = document.createElement("div");
    const decisionHeading = document.createElement("div");
    const fields = document.createElement("div");

    divider.className = "form-divider";
    decisionHeading.className = "form-heading";
    decisionHeading.innerHTML = `
      <div>
        <span class="section-number">02</span>
        <h2>Record the decision</h2>
        <p>Document approval, remaining risk, and the rollback boundary.</p>
      </div>
    `;
    fields.className = "field-grid field-grid-two artifact-fields";
    artifact.decisionFields.forEach((field) => fields.appendChild(createField(field)));
    form.append(divider, decisionHeading, fields);
  }
}

function initializePage() {
  if (!artifact) {
    window.location.replace("../index.html");
    return;
  }

  document.title = `MGP | ${artifact.title}`;
  document.querySelector("#header-title").textContent = artifact.title;
  document.querySelector("#artifact-eyebrow").textContent = artifact.eyebrow;
  document.querySelector("#artifact-title").textContent = artifact.title;
  document.querySelector("#artifact-description").textContent = artifact.description;
  document.querySelector("#source-link").href = artifact.source;
  document.querySelector("#source-link").download = artifact.fileName;
  document.querySelector("#footer-source-link").href = artifact.source;
  document.querySelector("#footer-source-link").download = artifact.fileName;
  document.querySelector("#rule-label").textContent = artifact.ruleLabel;
  document.querySelector("#rule-text").textContent = artifact.rule;
  document.querySelector("#return-link").href = artifact.returnUrl;
  createWorkflow();

  if (artifact.sections) {
    createFormSections();
  } else {
    createChecklist();
  }

  updateCompletion();
}

function updateCompletion() {
  const checkboxes = [...form.querySelectorAll('input[type="checkbox"]')];
  const requiredFields = [...form.querySelectorAll("[required]")];
  const tracked = checkboxes.length ? checkboxes : requiredFields;
  const completed = checkboxes.length
    ? checkboxes.filter((control) => control.checked).length
    : requiredFields.filter((control) => control.value.trim()).length;
  const percent = tracked.length ? Math.round((completed / tracked.length) * 100) : 0;

  document.querySelector("#completion-count").textContent = `${completed} of ${tracked.length}`;
  document.querySelector("#completion-bar").style.width = `${percent}%`;
}

function validateForm() {
  if (artifact.checklist) {
    const incomplete = [...form.querySelectorAll('input[type="checkbox"]')].some(
      (checkbox) => !checkbox.checked,
    );

    if (incomplete) {
      actionStatus.textContent = "Complete every checklist item before exporting.";
      actionStatus.classList.add("is-error");
      return false;
    }
  }

  if (!form.reportValidity()) {
    actionStatus.textContent = "Complete the required fields before exporting.";
    actionStatus.classList.add("is-error");
    return false;
  }

  actionStatus.classList.remove("is-error");
  return true;
}

function buildMarkdown() {
  let markdown = `# ${artifact.title}\n\n`;

  if (artifact.sections) {
    artifact.sections.forEach((section) => {
      markdown += `## ${section.title}\n\n`;
      section.fields.forEach(([label]) => {
        const control = document.querySelector(`#${toId(label)}`);
        markdown += `- ${label}: ${escapeMarkdown(control.value)}\n`;
      });
      markdown += "\n";
    });
  } else {
    artifact.checklist.forEach((item, index) => {
      const checked = form.elements[`item-${index}`].checked ? "x" : " ";
      markdown += `- [${checked}] ${item}\n`;
    });
    markdown += "\n";

    if (artifact.decisionFields) {
      markdown += "## Decision\n\n";
      artifact.decisionFields.forEach(([label]) => {
        const control = document.querySelector(`#${toId(label)}`);
        markdown += `- ${label}: ${escapeMarkdown(control.value)}\n`;
      });
      markdown += "\n";
    }
  }

  return markdown;
}

function showSuccess(message) {
  actionStatus.textContent = message;
  actionStatus.classList.remove("is-error");
}

form.addEventListener("input", updateCompletion);
form.addEventListener("change", updateCompletion);

document.querySelector("#copy-button").addEventListener("click", async () => {
  if (!validateForm()) {
    return;
  }

  try {
    await navigator.clipboard.writeText(buildMarkdown());
    showSuccess(`${artifact.title} copied as Markdown.`);
  } catch (error) {
    actionStatus.textContent = `Could not copy the artifact: ${error.message}`;
    actionStatus.classList.add("is-error");
  }
});

document.querySelector("#download-button").addEventListener("click", () => {
  if (!validateForm()) {
    return;
  }

  const file = new Blob([buildMarkdown()], { type: "text/markdown;charset=utf-8" });
  const downloadUrl = URL.createObjectURL(file);
  const link = document.createElement("a");

  link.href = downloadUrl;
  link.download = artifact.fileName;
  document.body.appendChild(link);
  link.click();
  link.remove();
  URL.revokeObjectURL(downloadUrl);
  showSuccess(`${artifact.fileName} downloaded.`);
});

document.querySelector("#print-button").addEventListener("click", () => {
  if (!validateForm()) {
    return;
  }

  showSuccess("Opening the print dialog.");
  window.print();
});

initializePage();
