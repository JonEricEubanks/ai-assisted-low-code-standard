const form = document.querySelector("#test-case-form");
const copyButton = document.querySelector("#copy-button");
const downloadButton = document.querySelector("#download-button");
const printButton = document.querySelector("#print-button");
const actionStatus = document.querySelector("#action-status");

function valueOf(id) {
  return document.querySelector(`#${id}`).value.trim();
}

function showStatus(message, isError = false) {
  actionStatus.textContent = message;
  actionStatus.classList.toggle("is-error", isError);
}

function validateForm() {
  const defectId = document.querySelector("#defect-id");
  defectId.setCustomValidity(
    valueOf("status") === "Failed" && !defectId.value.trim()
      ? "Enter a Defect ID when the test status is Failed."
      : "",
  );

  if (form.reportValidity()) {
    return true;
  }

  showStatus("Complete the required fields before exporting.", true);
  return false;
}

function buildMarkdown() {
  return `# Test Case

- Test ID: ${valueOf("test-id")}
- Requirement ID: ${valueOf("requirement-id")}
- Risk: ${valueOf("risk")}
- Environment: ${valueOf("environment")}
- Solution version: ${valueOf("solution-version")}
- Persona: ${valueOf("persona")}
- Test data: ${valueOf("test-data")}
- Executor: ${valueOf("executor")}
- Date/time: ${valueOf("date-time")}

## Preconditions

${valueOf("preconditions")}

## Steps

${valueOf("steps")}

## Expected result

${valueOf("expected-result")}

## Actual result

${valueOf("actual-result")}

- Status: ${valueOf("status")}
- Evidence IDs: ${valueOf("evidence-ids")}
- Defect ID: ${valueOf("defect-id")}
- Reviewer: ${valueOf("reviewer")}
`;
}

copyButton.addEventListener("click", async () => {
  if (!validateForm()) {
    return;
  }

  try {
    await navigator.clipboard.writeText(buildMarkdown());
    showStatus("Test case copied as Markdown.");
  } catch (error) {
    showStatus(`Could not copy the test case: ${error.message}`, true);
  }
});

downloadButton.addEventListener("click", () => {
  if (!validateForm()) {
    return;
  }

  const fileName = `${valueOf("test-id").replace(/[^a-z0-9_-]/gi, "-") || "test-case"}.md`;
  const file = new Blob([buildMarkdown()], { type: "text/markdown;charset=utf-8" });
  const downloadUrl = URL.createObjectURL(file);
  const link = document.createElement("a");

  link.href = downloadUrl;
  link.download = fileName;
  document.body.appendChild(link);
  link.click();
  link.remove();
  URL.revokeObjectURL(downloadUrl);
  showStatus(`${fileName} downloaded.`);
});

printButton.addEventListener("click", () => {
  if (!validateForm()) {
    return;
  }

  showStatus("Opening the print dialog.");
  window.print();
});
