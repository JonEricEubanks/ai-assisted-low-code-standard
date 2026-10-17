# FOIA Public Intake Flow — Deployment README

Flow: `FOIA Pilot - Public Intake (Survey123 to SharePoint)`
Status: **DESIGN PACKAGE — not deployed.** Nothing in this folder has touched Power Platform.
Pilot boundary: Community Essentials dev tenant, synthetic data only, production not authorized.

| File | Purpose |
|---|---|
| `survey123-schema.md` | XLSForm survey/choices/settings to build the public form in Survey123 Connect |
| `flow-design.md` | Trigger, every action, expressions, routing table, due-date rule, error paths, Mermaid chart |
| `flow-definition.json` | Importable definition (strip `_todo` keys first) |
| `test-plan.md` | TC-01…TC-18 with inputs, expected row/files/emails/status |
| `README.md` | This file — deploy, verify, limitations, bindings |

## 1. Prerequisites

| Item | Who | Notes |
|---|---|---|
| Survey123 form published from `survey123-schema.md` | GIS admin | Public sharing on the form item; note the **form item ID** |
| SharePoint lists per `../../sharepoint-schema.md` with `SourceSubmissionId` column on Requests | Pilot lead | Confirm choice values listed in §5 below |
| FOIA service account | M365 admin | Contribute on the three lists/library; **Send As** on the FOIA shared mailbox; ArcGIS org account able to read the survey feature layer |
| Shared mailbox `foia@<client>.example` (placeholder) | M365 admin | Pilot test mailbox, not a real client mailbox |
| Solution `FOIA Pilot` (unmanaged, dev) with publisher prefix `mgp` | Pilot lead | Holds env vars, connection references, flow |

## 2. Deploy — manual steps in the maker portal

The flowagent MCP is being re-authenticated, so this release is manual. Do every step as the
service account or with the service account's connections selected.

### 2.1 Environment variables (Solution → New → More → Environment variable)

Create each as **Text**, current value set for the dev environment. Names must match exactly.

| Schema name | Current value (dev) |
|---|---|
| `mgp_FOIASiteUrl` | `https://communityessentials.sharepoint.com/sites/Administration` |
| `mgp_FOIARequestsListId` | `f99e0269-3061-4892-87ac-3dabba92d416` |
| `mgp_FOIADepartmentsListId` | `afbfa1b0-47ef-41dc-ac89-32ba142ddeef` |
| `mgp_FOIARecordsLibraryId` | `2b47c60b-057c-498d-ab75-0097a8abeb74` |
| `mgp_FOIARecordsLibraryFolderPath` | server-relative root of `FOIA Pilot Records` (e.g. `/FOIA Pilot Records`) — confirm in the Create file folder picker |
| `mgp_FOIASharedMailbox` | pilot test mailbox address |
| `mgp_FOIAOfficerEmail` | pilot FOIA officer test address |
| `mgp_FOIAAppDeepLinkBaseUrl` | `https://apps.powerapps.com/play/e/<envId>/a/afe38862-8f10-4548-802f-c8d4c8d6603e?tenantId=<tenantId>` |
| `mgp_FOIATimeZone` | `Central Standard Time` |
| `mgp_FOIASurvey123FormItemId` | form item ID from Survey123 |

### 2.2 Connection references (Solution → New → More → Connection reference)

| Logical name | Connector | Bind to |
|---|---|---|
| `mgp_FOIA_ArcGIS` | ArcGIS | service account's ArcGIS org connection |
| `mgp_FOIA_SharePoint` | SharePoint | service account |
| `mgp_FOIA_Office365Outlook` | Office 365 Outlook | service account (has Send As on mailbox) |

### 2.3 Import the definition

Option A — paste into a solution flow (recommended for the pilot):

1. Strip the `_todo` keys. From this folder in PowerShell:
   ```powershell
   $j = Get-Content .\flow-definition.json -Raw | ConvertFrom-Json
   function Strip($o){ if($o -is [System.Management.Automation.PSCustomObject]){ $o.PSObject.Properties.Remove('_todo'); foreach($p in $o.PSObject.Properties){ Strip $p.Value } } elseif($o -is [System.Array]){ foreach($i in $o){ Strip $i } } }
   Strip $j
   $j | ConvertTo-Json -Depth 50 | Set-Content .\flow-definition.import.json
   ```
   Do not commit `flow-definition.import.json`; it is a build artifact.
2. In the solution, **New → Automation → Cloud flow → Automated**, skip the trigger picker,
   add the ArcGIS trigger **When a survey response is submitted**, pick the survey, set
   events = `addData`, Include submitted record = Yes, Include survey info = Yes, user/portal/
   server response = No. Save once so the webhook registers.
3. Open **Settings → Concurrency control** on the trigger: On, Degree of parallelism **1**.
4. Rebuild the actions in designer order from `flow-design.md` §4, using the action names
   exactly (the names appear in run history and in the error alert). For each expression,
   copy from the design file or from `flow-definition.import.json`. Use **Code view/Peek
   code** on each action to compare against the JSON.
5. Set `Create_item_FOIARequest` → Settings → Retry policy → **None**.
6. Set `Apply_to_each_Attachment` → Settings → Concurrency control → On, **1**.
7. Set `Get_attachment_from_URL` and `Create_file_RecordsLibrary` → Settings → Timeout `PT2M`.
8. Configure run-after on `Scope_Catch_NotifyFailure` = **Failed, Skipped, Timed out** from
   `Scope_Try_Notify`; on `Scope_Finally_Log` = all four from Catch; on
   `Condition_FailureOccurred` = Succeeded, Failed from Finally.
9. Save. Open Flow checker → 0 errors.

Option B — solution import: wrap `flow-definition.import.json` in an exported solution's
`Workflows/` folder with a matching `customizations.xml` entry. Only do this if someone on
the team has done a hand-built solution import before; otherwise use Option A.

### 2.4 Turn on

Leave the flow **Off** until `test-plan.md` sections A and B are complete and the reviewer has
signed the evidence sheet. Then turn on. The public survey link stays unpublished to the
public until the pilot lead approves.

## 3. Visual verification (mandatory per `standards/visual-verification.md`)

A passing Flow checker is not acceptance. Capture in the shared browser and store under
`../../evidence/visual/` as `{surface}-{breakpoint}-{yyyymmdd-hhmm}.png`.

| Surface | What to open | Capture | Inspect for |
|---|---|---|---|
| Flow designer | The saved flow, every scope expanded one level, Catch and Finally visible | `flow-designer-1366-*.png` full page | No action with a warning badge; no "unresolved dynamic content" chips; all connection icons show the service account; run-after arrows on Catch show the dotted multi-status style |
| Run detail — happy path | TC-01 run | `flow-run-tc01-1366-*.png` | Every action green except `Compose_Log_ReceiptSkipped` (skipped); `Create_item_FOIARequest` outputs show the expected field values; both email actions Succeeded |
| Run detail — failure path | TC-12 run | `flow-run-tc12-1366-*.png` | Create red; Attachments and Notify skipped; Catch green; Finally green; `Terminate_Failed` executed; run header shows **Failed** |
| SharePoint list | `FOIA Pilot Requests` default view filtered to today's rows | `sp-requests-view-1366-*.png` | New row visible with correct Title, Route, Primary Department, Due Date; `Due Date Confirmed` = No |
| SharePoint library | `FOIA Pilot Records` after TC-05 | `sp-records-view-1366-*.png` | File present with Request, Document Type, Redaction Status, Sensitivity columns populated |
| Emails | Officer test mailbox after TC-01 and TC-12 | `mail-staff-*.png`, `mail-alert-*.png` | Receipt has no links; alert has no requester PII |

Record each capture in the TC evidence row with finding and disposition. Phone/tablet
breakpoints apply to the canvas app and SharePoint pages, not to the flow designer; capture
the SharePoint view at 390 as well.

## 4. Known limitations (accepted for pilot)

1. Due date skips weekends only — no Village holidays, no 21-day commercial rule, no
   extensions. Suggested only; `DueDateConfirmed=false` until a human confirms in the app.
2. Only the `FeeWaiverStatement` attachment question is filed. Adding another attachment
   question requires a flow change.
3. Email format check is heuristic (no regex in expressions); not RFC 5322.
4. Resubmitting a run after a partial failure skips as a duplicate — it does not re-file
   attachments or resend emails. Recovery is manual (see error alert text).
5. Trigger concurrency = 1 cannot be turned off later without re-creating the trigger.
6. Error alert embeds connector error messages; these name columns, not values, but review
   before production.
7. `ReceivedDate` is the Central-time date the webhook fired, not the device time.
8. The canvas app does not yet read `Param("RequestId")`; the deep link opens the app's
   start screen. App follow-up item.
9. The app's RequestDetail screen renders `RequestRoute` as a stage name (Intake /
   Department Review / …) while this flow writes Police / Non-Police / Multi-Department /
   Unassigned. Raise with the app owner; do not change the flow.
10. Survey123 webhook has no delivery retry; a flow run failure does not re-fire the trigger.
    Failed submissions remain in the Survey123 feature layer and are recovered by resubmitting
    the run after the cause is fixed.

## 5. Items to confirm before first run (`_todo` register)

| # | Item | Where | How |
|---|---|---|---|
| 1 | Trigger payload field casing and `feature.attachments.FeeWaiverStatement[]` shape | `Compose_Attributes`, `Compose_AttachmentList` | Submit one test response with the flow Off; open trigger history → body; save as `evidence/trigger-sample.json` (synthetic) |
| 2 | `surveyId` accepts an environment variable | Trigger | If rejected, paste the literal form item ID and note it |
| 3 | Choice values: `RequestRoute` (Police, Non-Police, Multi-Department, Unassigned), `IntakeMethod` (Online Form), `OverallStatus` (New); library `DocumentType` (Request), `RedactionStatus` (Not Reviewed), `Sensitivity` (Internal) | List/library settings | Add missing values or adjust constants in the flow |
| 4 | `SourceSubmissionId` column exists on Requests | List settings | Present in `sharepoint-schema.md`; absent from the app's extracted data source — add if missing |
| 5 | `result()` on skipped scopes returns `[]` | `Filter_array_FailedActions` | TC-12; apply the documented fallback if it errors |
| 6 | `mgp_FOIARecordsLibraryFolderPath` exact value | `Create_file_RecordsLibrary` | Pick the folder once in the designer, read the path from Peek code, store in the env var |

## 6. Rollback

Turn the flow **Off**. No data is modified by this flow other than rows/files it created,
which are identifiable by `CurrentStageNotes`/`Notes` containing `Correlation <runId>`.
Remove test rows manually after the suite; never bulk-delete. Delete the webhook from the
Survey123 form settings if the flow is deleted, so the form does not POST to a dead endpoint.

## 7. Ownership and approval

| Role | Placeholder |
|---|---|
| Flow owner (run-as) | FOIA service account |
| Business owner | FOIA officer (pilot) |
| Technical owner | MGP pilot delivery lead |
| Approver to turn on | Pilot lead, after evidence sheet signed |

Evidence to retain: flow last-modified timestamp, connection references with bound account,
trigger sample, TC run IDs, action results, alert email copies, screenshots per §3,
reviewer name and date.
