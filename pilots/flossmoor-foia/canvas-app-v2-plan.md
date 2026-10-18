# Canvas App Plan

## Mode
CREATE

## App Requirements
Rebuild the Flossmoor FOIA pilot as a **DesktopOrTablet (1366x768, Scale-to-fit off)** Canvas app — v2 — replacing the Phone-type v1 in `..\canvas-app-src`. The v2 app is currently empty (Screen1 only). Four SharePoint data sources are already connected: `FOIA Pilot Requests`, `FOIA Pilot Assignments`, `FOIA Pilot Departments`, `FOIA Pilot Records`.

Design is **mobile-first with three tiers** per `standards\power-apps.md` → "Adaptive layout tiers" (phone `< 600`, tablet `600–1199`, desktop `>= 1200`). Every tier is a different composition of the same components with different inputs. More width earns more density and more simultaneous context; it never just stretches the phone layout.

Non-negotiables (from the standard's nine Canvas MCP sync rules — all apply):
1. Never reparent an existing control through sync (this is a CREATE, so every control is new — keep names unique across the whole app).
2. Structural rebuilds use a two-sync wipe-and-recreate (orchestrator's concern; builders must not rename/move controls after first sync).
3. Freshly created parent ⇒ freshly created descendants.
4. **No `CanvasComponent` instances inside a Gallery template** — use `ModernBadge` with the same Switch mapping.
5. **Event custom properties require `Default: =false`.**
6. **Never put `App.Width` behind a named formula.** Only literal tokens (`BreakpointPhone = 600`) live in `App.Formulas`; every breakpoint test is inline: `App.Width < BreakpointPhone`, `App.Width >= BreakpointDesktop`.
7. `ModernBadge`: `Intent` uses `BadgeIntent.Neutral` (not Subtle); `Size` is a number; `Content` is not readable as an output.
8. Studio device emulator does not drive `App.Width`; acceptance comes from a real browser viewport / device.
9. After a large sync, hard-reload Studio.

Reuse from v1 (proven): the Fluent token block (now in `App.pa.yaml`), the three component contracts (`cmpAppHeader`, `cmpSideNav`, `cmpStatusBadge`), the NewRequest `Patch` (IfError + `OverallStatus = "New"` + required-field gate incl. `IntakeMethod` default "Online Form" and `ReceivedDate` default `Today()`), the DepartmentWork / ResponseCloseout write logic, and the gallery `Items`/`Filter` formulas. **Do not reuse v1 screen compositions.**

## Working Directory
`C:\Users\tejas\OneDrive - MGP Inc\ManagedApps\AI_Process\pilots\flossmoor-foia\canvas-app-v2`

Files to produce (one per row of the Screens table). `App.pa.yaml` is already written by the planner. Component definitions go in a single `Components.pa.yaml` (root key `ComponentDefinitions:`).

## Discovery Summary
- Controls available: 141 — used in this app: `GroupContainer` (AutoLayout only), `Gallery` (Vertical), `ModernText`, `ModernButton`, `ModernIcon`, `ModernBadge`, `ModernTabList`, `ModernTextInput`, `ModernCombobox`, `ModernDropdown`, `ModernDatePicker`, `ModernCheckbox`, `ModernToggle`, `ModernRadio`, `CanvasComponent` (instances of our own component definitions). `ModernCard` exists but is **not** used: our list rows live in a Gallery (row tap = `Select(Parent)`), and `ModernCard` inside a component would add an unverified property surface.
- Data sources: `FOIA Pilot Requests`, `FOIA Pilot Assignments`, `FOIA Pilot Departments`, `FOIA Pilot Records` (all Kind: Connected, Writable, Delegatable).
- Connectors: none beyond the SharePoint-backed tables above (no `describe_api` needed).

## Data Source Schemas
Full `get_data_source_schema` output. Choice/Lookup columns are `Record` — read `.Value` (and `.Id` for lookups); Person columns are `Record` — read `.DisplayName` / `.Email`. The `{Braced}` columns are SharePoint system columns; do not bind to them.

### FOIA Pilot Requests
Required on create (set by the NewRequest Patch or defaulted — the save gate must block when any is blank): **Title, ReceivedDate, IntakeMethod, RequestRoute, RequestDescription, OverallStatus**.
```
Data Source: FOIA Pilot Requests
Kind: Connected

Columns (51):
  - {Attachments} (Display: "Attachments"): LazyTable
  - {ContentType} (Display: "Content type"): Record
  - {FilenameWithExtension} (Display: "File name with extension"): String
  - {FullPath} (Display: "Full Path"): String
  - {HasAttachments} (Display: "Has attachments"): Boolean
  - {Identifier} (Display: "Identifier"): String
  - {IsFolder} (Display: "Is folder"): Boolean
  - {Link} (Display: "Link to item"): String
  - {ModerationComment} (Display: "Comments associated with the content approval of this list item"): String
  - {ModerationStatus} (Display: "Content approval status"): String
  - {Name} (Display: "Name"): String
  - {Path} (Display: "Folder path"): String
  - {TriggerWindowEndToken} (Display: "Trigger Window End Token"): String
  - {TriggerWindowStartToken} (Display: "Trigger Window Start Token"): String
  - {VersionNumber} (Display: "Version number"): String
  - AssignedOfficer (Display: "Assigned Officer"): Record
  - Author (Display: "Created By"): Record
  - CertifiedCopies (Display: "Certified Copies"): Record
  - CloseoutNotes (Display: "Closeout Notes"): String
  - CommercialPurpose (Display: "Commercial Purpose"): Record
  - ComplianceAssetId (Display: "Compliance Asset Id"): String
  - Created: DateTime
  - CurrentStageNotes (Display: "Current Stage Notes"): String
  - DeliveryFormat (Display: "Delivery Format"): Record
  - DueDate (Display: "Due Date"): Date
  - DueDateConfirmed (Display: "Due Date Confirmed"): Boolean
  - Editor (Display: "Modified By"): Record
  - ExtensionDays (Display: "Extension Days"): Number
  - ExtensionStatus (Display: "Extension Status"): Record
  - ExtensionType (Display: "Extension Type"): Record
  - FeeWaiverRequested (Display: "Fee Waiver Requested"): Record
  - FinalResponseDate (Display: "Final Response Date"): Date
  - ID: Number
  - IntakeMethod (Display: "Intake Method"): Record
  - Modified: DateTime
  - OData__ColorTag (Display: "Color Tag"): String
  - OverallStatus (Display: "Overall Status"): Record
  - PrimaryDepartment (Display: "Primary Department"): Record
  - ReceivedDate (Display: "Received Date"): Date
  - RequestDescription (Display: "Request Description"): String
  - RequesterCity (Display: "Requester City"): String
  - RequesterEmail (Display: "Requester Email"): String
  - RequesterFirstName (Display: "Requester First Name"): String
  - RequesterLastName (Display: "Requester Last Name"): String
  - RequesterPhone (Display: "Requester Phone"): String
  - RequesterState (Display: "Requester State"): String
  - RequesterStreetAddress (Display: "Requester Street Address"): String
  - RequesterZip (Display: "Requester ZIP"): String
  - RequestRoute (Display: "Request Route"): Record
  - SourceSubmissionId (Display: "Source Submission ID"): String
  - Title: String
```

### FOIA Pilot Assignments
```
Data Source: FOIA Pilot Assignments
Kind: Connected

Columns (32):
  - {Attachments} (Display: "Attachments"): LazyTable
  - {ContentType} (Display: "Content type"): Record
  - {FilenameWithExtension} (Display: "File name with extension"): String
  - {FullPath} (Display: "Full Path"): String
  - {HasAttachments} (Display: "Has attachments"): Boolean
  - {Identifier} (Display: "Identifier"): String
  - {IsFolder} (Display: "Is folder"): Boolean
  - {Link} (Display: "Link to item"): String
  - {ModerationComment} (Display: "Comments associated with the content approval of this list item"): String
  - {ModerationStatus} (Display: "Content approval status"): String
  - {Name} (Display: "Name"): String
  - {Path} (Display: "Folder path"): String
  - {TriggerWindowEndToken} (Display: "Trigger Window End Token"): String
  - {TriggerWindowStartToken} (Display: "Trigger Window Start Token"): String
  - {VersionNumber} (Display: "Version number"): String
  - Active: Boolean
  - AssignedTo (Display: "Assigned To"): Record
  - AssignmentDueDate (Display: "Assignment Due Date"): Date
  - AssignmentStatus (Display: "Assignment Status"): Record
  - Author (Display: "Created By"): Record
  - ComplianceAssetId (Display: "Compliance Asset Id"): String
  - Created: DateTime
  - Department: Record
  - DepartmentCompleteDate (Display: "Department Complete Date"): Date
  - Editor (Display: "Modified By"): Record
  - ID: Number
  - Modified: DateTime
  - OData__ColorTag (Display: "Color Tag"): String
  - RedactionRequired (Display: "Redaction Required"): Record
  - Request: Record
  - ResponseNotes (Display: "Response Notes"): String
  - Title: String
```

### FOIA Pilot Departments
```
Data Source: FOIA Pilot Departments
Kind: Connected

Columns (27):
  - {Attachments} (Display: "Attachments"): LazyTable
  - {ContentType} (Display: "Content type"): Record
  - {FilenameWithExtension} (Display: "File name with extension"): String
  - {FullPath} (Display: "Full Path"): String
  - {HasAttachments} (Display: "Has attachments"): Boolean
  - {Identifier} (Display: "Identifier"): String
  - {IsFolder} (Display: "Is folder"): Boolean
  - {Link} (Display: "Link to item"): String
  - {ModerationComment} (Display: "Comments associated with the content approval of this list item"): String
  - {ModerationStatus} (Display: "Content approval status"): String
  - {Name} (Display: "Name"): String
  - {Path} (Display: "Folder path"): String
  - {TriggerWindowEndToken} (Display: "Trigger Window End Token"): String
  - {TriggerWindowStartToken} (Display: "Trigger Window Start Token"): String
  - {VersionNumber} (Display: "Version number"): String
  - Active: Boolean
  - Author (Display: "Created By"): Record
  - ComplianceAssetId (Display: "Compliance Asset Id"): String
  - Created: DateTime
  - DepartmentCode (Display: "Department Code"): String
  - Editor (Display: "Modified By"): Record
  - ID: Number
  - IsPolice (Display: "Is Police"): Boolean
  - Modified: DateTime
  - OData__ColorTag (Display: "Color Tag"): String
  - SortOrder (Display: "Sort Order"): Number
  - Title: String
```

### FOIA Pilot Records
```
Data Source: FOIA Pilot Records
Kind: Connected

Columns (37):
  - {ContentType} (Display: "Content type"): Record
  - {DriveId} (Display: "Drive ID"): String
  - {DriveItemId} (Display: "Drive item ID"): String
  - {FilenameWithExtension} (Display: "File name with extension"): String
  - {FullPath} (Display: "Full Path"): String
  - {Identifier} (Display: "Identifier"): String
  - {IsCheckedOut} (Display: "Checked out"): Boolean
  - {IsFolder} (Display: "Is folder"): Boolean
  - {Link} (Display: "Link to item"): String
  - {ModerationComment} (Display: "Comments associated with the content approval of this list item"): String
  - {ModerationStatus} (Display: "Content approval status"): String
  - {Name} (Display: "Name"): String
  - {Path} (Display: "Folder path"): String
  - {SensitivityLabelId} (Display: "Sensitivity Label Id"): String
  - {SensitivityLabelName} (Display: "Sensitivity Label Display Name"): String
  - {Thumbnail} (Display: "Thumbnail"): Record
  - {TriggerWindowEndToken} (Display: "Trigger Window End Token"): String
  - {TriggerWindowStartToken} (Display: "Trigger Window Start Token"): String
  - {VersionNumber} (Display: "Version number"): String
  - Author (Display: "Created By"): Record
  - CheckoutUser (Display: "Checked Out To"): Record
  - ComplianceAssetId (Display: "Compliance Asset Id"): String
  - Created: DateTime
  - Department: Record
  - DocumentType (Display: "Document Type"): Record
  - Editor (Display: "Modified By"): Record
  - ID: Number
  - IsFinalResponse (Display: "Is Final Response"): Boolean
  - Modified: DateTime
  - Notes: String
  - OData__ColorTag (Display: "Color Tag"): String
  - OData__DisplayName (Display: "Sensitivity (OData__DisplayName)"): String
  - OData__ExtendedDescription (Display: "Description"): String
  - RedactionStatus (Display: "Redaction Status"): Record
  - Request: Record
  - Sensitivity: Record
  - Title: String
```

## API Details
None — no connectors beyond the connected SharePoint tables.

## Screens
| Screen | File | Action | Purpose | Key Controls |
|--------|------|--------|---------|--------------|
| Components | Components.pa.yaml | Create | `ComponentDefinitions` for cmpAppHeader, cmpSideNav, cmpStatusBadge, cmpRequestDetailPane | GroupContainer, ModernButton, ModernText, ModernBadge, ModernIcon, ModernTabList, Gallery |
| App | App.pa.yaml | Modify (already written by planner; builders do not touch) | Tokens + `StartScreen: =Home` | — |
| Home | Home.pa.yaml | Create | The one list screen for all tiers; desktop = master-detail with persistent `cmpRequestDetailPane`; KPI tiles / compact stat strip; status-distribution bar (desktop) | cmpAppHeader, cmpSideNav, GroupContainer, ModernText, ModernIcon, ModernTextInput, ModernDropdown, Gallery, ModernBadge, ModernButton, cmpRequestDetailPane |
| RequestDetail | RequestDetail.pa.yaml | Create | Thin phone/tablet full-screen detail: header(ShowBack) + cmpRequestDetailPane + nav; reachable on desktop too | cmpAppHeader, cmpSideNav, cmpRequestDetailPane, ModernText, ModernButton |
| NewRequest | NewRequest.pa.yaml | Create | Intake form; phone 1-col cards + sticky action bar; tablet 2-col groups; desktop 2–3 col + "Intake guidance" side card; v1 Patch kept exactly | cmpAppHeader, cmpSideNav, GroupContainer, ModernText, ModernTextInput, ModernCombobox, ModernDatePicker, ModernCheckbox, ModernButton |
| DepartmentWork | DepartmentWork.pa.yaml | Create | Assignment cards 1/2/3 columns by tier + editor; v1 write logic kept | cmpAppHeader, cmpSideNav, Gallery, ModernBadge, ModernDropdown, ModernDatePicker, ModernToggle, ModernTextInput, ModernButton, ModernText |
| ResponseCloseout | ResponseCloseout.pa.yaml | Create | Readiness summary + final response form; v1 write logic kept | cmpAppHeader, cmpSideNav, GroupContainer, ModernText, ModernDatePicker, ModernRadio, ModernTextInput, ModernCheckbox, ModernButton |

## Aesthetic Direction
Refined Fluent 2 "civic operations console": neutral surfaces, one brand blue, semantic status colour that is never the only cue (every badge has an icon + text). Density grows with width.

- Palette (all tokens are named formulas in `App.pa.yaml` — use the token names, never raw RGBA in screens):
  - Primary background `ColorNeutralBg` = RGBA(250, 250, 250, 1)
  - Surface / cards `ColorSurface` = RGBA(255, 255, 255, 1)
  - Stroke `ColorNeutralStroke` = RGBA(225, 223, 221, 1)
  - Accent `ColorBrand` = RGBA(0, 120, 212, 1); hover `ColorBrandHover` = RGBA(16, 110, 190, 1); tint `ColorBrandTint` = RGBA(235, 243, 252, 1)
  - Text primary `ColorTextPrimary` = RGBA(36, 36, 36, 1); secondary `ColorTextSecondary` = RGBA(97, 97, 97, 1)
  - Semantic: `ColorSuccess` RGBA(16,124,16,1) / `ColorSuccessBg` RGBA(241,250,241,1); `ColorWarning` RGBA(157,93,0,1) / `ColorWarningBg` RGBA(255,249,245,1); `ColorCritical` RGBA(196,43,28,1) / `ColorCriticalBg` RGBA(253,243,244,1); `ColorInfo` RGBA(0,120,212,1)
- Layout strategy: **AutoLayout everywhere** (`GroupContainer` `Variant: AutoLayout`). No ManualLayout, no X/Y. Fixed `Width`/`Height` only on icons, badges, buttons, nav/header shells, and tiles — every such child sets `FillPortions: =0`.
- Card treatment: `Fill: =ColorSurface`, `BorderColor: =ColorNeutralStroke`, `BorderThickness: =1`, `DropShadow: =DropShadow.None`, radii `=RadiusSm` (4). Shell containers (screen root, header, nav) use radii `=0` and `DropShadow.None`.
- Typography (Segoe UI via modern controls). **Pick the size with an inline tier test:**

| Role | Phone `< 600` | Tablet | Desktop `>= 1200` | Formula |
|---|---|---|---|---|
| Body | 15 | 14 | 14 | `=If(App.Width < BreakpointPhone, FontSizeBodyPhone, FontSizeBody)` |
| Caption | 12 | 12 | 12 | `=FontSizeCaption` |
| Section | 16 | 16 | 16 | `=FontSizeSection` |
| Title | 20 | 22 | 24 | `=If(App.Width < BreakpointPhone, FontSizeTitlePhone, App.Width < BreakpointDesktop, FontSizeTitleTablet, FontSizeTitleDesktop)` |
| KPI | 28 | 30 | 32 | `=If(App.Width < BreakpointPhone, FontSizeKpiPhone, App.Width < BreakpointDesktop, FontSizeKpiTablet, FontSizeKpiDesktop)` |

  Headings `FontWeight.Semibold`; body `FontWeight.Normal`. Every `ModernText` sets `AutoHeight: =true`, `PaddingTop/Bottom/Left/Right: =0`, `AccessibleLabel: =Self.Text`, `LayoutMinHeight: =0`, `LayoutMinWidth: =0`.
- Touch targets: every button/input `Height: =ControlMinTouch` (44) or `=InputHeight` (44), `LayoutMinHeight` same.
- Page padding: `=If(App.Width < BreakpointPhone, PagePaddingPhone, PagePaddingWide)` (16 / 24).
- Desktop content cap: wrapper `Width: =Min(Parent.Width, ContentMaxWidth)` centered by the parent's `LayoutAlignItems: =LayoutAlignItems.Center` (parent is Vertical). Tiles never exceed `TileMaxWidth` (360): set `LayoutMaxWidth: =If(App.Width >= BreakpointDesktop, TileMaxWidth, 0)`.

### Tier acceptance matrix (from the standard — this is the checklist)

| Concern | Phone | Tablet | Desktop |
|---|---|---|---|
| Navigation | `cmpSideNav Placement="Bottom"` tab bar, icon + short label, ≥44 | `cmpSideNav Placement="Rail"` icon-only rail, 64 wide | Rail with icons + labels, 220 wide |
| Header actions | Icon-only (component does this automatically) | Icon + label primary, icon-only secondary | Icon + label |
| KPI tiles | 1 column, big value (`TileHeight` 104) | 2 columns | Single compact stat strip (`StatStripHeight` 64, 4 across, horizontal icon·value·label) |
| List / detail | Home list → tap row → `Navigate(RequestDetail)` | Same | **Master-detail** on Home: list pane 38 % + persistent `cmpRequestDetailPane`; row tap only sets `gblSelectedRequest` |
| Forms | Single column, one card per group, sticky bottom action bar above bottom nav | Two columns in bounded groups | Two/three columns + read-only side card |
| Content width | Full bleed, 16 padding | 24 padding | Cap 1600 and center |
| Supplementary panels | None | Collapsible (not used: nothing to collapse) | Activity timeline, status-distribution strip, quick-action strip |
| Empty states | Icon + one line + one primary action | Same | Same + hint of what will appear |

## Named Variables and Shared State
Global (`Set`) — all screens use these exact names:

| Variable | Type | Meaning / owner |
|---|---|---|
| `gblSelectedRequest` | Record of 'FOIA Pilot Requests' | Current request. Set by Home row tap, NewRequest save, Closeout save. Read by cmpRequestDetailPane (app scope), RequestDetail, DepartmentWork, ResponseCloseout. |
| `gblSelectedAssignment` | Record of 'FOIA Pilot Assignments' | Set by assignment row/card tap; DepartmentWork editor binds to it. |
| `gblSelectedDepartment` | Record (Department lookup) | `gblSelectedAssignment.Department`; DepartmentWork records filter. |
| `gblIsLoading`, `gblLoadError`, `gblPermissionDenied`, `gblSaveSuccess` | Boolean | Required user states (loading / error / permission / success). Reset in every screen's `OnVisible`. |
| `gblSearchText` | Text | Home search (`txtSearch.OnChange`). |
| `gblStatusFilter` | Text | Home status filter; `"All"` default. |
| `gblDepartmentFilter` | Text | Home department filter; `"All"` default. |
| `gblDueDateConfirmed` | Boolean | NewRequest human confirmation checkbox. |
| `gblExtensionValidationMessage` | Text | Extension-review message (detail pane). |

No collections. No `App.OnStart`. Tab state inside the detail pane is the `ModernTabList`'s own `Selected` — not a variable.

Status vocabulary (SharePoint choice `OverallStatus`): filters use `["All", "New", "In Progress", "On Hold", "Closed"]`; Closeout writes one of `["Ready", "Delivered", "Closed"]`. Badge mapping must therefore cover: New, In Progress, On Hold, Ready, Delivered, Closed, Complete, Overdue (default `BadgeIntent.Neutral`, icon `"Circle"`). Assignment statuses: New, Accepted, In Progress, Awaiting Clarification, Redaction, Complete, Cancelled.

Verified Fluent icon names (rendered in v1): `Home`, `Add`, `Document`, `People`, `CheckmarkCircle`, `ArrowLeft`, `ArrowClockwise`, `Warning`, `Info`, `Pause`, `Checkmark`, `Send`, `Circle`, `Edit`, `Dismiss`, `ChevronRight`, `Search`. Additional names used here and to be visually checked by the orchestrator: `Mail`, `Calendar`, `Clock`, `DocumentSearch`, `Filter`. If one fails to render, fall back to `Document`.

## Component Contracts

All four definitions live in **`Components.pa.yaml`** under one root `ComponentDefinitions:` key. All use `DefinitionType: CanvasComponent` and `AccessAppScope: true` (needed to read the `App.Formulas` tokens and `gblSelectedRequest`). Instances use `Control: CanvasComponent` + `ComponentName: <name>`. Canvas components **cannot contain other component instances** — inside a component use `ModernBadge` directly, never `cmpStatusBadge`.

### cmpAppHeader (reuse v1 contract verbatim)
Purpose: shared header on all five screens. Consumers: Home, RequestDetail, NewRequest, DepartmentWork, ResponseCloseout.

| Property | Kind | Type | Default |
|---|---|---|---|
| Title | Input | Text | `="FOIA"` |
| Subtitle | Input | Text | `=""` (hidden on phone or when blank) |
| ShowBack | Input | Boolean | `=false` |
| PrimaryLabel / PrimaryIcon | Input | Text | `=""` (button hidden when label blank; icon-only on phone) |
| SecondaryLabel / SecondaryIcon | Input | Text | `=""` |
| OnBack / OnPrimary / OnSecondary | Event | ReturnType None | `=false` |

Definition `Properties`: `Fill: =ColorSurface`, `Height: =HeaderHeight`, `Width: =App.Width`. Internals exactly as v1 `Components\cmpAppHeader.pa.yaml` (back button → titles column → secondary → primary, 1-px divider) with **one change**: `lblHeaderTitle.Size` = the Title tier formula above (20/22/24) instead of v1's 18/22. Buttons: `Height: =ControlMinTouch`, `Layout: =If(IsBlank(icon), ButtonLayout.TextOnly, App.Width < BreakpointPhone, ButtonLayout.IconOnly, ButtonLayout.IconBefore)`; primary uses `BasePaletteColor: =ColorBrand`, secondary `Appearance: =ButtonAppearance.Secondary`, back `Appearance: =ButtonAppearance.Subtle`, `Icon: ="ArrowLeft"`. Width of text buttons: `Len(label) * 9 + SpaceLg * 2 + If(IsBlank(icon), 0, 24)`; icon-only: `ControlMinTouch`.

Instance snippet (Home):
```yaml
- cmpHomeHeader:
    Control: CanvasComponent
    ComponentName: cmpAppHeader
    Properties:
      AlignInContainer: =AlignInContainer.Stretch
      FillPortions: =0
      Height: =HeaderHeight
      LayoutMinHeight: =HeaderHeight
      LayoutMinWidth: =0
      OnBack: =false
      OnPrimary: =Navigate(NewRequest, ScreenTransition.Fade)
      OnSecondary: |-
        =Set(gblIsLoading, true);
        Set(gblLoadError, false);
        Refresh('FOIA Pilot Requests');
        Set(gblIsLoading, false)
      PrimaryIcon: ="Add"
      PrimaryLabel: ="New request"
      SecondaryIcon: ="ArrowClockwise"
      SecondaryLabel: ="Refresh"
      ShowBack: =false
      Subtitle: ="Village of Flossmoor · Request queue and response readiness"
      Title: ="FOIA requests"
```

### cmpSideNav (reuse v1 contract; item list updated)
Purpose: the only navigation shell. `Placement="Bottom"` = phone tab bar; `Placement="Rail"` = tablet icon rail / desktop labelled rail.

| Property | Kind | Type | Default |
|---|---|---|---|
| ActiveScreen | Input | Text | `="Home"` — one of `"Home"`, `"NewRequest"`, `"DepartmentWork"`, `"ResponseCloseout"` (RequestDetail passes `"Home"`) |
| Placement | Input | Text | `="Rail"` |

Definition `Properties`: `Fill: =ColorSurface`, `Height: =If(cmpSideNav.Placement = "Bottom", BottomNavHeight, App.Height - HeaderHeight)`, `Width: =If(cmpSideNav.Placement = "Bottom", App.Width, If(App.Width >= BreakpointDesktop, NavRailWidthDesktop, NavRailWidthTablet))`.

Internals as v1 `Components\cmpSideNav.pa.yaml` but with **four** items (v1's RequestDetail item is removed): `btnNavHome` (Icon `"Home"`, Text `"Home"`, `Navigate(Home, ScreenTransition.None)`), `btnNavNewRequest` (`"Add"`, "New request"), `btnNavDepartmentWork` (`"People"`, "Department work"), `btnNavResponseCloseout` (`"CheckmarkCircle"`, "Closeout"). Each button:
- `Appearance: =If(cmpSideNav.ActiveScreen = "<Name>", ButtonAppearance.Secondary, ButtonAppearance.Subtle)`, `Color`, `FontWeight`, `IconStyle` driven by the same test
- `Layout: =If(cmpSideNav.Placement = "Rail" && App.Width >= BreakpointDesktop, ButtonLayout.IconBefore, ButtonLayout.IconOnly)` — on the phone bar the short label is given by `Tooltip`/`AccessibleLabel`; **phone labels under icons are not supported by `ModernButton`**, so the bottom bar is icon-only with ≥44 targets and accessible names (documented deviation from "icon + short label").
- `Width: =If(cmpSideNav.Placement = "Bottom", (Parent.Width - SpaceSm * 2 - SpaceXs * 3) / 4, Parent.Width - SpaceSm * 2)`, `Height: =ControlMinTouch`.
- Bottom placement shows a 1-px top divider; Rail shows a 1-px right divider (`cntNavDividerTop` / `cntNavDividerSide`, exactly as v1).

Instance snippets (every screen has both; only one is visible):
```yaml
- cmpHomeNavRail:
    Control: CanvasComponent
    ComponentName: cmpSideNav
    Properties:
      ActiveScreen: ="Home"
      AlignInContainer: =AlignInContainer.Stretch
      FillPortions: =0
      Height: =Parent.Height
      LayoutMinHeight: =0
      LayoutMinWidth: =0
      Placement: ="Rail"
      Visible: =App.Width >= BreakpointPhone
      Width: =If(App.Width >= BreakpointDesktop, NavRailWidthDesktop, NavRailWidthTablet)
```
```yaml
- cmpHomeNavBottom:
    Control: CanvasComponent
    ComponentName: cmpSideNav
    Properties:
      ActiveScreen: ="Home"
      AlignInContainer: =AlignInContainer.Stretch
      FillPortions: =0
      Height: =BottomNavHeight
      LayoutMinHeight: =BottomNavHeight
      LayoutMinWidth: =0
      Placement: ="Bottom"
      Visible: =App.Width < BreakpointPhone
      Width: =App.Width
```

### cmpStatusBadge (reuse v1 verbatim)
Purpose: status badge outside galleries (detail header, closeout summary). Input `Status: Text`, default `="Not set"`. `Height: =24`, `Width: =120`. Internals as v1 `Components\cmpStatusBadge.pa.yaml`: one `ModernBadge` with `Shape: =BadgeShape.Rounded`, `Size: =FontSizeCaption`, `FontWeight: =FontWeight.Semibold`, Icon/Intent `Switch` over New→Info/Informative, In Progress→ArrowClockwise/Highlight, On Hold→Pause/Caution, Ready→Checkmark/Attention, Delivered→Send/Positive, Closed→CheckmarkCircle/Positive, Complete→CheckmarkCircle/Positive, Overdue→Warning/Critical, else Circle/Neutral. **Inside any Gallery template use a `ModernBadge` with this same Switch instead** (sync rule 4).

Instance snippet:
```yaml
- cmpCloseoutStatusBadge:
    Control: CanvasComponent
    ComponentName: cmpStatusBadge
    Properties:
      AlignInContainer: =AlignInContainer.Start
      FillPortions: =0
      Height: =24
      LayoutMinHeight: =24
      LayoutMinWidth: =120
      Status: =Coalesce(gblSelectedRequest.OverallStatus.Value, "Not set")
      Width: =120
```

### cmpRequestDetailPane (NEW)
Purpose: the single detail surface. Consumers: **Home** (desktop right pane) and **RequestDetail** (phone/tablet full screen). Logic lives once.

**Record-input decision:** the pane reads **`gblSelectedRequest` through app scope** rather than a `Record`-typed input. Rationale: a `Record` custom property requires a declared schema that must mirror the SharePoint table; the authoring service's acceptance of that schema is unverified, whereas `AccessAppScope: true` is already proven by v1's three components, and every consumer binds the pane to the same global selection anyway. This app-scope dependency is recorded here as justified.

**Write decision:** the component performs **no writes**. Quick actions raise events; the host screen executes the `Patch` inside `IfError` so permission/error handling stays with the screen (standard: "A component … must not silently perform writes").

| Property | Kind | Type | Default | Notes |
|---|---|---|---|---|
| ShowQuickActions | Input | Boolean | `=true` | Host can hide the quick-action strip |
| OnConfirmDueDate | Event | ReturnType None | `=false` | Host patches `DueDateConfirmed: true` |
| OnOpenDepartmentWork | Event | ReturnType None | `=false` | Host sets `gblSelectedAssignment` (already set by the pane's assignment row tap) and navigates |
| OnOpenCloseout | Event | ReturnType None | `=false` | Host navigates to ResponseCloseout |

Definition `Properties`: `Fill: =ColorSurface`, `Height: =600`, `Width: =480` (hosts override). Root `cntPaneRoot` Vertical, `Fill: =ColorSurface`, `BorderColor: =ColorNeutralStroke`, `BorderThickness: =1`, radii `=RadiusSm`, `LayoutOverflowY: =LayoutOverflow.Scroll`, padding `=If(App.Width < BreakpointPhone, PagePaddingPhone, PagePaddingWide)`, `LayoutGap: =SpaceMd`, `Width/Height: =Parent.Width/Height`. Children, top to bottom (all `FillPortions: =0`, `AlignInContainer: =AlignInContainer.Stretch` unless noted):

1. `cntPaneHead` (Horizontal, `LayoutAlignItems.Start`, `LayoutGap: =SpaceMd`, `LayoutWrap: =true`): `cntPaneTitles` (Vertical, `FillPortions: =1`, `LayoutMinWidth: =200`) → `lblPaneTitle` (`Text: =Coalesce(gblSelectedRequest.Title, "No request selected")`, Title tier size, Semibold), `lblPaneMeta` (caption: `=gblSelectedRequest.RequesterFirstName & " " & gblSelectedRequest.RequesterLastName & " · Received " & If(IsBlank(gblSelectedRequest.ReceivedDate), "—", Text(gblSelectedRequest.ReceivedDate, "mmm d, yyyy")) & " · " & Coalesce(gblSelectedRequest.PrimaryDepartment.Value, "No department")`); `bdgPaneStatus` `ModernBadge` (cmpStatusBadge Switch, `Height: =24`, `Width: =120`, `Size: =FontSizeCaption`).
2. `cntPaneQuickActions` (Horizontal, `LayoutWrap: =true`, `LayoutGap: =SpaceSm`, `Visible: =cmpRequestDetailPane.ShowQuickActions`): `btnPaneConfirmDue` (`Appearance: =ButtonAppearance.Secondary`, `Icon: ="Checkmark"`, `Text: ="Confirm due date"`, `Visible: =!IsBlank(gblSelectedRequest.DueDate) && !gblSelectedRequest.DueDateConfirmed`, `OnSelect: =cmpRequestDetailPane.OnConfirmDueDate()`); `btnPaneDeptWork` (`Icon: ="People"`, "Open department work", `DisplayMode: =If(CountRows(Filter('FOIA Pilot Assignments', Request.Id = gblSelectedRequest.ID && Active = true)) = 0, DisplayMode.Disabled, DisplayMode.Edit)`, `OnSelect: =cmpRequestDetailPane.OnOpenDepartmentWork()`); `btnPaneCloseout` (`BasePaletteColor: =ColorBrand`, `Icon: ="CheckmarkCircle"`, "Closeout", `OnSelect: =cmpRequestDetailPane.OnOpenCloseout()`). All `Height: =ControlMinTouch`, `Layout: =If(App.Width < BreakpointPhone, ButtonLayout.IconOnly, ButtonLayout.IconBefore)`, `Width: =If(App.Width < BreakpointPhone, ControlMinTouch, Len(Self.Text) * 9 + SpaceLg * 2 + 24)`, `Tooltip: =Self.Text`.
3. `tabPaneDetail` `ModernTabList`: `Items: =["Summary", "Assignments", "Activity"]`, `Default: '={Value: "Summary"}'` (quoted — see conventions), `ItemDisplayText: =ThisItem.Value`, `Appearance: =TabListAppearance.Subtle`, `TabSize: =TabSize.Medium`, `Height: =ControlMinTouch`, `LayoutMinHeight: =ControlMinTouch`, `LayoutMinWidth: =0`, `Size: =FontSizeBody`, `AccessibleLabel: ="Request detail sections"`.
4. `cntPaneTabSummary` (Vertical, `Visible: =tabPaneDetail.Selected.Value = "Summary"`, `LayoutGap: =SpaceMd`): `cntPaneFields` (Horizontal, `LayoutWrap: =true`, `LayoutGap: =SpaceMd`) holding field blocks `cntPaneField<Name>` (Vertical, `FillPortions: =0`, `Height: =FieldHeight`, `LayoutMinWidth: =160`, `Width: =If(App.Width < BreakpointPhone, Parent.Width, (Parent.Width - SpaceMd) / 2 - 1)`) each with a caption label + value label (`AutoHeight`). Fields: Requester (`First & " " & Last`), Email, Phone, Received (`Text(ReceivedDate, "mmm d, yyyy")`), Working due date (`If(IsBlank(DueDate), "Not set", Text(DueDate, "mmm d, yyyy") & If(DueDateConfirmed, " · Confirmed", " · Unconfirmed"))`, value colour `=If(gblSelectedRequest.DueDateConfirmed, ColorTextPrimary, ColorWarning)`), Route (`RequestRoute.Value`), Intake method, Primary department, Delivery format, Certified copies, Fee waiver. Then full-width `lblPaneDescriptionCaption` + `lblPaneDescription` (`Text: =Coalesce(gblSelectedRequest.RequestDescription, "—")`, body size, `Wrap: =true`), `lblPaneStageNotes` (Current stage notes), and `cntPaneExtension` card: caption "Extension review", helper text "Enter a proposed extension only when staff have confirmed the request details. This screen does not calculate or silently change a due date.", row (Vertical on phone / Horizontal otherwise) of `datPaneExtensionDate` (`DefaultDate: =gblSelectedRequest.DueDate`, `Format: =DatePickerFormat.Short`, `IsEditable: =true`, `Width: =200`), `txtPaneExtensionNotes` (`FillPortions: =If(App.Width < BreakpointPhone, 0, 1)`, `MaxLength: =500`), `chkPaneExtensionConfirmed` (`Label: ="Human confirmation recorded"`, `Width: =240`); `lblPaneExtensionValidation` (`Text: =If(IsBlank(gblExtensionValidationMessage), "No extension has been saved.", gblExtensionValidationMessage)`, colour `=If(IsBlank(gblExtensionValidationMessage), ColorTextSecondary, ColorWarning)`); `btnPaneReviewExtension` (Secondary, `DisplayMode: =If(IsBlank(datPaneExtensionDate.SelectedDate) || !chkPaneExtensionConfirmed.Checked, DisplayMode.Disabled, DisplayMode.Edit)`, `OnSelect` = v1 three-branch `If` that only sets `gblExtensionValidationMessage` — no write).
5. `cntPaneTabAssignments` (Vertical, `Visible: =tabPaneDetail.Selected.Value = "Assignments"`): `galPaneAssignments` `Gallery` Vertical, `Items: =SortByColumns(Filter('FOIA Pilot Assignments', Request.Id = gblSelectedRequest.ID && Active = true), "AssignmentDueDate", SortOrder.Ascending)`, `TemplateSize: =72`, `TemplatePadding: =SpaceXs`, `Height: =Max(0, Self.AllItemsCount * (72 + SpaceXs * 2))`, `FillPortions: =0`, `ShowScrollbar: =false`, `OnSelect: |-\n  =Set(gblSelectedAssignment, ThisItem);\n  Set(gblSelectedDepartment, ThisItem.Department)`. Template: `cntPaneAssignmentRow` (Horizontal card, `Fill: =If(ThisItem.ID = gblSelectedAssignment.ID, ColorBrandTint, ColorSurface)`): texts (Title semibold; caption `=Coalesce(ThisItem.Department.Value, "Department not assigned") & " · Due " & If(IsBlank(ThisItem.AssignmentDueDate), "—", Text(ThisItem.AssignmentDueDate, "mmm d, yyyy")) & If(IsBlank(ThisItem.AssignedTo.DisplayName), "", " · " & ThisItem.AssignedTo.DisplayName)`), `bdgPaneAssignmentStatus` `ModernBadge` (assignment Switch: New→Info/Informative, Accepted→Checkmark/Informative, In Progress→ArrowClockwise/Highlight, Awaiting Clarification→Pause/Caution, Redaction→Edit/Attention, Complete→CheckmarkCircle/Positive, Cancelled→Dismiss/Neutral; `Visible: =App.Width >= BreakpointPhone`), `btnPaneAssignmentOpen` (`Icon: ="ChevronRight"`, IconOnly, `OnSelect: |-\n  =Set(gblSelectedAssignment, ThisItem);\n  Set(gblSelectedDepartment, ThisItem.Department);\n  cmpRequestDetailPane.OnOpenDepartmentWork()`). Every text child in the row: `OnSelect: =Select(Parent)`. Empty: `lblPaneAssignmentsEmpty` "No active department assignments for this request." `Visible: =galPaneAssignments.AllItemsCount = 0`.
6. `cntPaneTabActivity` (Vertical, `Visible: =tabPaneDetail.Selected.Value = "Activity"`): `galPaneTimeline` `Gallery` Vertical with a **synthetic timeline** built from the record (sortable ISO text keeps Date/DateTime columns from colliding in one `Table`):
```yaml
Items: |-
  =SortByColumns(
    Filter(
      Table(
        {When: Text(gblSelectedRequest.Created, "yyyy-mm-dd hh:mm"), Shown: Text(gblSelectedRequest.Created, "mmm d, yyyy"), Label: "Request created", Detail: "Logged by " & Coalesce(gblSelectedRequest.Author.DisplayName, "unknown"), Icon: "Add"},
        {When: Text(gblSelectedRequest.ReceivedDate, "yyyy-mm-dd") & " 00:00", Shown: Text(gblSelectedRequest.ReceivedDate, "mmm d, yyyy"), Label: "Received", Detail: "Intake: " & Coalesce(gblSelectedRequest.IntakeMethod.Value, "—") & " · Route: " & Coalesce(gblSelectedRequest.RequestRoute.Value, "—"), Icon: "Mail"},
        {When: Text(gblSelectedRequest.DueDate, "yyyy-mm-dd") & " 00:01", Shown: Text(gblSelectedRequest.DueDate, "mmm d, yyyy"), Label: If(gblSelectedRequest.DueDateConfirmed, "Due date confirmed", "Working due date (unconfirmed)"), Detail: "No statutory deadline is calculated by this app.", Icon: "Calendar"},
        {When: If(IsBlank(gblSelectedRequest.ExtensionStatus.Value), "", Text(gblSelectedRequest.Modified, "yyyy-mm-dd hh:mm")), Shown: Text(gblSelectedRequest.Modified, "mmm d, yyyy"), Label: "Extension " & Coalesce(gblSelectedRequest.ExtensionStatus.Value, ""), Detail: Coalesce(gblSelectedRequest.ExtensionType.Value, "—") & " · " & Text(Coalesce(gblSelectedRequest.ExtensionDays, 0)) & " days", Icon: "Clock"},
        {When: Text(gblSelectedRequest.FinalResponseDate, "yyyy-mm-dd") & " 23:59", Shown: Text(gblSelectedRequest.FinalResponseDate, "mmm d, yyyy"), Label: "Final response", Detail: Coalesce(gblSelectedRequest.CloseoutNotes, "No closeout notes"), Icon: "Send"},
        {When: Text(gblSelectedRequest.Modified, "yyyy-mm-dd hh:mm"), Shown: Text(gblSelectedRequest.Modified, "mmm d, yyyy"), Label: "Last modified", Detail: "By " & Coalesce(gblSelectedRequest.Editor.DisplayName, "unknown") & " · Status " & Coalesce(gblSelectedRequest.OverallStatus.Value, "—"), Icon: "Edit"}
      ),
      Len(When) > 6
    ),
    "When",
    SortOrder.Descending
  )
```
   `TemplateSize: =64`, `Height: =Max(0, Self.AllItemsCount * (64 + SpaceXs * 2))`, `FillPortions: =0`. Template `cntPaneTimelineRow` (Horizontal, `LayoutGap: =SpaceMd`, `LayoutAlignItems.Start`): `icoPaneTimeline` `ModernIcon` (`Icon: =ThisItem.Icon`, `IconColor: =ColorBrand`, 24×24, `AccessibleLabel: =ThisItem.Label`), `cntPaneTimelineText` (Vertical, `FillPortions: =1`) → `lblPaneTimelineLabel` (`Text: =ThisItem.Label`, Semibold, body), `lblPaneTimelineDetail` (`Text: =ThisItem.Shown & " · " & ThisItem.Detail`, caption, secondary). Empty: `lblPaneTimelineEmpty` "No dated activity yet." `Visible: =galPaneTimeline.AllItemsCount = 0`.

Accessibility: `tabPaneDetail.AccessibleLabel` set; every button has `AccessibleLabel`; focus order follows DOM order (head → quick actions → tabs → content). Width/height: fills host container; internally scrolls (`LayoutOverflowY.Scroll`) so hosts never nest a second scroller around it.

Instance snippet (Home desktop pane):
```yaml
- cmpHomeDetailPane:
    Control: CanvasComponent
    ComponentName: cmpRequestDetailPane
    Properties:
      AlignInContainer: =AlignInContainer.Stretch
      FillPortions: =1
      Height: =Parent.Height
      LayoutMinHeight: =0
      LayoutMinWidth: =0
      OnConfirmDueDate: |-
        =IfError(
          Patch('FOIA Pilot Requests', gblSelectedRequest, {DueDateConfirmed: true});
          Set(gblSelectedRequest, LookUp('FOIA Pilot Requests', ID = gblSelectedRequest.ID));
          Notify("Due date confirmed.", NotificationType.Success),
          Notify("The due date could not be confirmed: " & FirstError.Message, NotificationType.Error)
        )
      OnOpenCloseout: =Navigate(ResponseCloseout, ScreenTransition.None)
      OnOpenDepartmentWork: |-
        =If(IsBlank(gblSelectedAssignment) || gblSelectedAssignment.Request.Id <> gblSelectedRequest.ID,
          Set(gblSelectedAssignment, First(Filter('FOIA Pilot Assignments', Request.Id = gblSelectedRequest.ID && Active = true))));
        Set(gblSelectedDepartment, gblSelectedAssignment.Department);
        Navigate(DepartmentWork, ScreenTransition.None)
      ShowQuickActions: =true
      Visible: =!IsBlank(gblSelectedRequest)
      Width: =Parent.Width
```

## Per-Screen Specifications

### Shared screen skeleton (every screen)
Screen `Properties`: `Fill: =ColorNeutralBg`, `LoadingSpinnerColor: =ColorBrand`, `OnVisible` per screen. Children:
```
cnt<Screen>Shell            Vertical, Width/Height = Parent, Fill ColorNeutralBg, DropShadow None, radii 0
├─ cmp<Screen>Header        cmpAppHeader (FillPortions 0, Height HeaderHeight)
├─ cnt<Screen>Body          Horizontal, FillPortions 1, LayoutAlignItems Stretch, LayoutMinHeight 0
│  ├─ cmp<Screen>NavRail    cmpSideNav Placement "Rail", Visible App.Width >= BreakpointPhone
│  └─ cnt<Screen>ContentOuter  Vertical, FillPortions 1, LayoutAlignItems Center, LayoutMinWidth 0
│     └─ cnt<Screen>Content    Vertical, FillPortions 1, Width = Min(Parent.Width, ContentMaxWidth),
│                              padding = If(App.Width < BreakpointPhone, PagePaddingPhone, PagePaddingWide),
│                              LayoutGap SpaceMd, LayoutOverflowY Scroll (unless noted), LayoutMinWidth 0
└─ cmp<Screen>NavBottom     cmpSideNav Placement "Bottom", Visible App.Width < BreakpointPhone
```
Scroll rule: exactly one scroller per screen (`cnt<Screen>Content`), except Home desktop where the list pane gallery and the detail pane scroll independently. Children of a scrolling Vertical container use `FillPortions: =0` and an explicit `Height` (sum of their children + gaps + padding, v1 style) so AutoLayout can measure them.

Field block pattern (used by all forms): `cnt<Field>` Vertical, `FillPortions: =0`, `Height: =FieldHeight`, `LayoutMinHeight: =FieldHeight`, `LayoutGap: =6`, `LayoutMinWidth: =200`, `AlignInContainer: =AlignInContainer.Start`, `Width` per tier (see each screen); children `lbl<Field>` (caption, secondary, `Wrap: =false`) + the input (`AlignInContainer.Stretch`, `Height: =InputHeight`, `LayoutMinHeight: =InputHeight`, `LayoutMinWidth: =0`). Field groups are Horizontal containers with `LayoutWrap: =true`, `LayoutGap: =SpaceMd`.

---

### Home
- **File:** Home.pa.yaml
- **Purpose:** The single list screen for all tiers. Phone/tablet: KPI tiles → filters → list → tap navigates. Desktop: compact stat strip → status-distribution strip → master-detail (list pane 38 % | persistent `cmpRequestDetailPane`).
- **OnVisible:**
```
=Set(gblIsLoading, false);
Set(gblLoadError, false);
Set(gblPermissionDenied, false);
Set(gblSearchText, "");
Set(gblStatusFilter, "All");
Set(gblDepartmentFilter, "All")
```
  (`gblSelectedRequest` is intentionally **not** cleared so the desktop pane persists after returning from a sub-screen.)
- **Layout under `cntHomeContent`** (`LayoutOverflowY: =If(App.Width >= BreakpointDesktop, LayoutOverflow.Hide, LayoutOverflow.Scroll)`):
  1. `cntHomeKpis` — Horizontal, `LayoutWrap: =true`, `LayoutGap: =SpaceMd`, `FillPortions: =0`, `Height: =If(App.Width < BreakpointPhone, TileHeight * 4 + SpaceMd * 3, App.Width < BreakpointDesktop, TileHeight * 2 + SpaceMd, StatStripHeight)`. Four tiles `cntTileTotal`, `cntTileOpen`, `cntTileDueSoon`, `cntTileClosed` (card treatment):
     - `Width: =If(App.Width < BreakpointPhone, Parent.Width, App.Width < BreakpointDesktop, (Parent.Width - SpaceMd) / 2 - 1, (Parent.Width - SpaceMd * 3) / 4 - 1)`, `LayoutMaxWidth: =If(App.Width >= BreakpointDesktop, TileMaxWidth, 0)`, `Height: =If(App.Width >= BreakpointDesktop, StatStripHeight, TileHeight)`, `FillPortions: =0`.
     - `LayoutDirection: =If(App.Width >= BreakpointDesktop, LayoutDirection.Horizontal, LayoutDirection.Vertical)` — desktop renders icon · value · label inline (compact stat strip); phone/tablet stack head row (icon + caption) over big value over note.
     - Children: `cntTile<X>Head` (Horizontal, icon 20 px `ModernIcon` + caption label), `lblTile<X>Value` (KPI tier size, Semibold, `AccessibleLabel: ="<label>: " & Self.Text`), `lblTile<X>Note` (caption, `Visible: =App.Width < BreakpointDesktop`).
     - Values (v1 formulas, delegable):
       - Total: `=Text(CountRows('FOIA Pilot Requests'))`, icon `"Document"`, colour `ColorBrand`, note "All requests"
       - Open: `=Text(CountRows(Filter('FOIA Pilot Requests', OverallStatus.Value <> "Closed")))`, icon `"ArrowClockwise"`, `ColorInfo`, note "Open / in progress"
       - Due within 7 days: `=Text(CountRows(Filter('FOIA Pilot Requests', DueDateConfirmed = true && DueDate <= DateAdd(Today(), 7, TimeUnit.Days))))`, icon `"Warning"`, `ColorWarning`, note "Confirmed working due dates only"
       - Closed: `=Text(CountRows(Filter('FOIA Pilot Requests', OverallStatus.Value = "Closed")))`, icon `"CheckmarkCircle"`, `ColorSuccess`, note "Closed requests"
  2. `cntHomeDistribution` — **desktop only** (`Visible: =App.Width >= BreakpointDesktop`), Vertical, `FillPortions: =0`, `Height: =SpaceSm + SpaceXs + 20`, `LayoutGap: =SpaceXs`. Adds information: proportional status mix.
     - `cntDistributionBar` Horizontal, `Height: =SpaceSm`, `LayoutGap: =2`, radii `=RadiusSm`, `LayoutMinHeight: =SpaceSm`. Four segment containers `cntSegNew` / `cntSegInProgress` / `cntSegOnHold` / `cntSegClosed`: `Fill` = `ColorInfo` / `ColorBrand` / `ColorWarning` / `ColorSuccess`; `FillPortions: =CountRows(Filter('FOIA Pilot Requests', OverallStatus.Value = "<Status>"))`; `Height: =Parent.Height`; `LayoutMinWidth: =0`; `LayoutMinHeight: =0`; `Visible: =Self.FillPortions > 0` is **not** valid — instead set `Width: =0` is unnecessary; a zero `FillPortions` segment simply collapses.
     - `cntDistributionLegend` Horizontal, `LayoutGap: =SpaceMd`, `Height: =20`: four `ModernText` captions, e.g. `lblLegendNew`: `Text: ="New " & CountRows(Filter('FOIA Pilot Requests', OverallStatus.Value = "New"))`, `Color: =ColorInfo`, Semibold; likewise In Progress (`ColorBrand`), On Hold (`ColorWarning`), Closed (`ColorSuccess`). `AccessibleLabel: ="Status distribution: " & Self.Text`.
  3. `cntHomeMasterDetail` — `LayoutDirection: =If(App.Width >= BreakpointDesktop, LayoutDirection.Horizontal, LayoutDirection.Vertical)`, `LayoutGap: =SpaceMd`, `LayoutAlignItems: =LayoutAlignItems.Stretch`, `FillPortions: =If(App.Width >= BreakpointDesktop, 1, 0)`, `Height: =If(App.Width >= BreakpointDesktop, Parent.Height, cntHomeListPane.Height)`, `LayoutMinHeight: =0`.
     - **`cntHomeListPane`** Vertical, `LayoutGap: =SpaceSm`, `FillPortions: =0`, `Width: =If(App.Width >= BreakpointDesktop, Parent.Width * ListPaneRatio, Parent.Width)`, `LayoutMinWidth: =320`, `Height: =If(App.Width >= BreakpointDesktop, Parent.Height, cntHomeFilters.Height + lblQueueLoading.Height + lblQueueError.Height + lblQueuePermission.Height + lblQueueEmpty.Height + galRequests.Height + SpaceSm * 5)`:
       - `cntHomeFilters` — `LayoutDirection: =If(App.Width >= BreakpointPhone && App.Width < BreakpointDesktop, LayoutDirection.Horizontal, LayoutDirection.Vertical)` (phone stacked; tablet one row; desktop list pane stacked because the pane is narrow), `LayoutWrap: =true`, `LayoutGap: =SpaceSm`, `FillPortions: =0`, `Height: =If(App.Width >= BreakpointPhone && App.Width < BreakpointDesktop, InputHeight, InputHeight * 3 + SpaceSm * 2)`:
         - `txtSearch` `ModernTextInput`: `Type: =TextInputType.Search`, `Placeholder: ="Search title, requester, or description"`, `AccessibleLabel: ="Search requests"`, `TriggerOutput: =TriggerOutput.Delayed`, `OnChange: =Set(gblSearchText, Self.Text)`, `Height: =InputHeight`, `FillPortions: =If(App.Width >= BreakpointPhone && App.Width < BreakpointDesktop, 1, 0)`, `Width: =Parent.Width`, `LayoutMinWidth: =200`, `AlignInContainer: =AlignInContainer.Stretch`.
         - `cmbStatusFilter` `ModernDropdown`: `Items: =["All", "New", "In Progress", "On Hold", "Closed"]`, `ItemDisplayText: =ThisItem.Value`, `Default: =First(["All", "New", "In Progress", "On Hold", "Closed"])`, `OnChange: =Set(gblStatusFilter, Self.Selected.Value)`, `AccessibleLabel: ="Filter requests by status"`, `Width: =If(App.Width >= BreakpointPhone && App.Width < BreakpointDesktop, 180, Parent.Width)`, `LayoutMinWidth: =160`.
         - `cmbDepartmentFilter` `ModernDropdown`: `Items: =Ungroup(Table({Options: Table({Value:"All"})}, {Options: Distinct(Filter('FOIA Pilot Departments', Active = true), Title)}), Options)`, `Default: =First(<same expression>)`, `OnChange: =Set(gblDepartmentFilter, Self.Selected.Value)`, `Visible: =App.Width >= BreakpointPhone` (progressive disclosure: hidden on phone), `Width: =If(App.Width >= BreakpointPhone && App.Width < BreakpointDesktop, 220, Parent.Width)`. (`Distinct` over a filtered small reference table — ≤ 20 departments; approved bound.)
       - State labels (`FillPortions: =0`, `AutoHeight`): `lblQueueLoading` "Loading requests…" `Visible: =gblIsLoading`; `lblQueueError` (ColorCritical) "We couldn't load the request queue. Select Refresh to try again." `Visible: =gblLoadError && !gblPermissionDenied`; `lblQueuePermission` (ColorWarning) "You don't have permission to view FOIA requests. Contact a site owner for access." `Visible: =gblPermissionDenied`; `lblQueueEmpty` "No requests match these filters." `Visible: =!gblIsLoading && !gblLoadError && !gblPermissionDenied && galRequests.AllItemsCount = 0`.
       - **`galRequests`** `Gallery` `Variant: Vertical`: `AccessibleLabel: ="FOIA requests"`, `TabIndex: =0`, `TemplatePadding: =SpaceXs`, `TemplateSize: =If(App.Width < BreakpointPhone, 92, 76)`, `ShowScrollbar: =App.Width >= BreakpointDesktop`, `LoadingSpinner: =LoadingSpinner.Controls`, `FillPortions: =If(App.Width >= BreakpointDesktop, 1, 0)`, `Height: =If(App.Width >= BreakpointDesktop, Parent.Height, Max(0, Self.AllItemsCount * (Self.TemplateSize + SpaceXs * 2)))`, `LayoutMinHeight: =0`, `LayoutMinWidth: =0`, `Width: =Parent.Width`, `Visible: =!gblIsLoading && !gblLoadError && !gblPermissionDenied`, `Items` (v1, delegable `StartsWith`):
```
=SortByColumns(
  Filter(
    'FOIA Pilot Requests',
    (gblStatusFilter = "All" || OverallStatus.Value = gblStatusFilter) &&
    (gblDepartmentFilter = "All" || PrimaryDepartment.Value = gblDepartmentFilter) &&
    (IsBlank(gblSearchText) ||
      StartsWith(Title, gblSearchText) ||
      StartsWith(RequesterLastName, gblSearchText) ||
      StartsWith(RequestDescription, gblSearchText))
  ),
  "ReceivedDate",
  SortOrder.Descending
)
```
         `OnSelect: |-\n  =Set(gblSelectedRequest, ThisItem);\n  If(App.Width < BreakpointDesktop, Navigate(RequestDetail, ScreenTransition.Fade))`.
         Template `cntRequestRow` (Horizontal card; `Fill: =If(App.Width >= BreakpointDesktop && ThisItem.ID = gblSelectedRequest.ID, ColorBrandTint, ColorSurface)`, `Height: =Parent.TemplateHeight`, `Width: =Parent.TemplateWidth`, `LayoutGap: =SpaceMd`, padding `SpaceSm`/`SpaceMd`): `cntRequestRowText` (Vertical, `FillPortions: =1`, `LayoutMinWidth: =120`) → `lblRequestRowTitle` (Semibold, body tier size, `Wrap: =false`, `OnSelect: =Select(Parent)`), `lblRequestRowMeta` (caption: `=ThisItem.RequesterFirstName & " " & ThisItem.RequesterLastName & " · Received " & If(IsBlank(ThisItem.ReceivedDate), "—", Text(ThisItem.ReceivedDate, "mmm d, yyyy")) & If(App.Width < BreakpointPhone, " · " & Coalesce(ThisItem.OverallStatus.Value, "Not set"), "")`, `OnSelect: =Select(Parent)`); `bdgRequestRowStatus` `ModernBadge` (status Switch, 24×112, `Size: =12`, `Visible: =App.Width >= BreakpointPhone`); `btnRequestRowOpen` `ModernButton` (`Icon: ="ChevronRight"`, `Layout: =ButtonLayout.IconOnly`, Subtle, 44×44, `AccessibleLabel: ="Open request " & ThisItem.Title`, `OnSelect: =Select(Parent)`, `Visible: =App.Width < BreakpointDesktop`).
     - **`cntHomeDetailPane`** Vertical, `Visible: =App.Width >= BreakpointDesktop`, `FillPortions: =1`, `LayoutMinWidth: =0`, `LayoutMinHeight: =0`, `LayoutAlignItems: =LayoutAlignItems.Stretch`:
       - `cntHomeDetailEmpty` (card, `Visible: =IsBlank(gblSelectedRequest)`, `FillPortions: =1`, `LayoutAlignItems: =LayoutAlignItems.Center`, `LayoutJustifyContent: =LayoutJustifyContent.Center`, `LayoutGap: =SpaceSm`): `icoDetailEmpty` `ModernIcon` (`Icon: ="DocumentSearch"`, 48×48, `IconColor: =ColorTextSecondary`, `AccessibleLabel: ="No request selected"`), `lblDetailEmptyTitle` "Select a request" (Section size, Semibold, `Align: =Align.Center`), `lblDetailEmptyHint` "Summary, department assignments, and a dated activity timeline will appear here." (caption, centered, `Width: =320`), `btnDetailEmptyNew` ModernButton `BasePaletteColor: =ColorBrand`, `Icon: ="Add"`, "New request", `OnSelect: =Navigate(NewRequest, ScreenTransition.Fade)`.
       - `cmpHomeDetailPane` — the instance snippet in the Component Contracts section (`Visible: =!IsBlank(gblSelectedRequest)`).
- **Navigation:** header primary → NewRequest; header secondary → Refresh; row tap → RequestDetail (phone/tablet) or select (desktop); pane events → DepartmentWork / ResponseCloseout.
- **State:** filters reset in OnVisible; `gblSelectedRequest` preserved.

### RequestDetail
- **File:** RequestDetail.pa.yaml
- **Purpose:** Thin full-screen host for `cmpRequestDetailPane` on phone/tablet (and reachable on desktop). No business logic of its own beyond event handlers.
- **OnVisible:** `=Set(gblIsLoading, false); Set(gblLoadError, false); Set(gblPermissionDenied, false); Set(gblSaveSuccess, false); Set(gblExtensionValidationMessage, "")`
- **Header:** `cmpRequestDetailHeader` — `ShowBack: =true`, `OnBack: =Navigate(Home, ScreenTransition.None)`, `Title: =Coalesce(gblSelectedRequest.Title, "Request detail")`, `Subtitle: =If(IsBlank(gblSelectedRequest), "", "Received " & Text(gblSelectedRequest.ReceivedDate, "mmm d, yyyy"))`, `PrimaryLabel: ="Closeout"`, `PrimaryIcon: ="CheckmarkCircle"`, `OnPrimary: =Navigate(ResponseCloseout, ScreenTransition.None)`, no secondary.
- **Nav:** rail/bottom with `ActiveScreen: ="Home"`.
- **Content** (`cntRequestDetailContent`, `LayoutOverflowY: =LayoutOverflow.Hide` — the pane scrolls itself):
  - `cntRequestDetailEmpty` (`Visible: =IsBlank(gblSelectedRequest)`, same empty-state composition as Home's but hint omitted on phone: `lblDetailEmptyHint.Visible: =App.Width >= BreakpointPhone`; action button "Go to Home" → `Navigate(Home, ScreenTransition.None)`).
  - `cmpRequestDetailPaneHost` — `cmpRequestDetailPane`, `FillPortions: =1`, `Visible: =!IsBlank(gblSelectedRequest)`, `ShowQuickActions: =true`, event handlers **identical** to Home's instance (`OnConfirmDueDate` Patch inside `IfError`; `OnOpenDepartmentWork`; `OnOpenCloseout`).
- **Navigation:** back → Home; pane events → DepartmentWork / ResponseCloseout.

### NewRequest
- **File:** NewRequest.pa.yaml
- **Purpose:** Intake form. Keeps v1 write logic exactly.
- **OnVisible** (v1):
```
=Set(gblIsLoading, false);
Set(gblLoadError, false);
Set(gblSaveSuccess, false);
Set(gblDueDateConfirmed, false);
Reset(txtRequesterFirstName); Reset(txtRequesterLastName); Reset(txtRequesterEmail); Reset(txtRequesterPhone);
Reset(txtRequestDescription); Reset(cmbPrimaryDepartment); Reset(cmbIntakeMethod); Reset(cmbRequestRoute);
Reset(cmbDeliveryFormat); Reset(datReceivedDate); Reset(datDueDate); Reset(chkDueDateConfirmed);
Reset(chkCertifiedCopies); Reset(chkFeeWaiverRequested)
```
- **Header:** `Title: ="New FOIA request"`, `Subtitle: ="Record the intake exactly as received"`, `ShowBack: =true`, `OnBack: =Navigate(Home, ScreenTransition.None)`, no primary/secondary (actions live in the action bar).
- **Layout under `cntNewRequestContent`:** `cntNewRequestColumns` — `LayoutDirection: =If(App.Width >= BreakpointDesktop, LayoutDirection.Horizontal, LayoutDirection.Vertical)`, `LayoutGap: =SpaceLg`, `LayoutAlignItems: =LayoutAlignItems.Start`, `FillPortions: =0`, `Height: =If(App.Width >= BreakpointDesktop, Max(cntNewRequestForm.Height, cntIntakeGuidance.Height), cntNewRequestForm.Height)`:
  - **`cntNewRequestForm`** Vertical, `LayoutGap: =SpaceMd`, `FillPortions: =If(App.Width >= BreakpointDesktop, 1, 0)`, `Width: =Parent.Width` on phone/tablet, `Height` = sum of its three cards + gaps + action bar. Three **cards** (one group per card; card treatment; Vertical; `LayoutGap: =SpaceSm`; padding `SpaceMd`; `FillPortions: =0`; `Height` = title + field rows + gaps + padding):
    1. `cntCardRequester` — `lblRequesterSection` "Requester information" (Section, Semibold) + `cntRequesterFields` (Horizontal wrap) with field blocks `cntRequesterFirstName`*, `cntRequesterLastName`*, `cntRequesterEmail`, `cntRequesterPhone`. Inputs `txtRequesterFirstName` (`Required: =true`, `MaxLength: =100`), `txtRequesterLastName` (same), `txtRequesterEmail` (`MaxLength: =255`), `txtRequesterPhone` (`MaxLength: =30`).
    2. `cntCardRequest` — "Request details": `cntRequestDescriptionField` full width (`txtRequestDescription` `Type: =TextInputType.Multiline`, `Height: =112`, `MaxLength: =4000`, `Required: =true`, caption "What records are being requested? *") then wrap row: `cmbPrimaryDepartment`* (`ModernCombobox`, `Items: =SortByColumns(Filter('FOIA Pilot Departments', Active = true), "SortOrder", SortOrder.Ascending)`, `ItemDisplayText: =ThisItem.Title`, `SelectMultiple: =false`, `IsSearchable: =true`, `InputTextPlaceholder: ="Select a department"`), `cmbIntakeMethod`* (`Items: =Choices('FOIA Pilot Requests'.IntakeMethod)`, `ItemDisplayText: =ThisItem.Value`, `DefaultSelectedItems: =LookUp(Choices('FOIA Pilot Requests'.IntakeMethod), Value = "Online Form")`, `SelectMultiple: =false`, `IsSearchable: =false`), `cmbRequestRoute`* (`Items: =Choices('FOIA Pilot Requests'.RequestRoute)`, `ItemDisplayText: =ThisItem.Value`, `SelectMultiple: =false`, `IsSearchable: =false`, `InputTextPlaceholder: ="Select a route"`), `cmbDeliveryFormat` (`Items: =Choices('FOIA Pilot Requests'.DeliveryFormat)`).
    3. `cntCardDates` — "Dates and confirmations": wrap row `datReceivedDate`* (`ModernDatePicker`, `DefaultDate: =Today()`, `Format: =DatePickerFormat.Short`, `IsEditable: =true`), `datDueDate`* (`DefaultDate: =Blank()`, `Placeholder: ="Working due date"`); then `chkDueDateConfirmed` (`ModernCheckbox`, `Label: ="A person confirmed this working due date"`, `OnCheck: =Set(gblDueDateConfirmed, true)`, `OnUncheck: =Set(gblDueDateConfirmed, false)`, `Height: =InputHeight`, `CheckboxSize: =22`), `lblDueDateHelp` caption "No statutory deadline is calculated by this app.", `chkCertifiedCopies` (`Label: ="Certified copies requested"`), `chkFeeWaiverRequested` (`Label: ="Fee waiver requested"`).
    - Field block `Width` per tier: `=If(App.Width < BreakpointPhone, Parent.Width, App.Width < BreakpointDesktop, (Parent.Width - SpaceMd) / 2 - 1, (Parent.Width - SpaceMd * 2) / 3 - 1)` (1 / 2 / 3 columns). Starred (*) captions end with ` *`.
    - Status labels after the cards (`AutoHeight`, `FillPortions: =0`): `lblRequestValidation` (caption, `ColorWarning`, `Text: ="Complete the required fields and confirm the working due date to enable Save."`, `Visible: =btnSaveRequest.DisplayMode = DisplayMode.Disabled && !gblPermissionDenied`), `lblRequestError` (`ColorCritical`, "The request could not be saved. Check your access and try again.", `Visible: =gblLoadError && !gblPermissionDenied`), `lblRequestPermission` (`ColorWarning`, "You do not have permission to create requests in the connected SharePoint list.", `Visible: =gblPermissionDenied`), `lblRequestSuccess` (`ColorSuccess`, "Request saved successfully.", `Visible: =gblSaveSuccess`).
  - **`cntIntakeGuidance`** — **desktop only** read-only side card (`Visible: =App.Width >= BreakpointDesktop`, `FillPortions: =0`, `Width: =320`, `LayoutMinWidth: =280`, card treatment, Vertical, `LayoutGap: =SpaceSm`, padding `SpaceMd`, `Height` = sum of labels): `lblGuidanceTitle` "Intake guidance" (Section, Semibold); `lblGuidanceRoutes` body: "Routing: General records go to the Village Clerk's office; police records (reports, body-cam, dispatch) follow the Police route and are worked by the Police Department. Pick the Primary department that holds the records."; `lblGuidanceDueDate` body: "Due date rule: this app never calculates a statutory deadline. Enter the working due date staff agreed on, then tick the confirmation checkbox — Save stays disabled until a person confirms it."; `lblGuidanceIntake` body: "Intake method defaults to Online Form; change it for mail, email, phone, or walk-in. Received date defaults to today."; `lblGuidanceStatus` caption: "New requests are saved with status New and open in the detail view."
- **Sticky action bar `cntNewRequestActions`** — a direct child of `cntNewRequestShell` placed **between** `cntNewRequestBody` and `cmpNewRequestNavBottom` (so it is always visible above the bottom nav, outside the scroller): Horizontal, `Fill: =ColorSurface`, `BorderColor: =ColorNeutralStroke`, `BorderThickness: =1`, radii 0, `DropShadow: =DropShadow.None`, `FillPortions: =0`, `Height: =ControlMinTouch + SpaceSm * 2`, padding `SpaceSm` vertical / page padding horizontal, `LayoutGap: =SpaceSm`, `LayoutJustifyContent: =If(App.Width < BreakpointPhone, LayoutJustifyContent.SpaceBetween, LayoutJustifyContent.End)`, `LayoutAlignItems: =LayoutAlignItems.Center`:
  - `btnCancelRequest` (Secondary, `Text: ="Cancel"`, `Width: =If(App.Width < BreakpointPhone, (Parent.Width - PagePaddingPhone * 2 - SpaceSm) / 2, 120)`, `OnSelect: =Navigate(Home, ScreenTransition.None)`, `AccessibleLabel: ="Cancel new request"`).
  - `btnSaveRequest` (`BasePaletteColor: =ColorBrand`, `Text: ="Save request"`, `Width: =If(App.Width < BreakpointPhone, (Parent.Width - PagePaddingPhone * 2 - SpaceSm) / 2, 150)`, `AccessibleLabel: ="Save new FOIA request"`), `DisplayMode` **exactly v1**:
```
=If(
  IsBlank(txtRequesterFirstName.Text) || IsBlank(txtRequesterLastName.Text) || IsBlank(txtRequestDescription.Text) || IsBlank(cmbPrimaryDepartment.Selected) || IsBlank(cmbRequestRoute.Selected) || IsBlank(cmbIntakeMethod.Selected) || IsBlank(datReceivedDate.SelectedDate) || IsBlank(datDueDate.SelectedDate) || !gblDueDateConfirmed || gblPermissionDenied,
  DisplayMode.Disabled,
  DisplayMode.Edit
)
```
    `OnSelect` **exactly v1** (only the navigation target is unchanged — RequestDetail):
```
=Set(gblIsLoading, true);
Set(gblLoadError, false);
Set(gblSaveSuccess, false);
IfError(
  Set(
    gblSelectedRequest,
    Patch(
      'FOIA Pilot Requests',
      Defaults('FOIA Pilot Requests'),
      {
        Title: Concatenate(txtRequesterLastName.Text, ", ", txtRequesterFirstName.Text),
        RequesterFirstName: txtRequesterFirstName.Text,
        RequesterLastName: txtRequesterLastName.Text,
        RequesterEmail: txtRequesterEmail.Text,
        RequesterPhone: txtRequesterPhone.Text,
        RequestDescription: txtRequestDescription.Text,
        PrimaryDepartment: {Id: cmbPrimaryDepartment.Selected.ID, Value: cmbPrimaryDepartment.Selected.Title},
        IntakeMethod: cmbIntakeMethod.Selected,
        RequestRoute: cmbRequestRoute.Selected,
        DeliveryFormat: cmbDeliveryFormat.Selected,
        OverallStatus: LookUp(Choices('FOIA Pilot Requests'.OverallStatus), Value = "New"),
        ReceivedDate: datReceivedDate.SelectedDate,
        DueDate: datDueDate.SelectedDate,
        DueDateConfirmed: gblDueDateConfirmed,
        CertifiedCopies: LookUp(Choices('FOIA Pilot Requests'.CertifiedCopies), Value = If(chkCertifiedCopies.Checked, "Yes", "No")),
        FeeWaiverRequested: LookUp(Choices('FOIA Pilot Requests'.FeeWaiverRequested), Value = If(chkFeeWaiverRequested.Checked, "Yes", "No"))
      }
    )
  );
  Set(gblIsLoading, false);
  Set(gblSaveSuccess, true);
  Navigate(RequestDetail, ScreenTransition.Fade),
  Set(gblIsLoading, false);
  Set(gblLoadError, true);
  Notify("The request could not be saved: " & FirstError.Message, NotificationType.Error)
)
```
    (All six required columns — Title, ReceivedDate, IntakeMethod, RequestRoute, RequestDescription, OverallStatus — are set; the gate blocks when any input feeding them is blank.)
- **Navigation:** Cancel/back → Home; success → RequestDetail.

### DepartmentWork
- **File:** DepartmentWork.pa.yaml
- **Purpose:** Pick an assignment card, edit status / due date / redaction / notes, save or mark complete; see the department's linked records. v1 write logic kept.
- **OnVisible** (v1):
```
=Set(gblIsLoading, true);
Set(gblLoadError, false);
Set(gblPermissionDenied, false);
Set(gblSaveSuccess, false);
If(IsBlank(gblSelectedAssignment), Set(gblSelectedAssignment, First(Filter('FOIA Pilot Assignments', Request.Id = gblSelectedRequest.ID && Active = true))));
Set(gblSelectedDepartment, If(IsBlank(gblSelectedAssignment), Blank(), gblSelectedAssignment.Department));
Set(gblIsLoading, false)
```
- **Header:** `Title: ="Department work"`, `Subtitle: =Coalesce(gblSelectedRequest.Title, "")`, `ShowBack: =true`, `OnBack: =Navigate(If(App.Width >= BreakpointDesktop, Home, RequestDetail), ScreenTransition.None)`, `SecondaryLabel: ="Refresh"`, `SecondaryIcon: ="ArrowClockwise"`, `OnSecondary: =Refresh('FOIA Pilot Assignments'); Refresh('FOIA Pilot Records')`.
- **Content** (`cntDepartmentWorkContent`, scrolls):
  1. `cntDeptEmpty` (`Visible: =IsBlank(gblSelectedRequest)`): empty state "Select a request first" + button "Go to Home".
  2. `cntDeptAssignmentsCard` (card; `Visible: =!IsBlank(gblSelectedRequest)`): `lblDeptAssignmentsTitle` "Department assignments" (Section) + **`galAssignments`** `Gallery` `Variant: Vertical` with `WrapCount: =If(App.Width < BreakpointPhone, 1, App.Width < BreakpointDesktop, 2, 3)` (1 / 2 / 3 columns), `Items: =SortByColumns(Filter('FOIA Pilot Assignments', Request.Id = gblSelectedRequest.ID && Active = true), "AssignmentDueDate", SortOrder.Ascending)`, `TemplateSize: =If(App.Width < BreakpointPhone, 148, 164)`, `TemplatePadding: =SpaceXs`, `Height: =Max(0, RoundUp(Self.AllItemsCount / Self.WrapCount, 0) * (Self.TemplateSize + SpaceXs * 2))`, `FillPortions: =0`, `ShowScrollbar: =false`, `OnSelect: |-\n  =Set(gblSelectedAssignment, ThisItem);\n  Set(gblSelectedDepartment, ThisItem.Department);\n  Set(gblSaveSuccess, false)`. Template `cntAssignmentCard` (Vertical card, `Fill: =If(ThisItem.ID = gblSelectedAssignment.ID, ColorBrandTint, ColorSurface)`, `BorderColor: =If(ThisItem.ID = gblSelectedAssignment.ID, ColorBrand, ColorNeutralStroke)`): `lblAssignmentCardTitle` (Semibold, `OnSelect: =Select(Parent)`), `lblAssignmentCardDept` (caption `=If(IsBlank(ThisItem.Department), "Department not assigned", ThisItem.Department.Value) & " · Due " & If(IsBlank(ThisItem.AssignmentDueDate), "—", Text(ThisItem.AssignmentDueDate, "mmm d, yyyy"))`, `OnSelect: =Select(Parent)`), `cntAssignmentCardFooter` (Horizontal, SpaceBetween): `bdgAssignmentCardStatus` `ModernBadge` (assignment Switch, 24×112, `Size: =12`) + `btnAssignmentCardSelect` (`Appearance: =If(ThisItem.ID = gblSelectedAssignment.ID, ButtonAppearance.Primary, ButtonAppearance.Secondary)`, `BasePaletteColor: =ColorBrand`, `Text: =If(ThisItem.ID = gblSelectedAssignment.ID, "Selected", "Select")`, `Icon: =If(ThisItem.ID = gblSelectedAssignment.ID, "Checkmark", "")`, `Layout: =If(ThisItem.ID = gblSelectedAssignment.ID, ButtonLayout.IconBefore, ButtonLayout.TextOnly)`, `Height: =ControlMinTouch`, `Width: =110`, `OnSelect: =Select(Parent)`). `lblAssignmentsEmpty` "No active department assignments for this request." `Visible: =galAssignments.AllItemsCount = 0`.
  3. `cntDepartmentWorkEditor` (card; `Visible: =!IsBlank(gblSelectedAssignment)`): `lblAssignmentEditorTitle` `="Update " & Coalesce(gblSelectedAssignment.Title, "assignment")` (Section); `cntAssignmentEditorRow` (Horizontal wrap) field blocks with per-tier width `=If(App.Width < BreakpointPhone, Parent.Width, App.Width < BreakpointDesktop, (Parent.Width - SpaceMd) / 2 - 1, (Parent.Width - SpaceMd * 2) / 3 - 1)`:
     - `cmbAssignmentStatus` `ModernDropdown`: `Items: =Choices('FOIA Pilot Assignments'.AssignmentStatus)`, `ItemDisplayText: =ThisItem.Value`, `Default: =If(IsBlank(gblSelectedAssignment), Blank(), gblSelectedAssignment.AssignmentStatus)`.
     - `datAssignmentDueDate` `ModernDatePicker`: `DefaultDate: =If(IsBlank(gblSelectedAssignment), Blank(), gblSelectedAssignment.AssignmentDueDate)`, `Format: =DatePickerFormat.Short`, `IsEditable: =true`.
     - `tglRedactionRequired` `ModernToggle`: `Default: =If(IsBlank(gblSelectedAssignment), false, gblSelectedAssignment.RedactionRequired.Value = "Yes")`, `Label: ="Required"`, `ToggleSize: =24`, `Height: =InputHeight`.
     - `lblAssignmentGuidance` caption: "Confirm the human-entered due date before saving. Use response notes to describe records found, exemptions, or follow-up needed."
     - `txtResponseNotes` `ModernTextInput` Multiline, `Height: =96`, `MaxLength: =4000`, `Required: =true`, `Default: =If(IsBlank(gblSelectedAssignment), "", Coalesce(gblSelectedAssignment.ResponseNotes, ""))`, `Placeholder: ="Add department response notes"`.
     - `cntAssignmentActions` (Vertical on phone / Horizontal otherwise, `LayoutGap: =SpaceSm`/`SpaceMd`): **`btnSaveAssignment`** `DisplayMode: =If(IsBlank(gblSelectedAssignment) || IsBlank(cmbAssignmentStatus.Selected) || IsBlank(datAssignmentDueDate.SelectedDate) || IsBlank(Trim(txtResponseNotes.Text)) || gblPermissionDenied, DisplayMode.Disabled, DisplayMode.Edit)`, `OnSelect` **exactly v1**:
```
=Set(gblSaveSuccess, false);
If(IsBlank(cmbAssignmentStatus.Selected) || IsBlank(datAssignmentDueDate.SelectedDate) || IsBlank(Trim(txtResponseNotes.Text)),
  Notify("Status, due date, and response notes are required.", NotificationType.Error),
  IfError(
    Patch('FOIA Pilot Assignments', gblSelectedAssignment, {AssignmentStatus: cmbAssignmentStatus.Selected, AssignmentDueDate: datAssignmentDueDate.SelectedDate, RedactionRequired: {Value: If(tglRedactionRequired.Checked, "Yes", "No")}, ResponseNotes: txtResponseNotes.Text});
    Set(gblSelectedAssignment, LookUp('FOIA Pilot Assignments', ID = gblSelectedAssignment.ID));
    Set(gblSaveSuccess, true);
    Notify("Assignment saved.", NotificationType.Success),
    Notify("The assignment could not be saved: " & FirstError.Message, NotificationType.Error)
  )
)
```
       **`btnMarkComplete`** (Secondary, `Icon: ="CheckmarkCircle"`, `DisplayMode: =If(IsBlank(gblSelectedAssignment) || IsBlank(Trim(txtResponseNotes.Text)) || gblPermissionDenied, DisplayMode.Disabled, DisplayMode.Edit)`), `OnSelect` **exactly v1**:
```
=If(IsBlank(Trim(txtResponseNotes.Text)),
  Notify("Add response notes before marking the assignment complete.", NotificationType.Error),
  IfError(
    Patch('FOIA Pilot Assignments', gblSelectedAssignment, {AssignmentStatus: {Value: "Complete"}, DepartmentCompleteDate: Today(), ResponseNotes: txtResponseNotes.Text, RedactionRequired: {Value: If(tglRedactionRequired.Checked, "Yes", "No")}});
    Set(gblSelectedAssignment, LookUp('FOIA Pilot Assignments', ID = gblSelectedAssignment.ID));
    Set(gblSaveSuccess, true);
    Notify("Assignment marked complete.", NotificationType.Success),
    Notify("The assignment could not be marked complete: " & FirstError.Message, NotificationType.Error)
  )
)
```
       Buttons `Height: =ControlMinTouch`; on phone `AlignInContainer.Stretch`, otherwise `Width: =180` / `=190`. `lblAssignmentSaved` (`ColorSuccess`, "Changes saved.", `Visible: =gblSaveSuccess`).
     - **YAML note:** the two `Patch` calls above contain `{Value: ...}` record literals → the whole `OnSelect` must be a `|-` block (block scalars are safe; only inline plain scalars need quoting).
  4. `cntDepartmentRecords` (card; `Visible: =!IsBlank(gblSelectedAssignment)`): `lblDepartmentRecordsTitle` "Linked records" (Section), `lblDepartmentRecordsMeta` caption `="Records for " & Coalesce(gblSelectedAssignment.Department.Value, "this department")`, `galDepartmentRecords` Gallery Vertical `Items: =If(IsBlank(gblSelectedAssignment), Blank(), Filter('FOIA Pilot Records', Request.Id = gblSelectedRequest.ID && Department.Id = gblSelectedAssignment.Department.Id))`, `TemplateSize: =52`, computed `Height`; row: `icoRecord` `ModernIcon` `"Document"` 20 px, `lblRecordTitle` (Semibold, `=ThisItem.Title`), `lblRecordMeta` (caption `=Coalesce(ThisItem.DocumentType.Value, "Document") & " · " & Coalesce(ThisItem.RedactionStatus.Value, "No redaction status") & If(ThisItem.IsFinalResponse, " · Final response", "")`), desktop extra `bdgRecordSensitivity` `ModernBadge` (`Content: =Coalesce(ThisItem.Sensitivity.Value, "Unlabelled")`, `Intent: =BadgeIntent.Neutral`, `Visible: =App.Width >= BreakpointDesktop`). `lblDepartmentRecordsEmpty` "No records are linked to this department yet." `Visible: =galDepartmentRecords.AllItemsCount = 0 && !IsBlank(gblSelectedAssignment)`.
- **Tiering:** cards 1/2/3 columns via `WrapCount`; editor fields 1/2/3 columns; on desktop `cntDeptAssignmentsCard` and `cntDepartmentWorkEditor` sit in a Horizontal `cntDeptTopRow` (editor `FillPortions: =1`, assignments `Width: =Parent.Width * 0.55`) — on phone/tablet stacked vertically (`LayoutDirection` tier test). Records card always full width below.
- **Navigation:** back → Home (desktop) / RequestDetail (phone/tablet).

### ResponseCloseout
- **File:** ResponseCloseout.pa.yaml
- **Purpose:** Readiness summary + final-response form; closes the request. v1 write logic kept.
- **OnVisible:** `=Set(gblIsLoading, false); Set(gblLoadError, false); Set(gblSaveSuccess, false)`
- **Header:** `Title: ="Response closeout"`, `Subtitle: =Coalesce(gblSelectedRequest.Title, "")`, `ShowBack: =true`, `OnBack: =Navigate(If(App.Width >= BreakpointDesktop, Home, RequestDetail), ScreenTransition.None)`.
- **Content** (`cntResponseCloseoutContent`, scrolls): `cntCloseoutEmpty` (`Visible: =IsBlank(gblSelectedRequest)`, empty state + "Go to Home"); then `cntCloseoutColumns` — `LayoutDirection: =If(App.Width >= BreakpointDesktop, LayoutDirection.Horizontal, LayoutDirection.Vertical)`, `LayoutGap: =SpaceLg`, `LayoutAlignItems: =LayoutAlignItems.Start`, `Visible: =!IsBlank(gblSelectedRequest)`:
  1. **`cntCloseoutReadiness`** (card; desktop `Width: =360`, `FillPortions: =0`; phone/tablet `Width: =Parent.Width`): `lblReadinessTitle` "Response readiness" (Section); `cmpCloseoutStatusBadge` (instance snippet above); three readiness rows (`cntReadinessRow<X>` Horizontal: `ModernIcon` 20 px + label) — Assignments: icon `=If(CountRows(Filter('FOIA Pilot Assignments', Request.Id = gblSelectedRequest.ID && Active = true && AssignmentStatus.Value <> "Complete")) = 0, "CheckmarkCircle", "Warning")`, colour Success/Warning, text `=CountRows(Filter('FOIA Pilot Assignments', Request.Id = gblSelectedRequest.ID && Active = true && AssignmentStatus.Value <> "Complete")) & " assignment(s) still open"`; Final documents: `=CountRows(Filter('FOIA Pilot Records', Request.Id = gblSelectedRequest.ID && IsFinalResponse = true)) & " final-response record(s)"`; Working due date: `=If(IsBlank(gblSelectedRequest.DueDate), "No working due date", Text(gblSelectedRequest.DueDate, "mmm d, yyyy") & If(gblSelectedRequest.DueDateConfirmed, " · Confirmed", " · Unconfirmed"))`. On tablet (`600–1199`) the three rows sit in one wrapped Horizontal row (bounded two-column feel); on phone stacked.
  2. **`cntCloseoutForm`** (card; `FillPortions: =If(App.Width >= BreakpointDesktop, 1, 0)`, otherwise `Width: =Parent.Width`): `lblCloseoutFormTitle` "Final response details" (Section); wrap row (field width `=If(App.Width < BreakpointPhone, Parent.Width, (Parent.Width - SpaceMd) / 2 - 1)`): `datFinalResponseDate` (`DefaultDate: =gblSelectedRequest.FinalResponseDate`, `Format: =DatePickerFormat.Short`, `IsEditable: =true`), `radCloseoutStatus` `ModernRadio` (`Items: =["Ready", "Delivered", "Closed"]`, `ItemDisplayText: =ThisItem.Value`, `Default: =First(["Ready", "Delivered", "Closed"])`, `Layout: =If(App.Width < BreakpointPhone, OptionLayout.Vertical, OptionLayout.Horizontal)`, `Height: =If(App.Width < BreakpointPhone, 132, InputHeight)`, `Required: =true`, `OnChange: =Set(gblSaveSuccess, false)`, `AccessibleLabel: ="Closeout status"`) — this field block's `Height` is `=If(App.Width < BreakpointPhone, 160, FieldHeight)`; `txtCloseoutNotes` Multiline `Height: =112`, `MaxLength: =2000`, `Required: =true`, `Default: =Coalesce(gblSelectedRequest.CloseoutNotes, "")`, `Placeholder: ="Summarize the final response, delivery decision, or any follow-up needed."`, `ValidationState: =If(IsBlank(Self.Text) && !IsBlank(gblSelectedRequest), ValidationState.Error, ValidationState.None)`; `chkFinalResponseDocument` (`Label: ="Final response document is identified in the records source"`, `Default: =CountRows(Filter('FOIA Pilot Records', Request.Id = gblSelectedRequest.ID && IsFinalResponse = true)) > 0`, `CheckboxSize: =22`, `OnCheck`/`OnUncheck: =Set(gblSaveSuccess, false)`).
     - `cntCloseoutValidation` (Vertical, `Fill: =If(gblSaveSuccess, ColorSuccessBg, ColorCriticalBg)`, border, `Visible` **v1**: `=!IsBlank(gblSelectedRequest) && (gblSaveSuccess || gblLoadError || IsBlank(datFinalResponseDate.SelectedDate) || IsBlank(radCloseoutStatus.Selected) || IsBlank(txtCloseoutNotes.Text) || !chkFinalResponseDocument.Checked || CountRows(Filter('FOIA Pilot Assignments', Request.Id = gblSelectedRequest.ID && Active = true && AssignmentStatus.Value <> "Complete")) > 0)`): `lblCloseoutValidation` (Semibold, colour Success/Critical, `Text` **v1** nested `If` chain: saved → "Closeout saved successfully." / error → "The request could not be saved. Check permissions and try again." / no date → "A final response date is required." / no status → "Choose a closeout status." / no notes → "Add closeout notes before closing." / doc unchecked → "Confirm the final-response document indicator." / else "Complete all active assignments before closing the request."), `lblCloseoutValidationDetail` caption "No deadline is calculated here; the displayed date requires human confirmation."
     - `cntCloseoutActions` (Vertical on phone / Horizontal End otherwise): `btnValidateCloseout` (Secondary, "Validate closeout", `OnSelect` v1: `=If(IsBlank(datFinalResponseDate.SelectedDate) || IsBlank(radCloseoutStatus.Selected) || IsBlank(txtCloseoutNotes.Text) || !chkFinalResponseDocument.Checked || CountRows(Filter('FOIA Pilot Assignments', Request.Id = gblSelectedRequest.ID && Active = true && AssignmentStatus.Value <> "Complete")) > 0, Set(gblSaveSuccess, false), Set(gblSaveSuccess, true))`); **`btnCloseoutRequest`** (`BasePaletteColor: =ColorBrand`, `Icon: ="CheckmarkCircle"`, "Close request", `DisplayMode` v1: `=If(IsBlank(gblSelectedRequest) || IsBlank(datFinalResponseDate.SelectedDate) || IsBlank(radCloseoutStatus.Selected) || IsBlank(txtCloseoutNotes.Text) || !chkFinalResponseDocument.Checked || CountRows(Filter('FOIA Pilot Assignments', Request.Id = gblSelectedRequest.ID && Active = true && AssignmentStatus.Value <> "Complete")) > 0, DisplayMode.Disabled, DisplayMode.Edit)`), `OnSelect` **v1 plus the required error notification**:
```
=IfError(
  Patch(
    'FOIA Pilot Requests',
    gblSelectedRequest,
    {
      FinalResponseDate: datFinalResponseDate.SelectedDate,
      OverallStatus: radCloseoutStatus.Selected,
      CloseoutNotes: txtCloseoutNotes.Text
    }
  );
  Set(gblSaveSuccess, true);
  Refresh('FOIA Pilot Requests');
  Set(gblSelectedRequest, LookUp('FOIA Pilot Requests', ID = gblSelectedRequest.ID));
  Navigate(If(App.Width >= BreakpointDesktop, Home, RequestDetail), ScreenTransition.Cover),
  Set(gblLoadError, true);
  Set(gblSaveSuccess, false);
  Notify("The request could not be closed: " & FirstError.Message, NotificationType.Error)
)
```
- **Navigation:** back → Home/RequestDetail; success → Home (desktop) / RequestDetail (phone/tablet).

## TechnicalGuide Key Conventions
- **Every property value starts with `=`.** Text literals: `Text: ="FOIA requests"`. Booleans: `Visible: =true`.
- **Multi-line formulas use `|-`**, with `=` on the first content line. Any formula containing `{Value: ...}` or `{Id: ...}` record literals **must** be a `|-` block, or — if single-line — the whole value must be YAML-quoted: `Default: '={Value: "Summary"}'`. `ModernTabList.Default` is the one place this bites in this app.
- Plain scalars containing `: ` must be quoted: `Text: ="Status: " & x` is already safe because it starts with `=` followed by a quote, but `HintText: =Label: x` is not.
- **File structure:** screen files start with `Screens:\n  <ScreenName>:\n    Properties: ...\n    Children:` ; `Components.pa.yaml` starts with `ComponentDefinitions:` ; `App.pa.yaml` starts with `App:` (already written — do not re-emit).
- Component instance: `Control: CanvasComponent` + `ComponentName: cmpX` (sibling keys at the same level as `Properties`). Component definition: `DefinitionType: CanvasComponent`, `AccessAppScope: true`, `CustomProperties:` with `PropertyKind: Input|Event`, `DisplayName`, `Description`, `DataType: Text|Boolean|Number` (inputs) or `ReturnType: None` (events), **`Default`** on every property (`=false` for events).
- `GroupContainer` requires `Variant: AutoLayout` and `LayoutDirection`. Children of an AutoLayout container with a fixed `Width`/`Height` **must** set `FillPortions: =0`. Children that should fill set `FillPortions: =1` and `LayoutMinWidth/Height: =0` so they can shrink.
- `Gallery` requires `Variant: Vertical`; its first child is the template root. Row-tap pattern: gallery `OnSelect` holds the action; every text child in the template sets `OnSelect: =Select(Parent)`.
- Enum references: `LayoutDirection.Vertical`, `LayoutAlignItems.Stretch`, `LayoutJustifyContent.SpaceBetween`, `LayoutOverflow.Scroll`, `AlignInContainer.Stretch`, `DropShadow.None`, `ButtonAppearance.Secondary`, `ButtonLayout.IconOnly`, `IconStyle.Filled`, `BadgeIntent.Neutral`, `BadgeShape.Rounded`, `TabListAppearance.Subtle`, `TabSize.Medium`, `TextInputType.Multiline`, `TextInputType.Search`, `TriggerOutput.Delayed`, `DatePickerFormat.Short`, `OptionLayout.Horizontal`, `ValidationState.Error`, `DisplayMode.Disabled`, `FontWeight.Semibold`, `Align.Center`, `ScreenTransition.None|Fade|Cover`, `NotificationType.Error|Success`, `SortOrder.Descending`, `TimeUnit.Days`, `LoadingSpinner.Controls`.
- Option-set / choice lookups: `LookUp(Choices('FOIA Pilot Requests'.OverallStatus), Value = "New")`. Lookup write: `{Id: n, Value: "text"}`. Choice write from a text table: `{Value: "Complete"}`.
- Date text: lower-case format strings, e.g. `Text(d, "mmm d, yyyy")`.
- **Breakpoints inline only:** `App.Width < BreakpointPhone`, `App.Width >= BreakpointPhone && App.Width < BreakpointDesktop`, `App.Width >= BreakpointDesktop`. Three-way: `If(App.Width < BreakpointPhone, a, App.Width < BreakpointDesktop, b, c)`.
- Naming: `scr`-less screen names as given (Home, RequestDetail, …); containers `cnt`, labels `lbl`, buttons `btn`, inputs `txt`, combos `cmb`, date pickers `dat`, checkboxes `chk`, toggles `tgl`, radios `rad`, galleries `gal`, icons `ico`, badges `bdg`, tabs `tab`, component instances `cmp`. **Control names must be unique across the entire app** (sync rule 1) — prefix screen-specific controls (`cntHome…`, `cntDept…`, `cntCloseout…`, `lblPane…`).
- Do **not** call `compile_canvas`; the orchestrator validates.

## Control Definitions
Full `describe_control` output. Property-name audit done: only names listed below exist. Notable corrections vs. v1 habits: `ModernDatePicker.Format` is the enum `DatePickerFormat` (not a text mask); `ModernRadio.Layout` is `OptionLayout`; `ModernTextInput.ValidationState` is the enum `ValidationState`; `ModernBadge.Size` is a Number; `ModernText` has no `Tooltip`; `ModernButton`/`ModernIcon` have no `AutoHeight`.

### GroupContainer
```
# Control GroupContainer
Part of the control family Classic.

Control creation keywords:
Control: GroupContainer
Variant: <variant name> # (required) see below for the list of variants

The `Variant` keyword is required and must be one of the following:
- `AutoLayout`
- `GridLayout`
- `ManualLayout`

Input Properties:
  - BorderColor: Color            Default: RGBA(0, 0, 0, 1)
  - BorderStyle: Enum             Default: BorderStyle.Solid   (BorderStyle: Dashed, Dotted, None, Solid)
  - BorderThickness: Number       Default: 0
  - ContentLanguage: Text         Default: ""
  - DropShadow: Enum              Default: DropShadow.Light    (DropShadow: Bold, ExtraBold, Light, None, Regular, Semibold, Semilight)
  - EnableChildFocus: Boolean     Default: true
  - Fill: Color                   Default: RGBA(0, 0, 0, 0)
  - Height: Number                Default: 200
  - RadiusBottomLeft: Number      Default: 4
  - RadiusBottomRight: Number     Default: 4
  - RadiusTopLeft: Number         Default: 4
  - RadiusTopRight: Number        Default: 4
  - Visible: Boolean              Default: true
  - Width: Number                 Default: 500
  - X: Number                     Default: 0
  - Y: Number                     Default: 0

Additional input properties for variant `AutoLayout`:
  - LayoutAlignItems: Enum        Default: LayoutAlignItems.Start      (LayoutAlignItems: Center, End, Start, Stretch)
  - LayoutDirection: Enum         Default: LayoutDirection.Horizontal  Required: true  (LayoutDirection: Horizontal, Vertical)
  - LayoutGap: Number             Default: 0
  - LayoutJustifyContent: Enum    Default: LayoutJustifyContent.Start  (LayoutJustifyContent: Center, End, SpaceBetween, Start)
  - LayoutOverflowX: Enum         Default: LayoutOverflow.Hide         (LayoutOverflow: Hide, Scroll)
  - LayoutOverflowY: Enum         Default: LayoutOverflow.Hide         (LayoutOverflow: Hide, Scroll)
  - LayoutWrap: Boolean           Default: false
  - PaddingBottom: Number         Default: 0
  - PaddingLeft: Number           Default: 0
  - PaddingRight: Number          Default: 0
  - PaddingTop: Number            Default: 0

Additional input properties for variant `GridLayout`:
  - ChildTabPriority: Boolean (true), LayoutGap: Number (8), LayoutGridColumnMinWidth: Number (0), LayoutGridColumns: Number (4),
    LayoutGridRowMinHeight: Number (0), LayoutGridRows: Number (2), LayoutOverflowX/Y: Enum LayoutOverflow (Hide), PaddingBottom/Left/Right/Top: Number (8)

Additional input properties for variant `ManualLayout`:
  - ChildTabPriority: Boolean (true), PaddingBottom/Left/Right/Top: Number (0)

Additional input properties if a child of a Vertical or Horizontal GroupContainer:
  - AlignInContainer: Enum        Default: AlignInContainer.Stretch    (AlignInContainer: Center, End, SetByContainer, Start, Stretch)
  - FillPortions: Number          Default: 1
  - LayoutMaxHeight: Number       Default: 0
  - LayoutMaxWidth: Number        Default: 0
  - LayoutMinHeight: Number       Default: 100
  - LayoutMinWidth: Number        Default: 250

Additional input properties if a child of a Grid GroupContainer:
  - LayoutGridColumnEnd, LayoutGridColumnStart, LayoutGridRowEnd, LayoutGridRowStart: Number

Output Properties:
  BorderColor, BorderStyle, BorderThickness, ChildTabPriority, ContentLanguage, DropShadow, EnableChildFocus, Fill, Height,
  LayoutGridColumnMinWidth, LayoutGridColumns, LayoutGridRowMinHeight, LayoutGridRows, PaddingBottom, PaddingLeft, PaddingRight,
  PaddingTop, RadiusBottomLeft, RadiusBottomRight, RadiusTopLeft, RadiusTopRight, Visible, Width, X, Y
```
Note: `GroupContainer` has **no `OnSelect`** and **no `AccessibleLabel`**. Default `LayoutMinHeight` 100 / `LayoutMinWidth` 250 are large — always set them explicitly (usually `=0`).

### ModernTabList
```
# Control ModernTabList
Part of the control family React.

Control creation keywords:
Control: ModernTabList

Input Properties:
  - AccessibleLabel: Text         Default: ""
  - Align: Enum                   Default: Align.Left                  (Align: Center, Justify, Left, Right)
  - Alignment: Enum               Default: LayoutDirection.Horizontal  (LayoutDirection: Horizontal, Vertical)
  - Appearance: Enum              Default: TabListAppearance.Transparent (TabListAppearance: FilledCircular, Subtle, SubtleCircular, Transparent)
  - BasePaletteColor: Color
  - Color: Color
  - ContentLanguage: Text         Default: ""
  - Default: Record
  - DisplayMode: Enum             Default: DisplayMode.Edit            (DisplayMode: Disabled, Edit, View)
  - Font: Enum                    Default: ""                          (Font: Arial, Courier New, Dancing Script, Georgia, Great Vibes, Lato, Lato Black, Lato Hairline, Lato Light, Open Sans, Open Sans Condensed, Patrick Hand, Segoe UI, Verdana)
  - FontWeight: Enum                                                   (FontWeight: Bold, Lighter, Normal, Semibold)
  - Height: Number                Default: 60
  - Italic: Boolean               Default: false
  - ItemDisplayText: Text         Default: ThisItem.Value
  - Items: Table                  Default: Table({Value: "Item 1"}, {Value: "Item 2"}, {Value: "Item 3"})
  - OnChange: Boolean             Default: false
  - OnSelect: Boolean             Default: false
  - PaddingBottom: Number
  - PaddingLeft: Number
  - PaddingRight: Number
  - PaddingTop: Number
  - Size: Number                  Default: 14
  - Strikethrough: Boolean        Default: false
  - TabSize: Enum                 Default: TabSize.Large               (TabSize: Large, Medium, Small)
  - Underline: Boolean            Default: false
  - Visible: Boolean              Default: true
  - Width: Number                 Default: 300
  - X: Number                     Default: 0
  - Y: Number                     Default: 0

Additional input properties if a child of a Vertical or Horizontal GroupContainer:
  - AlignInContainer: Enum        Default: AlignInContainer.SetByContainer (Center, End, SetByContainer, Start, Stretch)
  - FillPortions: Number          Default: 0
  - LayoutMaxHeight: Number       Default: 0
  - LayoutMaxWidth: Number        Default: 0
  - LayoutMinHeight: Number       Default: 60
  - LayoutMinWidth: Number        Default: 300

Additional input properties if a child of a Grid GroupContainer:
  - LayoutGridColumnEnd, LayoutGridColumnStart, LayoutGridRowEnd, LayoutGridRowStart: Number

Output Properties:
  AccessibleLabel, Align, Alignment, Appearance, BasePaletteColor, Color, ContentLanguage, DisplayMode, Font, FontWeight, Height, Italic,
  PaddingBottom, PaddingLeft, PaddingRight, PaddingTop, Selected: Record, Size, Strikethrough, TabSize, Underline, Visible, Width, X, Y
```

### ModernText
```
# Control ModernText
Part of the control family React.

Control creation keywords:
Control: ModernText

Input Properties:
  - AccessibleLabel: Text         Default: ""
  - Align: Enum                   Default: Align.Left                  (Align: Center, Justify, Left, Right)
  - AutoHeight: Boolean           Default: false
  - BorderColor: Color
  - BorderStyle: Enum             Default: ""                          (BorderStyle: Dashed, Dotted, None, Solid)
  - BorderThickness: Number
  - Color: Color
  - ContentLanguage: Text         Default: ""
  - DisplayMode: Enum             Default: DisplayMode.Edit            (DisplayMode: Disabled, Edit, View)
  - Fill: Color
  - Font: Enum                    Default: ""                          (Font: Arial, Courier New, Dancing Script, Georgia, Great Vibes, Lato, Lato Black, Lato Hairline, Lato Light, Open Sans, Open Sans Condensed, Patrick Hand, Segoe UI, Verdana)
  - FontWeight: Enum              Default: FontWeight.Normal           (FontWeight: Bold, Lighter, Normal, Semibold)
  - Height: Number                Default: 32
  - Italic: Boolean               Default: false
  - OnSelect: Boolean             Default: false
  - PaddingBottom: Number         Default: 5
  - PaddingLeft: Number           Default: 5
  - PaddingRight: Number          Default: 5
  - PaddingTop: Number            Default: 5
  - RadiusBottomLeft: Number
  - RadiusBottomRight: Number
  - RadiusTopLeft: Number
  - RadiusTopRight: Number
  - Size: Number                  Default: 15
  - Strikethrough: Boolean        Default: false
  - Text: Text                    Default: "Text"
  - Underline: Boolean            Default: false
  - VerticalAlign: Enum           Default: VerticalAlign.Middle        (VerticalAlign: Bottom, Middle, Top)
  - Visible: Boolean              Default: true
  - Width: Number                 Default: 150
  - Wrap: Boolean                 Default: true
  - X: Number                     Default: 0
  - Y: Number                     Default: 0

Additional input properties if a child of a Vertical or Horizontal GroupContainer:
  - AlignInContainer: Enum        Default: AlignInContainer.SetByContainer (Center, End, SetByContainer, Start, Stretch)
  - FillPortions: Number          Default: 0
  - LayoutMaxHeight: Number       Default: 0
  - LayoutMaxWidth: Number        Default: 0
  - LayoutMinHeight: Number       Default: 32
  - LayoutMinWidth: Number        Default: 150

Additional input properties if a child of a Grid GroupContainer:
  - LayoutGridColumnEnd, LayoutGridColumnStart, LayoutGridRowEnd, LayoutGridRowStart: Number

Output Properties:
  AccessibleLabel, Align, AutoHeight, BorderColor, BorderStyle, BorderThickness, Color, ContentLanguage, DisplayMode, Fill, Font, FontWeight,
  Height, Italic, PaddingBottom, PaddingLeft, PaddingRight, PaddingTop, RadiusBottomLeft, RadiusBottomRight, RadiusTopLeft, RadiusTopRight,
  Size, Strikethrough, Text, Underline, VerticalAlign, Visible, Width, Wrap, X, Y
```

### ModernButton
```
# Control ModernButton
Part of the control family React.

Control creation keywords:
Control: ModernButton

Input Properties:
  - AccessibleLabel: Text         Default: ""
  - Align: Enum                                                        (Align: Center, Justify, Left, Right)
  - Appearance: Enum              Default: ButtonAppearance.Primary    (ButtonAppearance: Outline, Primary, Secondary, Subtle, Transparent)
  - BasePaletteColor: Color
  - BorderColor: Color
  - BorderStyle: Enum             Default: ""                          (BorderStyle: Dashed, Dotted, None, Solid)
  - BorderThickness: Number
  - Color: Color
  - ContentLanguage: Text         Default: ""
  - DisplayMode: Enum             Default: DisplayMode.Edit            (DisplayMode: Disabled, Edit, View)
  - Font: Enum                    Default: ""                          (Font: Arial, Courier New, Dancing Script, Georgia, Great Vibes, Lato, Lato Black, Lato Hairline, Lato Light, Open Sans, Open Sans Condensed, Patrick Hand, Segoe UI, Verdana)
  - FontWeight: Enum                                                   (FontWeight: Bold, Lighter, Normal, Semibold)
  - Height: Number                Default: 32
  - Icon: Text                    Default: ""
  - IconRotation: Number          Default: 0
  - IconStyle: Enum               Default: IconStyle.Outline           (IconStyle: Filled, Outline)
  - Italic: Boolean               Default: false
  - Layout: Enum                  Default: ButtonLayout.IconBefore     (ButtonLayout: IconAfter, IconBefore, IconOnly, TextOnly)
  - OnSelect: Boolean             Default: false
  - PaddingBottom: Number
  - PaddingLeft: Number
  - PaddingRight: Number
  - PaddingTop: Number
  - RadiusBottomLeft: Number
  - RadiusBottomRight: Number
  - RadiusTopLeft: Number
  - RadiusTopRight: Number
  - Size: Number                  Default: 0
  - Strikethrough: Boolean        Default: false
  - Text: Text                    Default: "Button"
  - Tooltip: Text                 Default: ""
  - Underline: Boolean            Default: false
  - VerticalAlign: Enum                                                (VerticalAlign: Bottom, Middle, Top)
  - Visible: Boolean              Default: true
  - Width: Number                 Default: 96
  - X: Number                     Default: 0
  - Y: Number                     Default: 0

Additional input properties if a child of a Vertical or Horizontal GroupContainer:
  - AlignInContainer: Enum        Default: AlignInContainer.SetByContainer (Center, End, SetByContainer, Start, Stretch)
  - FillPortions: Number          Default: 0
  - LayoutMaxHeight: Number       Default: 0
  - LayoutMaxWidth: Number        Default: 0
  - LayoutMinHeight: Number       Default: 32
  - LayoutMinWidth: Number        Default: 96

Additional input properties if a child of a Grid GroupContainer:
  - LayoutGridColumnEnd, LayoutGridColumnStart, LayoutGridRowEnd, LayoutGridRowStart: Number

Output Properties:
  AccessibleLabel, Align, BasePaletteColor, BorderColor, BorderStyle, BorderThickness, Color, ContentLanguage, DisplayMode, Font, FontWeight,
  Height, Italic, PaddingBottom, PaddingLeft, PaddingRight, PaddingTop, RadiusBottomLeft, RadiusBottomRight, RadiusTopLeft, RadiusTopRight,
  Size, Strikethrough, Text, Tooltip, Underline, VerticalAlign, Visible, Width, X, Y
```

### ModernIcon
```
# Control ModernIcon
Part of the control family React.

Control creation keywords:
Control: ModernIcon

Input Properties:
  - AccessibleLabel: Text         Default: ""
  - BasePaletteColor: Color
  - BorderColor: Color
  - BorderStyle: Enum             Default: ""                          (BorderStyle: Dashed, Dotted, None, Solid)
  - BorderThickness: Number
  - ContentLanguage: Text         Default: ""
  - DisplayMode: Enum             Default: DisplayMode.Edit            (DisplayMode: Disabled, Edit, View)
  - Fill: Color
  - Height: Number                Default: 32
  - Icon: Text                    Default: "Add"
  - IconColor: Color
  - IconStyle: Enum               Default: IconStyle.Outline           (IconStyle: Filled, Outline)
  - OnSelect: Boolean             Default: false
  - PaddingBottom: Number         Default: 0
  - PaddingLeft: Number           Default: 0
  - PaddingRight: Number          Default: 0
  - PaddingTop: Number            Default: 0
  - RadiusBottomLeft: Number
  - RadiusBottomRight: Number
  - RadiusTopLeft: Number
  - RadiusTopRight: Number
  - Rotation: Number              Default: 0
  - Tooltip: Text                 Default: ""
  - Visible: Boolean              Default: true
  - Width: Number                 Default: 32
  - X: Number                     Default: 0
  - Y: Number                     Default: 0

Additional input properties if a child of a Vertical or Horizontal GroupContainer:
  - AlignInContainer: Enum        Default: AlignInContainer.SetByContainer (Center, End, SetByContainer, Start, Stretch)
  - FillPortions: Number          Default: 0
  - LayoutMaxHeight: Number       Default: 0
  - LayoutMaxWidth: Number        Default: 0
  - LayoutMinHeight: Number       Default: 32
  - LayoutMinWidth: Number        Default: 32

Additional input properties if a child of a Grid GroupContainer:
  - LayoutGridColumnEnd, LayoutGridColumnStart, LayoutGridRowEnd, LayoutGridRowStart: Number

Output Properties:
  AccessibleLabel, BasePaletteColor, BorderColor, BorderStyle, BorderThickness, ContentLanguage, DisplayMode, Fill, Height, PaddingBottom,
  PaddingLeft, PaddingRight, PaddingTop, RadiusBottomLeft, RadiusBottomRight, RadiusTopLeft, RadiusTopRight, Tooltip, Visible, Width, X, Y
```

### ModernBadge
```
# Control ModernBadge
Part of the control family React.

Control creation keywords:
Control: ModernBadge

Input Properties:
  - AccessibleLabel: Text         Default: ""
  - Align: Enum                   Default: Align.Center                (Align: Center, Justify, Left, Right)
  - Appearance: Enum              Default: BadgeAppearance.Tint        (BadgeAppearance: Filled, Ghost, Outline, Tint)
  - BasePaletteColor: Color
  - BorderColor: Color
  - BorderStyle: Enum             Default: ""                          (BorderStyle: Dashed, Dotted, None, Solid)
  - BorderThickness: Number
  - Color: Color
  - Content: Text                 Default: "AB"
  - ContentLanguage: Text         Default: ""
  - DisplayMode: Enum             Default: DisplayMode.Edit            (DisplayMode: Disabled, Edit, View)
  - Fill: Color
  - Font: Enum                    Default: ""                          (Font: Arial, Courier New, Dancing Script, Georgia, Great Vibes, Lato, Lato Black, Lato Hairline, Lato Light, Open Sans, Open Sans Condensed, Patrick Hand, Segoe UI, Verdana)
  - FontWeight: Enum                                                   (FontWeight: Bold, Lighter, Normal, Semibold)
  - Height: Number                Default: 32
  - Icon: Text                    Default: ""
  - IconPosition: Enum            Default: BadgeIconPosition.Before    (BadgeIconPosition: After, Before)
  - Intent: Enum                  Default: BadgeIntent.Positive        (BadgeIntent: Attention, Caution, Critical, Highlight, Informative, Neutral, Positive, Urgent)
  - Italic: Boolean               Default: false
  - OnSelect: Boolean             Default: false
  - PaddingBottom: Number
  - PaddingLeft: Number
  - PaddingRight: Number
  - PaddingTop: Number
  - RadiusBottomLeft: Number
  - RadiusBottomRight: Number
  - RadiusTopLeft: Number
  - RadiusTopRight: Number
  - Shape: Enum                   Default: BadgeShape.Circular         (BadgeShape: Circular, Rounded, Square)
  - Size: Number                  Default: 0
  - Strikethrough: Boolean        Default: false
  - Tooltip: Text                 Default: ""
  - Underline: Boolean            Default: false
  - VerticalAlign: Enum           Default: VerticalAlign.Middle        (VerticalAlign: Bottom, Middle, Top)
  - Visible: Boolean              Default: true
  - Width: Number                 Default: 64
  - X: Number                     Default: 0
  - Y: Number                     Default: 0

Additional input properties if a child of a Vertical or Horizontal GroupContainer:
  - AlignInContainer: Enum        Default: AlignInContainer.SetByContainer (Center, End, SetByContainer, Start, Stretch)
  - FillPortions: Number          Default: 0
  - LayoutMaxHeight: Number       Default: 0
  - LayoutMaxWidth: Number        Default: 0
  - LayoutMinHeight: Number       Default: 32
  - LayoutMinWidth: Number        Default: 64

Additional input properties if a child of a Grid GroupContainer:
  - LayoutGridColumnEnd, LayoutGridColumnStart, LayoutGridRowEnd, LayoutGridRowStart: Number

Output Properties (note: Content is NOT an output):
  AccessibleLabel, Align, BasePaletteColor, BorderColor, BorderStyle, BorderThickness, Color, ContentLanguage, DisplayMode, Fill, Font,
  FontWeight, Height, Italic, PaddingBottom, PaddingLeft, PaddingRight, PaddingTop, RadiusBottomLeft, RadiusBottomRight, RadiusTopLeft,
  RadiusTopRight, Size, Strikethrough, Tooltip, Underline, VerticalAlign, Visible, Width, X, Y
```

### Gallery
```
# Control Gallery
Part of the control family Classic.

Control creation keywords:
Control: Gallery
Variant: <variant name> # (required): Horizontal | VariableHeight | Vertical

Input Properties (all variants):
  - BorderStyle: Enum             Default: BorderStyle.Solid           (BorderStyle: Dashed, Dotted, None, Solid)
  - ContentLanguage: Text         Default: ""
  - Default: Record
  - DisplayMode: Enum             Default: DisplayMode.Edit            (DisplayMode: Disabled, Edit, View)
  - Fill: Color                   Default: RGBA(0, 0, 0, 0)
  - FocusedBorderColor: Color     Default: Self.BorderColor
  - FocusedBorderThickness: Number Default: 4
  - LoadingSpinnerColor: Color    Default: Self.BorderColor
  - NavigationStep: Number        Default: 1
  - Selectable: Boolean           Default: true
  - ShowNavigation: Boolean       Default: false
  - TabIndex: Number              Default: -1
  - Transition: Enum              Default: Transition.None             (Transition: None, Pop, Push)
  - Visible: Boolean              Default: true

Additional input properties for variant `Vertical` (used in this app):
  - AccessibleLabel: Text         Default: ""
  - BorderColor: Color            Default: App.Theme.Colors.Darker40
  - BorderThickness: Number       Default: 0
  - DelayItemLoading: Boolean     Default: true
  - Height: Number                Default: 575
  - Items: Table                  Default: CustomGallerySample
  - LoadingSpinner: Enum          Default: LoadingSpinner.Data         (LoadingSpinner: Controls, Data, None)
  - ShowScrollbar: Boolean        Default: true
  - TemplatePadding: Number       Default: 5
  - TemplateSize: Number          Default: If(Self.Layout = Layout.Horizontal, Min(280, Self.Width - 60), Min(280, Self.Height - 60))
  - Width: Number                 Default: 640
  - WrapCount: Number             Default: 1
  - X: Number                     Default: 0
  - Y: Number                     Default: 0
  (`Horizontal` has the same set; `VariableHeight` replaces WrapCount with MaxTemplateSize: Number Default 5000 and TemplateSize Default 280)

Additional input properties if a child of a Vertical or Horizontal GroupContainer:
  - AlignInContainer: Enum        Default: AlignInContainer.Stretch    (Center, End, SetByContainer, Start, Stretch)
  - FillPortions: Number          Default: 1
  - LayoutMaxHeight: Number       Default: 0
  - LayoutMaxWidth: Number        Default: 0
  - LayoutMinHeight: Number       Default: 287
  - LayoutMinWidth: Number        Default: 320

Additional input properties if a child of a Grid GroupContainer:
  - LayoutGridColumnEnd, LayoutGridColumnStart, LayoutGridRowEnd, LayoutGridRowStart: Number

Output Properties:
  AccessibleLabel, AllItems: Table, AllItemsCount: Number, BorderColor, BorderStyle, BorderThickness, ContentLanguage, DisplayMode, Fill,
  FocusedBorderColor, FocusedBorderThickness, Height, Selected: Record, TabIndex, TemplateHeight: Number, TemplatePadding,
  TemplateWidth: Number, Valid, Visible, VisibleIndex, Width, X, Y
```
Note: `OnSelect` is accepted on Gallery (v1 compiled with it) even though the describe output lists it under neither heading; inside the template use `Parent.TemplateHeight` / `Parent.TemplateWidth`. Default `LayoutMinHeight` 287 — set `=0`.

### ModernTextInput
```
# Control ModernTextInput
Part of the control family React.

Control creation keywords:
Control: ModernTextInput

Input Properties:
  - AccessibleLabel: Text         Default: ""
  - Align: Enum                   Default: Align.Left                  (Align: Center, Justify, Left, Right)
  - Appearance: Enum              Default: Appearance.FilledDarker     (Appearance: FilledDarker, FilledLighter, Outline)
  - BasePaletteColor: Color
  - BorderColor: Color
  - BorderStyle: Enum             Default: ""                          (BorderStyle: Dashed, Dotted, None, Solid)
  - BorderThickness: Number
  - Color: Color
  - ContentLanguage: Text         Default: ""
  - Default: Text                 Default: ""
  - DisplayMode: Enum             Default: DisplayMode.Edit            (DisplayMode: Disabled, Edit, View)
  - Fill: Color
  - Font: Enum                    Default: ""                          (Font: Arial, Courier New, Dancing Script, Georgia, Great Vibes, Lato, Lato Black, Lato Hairline, Lato Light, Open Sans, Open Sans Condensed, Patrick Hand, Segoe UI, Verdana)
  - FontWeight: Enum              Default: FontWeight.Normal           (FontWeight: Bold, Lighter, Normal, Semibold)
  - Height: Number                Default: 32
  - Italic: Boolean               Default: false
  - MaxLength: Number
  - OnChange: Boolean             Default: false
  - PaddingBottom: Number
  - PaddingLeft: Number
  - PaddingRight: Number
  - PaddingTop: Number
  - Placeholder: Text             Default: "Enter text"
  - RadiusBottomLeft: Number
  - RadiusBottomRight: Number
  - RadiusTopLeft: Number
  - RadiusTopRight: Number
  - Required: Boolean             Default: false
  - Size: Number                  Default: 14
  - Strikethrough: Boolean        Default: false
  - TriggerOutput: Enum           Default: TriggerOutput.Keypress      (TriggerOutput: Delayed, FocusOut, Keypress)
  - Type: Enum                    Default: TextInputType.SingleLine    (TextInputType: Multiline, Password, Search, SingleLine)
  - Underline: Boolean            Default: false
  - ValidationState: Enum         Default: ValidationState.None        (ValidationState: Error, None)
  - Visible: Boolean              Default: true
  - Width: Number                 Default: 320
  - X: Number                     Default: 0
  - Y: Number                     Default: 0

Additional input properties if a child of a Vertical or Horizontal GroupContainer:
  - AlignInContainer: Enum        Default: AlignInContainer.SetByContainer (Center, End, SetByContainer, Start, Stretch)
  - FillPortions: Number          Default: 0
  - LayoutMaxHeight: Number       Default: 0
  - LayoutMaxWidth: Number        Default: 0
  - LayoutMinHeight: Number       Default: 32
  - LayoutMinWidth: Number        Default: 320

Additional input properties if a child of a Grid GroupContainer:
  - LayoutGridColumnEnd, LayoutGridColumnStart, LayoutGridRowEnd, LayoutGridRowStart: Number

Output Properties:
  AccessibleLabel, Align, Appearance, BasePaletteColor, BorderColor, BorderStyle, BorderThickness, Color, ContentLanguage, DisplayMode, Fill,
  Font, FontWeight, Height, Italic, MaxLength, PaddingBottom, PaddingLeft, PaddingRight, PaddingTop, Placeholder, RadiusBottomLeft,
  RadiusBottomRight, RadiusTopLeft, RadiusTopRight, Required, Size, Strikethrough, Text: Text, TriggerOutput, Type, Underline,
  ValidationState, Visible, Width, X, Y
```

### ModernCombobox
```
# Control ModernCombobox
Part of the control family React.

Control creation keywords:
Control: ModernCombobox

Input Properties:
  - AccessibleLabel: Text         Default: ""
  - AllowExternalSelectedItems: Boolean Default: true
  - Appearance: Enum              Default: Appearance.FilledDarker     (Appearance: FilledDarker, FilledLighter, Outline)
  - BasePaletteColor: Color
  - BorderColor: Color
  - BorderStyle: Enum             Default: ""                          (BorderStyle: Dashed, Dotted, None, Solid)
  - BorderThickness: Number
  - Color: Color
  - ContentLanguage: Text         Default: ""
  - DefaultSelectedItems: Table
  - DelayOutput: Boolean          Default: false
  - DisplayMode: Enum             Default: DisplayMode.Edit            (DisplayMode: Disabled, Edit, View)
  - Fill: Color
  - Font: Enum                    Default: ""                          (Font: Arial, Courier New, Dancing Script, Georgia, Great Vibes, Lato, Lato Black, Lato Hairline, Lato Light, Open Sans, Open Sans Condensed, Patrick Hand, Segoe UI, Verdana)
  - FontWeight: Enum              Default: FontWeight.Normal           (FontWeight: Bold, Lighter, Normal, Semibold)
  - Height: Number                Default: 32
  - InputTextPlaceholder: Text    Default: "Find items"
  - IsSearchable: Boolean         Default: true
  - Italic: Boolean               Default: false
  - ItemDisplayText: Text         Default: ThisItem.Value1
  - Items: Table                  Default: ComboBoxSample
  - MultiValueDelimiter: Text     Default: ", "
  - OnChange: Boolean             Default: false
  - PaddingBottom: Number
  - PaddingLeft: Number
  - PaddingRight: Number
  - PaddingTop: Number
  - RadiusBottomLeft: Number
  - RadiusBottomRight: Number
  - RadiusTopLeft: Number
  - RadiusTopRight: Number
  - Required: Boolean             Default: false
  - SelectMultiple: Boolean       Default: true
  - Size: Number                  Default: 14
  - Strikethrough: Boolean        Default: false
  - Underline: Boolean            Default: false
  - ValidationState: Enum         Default: ValidationState.None        (ValidationState: Error, None)
  - Visible: Boolean              Default: true
  - Width: Number                 Default: 320
  - X: Number                     Default: 0
  - Y: Number                     Default: 0

Additional input properties if a child of a Vertical or Horizontal GroupContainer:
  - AlignInContainer: Enum        Default: AlignInContainer.SetByContainer (Center, End, SetByContainer, Start, Stretch)
  - FillPortions: Number          Default: 0
  - LayoutMaxHeight: Number       Default: 0
  - LayoutMaxWidth: Number        Default: 0
  - LayoutMinHeight: Number       Default: 32
  - LayoutMinWidth: Number        Default: 320

Additional input properties if a child of a Grid GroupContainer:
  - LayoutGridColumnEnd, LayoutGridColumnStart, LayoutGridRowEnd, LayoutGridRowStart: Number

Output Properties:
  AccessibleLabel, Appearance, BasePaletteColor, BorderColor, BorderStyle, BorderThickness, Color, ContentLanguage, DisplayMode, Fill, Font,
  FontWeight, Height, InputTextPlaceholder, Italic, MultiValueDelimiter, PaddingBottom, PaddingLeft, PaddingRight, PaddingTop,
  RadiusBottomLeft, RadiusBottomRight, RadiusTopLeft, RadiusTopRight, SearchText: Text, Selected: Record, SelectedItems: Table, Size,
  Strikethrough, Underline, ValidationState, Visible, Width, X, Y
```

### ModernDatePicker
```
# Control ModernDatePicker
Part of the control family React.

Control creation keywords:
Control: ModernDatePicker

Input Properties:
  - AccessibleLabel: Text         Default: ""
  - Appearance: Enum              Default: Appearance.FilledDarker     (Appearance: FilledDarker, FilledLighter, Outline)
  - BasePaletteColor: Color
  - BorderColor: Color
  - BorderStyle: Enum                                                  (BorderStyle: Dashed, Dotted, None, Solid)
  - BorderThickness: Number
  - Color: Color
  - ContentLanguage: Text         Default: ""
  - DateTimeZone: Enum            Default: DateTimeZone.Local          (DateTimeZone: Local, UTC)
  - DefaultDate: Date
  - DisplayMode: Enum             Default: DisplayMode.Edit            (DisplayMode: Disabled, Edit, View)
  - EndDate: Date                 Default: Date(Year(Today())+100, 12, 31)
  - Fill: Color
  - Font: Enum                                                         (Font: Arial, Courier New, Dancing Script, Georgia, Great Vibes, Lato, Lato Black, Lato Hairline, Lato Light, Open Sans, Open Sans Condensed, Patrick Hand, Segoe UI, Verdana)
  - FontWeight: Enum                                                   (FontWeight: Bold, Lighter, Normal, Semibold)
  - Format: Enum                  Default: DatePickerFormat.LongAbbreviated (DatePickerFormat: LongAbbreviated, Short, YearMonth)
  - Height: Number                Default: 32
  - IsEditable: Boolean           Default: false
  - Italic: Boolean               Default: false
  - OnChange: Boolean             Default: false
  - PaddingBottom: Number
  - PaddingLeft: Number
  - PaddingRight: Number
  - PaddingTop: Number
  - Placeholder: Text             Default: "Select a date"
  - RadiusBottomLeft: Number
  - RadiusBottomRight: Number
  - RadiusTopLeft: Number
  - RadiusTopRight: Number
  - Size: Number                  Default: 14
  - StartDate: Date               Default: Date(1900, 1, 1)
  - StartOfWeek: Enum             Default: StartOfWeek.Sunday          (StartOfWeek: Friday, Monday, MondayZero, Saturday, Sunday, Thursday, Tuesday, Wednesday)
  - Strikethrough: Boolean        Default: false
  - Underline: Boolean            Default: false
  - ValidationState: Enum         Default: ValidationState.None        (ValidationState: Error, None)
  - Visible: Boolean              Default: true
  - Width: Number                 Default: 320
  - X: Number                     Default: 0
  - Y: Number                     Default: 0

Additional input properties if a child of a Vertical or Horizontal GroupContainer:
  - AlignInContainer: Enum        Default: AlignInContainer.SetByContainer (Center, End, SetByContainer, Start, Stretch)
  - FillPortions: Number          Default: 0
  - LayoutMaxHeight: Number       Default: 0
  - LayoutMaxWidth: Number        Default: 0
  - LayoutMinHeight: Number       Default: 32
  - LayoutMinWidth: Number        Default: 320

Additional input properties if a child of a Grid GroupContainer:
  - LayoutGridColumnEnd, LayoutGridColumnStart, LayoutGridRowEnd, LayoutGridRowStart: Number

Output Properties:
  AccessibleLabel, Appearance, BasePaletteColor, BorderColor, BorderStyle, BorderThickness, Color, ContentLanguage, DisplayMode, Fill, Font,
  FontWeight, Height, Italic, PaddingBottom, PaddingLeft, PaddingRight, PaddingTop, Placeholder, RadiusBottomLeft, RadiusBottomRight,
  RadiusTopLeft, RadiusTopRight, SelectedDate: Date, Size, Strikethrough, Underline, ValidationState, Visible, Width, X, Y
```

### ModernDropdown
```
# Control ModernDropdown
Part of the control family React.

Control creation keywords:
Control: ModernDropdown

Input Properties:
  - AccessibleLabel: Text         Default: ""
  - Appearance: Enum              Default: Appearance.FilledDarker     (Appearance: FilledDarker, FilledLighter, Outline)
  - BasePaletteColor: Color
  - BorderColor: Color
  - BorderStyle: Enum             Default: ""                          (BorderStyle: Dashed, Dotted, None, Solid)
  - BorderThickness: Number
  - Color: Color
  - ContentLanguage: Text         Default: ""
  - Default: Record
  - DisplayMode: Enum             Default: DisplayMode.Edit            (DisplayMode: Disabled, Edit, View)
  - Fill: Color
  - Font: Enum                    Default: ""                          (Font: Arial, Courier New, Dancing Script, Georgia, Great Vibes, Lato, Lato Black, Lato Hairline, Lato Light, Open Sans, Open Sans Condensed, Patrick Hand, Segoe UI, Verdana)
  - FontWeight: Enum              Default: FontWeight.Normal           (FontWeight: Bold, Lighter, Normal, Semibold)
  - Height: Number                Default: 32
  - Italic: Boolean               Default: false
  - ItemDisplayText: Text         Default: ThisItem.Value1
  - Items: Table                  Default: ComboBoxSample
  - OnChange: Boolean             Default: false
  - PaddingBottom: Number
  - PaddingLeft: Number
  - PaddingRight: Number
  - PaddingTop: Number
  - RadiusBottomLeft: Number
  - RadiusBottomRight: Number
  - RadiusTopLeft: Number
  - RadiusTopRight: Number
  - Required: Boolean             Default: false
  - Size: Number                  Default: 14
  - Strikethrough: Boolean        Default: false
  - Underline: Boolean            Default: false
  - ValidationState: Enum         Default: ValidationState.None        (ValidationState: Error, None)
  - Visible: Boolean              Default: true
  - Width: Number                 Default: 320
  - X: Number                     Default: 0
  - Y: Number                     Default: 0

Additional input properties if a child of a Vertical or Horizontal GroupContainer:
  - AlignInContainer: Enum        Default: AlignInContainer.SetByContainer (Center, End, SetByContainer, Start, Stretch)
  - FillPortions: Number          Default: 0
  - LayoutMaxHeight: Number       Default: 0
  - LayoutMaxWidth: Number        Default: 0
  - LayoutMinHeight: Number       Default: 32
  - LayoutMinWidth: Number        Default: 320

Additional input properties if a child of a Grid GroupContainer:
  - LayoutGridColumnEnd, LayoutGridColumnStart, LayoutGridRowEnd, LayoutGridRowStart: Number

Output Properties:
  AccessibleLabel, Appearance, BasePaletteColor, BorderColor, BorderStyle, BorderThickness, Color, ContentLanguage, DisplayMode, Fill, Font,
  FontWeight, Height, Italic, PaddingBottom, PaddingLeft, PaddingRight, PaddingTop, RadiusBottomLeft, RadiusBottomRight, RadiusTopLeft,
  RadiusTopRight, Selected: Record, Size, Strikethrough, Underline, ValidationState, Visible, Width, X, Y
```

### ModernCheckbox
```
# Control ModernCheckbox
Part of the control family React.

Control creation keywords:
Control: ModernCheckbox

Input Properties:
  - AccessibleLabel: Text         Default: ""
  - BasePaletteColor: Color
  - CheckboxSize: Number          Default: 16
  - Color: Color
  - ContentLanguage: Text         Default: ""
  - Default: Boolean              Default: false
  - DisplayMode: Enum             Default: DisplayMode.Edit            (DisplayMode: Disabled, Edit, View)
  - Font: Enum                    Default: ""                          (Font: Arial, Courier New, Dancing Script, Georgia, Great Vibes, Lato, Lato Black, Lato Hairline, Lato Light, Open Sans, Open Sans Condensed, Patrick Hand, Segoe UI, Verdana)
  - FontWeight: Enum                                                   (FontWeight: Bold, Lighter, Normal, Semibold)
  - Height: Number                Default: 32
  - Italic: Boolean               Default: false
  - Label: Text                   Default: "Checkbox"
  - OnCheck: Boolean              Default: false
  - OnUncheck: Boolean            Default: false
  - Size: Number                  Default: 0
  - Strikethrough: Boolean        Default: false
  - Tooltip: Text                 Default: ""
  - Underline: Boolean            Default: false
  - Visible: Boolean              Default: true
  - Width: Number                 Default: 160
  - X: Number                     Default: 0
  - Y: Number                     Default: 0

Additional input properties if a child of a Vertical or Horizontal GroupContainer:
  - AlignInContainer: Enum        Default: AlignInContainer.SetByContainer (Center, End, SetByContainer, Start, Stretch)
  - FillPortions: Number          Default: 0
  - LayoutMaxHeight: Number       Default: 0
  - LayoutMaxWidth: Number        Default: 0
  - LayoutMinHeight: Number       Default: 32
  - LayoutMinWidth: Number        Default: 160

Additional input properties if a child of a Grid GroupContainer:
  - LayoutGridColumnEnd, LayoutGridColumnStart, LayoutGridRowEnd, LayoutGridRowStart: Number

Output Properties:
  AccessibleLabel, BasePaletteColor, CheckboxSize, Checked: Boolean, Color, ContentLanguage, DisplayMode, Font, FontWeight, Height, Italic,
  Label, Size, Strikethrough, Tooltip, Underline, Visible, Width, X, Y
```

### ModernToggle
```
# Control ModernToggle
Part of the control family React.

Control creation keywords:
Control: ModernToggle

Input Properties:
  - AccessibleLabel: Text         Default: ""
  - BasePaletteColor: Color
  - Color: Color
  - ContentLanguage: Text         Default: ""
  - Default: Boolean              Default: false
  - DisplayMode: Enum             Default: DisplayMode.Edit            (DisplayMode: Disabled, Edit, View)
  - Font: Enum                    Default: ""                          (Font: Arial, Courier New, Dancing Script, Georgia, Great Vibes, Lato, Lato Black, Lato Hairline, Lato Light, Open Sans, Open Sans Condensed, Patrick Hand, Segoe UI, Verdana)
  - FontWeight: Enum                                                   (FontWeight: Bold, Lighter, Normal, Semibold)
  - Height: Number                Default: 35
  - Italic: Boolean               Default: false
  - Label: Text                   Default: "Label"
  - LabelPosition: Enum           Default: ToggleLabelPosition.After   (ToggleLabelPosition: Above, After, Before)
  - OnCheck: Boolean              Default: false
  - OnUncheck: Boolean            Default: false
  - Size: Number                  Default: 0
  - Strikethrough: Boolean        Default: false
  - ToggleSize: Number            Default: 40
  - Tooltip: Text                 Default: ""
  - Underline: Boolean            Default: false
  - Visible: Boolean              Default: true
  - Width: Number                 Default: 113
  - X: Number                     Default: 0
  - Y: Number                     Default: 0

Additional input properties if a child of a Vertical or Horizontal GroupContainer:
  - AlignInContainer: Enum        Default: AlignInContainer.SetByContainer (Center, End, SetByContainer, Start, Stretch)
  - FillPortions: Number          Default: 0
  - LayoutMaxHeight: Number       Default: 0
  - LayoutMaxWidth: Number        Default: 0
  - LayoutMinHeight: Number       Default: 35
  - LayoutMinWidth: Number        Default: 113

Additional input properties if a child of a Grid GroupContainer:
  - LayoutGridColumnEnd, LayoutGridColumnStart, LayoutGridRowEnd, LayoutGridRowStart: Number

Output Properties:
  AccessibleLabel, BasePaletteColor, Checked: Boolean, Color, ContentLanguage, DisplayMode, Font, FontWeight, Height, Italic, Label,
  LabelPosition, Size, Strikethrough, ToggleSize, Tooltip, Underline, Visible, Width, X, Y
```

### ModernRadio
```
# Control ModernRadio
Part of the control family React.

Control creation keywords:
Control: ModernRadio

Input Properties:
  - AccessibleLabel: Text         Default: ""
  - BasePaletteColor: Color
  - BorderColor: Color
  - BorderStyle: Enum             Default: ""                          (BorderStyle: Dashed, Dotted, None, Solid)
  - BorderThickness: Number
  - Color: Color
  - ContentLanguage: Text         Default: ""
  - Default: Record
  - DisabledColor: Color          Default: RGBA(186, 186, 186, 1)
  - DisplayMode: Enum             Default: DisplayMode.Edit            (DisplayMode: Disabled, Edit, View)
  - Fill: Color
  - Font: Enum                    Default: ""                          (Font: Arial, Courier New, Dancing Script, Georgia, Great Vibes, Lato, Lato Black, Lato Hairline, Lato Light, Open Sans, Open Sans Condensed, Patrick Hand, Segoe UI, Verdana)
  - FontWeight: Enum              Default: FontWeight.Normal           (FontWeight: Bold, Lighter, Normal, Semibold)
  - Height: Number                Default: 100
  - Italic: Boolean               Default: false
  - ItemDisplayText: Text         Default: ThisItem.Value
  - Items: Table                  Default: RadioSample
  - Layout: Enum                  Default: OptionLayout.Vertical       (OptionLayout: Horizontal, HorizontalStacked, Vertical)
  - LineHeight: Number            Default: 16
  - OnChange: Boolean             Default: false
  - PaddingBottom: Number
  - PaddingLeft: Number
  - PaddingRight: Number
  - PaddingTop: Number
  - RadioBackgroundFill: Color
  - RadioBorderColor: Color
  - RadioSelectionFill: Color
  - RadioSize: Number             Default: 14
  - RadiusBottomLeft: Number
  - RadiusBottomRight: Number
  - RadiusTopLeft: Number
  - RadiusTopRight: Number
  - Required: Boolean             Default: false
  - Size: Number                  Default: 14
  - Strikethrough: Boolean        Default: false
  - Underline: Boolean            Default: false
  - Visible: Boolean              Default: true
  - Width: Number                 Default: 320
  - X: Number                     Default: 0
  - Y: Number                     Default: 0

Additional input properties if a child of a Vertical or Horizontal GroupContainer:
  - AlignInContainer: Enum        Default: AlignInContainer.SetByContainer (Center, End, SetByContainer, Start, Stretch)
  - FillPortions: Number          Default: 0
  - LayoutMaxHeight: Number       Default: 0
  - LayoutMaxWidth: Number        Default: 0
  - LayoutMinHeight: Number       Default: 100
  - LayoutMinWidth: Number        Default: 320

Additional input properties if a child of a Grid GroupContainer:
  - LayoutGridColumnEnd, LayoutGridColumnStart, LayoutGridRowEnd, LayoutGridRowStart: Number

Output Properties:
  AccessibleLabel, BasePaletteColor, BorderColor, BorderStyle, BorderThickness, Color, ContentLanguage, DisabledColor, DisplayMode, Fill, Font,
  FontWeight, Height, Italic, Layout, LineHeight, PaddingBottom, PaddingLeft, PaddingRight, PaddingTop, RadioBackgroundFill, RadioBorderColor,
  RadioSelectionFill, RadioSize, RadiusBottomLeft, RadiusBottomRight, RadiusTopLeft, RadiusTopRight, Selected: Record, Size, Strikethrough,
  Underline, Visible, Width, X, Y
```

### CanvasComponent (instances) and ComponentDefinitions
Not a `describe_control` target. Verified syntax (compiled in v1):
```yaml
# definition (Components.pa.yaml)
ComponentDefinitions:
  cmpX:
    DefinitionType: CanvasComponent
    Description: ...
    AccessAppScope: true
    CustomProperties:
      SomeInput:
        PropertyKind: Input
        DisplayName: SomeInput
        Description: ...
        DataType: Text          # Text | Boolean | Number
        Default: =""
      SomeEvent:
        PropertyKind: Event
        DisplayName: SomeEvent
        Description: ...
        ReturnType: None
        Default: =false         # REQUIRED (sync rule 5)
    Properties:
      Height: =...
      Width: =...
    Children:
      - cntRoot: ...
# instance (screen file)
- cmpXInstance:
    Control: CanvasComponent
    ComponentName: cmpX
    Properties:
      SomeInput: ="value"
      SomeEvent: =Navigate(Home, ScreenTransition.None)
      Height: =...
      Width: =...
```
Inside a definition, read inputs as `cmpX.SomeInput` and raise events as `cmpX.SomeEvent()`. Instances also accept the AutoLayout child properties (`AlignInContainer`, `FillPortions`, `LayoutMinHeight`, `LayoutMinWidth`).


