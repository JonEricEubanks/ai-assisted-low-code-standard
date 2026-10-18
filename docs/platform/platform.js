const platformConfigs = {
  "power-apps": {
    title: "Power Apps quick path",
    icon: "../assets/product-icons/power-apps.svg",
    summary:
      "Use this route for a focused Canvas app change or build. It keeps the full standard available without making you read it before you can take the next action.",
    standard: "../guide/index.html?doc=standards%2Fpower-apps.md",
    launchUrl: "https://make.powerapps.com",
    launchLabel: "Open Power Apps",
    skill: "power-apps-delivery",
    workType: "Power Apps Canvas app",
    useWhen: [
      "Users need a guided interface, multiple screens, validation, or role-based actions.",
      "The approved intake recommends a Canvas app rather than Forms, Survey123, or a SharePoint-only experience.",
      "You are changing an existing app or creating a bounded new app in an approved environment."
    ],
    inputs: [
      "Approved intake baseline and architecture decision.",
      "Environment and existing app ID, or confirmation that this is a new app.",
      "Data sources, required columns, permissions, expected volume, and connector ownership.",
      "Personas, supported devices, acceptance criteria, business owner, and support owner."
    ],
    blockers: [
      "App ownership, environment, data source, or permission boundary is unknown.",
      "Licensing, external-user access, records, or sensitive-data decisions are unresolved.",
      "A multi-device app was created with the Phone form factor instead of Tablet."
    ],
    steps: [
      {
        title: "Confirm the approved baseline",
        text: "Verify requirement IDs, acceptance criteria, personas, data, risk, and the architecture decision.",
        proof: "Proof: approved intake + architecture"
      },
      {
        title: "Open the correct app",
        text: "Confirm environment and app ID. For new multi-device work, start with the Tablet form factor.",
        proof: "Proof: environment + app reference"
      },
      {
        title: "Start the governed build",
        text: "Select MGP Delivery in Copilot Chat, paste the starter prompt, and let it verify tools and blockers.",
        proof: "Proof: agent reports ready to build"
      },
      {
        title: "Build and check continuously",
        text: "Implement the approved slice, handle errors, test responsive states, and run App Checker and accessibility checks.",
        proof: "Proof: checks + requirement evidence"
      },
      {
        title: "Validate, release, hand off",
        text: "Independently test acceptance criteria, complete release approval, and transfer support ownership.",
        proof: "Proof: tests + release + handoff"
      }
    ],
    done: [
      "Every approved acceptance criterion has a passing test and evidence.",
      "Responsive, accessibility, permission, error, empty, loading, and success states are verified.",
      "App/environment/version, data sources, connections, owner, support, and rollback are documented.",
      "Independent review and release approval are complete."
    ]
  },
  "power-automate": {
    title: "Power Automate quick path",
    icon: "../assets/product-icons/power-automate.svg",
    summary:
      "Use this route for a single cloud flow or a bounded flow change. Start with trigger and ownership facts, then make failure and recovery behavior visible.",
    standard: "../guide/index.html?doc=standards%2Fpower-automate.md",
    launchUrl: "https://make.powerautomate.com",
    launchLabel: "Open Power Automate",
    skill: "power-automate-delivery",
    workType: "Power Automate cloud flow",
    useWhen: [
      "Work must run on an event, schedule, approval, notification, or system-to-system action.",
      "The approved intake recommends automation rather than a user-facing app.",
      "You are changing an existing flow or creating a bounded new cloud flow."
    ],
    inputs: [
      "Approved intake baseline and architecture decision.",
      "Environment and existing flow ID, or confirmation that this is a new flow.",
      "Trigger, inputs, outputs, downstream effects, and acceptance criteria.",
      "Owner, connection identity, connection references, secrets boundary, and support route."
    ],
    blockers: [
      "Flow owner, service identity, connection owner, or environment is unknown.",
      "Destructive actions, external communication, or production changes lack explicit approval.",
      "Retry, duplicate, concurrency, failure notification, or recovery behavior is undecided."
    ],
    steps: [
      {
        title: "Confirm the approved baseline",
        text: "Verify trigger, inputs, outputs, owner, downstream effects, risk, and acceptance criteria.",
        proof: "Proof: approved intake + architecture"
      },
      {
        title: "Open the correct flow",
        text: "Confirm environment, flow ID, owner, connections, and whether you are editing or creating.",
        proof: "Proof: environment + flow reference"
      },
      {
        title: "Start the governed build",
        text: "Select MGP Delivery, paste the starter prompt, and let it verify Flow tooling and blockers.",
        proof: "Proof: agent reports ready to build"
      },
      {
        title: "Build for failure",
        text: "Use clear scopes and names; implement idempotency, retry, timeout, logging, alerting, and recovery.",
        proof: "Proof: preflight + failure evidence"
      },
      {
        title: "Validate, release, hand off",
        text: "Test happy, invalid, duplicate, timeout, denied, partial-failure, and recovery paths before approval.",
        proof: "Proof: run IDs + release + handoff"
      }
    ],
    done: [
      "Happy, validation, duplicate, concurrency, connector-failure, and recovery paths are proven.",
      "Connections, connection references, environment variables, owner, monitoring, and alerts are documented.",
      "No secret or sensitive payload is exposed in definitions, logs, or notifications.",
      "Independent review and release approval are complete."
    ]
  },
  sharepoint: {
    title: "SharePoint quick path",
    icon: "../assets/product-icons/sharepoint.svg",
    summary:
      "Use this route for a SharePoint list, library, page, or bounded information-architecture change. Define the structure and permission model before clicking Create.",
    standard: "../guide/index.html?doc=standards%2Fsharepoint.md",
    launchUrl: "https://www.microsoft365.com/launch/sharepoint",
    launchLabel: "Open SharePoint",
    skill: "sharepoint-delivery",
    workType: "SharePoint list, library, or modern page",
    useWhen: [
      "The need is structured data, document management, a modern information page, or lightweight collaboration.",
      "The approved intake recommends SharePoint without requiring a custom app experience.",
      "You are changing an existing site asset or creating a bounded new list, library, or page."
    ],
    inputs: [
      "Approved intake baseline and architecture decision.",
      "Site URL and existing list/library/page reference, or approval to create a new asset.",
      "Columns, types, required/default values, stable internal names, views, volume, and indexes.",
      "Owner, personas, permission inheritance, retention, versioning, integrations, and support."
    ],
    blockers: [
      "Site owner, target site, permission model, or records owner is unknown.",
      "Sensitive data, external access, retention, or inheritance decisions are unresolved.",
      "Integrations depend on column names or schema that have not been approved."
    ],
    steps: [
      {
        title: "Confirm the approved baseline",
        text: "Verify the business entity, site, ownership, schema, access, records, and acceptance criteria.",
        proof: "Proof: approved intake + architecture"
      },
      {
        title: "Confirm the target asset",
        text: "Verify site URL, existing asset reference, permissions, and whether the change is list, library, or page.",
        proof: "Proof: site + asset reference"
      },
      {
        title: "Start the governed build",
        text: "Select MGP Delivery, paste the starter prompt, and let it verify approved SharePoint access and blockers.",
        proof: "Proof: agent reports ready to build"
      },
      {
        title: "Build the approved structure",
        text: "Create schema, views, indexes, versioning, permissions, and integration contracts without silent defaults.",
        proof: "Proof: schema + permission evidence"
      },
      {
        title: "Validate, release, hand off",
        text: "Test volume, views, permissions, retention, integrations, accessibility, recovery, and ownership.",
        proof: "Proof: tests + release + handoff"
      }
    ],
    done: [
      "Schema, internal names, required/default values, views, indexes, and expected volume are verified.",
      "Permission inheritance, personas, retention, versioning, and integrations are tested.",
      "Desktop and phone presentation, accessibility, backup, recovery, owner, and support are documented.",
      "Independent review and release approval are complete."
    ]
  },
  integrated: {
    title: "Integrated solution quick path",
    icon: "../assets/product-icons/power-platform.svg",
    summary:
      "Use this route when more than one platform participates in the outcome. Define boundaries, ownership, and failure behavior before building any component.",
    standard: "../guide/index.html?doc=standards%2Fintegrated-solutions.md",
    launchUrl: "https://make.powerapps.com",
    launchLabel: "Open Power Platform",
    skill: "architecture-and-impact",
    workType: "integrated Power Platform and Microsoft 365 solution",
    useWhen: [
      "The approved solution combines an app, flow, SharePoint asset, connector, or external integration.",
      "A failure or permission change in one component can affect another component.",
      "Architecture and interface ownership must be explicit before platform-specific builds begin."
    ],
    inputs: [
      "Approved intake baseline and architecture decision.",
      "Component inventory, environments, owners, identities, data flow, and interface contracts.",
      "Cross-platform acceptance criteria, failure behavior, monitoring, rollback, and support boundaries."
    ],
    blockers: [
      "Component, data, identity, or ownership boundaries are unknown.",
      "Cross-environment dependencies, licensing, records, or external interfaces are unresolved.",
      "No accountable owner exists for end-to-end failure and recovery."
    ],
    steps: [
      {
        title: "Confirm the approved baseline",
        text: "Verify the end-to-end outcome, requirements, risk, data, owners, and architecture decision.",
        proof: "Proof: approved intake + architecture"
      },
      {
        title: "Map every component",
        text: "Record platforms, environments, identities, interfaces, dependencies, and accountable owners.",
        proof: "Proof: component + dependency map"
      },
      {
        title: "Start with architecture",
        text: "Select MGP Delivery, paste the starter prompt, and resolve cross-platform blockers before build.",
        proof: "Proof: approved component sequence"
      },
      {
        title: "Build bounded components",
        text: "Route each component to its platform skill and retain interface, failure, and evidence contracts.",
        proof: "Proof: component tests + interface tests"
      },
      {
        title: "Validate end to end",
        text: "Test permissions, failures, recovery, monitoring, rollback, release order, and support ownership.",
        proof: "Proof: end-to-end release + handoff"
      }
    ],
    done: [
      "Every component, interface, environment, identity, dependency, and owner is documented.",
      "Component tests and end-to-end failure, recovery, permission, and rollback tests pass.",
      "Release order, monitoring, support boundaries, and coordinated rollback are approved.",
      "Independent review and end-to-end ownership acceptance are complete."
    ]
  }
};

const params = new URLSearchParams(window.location.search);
const requestedType = params.get("type") || "power-apps";
const platformType = Object.hasOwn(platformConfigs, requestedType) ? requestedType : "power-apps";
const config = platformConfigs[platformType];

const elements = {
  icon: document.querySelector("#platform-icon"),
  title: document.querySelector("#platform-title"),
  summary: document.querySelector("#platform-summary"),
  useWhen: document.querySelector("#use-when-list"),
  inputs: document.querySelector("#inputs-list"),
  blockers: document.querySelector("#blockers-list"),
  steps: document.querySelector("#steps-list"),
  standardLink: document.querySelector("#standard-link"),
  launchLink: document.querySelector("#platform-launch-link"),
  done: document.querySelector("#done-list"),
  solutionName: document.querySelector("#solution-name"),
  assetReference: document.querySelector("#asset-reference"),
  prompt: document.querySelector("#platform-prompt"),
  copyButton: document.querySelector("#copy-platform-prompt"),
  promptStatus: document.querySelector("#prompt-status")
};

function renderList(element, items) {
  element.replaceChildren(
    ...items.map((item) => {
      const listItem = document.createElement("li");
      listItem.textContent = item;
      return listItem;
    })
  );
}

function renderSteps() {
  elements.steps.replaceChildren(
    ...config.steps.map((step, index) => {
      const listItem = document.createElement("li");

      const number = document.createElement("span");
      number.className = "step-number";
      number.textContent = String(index + 1).padStart(2, "0");

      const title = document.createElement("strong");
      title.textContent = step.title;

      const text = document.createElement("p");
      text.textContent = step.text;

      const proof = document.createElement("span");
      proof.className = "step-proof";
      proof.textContent = step.proof;

      listItem.append(number, title, text, proof);
      return listItem;
    })
  );
}

function buildPrompt() {
  const solutionName = elements.solutionName.value.trim() || "[project or solution name]";
  const assetReference = elements.assetReference.value.trim() || "[new work or existing asset reference]";

  return `I am working in the MGP Power Desk repository with the MGP Delivery agent.

The solution-intake baseline and architecture decision are approved.

Work type: ${config.workType}
Project or solution: ${solutionName}
Existing asset or target reference: ${assetReference}

Use the ${config.skill} skill and the governed source procedures in this repository.

Before implementation:
1. Confirm the active lifecycle stage.
2. Verify the required platform tools and authenticated access are available.
3. Check the approved baseline for every required input.
4. Separate confirmed facts, assumptions, recommendations, and unknowns.
5. Stop and list blockers instead of inventing missing details.

If ready, give me the exact first bounded action, the evidence to capture, and the approval required before the next stage. Do not make production, permission, retention, or destructive changes without explicit approval.`;
}

function renderPrompt() {
  elements.prompt.textContent = buildPrompt();
  elements.promptStatus.textContent = "";
}

async function copyPrompt() {
  const prompt = buildPrompt();
  try {
    await navigator.clipboard.writeText(prompt);
    elements.promptStatus.textContent = "Prompt copied. Paste it into GitHub Copilot Chat with MGP Delivery selected.";
  } catch {
    elements.promptStatus.textContent = "Copy was blocked. Select the prompt text above and copy it manually.";
  }
}

document.title = `MGP | ${config.title}`;
elements.icon.src = config.icon;
elements.title.textContent = config.title;
elements.summary.textContent = config.summary;
elements.standardLink.href = config.standard;
elements.launchLink.href = config.launchUrl;
elements.launchLink.firstChild.textContent = `${config.launchLabel} `;
document
  .querySelector(`[data-platform-link="${platformType}"]`)
  ?.setAttribute("aria-current", "page");
renderList(elements.useWhen, config.useWhen);
renderList(elements.inputs, config.inputs);
renderList(elements.blockers, config.blockers);
renderList(elements.done, config.done);
renderSteps();
renderPrompt();

elements.solutionName.addEventListener("input", renderPrompt);
elements.assetReference.addEventListener("input", renderPrompt);
elements.copyButton.addEventListener("click", copyPrompt);
