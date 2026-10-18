const sharePointInput = document.querySelector("#sharepoint-url");
const generateButton = document.querySelector("#generate-prompt");
const copyPromptButton = document.querySelector("#copy-prompt");
const copySetupButton = document.querySelector("#copy-setup-command");
const promptOutput = document.querySelector("#prompt-output");
const promptText = document.querySelector("#prompt-text");
const urlError = document.querySelector("#url-error");
const promptCopyStatus = document.querySelector("#prompt-copy-status");
const setupCopyStatus = document.querySelector("#setup-copy-status");

const setupCommand = ".\\scripts\\Test-DeveloperSetup.ps1";

function buildPrompt(folderUrl) {
  return `Run MGP solution intake for this approved CSM SharePoint project folder:

${folderUrl}

Use the solution-intake skill and the governed MGP intake standard.

First verify that an approved authenticated SharePoint or Microsoft 365 tool can list and read the folder. If access or permissions are missing, stop and tell me exactly what is required. Do not claim to have reviewed inaccessible content.

Inventory the folder and identify the authoritative charter, scope, user stories, attachments, and supporting documents. Record duplicates, conflicts, missing files, and uncertain source precedence.

Then:
1. Separate confirmed facts, implied requirements, assumptions, and unknowns.
2. Normalize the requirements and derive testable acceptance criteria.
3. Identify Tier 1 blocking questions, capped at eight and routed to named roles.
4. Classify complexity, risk, records impact, and external exposure.
5. Recommend the smallest supportable MGP platform shape and name the requirement forcing each component.
6. Produce the Triage Record, Solution Brief, acceptance-criteria table, platform recommendation, question set, risk-register seed, and Ready/Discovery/Re-scope disposition.

Do not design or build the solution, modify any environment, or change permissions. Stop after the intake disposition and ask for my explicit approval before architecture.`;
}

function validSharePointUrl(value) {
  try {
    const url = new URL(value);
    return url.protocol === "https:" && url.hostname.toLowerCase().endsWith(".sharepoint.com");
  } catch {
    return false;
  }
}

async function copyText(value, statusElement, successMessage) {
  try {
    await navigator.clipboard.writeText(value);
    statusElement.textContent = successMessage;
    statusElement.classList.remove("is-error");
  } catch (error) {
    statusElement.textContent = `Copy failed: ${error.message}`;
    statusElement.classList.add("is-error");
  }
}

generateButton.addEventListener("click", () => {
  const folderUrl = sharePointInput.value.trim();

  if (!validSharePointUrl(folderUrl)) {
    urlError.textContent =
      "Enter an HTTPS SharePoint project-folder URL ending in .sharepoint.com.";
    promptOutput.hidden = true;
    sharePointInput.focus();
    return;
  }

  urlError.textContent = "";
  promptText.textContent = buildPrompt(folderUrl);
  promptOutput.hidden = false;
  promptCopyStatus.textContent = "";
  promptOutput.scrollIntoView({ behavior: "smooth", block: "nearest" });
});

sharePointInput.addEventListener("input", () => {
  urlError.textContent = "";
});

sharePointInput.addEventListener("keydown", (event) => {
  if (event.key === "Enter") {
    event.preventDefault();
    generateButton.click();
  }
});

copyPromptButton.addEventListener("click", () => {
  copyText(promptText.textContent, promptCopyStatus, "Prompt copied. Paste it into Copilot Chat.");
});

copySetupButton.addEventListener("click", () => {
  copyText(setupCommand, setupCopyStatus, "Readiness command copied.");
});
