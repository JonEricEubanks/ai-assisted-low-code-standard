# Test Plan — FOIA Public Intake Flow

Covers the required validation list in `standards/power-automate.md`. All data is synthetic.
Every case records: inputs, expected `FOIA Pilot Requests` row, expected `FOIA Pilot Records`
files, expected emails, expected run status, and the evidence to capture (run ID, action
results, screenshot per `standards/visual-verification.md`).

Conventions:

- "Officer" = `mgp_FOIAOfficerEmail`. "Mailbox" = `mgp_FOIASharedMailbox`. Use pilot
  test mailboxes only; never a real requester address.
- `D` = Central-time date the run starts. Expected `DueDate` is computed from `D` per
  `flow-design.md` §6 (weekday +7, Sat +9, Sun +8).
- "Row" columns not listed are expected empty/null. Always expected on a created row:
  `IntakeMethod=Online Form`, `OverallStatus=New`, `ReceivedDate=D`, `DueDateConfirmed=false`,
  `SourceSubmissionId=<globalid>`, `CurrentStageNotes` contains the correlation ID.
- Submit through the **published public survey URL** (not Survey123 Connect preview) so the
  webhook fires exactly as it will for the public.

## A. Definition validation and preflight (before any run)

| ID | Check | Expected |
|---|---|---|
| PF-01 | Strip `_todo` keys; import definition; open designer | Designer loads; no action shows a configuration-warning badge; all three connection references resolved |
| PF-02 | Flow checker | 0 errors. Warnings only for known items (none expected) |
| PF-03 | Environment variables | All 10 `mgp_FOIA*` variables have current values in the target environment |
| PF-04 | Trigger registration | Saving the flow registers a webhook on the Survey123 form (visible in survey settings → Webhooks) |
| PF-05 | Designer screenshot | Full-page capture `flow-designer-1366-<yyyymmdd-hhmm>.png` in evidence folder; every scope expanded one level |

## B. Functional cases

### TC-01 Happy path — single non-police department, email, no attachment

| | |
|---|---|
| Inputs | First `Ada`, Last `Lovelace`, Email `ada.test@example.com`, Phone `708-555-0101`, Delivery `Electronic`, Description `Copies of the FY2025 approved budget ordinance.`, Departments = `Finance`, Commercial `No`, Certified `No`, FeeWaiver `No` |
| Expected row | `Title=Lovelace, Ada`; `RequestRoute=Non-Police`; `PrimaryDepartment=Finance`; `RequesterEmail=ada.test@example.com`; `DueDate` per rule; `CommercialPurpose=No`; `DeliveryFormat=Electronic`; `CertifiedCopies=No`; `FeeWaiverRequested=No` |
| Expected files | none |
| Expected emails | Receipt → `ada.test@example.com` from Mailbox, subject `FOIA request received - #<ID>`, body has request number, date, summary, no links. Staff → Officer, subject `New FOIA request #<ID> - Non-Police - Finance`, body has deep link ending `&RequestId=<ID>`, `Attachments filed: 0`, `Receipt email: Sent` |
| Run status | Succeeded. `Scope_Catch_NotifyFailure` Skipped. `Compose_RunSummary.receiptStatus=Succeeded` |
| Evidence | Run ID; `run-detail-1366-*.png` showing Create item outputs and both email actions Succeeded |

### TC-02 Happy path — Police only

| | |
|---|---|
| Inputs | As TC-01 but Departments = `Police_Department`, Description `Incident report for 2026-09-30 at 1000 Sterling Ave (synthetic).` |
| Expected row | `RequestRoute=Police`; `PrimaryDepartment=Police Department` |
| Expected emails | Receipt sent; Staff subject `… - Police - Police Department` |
| Run status | Succeeded |

### TC-03 Happy path — multi-department including Police

| | |
|---|---|
| Inputs | Departments = `Police_Department,Public_Works_Department` |
| Expected row | `RequestRoute=Multi-Department`; `PrimaryDepartment=Administration`; `CurrentStageNotes` contains `Police Department; Public Works Department` |
| Expected emails | Staff subject `… - Multi-Department - Administration` |
| Run status | Succeeded |

### TC-04 Happy path — no department selected

| | |
|---|---|
| Inputs | Departments left blank |
| Expected row | `RequestRoute=Unassigned`; `PrimaryDepartment=Administration`; `CurrentStageNotes` contains `Departments selected: ` followed by nothing |
| Run status | Succeeded. `Filter_array_DepartmentTitles` output `[]` |

### TC-05 Attachment present — fee waiver with file

| | |
|---|---|
| Inputs | As TC-01 plus FeeWaiver `Yes`, attach `feewaiver-synthetic.pdf` (≈50 KB) |
| Expected row | `FeeWaiverRequested=Yes` |
| Expected files | One file in `FOIA Pilot Records` named `<ID>-FeeWaiver-<attId>-feewaiver-synthetic.pdf`; `Request=<ID>`; `DocumentType=Request`; `RedactionStatus=Not Reviewed`; `Sensitivity=Internal`; `IsFinalResponse=No`; `Notes` has source attachment id and correlation; file opens and matches the upload byte-for-byte (compare size) |
| Expected emails | Staff body `Attachments filed: 1` |
| Run status | Succeeded. `Apply_to_each_Attachment` 1 iteration, all three inner actions Succeeded |

### TC-06 Attachment absent with fee waiver = Yes

| | |
|---|---|
| Inputs | FeeWaiver `Yes`, no file (only possible if the survey `required` rule is relaxed in a test copy; otherwise record as *not reachable from the published form* and skip) |
| Expected | `Compose_AttachmentList=[]`; loop skipped; row created; staff body `Attachments filed: 0` |
| Run status | Succeeded |

### TC-07 Idempotent retry — same submission twice

| | |
|---|---|
| Setup | Complete TC-01. Note its run ID and row ID. |
| Action | In run history, **Resubmit** the TC-01 run (same trigger payload, same `globalid`). |
| Expected row | No new row. Count of rows with that `SourceSubmissionId` remains 1. |
| Expected files/emails | None |
| Run status | Succeeded via `Terminate_DuplicateSkipped`. `Compose_Log_DuplicateSkipped.existingRequestId` = original row ID. Later scopes not executed. |
| Evidence | Both run IDs; list filtered on `SourceSubmissionId` showing one row |

### TC-08 Concurrent submissions

| | |
|---|---|
| Action | Two testers submit distinct responses within 5 seconds. |
| Expected | Two runs, processed one after the other (trigger concurrency 1); two rows with distinct `SourceSubmissionId`; 2 receipts, 2 staff emails. No cross-contamination of values. |
| Run status | Both Succeeded |

### TC-09 No requester email

| | |
|---|---|
| Inputs | Delivery `Paper`, Email blank, full postal address, Departments `Building_Department` |
| Expected row | `RequesterEmail` empty; `DeliveryFormat=Paper`; address fields populated; `RequestRoute=Non-Police`; `PrimaryDepartment=Building Department` |
| Expected emails | **No receipt.** Staff email sent with `Receipt email: Skipped - no valid requester email` |
| Run status | Succeeded. `Condition_SendReceipt=false`; `Compose_Log_ReceiptSkipped` present |

### TC-10 Invalid email format

| | |
|---|---|
| Inputs | Delivery `Paper` (so the survey does not enforce the regex), Email `not-an-email` |
| Expected row | `RequesterEmail=not-an-email` (raw value stored for staff correction) |
| Expected emails | No receipt; staff email shows `Skipped` |
| Run status | Succeeded. `Compose_IsRequesterEmailValid=false` |
| Variants | Also run `a@b` (no dot after @) and ` MIXED@Example.COM ` (expect valid, stored lower-cased and trimmed, receipt sent) |

### TC-11 Weekend ReceivedDate

| | |
|---|---|
| Action | Submit on a Saturday and again on a Sunday (Central time). If scheduling is impractical, temporarily set `mgp_FOIATimeZone` to a zone where the current date is Sat/Sun and record the substitution. |
| Expected row | Saturday `D` → `DueDate = D+9` (a Monday). Sunday `D` → `DueDate = D+8` (a Monday). Weekday control → `D+7`. All `DueDateConfirmed=false`. |
| Run status | Succeeded |

### TC-12 SharePoint create failure

| | |
|---|---|
| Setup | In a **test copy** of the flow, change `item/RequestRoute/Value` to `ZZ-Invalid` (a choice value that does not exist), or temporarily remove Contribute from the service account on the Requests list. |
| Expected row | None created |
| Expected files/emails | No receipt, no staff notification. **Error alert** → Officer, importance High, subject `FOIA intake flow FAILED - correlation <runId>`, body contains correlation ID, submission ID, `Request number: not created`, failed action `Create_item_FOIARequest` with SharePoint error code/message, run link. Body contains **no** requester name/email/address. |
| Run status | **Failed** with code `FOIAIntakeFailed`. `Scope_Try_Attachments` and `Scope_Try_Notify` Skipped; `Scope_Catch_NotifyFailure` Succeeded; `Scope_Finally_Log` Succeeded; `Terminate_Failed` executed. |
| Also verify | `Filter_array_FailedActions` ran without error although two scopes were skipped (confirms the `result()` `_todo`). If it errored, apply the fallback noted in `flow-design.md` §4.6 and re-run. |
| Evidence | `run-detail-1366-*.png` of the failed run with Catch expanded; copy of the alert email |

### TC-13 Department lookup not found

| | |
|---|---|
| Setup | In `FOIA Pilot Departments`, temporarily rename `Finance` to `Finance Dept` (restore afterwards). Submit with Departments `Finance`. |
| Expected row | None created |
| Expected emails | Error alert only; failed action `Compose_RaiseError_DepartmentNotFound`, message starts `DepartmentNotFound: no FOIA Pilot Departments item with Title = Finance` |
| Run status | Failed (`FOIAIntakeFailed`) |
| Recovery | Restore the title; **Resubmit** the failed run → new row created (no duplicate because the first attempt created nothing). Record the second run ID. |

### TC-14 Missing submission ID (payload guard)

| | |
|---|---|
| Setup | Not reachable from Survey123 in normal operation. Test by resubmitting a saved run after editing the payload in a test copy whose trigger is replaced with a manual HTTP trigger carrying the same JSON minus `globalid`/`objectid`/`result.globalId`. If that harness is unavailable, record as *design-reviewed, not executed*. |
| Expected | No row; error alert with `MissingSubmissionId`; run Failed |

### TC-15 Partial failure — attachment step fails after create

| | |
|---|---|
| Setup | Test copy: set `mgp_FOIARecordsLibraryFolderPath` to a non-existent folder. Submit TC-05 inputs. |
| Expected row | Row **is** created (Create succeeded) |
| Expected files | none |
| Expected emails | **No receipt, no staff notification.** Error alert shows `Request number: <ID>` and failed action `Apply_to_each_Attachment` / `Create_file_RecordsLibrary`. |
| Run status | Failed |
| Recovery | Restore the variable. Resubmit → `DuplicateSkipped` (row already exists) — confirms the documented limitation that attachments are **not** re-filed. Officer uploads the file manually and tags it; record that manual step. |

### TC-16 Email send failure (connector/auth)

| | |
|---|---|
| Setup | Test copy: set `mgp_FOIASharedMailbox` to a mailbox the service account has no Send As rights on. Submit TC-01 inputs. |
| Expected | Row created; attachments n/a; receipt action **Failed** (403/ErrorSendAsDenied); Catch runs; error alert **also fails** (same mailbox); `Scope_Finally_Log` still runs; `Condition_FailureOccurred` true → `Terminate_Failed`. |
| Run status | Failed — never Succeeded. Platform "flow run failed" notification to the owner is the backstop alert. |

### TC-17 Permission / service-account continuity

| | |
|---|---|
| Check | Flow owner = service account; connection references all bound to the service account, not a developer; service account has Contribute on Requests, Departments (read), Records; Send As on Mailbox; ArcGIS org role that can read the survey's feature layer and attachments. |
| Expected | Documented in README; a run executed while the developer account is signed out of all connections still Succeeds. |

### TC-18 Throttling / timeout behaviour

| | |
|---|---|
| Check | Review `Get_attachment_from_URL` and `Create_file_RecordsLibrary` have `timeout PT2M`; `Create_item_FOIARequest` retry policy `none`; other actions default retry. Submit TC-05 with a 20 MB synthetic PDF. |
| Expected | Succeeds within timeout, or fails cleanly through Catch with a timeout error — never hangs or partially tags a file. |

## C. Approval paths

Not applicable — this flow contains no approval actions (decision 4: due date is confirmed
by a human in the app, not via an approval). Record "N/A — no approvals in scope" in the
evidence sheet.

## D. Monitoring and support

| ID | Check | Expected |
|---|---|---|
| MS-01 | `Compose_RunSummary` on a TC-01 run | JSON shows correlationId, submissionId, requestNumber, route, primaryDepartment, dueDateSuggested, receiptStatus `Succeeded`, catchStatus `Skipped` |
| MS-02 | Error alert content review (TC-12, TC-13, TC-15) | Contains correlation ID + submission ID; **no** requester PII; run link opens the run |
| MS-03 | Flow analytics after suite | Run counts match submitted cases; failures match TC-12/13/14/15/16 only |

## E. Evidence sheet (fill per run)

| Case | Run ID | Trigger `globalid` | Row ID | Files | Receipt | Staff | Alert | Run status | Screenshot | Reviewer | Disposition |
|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-01 | | | | | | | | | | | |
| … | | | | | | | | | | | |

Also record: flow version (last modified timestamp), connection references by logical name
and bound account, the trigger sample JSON (redacted of synthetic PII is fine), and the
approver's name/date before the flow is turned on for the public survey.
