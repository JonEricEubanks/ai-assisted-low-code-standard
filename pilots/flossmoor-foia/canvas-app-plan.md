# Canvas App Plan

## Mode
EDIT (complex) — responsive + reusable-component + Fluent 2 refactor of the Flossmoor FOIA pilot app.

## Edit Requirements
1. **RESPONSIVE** — phone (`App.Width < 600`), tablet (`600–1199`), desktop (`>= 1200`). Keep and use the existing `BreakpointPhone`, `BreakpointDesktop`, `SpaceXs/Sm/Md/Lg`, `ControlMinTouch` named formulas. Every `GroupContainer` is `Variant: AutoLayout`. Every `ModernText` that can wrap has `AutoHeight: =true`. No fixed `Width` on text; use `FillPortions`, `LayoutMinWidth`, `Parent.Width` formulas and container `LayoutAlignItems: =LayoutAlignItems.Stretch`.
2. **COMPONENTS** — replace the per-screen `cntXxxHeader` shell with reusable Canvas components in a new `Components.pa.yaml`: `cmpAppHeader`, `cmpSideNav` (one component, `Placement` input renders left rail on tablet/desktop and bottom bar on phone), `cmpStatusBadge`. Instances use `Control: CanvasComponent` + `ComponentName:`. **Never** `Control: Component` (authoring service rejects it).
3. **FLUENT** — replace the navy/gold palette with Fluent 2 tokens (block below, paste verbatim). Keep existing formula names; alias `ColorNavy`, `ColorGold`, `ColorCharcoal`, `ColorBorder` to the new tokens. Segoe UI via modern controls, 4 px radius, 1 px neutral strokes instead of shadows.
4. **VISUAL DEFECTS to fix** — (a) header buttons wrapping mid-word → buttons get `FillPortions: =0`, explicit `Width` + equal `LayoutMinWidth`, `Size: =FontSizeBody`, collapse to icon-only on phone; (b) KPI/summary cards show purple broken image placeholders → the cause is `ModernCard` defaulting `Image`/`HeaderImage` to `SampleCardImage`; **remove every `ModernCard`** and rebuild as the Tile / Row patterns below using `GroupContainer` + `ModernIcon` + `ModernText`; (c) 5 Dashboard App Checker layout warnings → never set both `FillPortions > 0` and `Width` on the same child; inside `LayoutWrap: =true` containers all children use `FillPortions: =0` + formula `Width`; direction-switching containers use `FillPortions: =If(IsPhone, 0, 1)`.
5. **SCOPE GUARD** — only the 4 connected data sources (`'FOIA Pilot Requests'`, `'FOIA Pilot Assignments'`, `'FOIA Pilot Departments'`, `'FOIA Pilot Records'`) with the exact column names in `## Data Source Schemas`. No new data sources. No legal due-date auto-calculation (keep the "human-confirmed working due date" language and `DueDateConfirmed` gating). No retention/deletion. No publishing. Do not change any `Patch`/`Filter`/`LookUp` data logic except where this plan explicitly says so.

## Working Directory
`C:\Users\tejas\OneDrive - MGP Inc\ManagedApps\AI_Process\pilots\flossmoor-foia\canvas-app-src`

## Current App Summary
- Screens (all exist, all AutoLayout, each with its own duplicated header container):
  - `Dashboard` — KPI cards (4 × `ModernCard`), search/status/department filters, `galRecentRequests` (Vertical gallery of `ModernCard` rows) → navigates to `RequestDetail`.
  - `NewRequest` — manual intake form built from `ModernTextInput`/`ModernCombobox`/`ModernDatePicker`/`ModernCheckbox`; saves via `Patch('FOIA Pilot Requests', Defaults(...), {...})`; hidden unused `frmRequestIntake` Form.
  - `RequestDetail` — 4 summary `ModernCard`s, stage/status badges + `ModernProgressBar`, two info columns, `galAssignments` (VariableHeight gallery), extension review block, action buttons to `DepartmentWork` / `ResponseCloseout`.
  - `DepartmentWork` — horizontal `galDepartmentAssignments` (`ModernCard` per assignment), assignment editor (`ModernDropdown`, `ModernDatePicker`, `ModernToggle`, `ModernTextInput`) with Save / Mark complete `Patch`es, `galDepartmentRecords`.
  - `ResponseCloseout` — 3 readiness `ModernCard`s, readiness banner, final date/status/notes editor, validation block, Validate / Close `Patch`.
- Layout strategy: AutoLayout throughout, but many fixed `Width`/`Height` literals, `FillPortions` + `Width` conflicts inside `LayoutWrap` containers, several containers with no `Height` (default 225) and missing `AutoHeight` on wrapping text.
- Current palette (to be replaced): `ColorNavy RGBA(27,40,63,1)`, `ColorGold RGBA(213,164,57,1)`, `ColorSurface RGBA(244,246,248,1)` (grey page bg), `ColorBorder RGBA(214,220,226,1)`, `ColorTextPrimary RGBA(27,40,52,1)`, `ColorTextSecondary RGBA(86,101,116,1)`, success/warning/critical/info custom values. Headers are navy fills with gold titles; `Color.White` and literal `RGBA(255,255,255,1)` fills appear on content containers.
- Variables in use (global, keep all names): `gblIsLoading` (Boolean), `gblLoadError` (Boolean), `gblPermissionDenied` (Boolean), `gblSaveSuccess` (Boolean), `gblSearchText` (Text), `gblStatusFilter` (Text), `gblDepartmentFilter` (Text), `gblSelectedRequest` (Record of 'FOIA Pilot Requests'), `gblSelectedAssignment` (Record of 'FOIA Pilot Assignments'), `gblSelectedDepartment` (Record {Id, Value}), `gblDueDateConfirmed` (Boolean), `gblExtensionValidationMessage` (Text).
- Existing named formulas: `ColorNavy, ColorCharcoal, ColorGold, ColorSurface, ColorBorder, ColorTextPrimary, ColorTextSecondary, ColorSuccess, ColorWarning, ColorCritical, ColorInfo, BreakpointPhone, BreakpointDesktop, SpaceXs, SpaceSm, SpaceMd, SpaceLg, ControlMinTouch`.
- Data sources: the four SharePoint lists above. `App.StartScreen = Dashboard`, `App.Theme = PowerAppsTheme`.
- Live session note: `list_controls` shows a stub Canvas component `cmpAppHeader` already in the coauthoring session (only a required `Title` input, 640×640 default size) from an earlier compile check. `Components.pa.yaml` **replaces** that definition in full; all custom properties must declare a `Default`.

## Screens
| Screen | File | Action | Summary of Changes |
|--------|------|--------|--------------------|
| Components | Components.pa.yaml | **Create** | `ComponentDefinitions:` for `cmpAppHeader`, `cmpSideNav`, `cmpStatusBadge` (full contracts below). |
| App | App.pa.yaml | Modify | Replace `Formulas` with the Fluent token block (verbatim below). Keep `StartScreen`, `Theme`. |
| Dashboard | Dashboard.pa.yaml | Modify | Shell replacement; KPI `ModernCard`s → Tiles with `ModernIcon`; filter row → direction-switching; gallery rows → Row pattern with `cmpStatusBadge` + Open button; fix FillPortions/Width conflicts; remove `cntQueueBody` wrapper. |
| NewRequest | NewRequest.pa.yaml | Modify | Shell replacement; form shell becomes the scroller with sticky action bar; field groups get formula widths/heights; AutoHeight on all labels; remove unused `frmRequestIntake`; Fluent button styling. |
| RequestDetail | RequestDetail.pa.yaml | Modify | Shell replacement (dynamic title); summary `ModernCard`s → Tiles; status badges → `cmpStatusBadge`; two-column info → auto-height sections; assignment rows → Row pattern with Open button; extension + action rows direction-switching. |
| DepartmentWork | DepartmentWork.pa.yaml | Modify | Shell replacement; assignment selector cards → Row pattern with Select button; editor rows direction-switching; section heights formula-driven; `Color.White` → `ColorSurface`. |
| ResponseCloseout | ResponseCloseout.pa.yaml | Modify | Shell replacement; readiness `ModernCard`s → Tiles; banner/validation blocks auto-height with Fluent tints; editor rows direction-switching; radio stacks on phone. |
| _EditorState | _EditorState.pa.yaml | Modify (optional) | Add `ComponentDefinitionsOrder: [cmpAppHeader, cmpSideNav, cmpStatusBadge]` under `EditorState`. |

## Data Source Schemas
Source: `pilots\flossmoor-foia\datasource-schema.md` (verified live column names). Site `https://communityessentials.sharepoint.com/sites/Administration`. Use these logical names exactly. Choice/lookup columns are records (`.Value`, `.Id`); person columns are records (`.DisplayName`, `.Email`, `.Claims`); date columns are date values.

### FOIA Pilot Requests
| Logical name | Type | Notes |
|---|---|---|
| ID | integer | |
| Title | string | |
| ReceivedDate | date | |
| IntakeMethod | choice | `.Value`, `.Id` |
| RequestRoute | choice | `.Value` — values used: "Intake", "Department Review", "Response Preparation", "Closed" |
| RequestDescription | string | multiline |
| OverallStatus | choice | `.Value` — values used: "New", "In Progress", "On Hold", "Ready", "Delivered", "Closed" |
| CommercialPurpose | choice | |
| RequesterFirstName / RequesterLastName | string | |
| RequesterStreetAddress / RequesterCity / RequesterState / RequesterZip | string | |
| RequesterEmail / RequesterPhone | string | |
| DeliveryFormat | choice | |
| CertifiedCopies | choice | Yes/No |
| FeeWaiverRequested | choice | Yes/No |
| DueDate | date | human-entered working due date |
| DueDateConfirmed | boolean | |
| PrimaryDepartment | lookup | `.Value`, `.Id` |
| AssignedOfficer | person | |
| ExtensionType | choice | |
| ExtensionDays | number | |
| ExtensionStatus | choice | |
| FinalResponseDate | date | |
| CloseoutNotes | string | |
| CurrentStageNotes | string | |
| Modified / Created | date-time | |
| Author / Editor | person | |

### FOIA Pilot Assignments
| Logical name | Type | Notes |
|---|---|---|
| ID | integer | |
| Title | string | |
| AssignmentStatus | choice | `.Value` — "Complete" is the terminal value |
| Request | lookup | `.Id` = Requests.ID |
| Department | lookup | `.Value`, `.Id` |
| AssignedTo | person | |
| AssignmentDueDate | date | |
| RedactionRequired | choice | Yes/No |
| DepartmentCompleteDate | date | |
| ResponseNotes | string | |
| Active | boolean | |
| Modified / Created | date-time | |
| Author / Editor | person | |

### FOIA Pilot Departments
| Logical name | Type |
|---|---|
| ID | integer |
| Title | string |
| DepartmentCode | string |
| Active | boolean |
| SortOrder | number |
| IsPolice | boolean |
| Modified / Created | date-time |
| Author / Editor | person |

### FOIA Pilot Records
| Logical name | Type | Notes |
|---|---|---|
| ID | integer | |
| Title | string | |
| DocumentType | choice | |
| OData__ExtendedDescription | string | Description |
| Request | lookup | `.Id` |
| Department | lookup | `.Id`, `.Value` |
| RedactionStatus | choice | |
| IsFinalResponse | boolean | |
| Sensitivity | choice | |
| Notes | string | |
| CheckoutUser | person | |
| OData__DisplayName | string | |
| Modified / Created | date-time | |
| Author / Editor | person | |

## App.pa.yaml — Fluent 2 Token Block (paste verbatim)

Replace the entire `Formulas` value in `App.pa.yaml` with the block below. Keep `StartScreen: =Dashboard` and `Theme: =PowerAppsTheme` unchanged. Every existing formula name is preserved (aliases at the bottom) so no screen reference breaks.

```yaml
App:
  Properties:
    Formulas: |-
      =// ---- Fluent 2 color tokens ----
      ColorBrand = RGBA(0, 120, 212, 1);
      ColorBrandHover = RGBA(16, 110, 190, 1);
      ColorBrandTint = RGBA(235, 243, 252, 1);
      ColorNeutralBg = RGBA(250, 250, 250, 1);
      ColorSurface = RGBA(255, 255, 255, 1);
      ColorNeutralStroke = RGBA(225, 223, 221, 1);
      ColorTextPrimary = RGBA(36, 36, 36, 1);
      ColorTextSecondary = RGBA(97, 97, 97, 1);
      ColorSuccess = RGBA(16, 124, 16, 1);
      ColorWarning = RGBA(157, 93, 0, 1);
      ColorCritical = RGBA(196, 43, 28, 1);
      ColorInfo = RGBA(0, 120, 212, 1);
      ColorSuccessBg = RGBA(241, 250, 241, 1);
      ColorWarningBg = RGBA(255, 249, 245, 1);
      ColorCriticalBg = RGBA(253, 243, 244, 1);
      // ---- Legacy aliases (retired names; do not use in new code) ----
      ColorNavy = ColorBrand;
      ColorCharcoal = ColorTextPrimary;
      ColorGold = ColorBrand;
      ColorBorder = ColorNeutralStroke;
      // ---- Breakpoints ----
      BreakpointPhone = 600;
      BreakpointDesktop = 1200;
      IsPhone = App.Width < BreakpointPhone;
      IsTablet = App.Width >= BreakpointPhone && App.Width < BreakpointDesktop;
      IsDesktop = App.Width >= BreakpointDesktop;
      // ---- Spacing / sizing ----
      SpaceXs = 4;
      SpaceSm = 8;
      SpaceMd = 16;
      SpaceLg = 24;
      RadiusSm = 4;
      ControlMinTouch = 44;
      InputHeight = 44;
      FieldHeight = 72;
      HeaderHeight = 64;
      NavRailWidth = If(IsDesktop, 220, 64);
      BottomNavHeight = 56;
      PagePadding = If(IsPhone, SpaceMd, SpaceLg);
      TileHeight = 104;
      // ---- Type scale (Segoe UI via modern controls) ----
      FontSizeTitle = If(IsPhone, 18, 22);
      FontSizeSection = 16;
      FontSizeBody = 14;
      FontSizeCaption = 12;
      FontSizeKpi = 28
    StartScreen: =Dashboard
    Theme: =PowerAppsTheme
```

Usage rules for every screen builder:
- Page background: screen `Fill: =ColorNeutralBg` and shell container `Fill: =ColorNeutralBg`. Cards/tiles/sections: `Fill: =ColorSurface`, `BorderColor: =ColorNeutralStroke`, `BorderThickness: =1`, `BorderStyle: =BorderStyle.Solid`, all four `Radius*: =RadiusSm`, `DropShadow: =DropShadow.None`.
- Primary buttons: `Appearance: =ButtonAppearance.Primary`, `BasePaletteColor: =ColorBrand`. Secondary: `Appearance: =ButtonAppearance.Secondary` (no `BasePaletteColor`, no `Color`). Subtle/icon buttons: `Appearance: =ButtonAppearance.Subtle`. Never use `ColorGold`/`ColorNavy`/`Color.White` in new or edited YAML — use `ColorBrand`, `ColorTextPrimary`, `ColorSurface`.
- Text: titles `Size: =FontSizeTitle`, section headings `Size: =FontSizeSection` + `FontWeight: =FontWeight.Semibold` + `Color: =ColorTextPrimary`, body `Size: =FontSizeBody`, captions `Size: =FontSizeCaption` + `Color: =ColorTextSecondary`, KPI values `Size: =FontSizeKpi` + `FontWeight: =FontWeight.Semibold`.
- Semantic color is never the only cue: pair `ColorSuccess/Warning/Critical` with an icon (`ModernIcon` or badge `Icon`) or text.

## Components.pa.yaml — Definitions (Create)

File root key is `ComponentDefinitions:`. All three components set `AccessAppScope: true` (plain YAML boolean, not a formula) so they can read App named formulas (`ColorBrand`, `IsPhone`, …) and call `Navigate` to app screens. Inside a definition, reference custom properties as `<ComponentName>.<Property>` (e.g. `cmpAppHeader.Title`) and raise an event as `<ComponentName>.<Event>()` (e.g. `cmpAppHeader.OnBack()`). Component root children are positioned manually — the first child is always one `GroupContainer` with `X: =0`, `Y: =0`, `Width: =Parent.Width`, `Height: =Parent.Height`. Component `Properties` may not include `X`, `Y`, or `Visible` (schema rule).

Property-kind syntax (official pa-yaml v3.0 schema): `Input` requires `DataType` (+ optional `Default`); `Event` requires `ReturnType: None` (optional `Default`, optional `Parameters`). `DisplayName` is accepted (deprecated) and verified to compile.

### cmpAppHeader

**Purpose:** Shared top bar for all five screens. Consuming screens: Dashboard, NewRequest, RequestDetail, DepartmentWork, ResponseCloseout.
**Breakpoint behavior:** Height is set by the instance (`HeaderHeight`). Phone: back/secondary/primary buttons collapse to icon-only (when an icon is supplied), subtitle hidden, title 18 px. Tablet/desktop: text buttons, subtitle shown, title 22 px. Buttons never flex (`FillPortions: =0`, `Width` = `LayoutMinWidth`) so labels cannot wrap mid-word.
**Accessibility:** every button has `AccessibleLabel` and `Tooltip`; title has `AccessibleLabel`. Focus order: Back → Secondary → Primary.
**App-scope dependencies (justified):** named formulas only (colors, breakpoints, spacing). No global variables, no data writes.

Contract:

| Property | Kind | DataType / ReturnType | Default | Purpose |
|---|---|---|---|---|
| Title | Input | Text | `="FOIA"` | Page title |
| Subtitle | Input | Text | `=""` | Caption under title; hidden on phone or when blank |
| ShowBack | Input | Boolean | `=false` | Shows the Back button |
| PrimaryLabel | Input | Text | `=""` | Primary button text; button hidden when blank |
| PrimaryIcon | Input | Text | `=""` | Fluent icon name for primary (e.g. "Add"); enables icon-only on phone |
| SecondaryLabel | Input | Text | `=""` | Secondary button text; hidden when blank |
| SecondaryIcon | Input | Text | `=""` | Fluent icon name for secondary (e.g. "ArrowClockwise") |
| OnBack | Event | None | — | Raised by Back button |
| OnPrimary | Event | None | — | Raised by primary button |
| OnSecondary | Event | None | — | Raised by secondary button |

```yaml
ComponentDefinitions:
  cmpAppHeader:
    DefinitionType: CanvasComponent
    Description: Shared Fluent app header with optional back, secondary and primary actions.
    AccessAppScope: true
    CustomProperties:
      Title:
        PropertyKind: Input
        DisplayName: Title
        Description: Page title shown in the header.
        DataType: Text
        Default: ="FOIA"
      Subtitle:
        PropertyKind: Input
        DisplayName: Subtitle
        Description: Caption under the title. Hidden on phone widths or when blank.
        DataType: Text
        Default: =""
      ShowBack:
        PropertyKind: Input
        DisplayName: ShowBack
        Description: Shows the Back button when true.
        DataType: Boolean
        Default: =false
      PrimaryLabel:
        PropertyKind: Input
        DisplayName: PrimaryLabel
        Description: Text of the primary action. Button hidden when blank.
        DataType: Text
        Default: =""
      PrimaryIcon:
        PropertyKind: Input
        DisplayName: PrimaryIcon
        Description: Fluent icon name for the primary action (icon-only on phone).
        DataType: Text
        Default: =""
      SecondaryLabel:
        PropertyKind: Input
        DisplayName: SecondaryLabel
        Description: Text of the secondary action. Button hidden when blank.
        DataType: Text
        Default: =""
      SecondaryIcon:
        PropertyKind: Input
        DisplayName: SecondaryIcon
        Description: Fluent icon name for the secondary action (icon-only on phone).
        DataType: Text
        Default: =""
      OnBack:
        PropertyKind: Event
        DisplayName: OnBack
        Description: Raised when the Back button is selected.
        ReturnType: None
      OnPrimary:
        PropertyKind: Event
        DisplayName: OnPrimary
        Description: Raised when the primary action is selected.
        ReturnType: None
      OnSecondary:
        PropertyKind: Event
        DisplayName: OnSecondary
        Description: Raised when the secondary action is selected.
        ReturnType: None
    Properties:
      Fill: =ColorSurface
      Height: =HeaderHeight
      Width: =App.Width
    Children:
      - cntHeaderRoot:
          Control: GroupContainer
          Variant: AutoLayout
          Properties:
            Fill: =ColorSurface
            Height: =Parent.Height
            LayoutAlignItems: =LayoutAlignItems.Stretch
            LayoutDirection: =LayoutDirection.Vertical
            LayoutGap: =0
            Width: =Parent.Width
            X: =0
            Y: =0
          Children:
            - cntHeaderBar:
                Control: GroupContainer
                Variant: AutoLayout
                Properties:
                  FillPortions: =1
                  LayoutAlignItems: =LayoutAlignItems.Center
                  LayoutDirection: =LayoutDirection.Horizontal
                  LayoutGap: =SpaceSm
                  LayoutMinHeight: =0
                  PaddingLeft: =PagePadding
                  PaddingRight: =PagePadding
                Children:
                  - btnHeaderBack:
                      Control: ModernButton
                      Properties:
                        AccessibleLabel: ="Go back"
                        Appearance: =ButtonAppearance.Subtle
                        FillPortions: =0
                        Height: =ControlMinTouch - 4
                        Icon: ="ArrowLeft"
                        Layout: =If(IsPhone, ButtonLayout.IconOnly, ButtonLayout.IconBefore)
                        LayoutMinWidth: =If(IsPhone, ControlMinTouch, 96)
                        OnSelect: =cmpAppHeader.OnBack()
                        Size: =FontSizeBody
                        Text: ="Back"
                        Tooltip: ="Back"
                        Visible: =cmpAppHeader.ShowBack
                        Width: =If(IsPhone, ControlMinTouch, 96)
                  - cntHeaderTitles:
                      Control: GroupContainer
                      Variant: AutoLayout
                      Properties:
                        FillPortions: =1
                        LayoutAlignItems: =LayoutAlignItems.Stretch
                        LayoutDirection: =LayoutDirection.Vertical
                        LayoutGap: =0
                        LayoutJustifyContent: =LayoutJustifyContent.Center
                        LayoutMinHeight: =0
                        LayoutMinWidth: =120
                      Children:
                        - lblHeaderTitle:
                            Control: ModernText
                            Properties:
                              AccessibleLabel: =Self.Text
                              AutoHeight: =true
                              Color: =ColorTextPrimary
                              FontWeight: =FontWeight.Semibold
                              PaddingBottom: =0
                              PaddingLeft: =0
                              PaddingRight: =0
                              PaddingTop: =0
                              Size: =FontSizeTitle
                              Text: =cmpAppHeader.Title
                        - lblHeaderSubtitle:
                            Control: ModernText
                            Properties:
                              AccessibleLabel: =Self.Text
                              AutoHeight: =true
                              Color: =ColorTextSecondary
                              PaddingBottom: =0
                              PaddingLeft: =0
                              PaddingRight: =0
                              PaddingTop: =0
                              Size: =FontSizeCaption
                              Text: =cmpAppHeader.Subtitle
                              Visible: =!IsPhone && !IsBlank(cmpAppHeader.Subtitle)
                  - btnHeaderSecondary:
                      Control: ModernButton
                      Properties:
                        AccessibleLabel: =cmpAppHeader.SecondaryLabel
                        Appearance: =ButtonAppearance.Secondary
                        FillPortions: =0
                        Height: =ControlMinTouch - 4
                        Icon: =cmpAppHeader.SecondaryIcon
                        Layout: |-
                          =If(IsBlank(cmpAppHeader.SecondaryIcon), ButtonLayout.TextOnly,
                              IsPhone, ButtonLayout.IconOnly,
                              ButtonLayout.IconBefore)
                        LayoutMinWidth: =Self.Width
                        OnSelect: =cmpAppHeader.OnSecondary()
                        Size: =FontSizeBody
                        Text: =cmpAppHeader.SecondaryLabel
                        Tooltip: =cmpAppHeader.SecondaryLabel
                        Visible: =!IsBlank(cmpAppHeader.SecondaryLabel)
                        Width: |-
                          =If(IsPhone && !IsBlank(cmpAppHeader.SecondaryIcon), ControlMinTouch,
                              Len(cmpAppHeader.SecondaryLabel) * 9 + SpaceLg * 2 + If(IsBlank(cmpAppHeader.SecondaryIcon), 0, 24))
                  - btnHeaderPrimary:
                      Control: ModernButton
                      Properties:
                        AccessibleLabel: =cmpAppHeader.PrimaryLabel
                        Appearance: =ButtonAppearance.Primary
                        BasePaletteColor: =ColorBrand
                        FillPortions: =0
                        Height: =ControlMinTouch - 4
                        Icon: =cmpAppHeader.PrimaryIcon
                        Layout: |-
                          =If(IsBlank(cmpAppHeader.PrimaryIcon), ButtonLayout.TextOnly,
                              IsPhone, ButtonLayout.IconOnly,
                              ButtonLayout.IconBefore)
                        LayoutMinWidth: =Self.Width
                        OnSelect: =cmpAppHeader.OnPrimary()
                        Size: =FontSizeBody
                        Text: =cmpAppHeader.PrimaryLabel
                        Tooltip: =cmpAppHeader.PrimaryLabel
                        Visible: =!IsBlank(cmpAppHeader.PrimaryLabel)
                        Width: |-
                          =If(IsPhone && !IsBlank(cmpAppHeader.PrimaryIcon), ControlMinTouch,
                              Len(cmpAppHeader.PrimaryLabel) * 9 + SpaceLg * 2 + If(IsBlank(cmpAppHeader.PrimaryIcon), 0, 24))
            - cntHeaderDivider:
                Control: GroupContainer
                Variant: AutoLayout
                Properties:
                  Fill: =ColorNeutralStroke
                  FillPortions: =0
                  Height: =1
                  LayoutDirection: =LayoutDirection.Horizontal
                  LayoutMinHeight: =1
```

> If the compiler rejects `LayoutMinWidth: =Self.Width`, repeat the full `Width` formula in `LayoutMinWidth` instead.

**Instance snippet (paste into every screen, rename `cmpXxxHeader`):**

```yaml
- cmpDashboardHeader:
    Control: CanvasComponent
    ComponentName: cmpAppHeader
    Properties:
      AlignInContainer: =AlignInContainer.Stretch
      FillPortions: =0
      Height: =HeaderHeight
      LayoutMinHeight: =HeaderHeight
      OnBack: =Navigate(Dashboard, ScreenTransition.None)
      OnPrimary: =Navigate(NewRequest, ScreenTransition.Fade)
      OnSecondary: =false
      PrimaryIcon: ="Add"
      PrimaryLabel: ="New request"
      SecondaryIcon: =""
      SecondaryLabel: =""
      ShowBack: =false
      Subtitle: ="Village of Flossmoor · Request queue and response readiness"
      Title: ="FOIA requests"
```

### cmpSideNav

**Purpose:** Single navigation component for all five screens. `Placement = "Rail"` renders a left rail (desktop: icon + label, 220 px; tablet: icon-only, 64 px). `Placement = "Bottom"` renders a phone bottom tab bar (icon-only, 56 px). Each screen places **two instances** (rail + bottom) and toggles `Visible` by breakpoint — the component itself does not decide placement, so no layout-reflow trick is needed inside a Horizontal/Vertical shell.
**Breakpoint behavior:** rail width comes from the instance (`NavRailWidth`), bottom height from `BottomNavHeight`. Desktop rail buttons are left-aligned `IconBefore`; tablet/phone are `IconOnly` with `Tooltip`.
**Active state (non-color cue):** active item = `ButtonAppearance.Secondary` + `FontWeight.Semibold` + `IconStyle.Filled` + `Color: =ColorBrand`; inactive = `Subtle` + Normal + Outline + `ColorTextPrimary`.
**Accessibility:** each button has `AccessibleLabel` ("Go to Dashboard" …) and `Tooltip`; all are ≥ 44 px targets. Tab order top-to-bottom / left-to-right.
**App-scope dependencies (justified):** named formulas + `Navigate` to app screens. Navigating to RequestDetail/DepartmentWork/ResponseCloseout without a selected request is safe — those screens already render an empty state.

Contract:

| Property | Kind | DataType | Default | Purpose |
|---|---|---|---|---|
| ActiveScreen | Input | Text | `="Dashboard"` | One of "Dashboard", "NewRequest", "RequestDetail", "DepartmentWork", "ResponseCloseout" |
| Placement | Input | Text | `="Rail"` | "Rail" (vertical, left) or "Bottom" (horizontal, phone) |

Nav items (order, label, icon, target):
1. Dashboard — "Dashboard" — `Home` — `Navigate(Dashboard, ScreenTransition.None)`
2. NewRequest — "New request" — `Add` — `Navigate(NewRequest, ScreenTransition.None)`
3. RequestDetail — "Request detail" — `Document` — `Navigate(RequestDetail, ScreenTransition.None)`
4. DepartmentWork — "Department work" — `People` — `Navigate(DepartmentWork, ScreenTransition.None)`
5. ResponseCloseout — "Closeout" — `CheckmarkCircle` — `Navigate(ResponseCloseout, ScreenTransition.None)`

```yaml
  cmpSideNav:
    DefinitionType: CanvasComponent
    Description: Shared navigation. Placement "Rail" = left rail (desktop/tablet); "Bottom" = phone tab bar.
    AccessAppScope: true
    CustomProperties:
      ActiveScreen:
        PropertyKind: Input
        DisplayName: ActiveScreen
        Description: Name of the current screen used to highlight the active item.
        DataType: Text
        Default: ="Dashboard"
      Placement:
        PropertyKind: Input
        DisplayName: Placement
        Description: Rail (vertical left rail) or Bottom (horizontal phone bar).
        DataType: Text
        Default: ="Rail"
    Properties:
      Fill: =ColorSurface
      Height: =If(cmpSideNav.Placement = "Bottom", BottomNavHeight, App.Height - HeaderHeight)
      Width: =If(cmpSideNav.Placement = "Bottom", App.Width, NavRailWidth)
    Children:
      - cntNavRoot:
          Control: GroupContainer
          Variant: AutoLayout
          Properties:
            Fill: =ColorSurface
            Height: =Parent.Height
            LayoutAlignItems: =LayoutAlignItems.Stretch
            LayoutDirection: =If(cmpSideNav.Placement = "Bottom", LayoutDirection.Vertical, LayoutDirection.Horizontal)
            LayoutGap: =0
            Width: =Parent.Width
            X: =0
            Y: =0
          Children:
            - cntNavDividerTop:
                Control: GroupContainer
                Variant: AutoLayout
                Properties:
                  Fill: =ColorNeutralStroke
                  FillPortions: =0
                  Height: =1
                  LayoutDirection: =LayoutDirection.Horizontal
                  LayoutMinHeight: =1
                  LayoutMinWidth: =0
                  Visible: =cmpSideNav.Placement = "Bottom"
            - cntNavItems:
                Control: GroupContainer
                Variant: AutoLayout
                Properties:
                  FillPortions: =1
                  LayoutAlignItems: =If(cmpSideNav.Placement = "Bottom", LayoutAlignItems.Center, LayoutAlignItems.Stretch)
                  LayoutDirection: =If(cmpSideNav.Placement = "Bottom", LayoutDirection.Horizontal, LayoutDirection.Vertical)
                  LayoutGap: =SpaceXs
                  LayoutJustifyContent: =If(cmpSideNav.Placement = "Bottom", LayoutJustifyContent.SpaceBetween, LayoutJustifyContent.Start)
                  LayoutMinHeight: =0
                  LayoutMinWidth: =0
                  PaddingBottom: =SpaceSm
                  PaddingLeft: =SpaceSm
                  PaddingRight: =SpaceSm
                  PaddingTop: =SpaceSm
                Children:
                  - btnNavDashboard:
                      Control: ModernButton
                      Properties:
                        AccessibleLabel: ="Go to Dashboard"
                        Align: =If(cmpSideNav.Placement = "Rail" && IsDesktop, Align.Left, Align.Center)
                        AlignInContainer: =If(cmpSideNav.Placement = "Bottom", AlignInContainer.Center, AlignInContainer.Stretch)
                        Appearance: =If(cmpSideNav.ActiveScreen = "Dashboard", ButtonAppearance.Secondary, ButtonAppearance.Subtle)
                        Color: =If(cmpSideNav.ActiveScreen = "Dashboard", ColorBrand, ColorTextPrimary)
                        FillPortions: =If(cmpSideNav.Placement = "Bottom", 1, 0)
                        FontWeight: =If(cmpSideNav.ActiveScreen = "Dashboard", FontWeight.Semibold, FontWeight.Normal)
                        Height: =ControlMinTouch
                        Icon: ="Home"
                        IconStyle: =If(cmpSideNav.ActiveScreen = "Dashboard", IconStyle.Filled, IconStyle.Outline)
                        Layout: =If(cmpSideNav.Placement = "Rail" && IsDesktop, ButtonLayout.IconBefore, ButtonLayout.IconOnly)
                        LayoutMinHeight: =ControlMinTouch
                        LayoutMinWidth: =ControlMinTouch
                        OnSelect: =Navigate(Dashboard, ScreenTransition.None)
                        Size: =FontSizeBody
                        Text: ="Dashboard"
                        Tooltip: ="Dashboard"
                        Width: =Parent.Width - SpaceSm * 2
                  # Repeat the exact block above for:
                  #   btnNavNewRequest       ActiveScreen "NewRequest"       Icon "Add"             Text "New request"     Navigate(NewRequest, ScreenTransition.None)
                  #   btnNavRequestDetail    ActiveScreen "RequestDetail"    Icon "Document"        Text "Request detail"  Navigate(RequestDetail, ScreenTransition.None)
                  #   btnNavDepartmentWork   ActiveScreen "DepartmentWork"   Icon "People"          Text "Department work" Navigate(DepartmentWork, ScreenTransition.None)
                  #   btnNavResponseCloseout ActiveScreen "ResponseCloseout" Icon "CheckmarkCircle" Text "Closeout"        Navigate(ResponseCloseout, ScreenTransition.None)
                  # (write them out in full — YAML comments are placeholders for this plan only)
            - cntNavDividerSide:
                Control: GroupContainer
                Variant: AutoLayout
                Properties:
                  Fill: =ColorNeutralStroke
                  FillPortions: =0
                  LayoutDirection: =LayoutDirection.Vertical
                  LayoutMinHeight: =0
                  LayoutMinWidth: =1
                  Visible: =cmpSideNav.Placement = "Rail"
                  Width: =1
```

**Instance snippets (both go in every screen; see Shell pattern for placement):**

```yaml
# inside cntXxxBody (Horizontal) — first child
- cmpDashboardNavRail:
    Control: CanvasComponent
    ComponentName: cmpSideNav
    Properties:
      ActiveScreen: ="Dashboard"
      AlignInContainer: =AlignInContainer.Stretch
      FillPortions: =0
      LayoutMinWidth: =NavRailWidth
      Placement: ="Rail"
      Visible: =!IsPhone
      Width: =NavRailWidth

# inside cntXxxShell (Vertical) — last child, after cntXxxBody
- cmpDashboardNavBottom:
    Control: CanvasComponent
    ComponentName: cmpSideNav
    Properties:
      ActiveScreen: ="Dashboard"
      AlignInContainer: =AlignInContainer.Stretch
      FillPortions: =0
      Height: =BottomNavHeight
      LayoutMinHeight: =BottomNavHeight
      Placement: ="Bottom"
      Visible: =IsPhone
```

### cmpStatusBadge

**Purpose:** Maps `OverallStatus.Value` / `AssignmentStatus.Value` text to a Fluent semantic badge with an icon (non-color cue). Consuming screens: Dashboard (gallery rows), RequestDetail (status tile, stage/status row, assignment rows), DepartmentWork (assignment selector rows), ResponseCloseout (readiness tile).
**Breakpoint behavior:** size set by instance (`Width` 112–128, `Height` 24–28); content is a single line and does not wrap.
**Accessibility:** `AccessibleLabel = "Status: " & Status`; icon + text together convey state.
**App-scope dependencies:** none except named formulas (`FontSizeCaption`).

Contract:

| Property | Kind | DataType | Default | Purpose |
|---|---|---|---|---|
| Status | Input | Text | `="Not set"` | Status text to display and map |

Mapping (`Switch` on `Status`):

| Status | Intent | Icon |
|---|---|---|
| "New" | `BadgeIntent.Informative` | `Info` |
| "In Progress" | `BadgeIntent.Highlight` | `ArrowClockwise` |
| "On Hold" | `BadgeIntent.Caution` | `Pause` |
| "Ready" | `BadgeIntent.Attention` | `Checkmark` |
| "Delivered" | `BadgeIntent.Positive` | `Send` |
| "Closed" | `BadgeIntent.Positive` | `CheckmarkCircle` |
| "Complete" | `BadgeIntent.Positive` | `CheckmarkCircle` |
| "Overdue" | `BadgeIntent.Critical` | `Warning` |
| anything else / blank | `BadgeIntent.Neutral` | `Circle` |

```yaml
  cmpStatusBadge:
    DefinitionType: CanvasComponent
    Description: Fluent semantic status badge with icon for FOIA status values.
    AccessAppScope: true
    CustomProperties:
      Status:
        PropertyKind: Input
        DisplayName: Status
        Description: Status text (OverallStatus.Value or AssignmentStatus.Value).
        DataType: Text
        Default: ="Not set"
    Properties:
      Fill: =RGBA(0, 0, 0, 0)
      Height: =24
      Width: =120
    Children:
      - bdgStatus:
          Control: ModernBadge
          Properties:
            AccessibleLabel: ="Status: " & Coalesce(cmpStatusBadge.Status, "Not set")
            Appearance: =BadgeAppearance.Tint
            Content: =Coalesce(cmpStatusBadge.Status, "Not set")
            FontWeight: =FontWeight.Semibold
            Height: =Parent.Height
            Icon: |-
              =Switch(cmpStatusBadge.Status,
                "New", "Info",
                "In Progress", "ArrowClockwise",
                "On Hold", "Pause",
                "Ready", "Checkmark",
                "Delivered", "Send",
                "Closed", "CheckmarkCircle",
                "Complete", "CheckmarkCircle",
                "Overdue", "Warning",
                "Circle")
            IconPosition: =BadgeIconPosition.Before
            Intent: |-
              =Switch(cmpStatusBadge.Status,
                "New", BadgeIntent.Informative,
                "In Progress", BadgeIntent.Highlight,
                "On Hold", BadgeIntent.Caution,
                "Ready", BadgeIntent.Attention,
                "Delivered", BadgeIntent.Positive,
                "Closed", BadgeIntent.Positive,
                "Complete", BadgeIntent.Positive,
                "Overdue", BadgeIntent.Critical,
                BadgeIntent.Neutral)
            Shape: =BadgeShape.Rounded
            Size: =FontSizeCaption
            Width: =Parent.Width
            X: =0
            Y: =0
```

**Instance snippet:**

```yaml
- cmpRowStatus:
    Control: CanvasComponent
    ComponentName: cmpStatusBadge
    Properties:
      AlignInContainer: =AlignInContainer.Center
      FillPortions: =0
      Height: =24
      LayoutMinHeight: =24
      LayoutMinWidth: =112
      Status: =Coalesce(ThisItem.OverallStatus.Value, "Not set")
      Width: =112
```

Component compile order: builders writing `Components.pa.yaml` must put all three definitions under one `ComponentDefinitions:` root in the order `cmpAppHeader`, `cmpSideNav`, `cmpStatusBadge`. The orchestrator compiles after all files are written (do not call `compile_canvas` from a builder).

## Shared Layout Patterns (every screen builder applies these)

### P1 — Shell replacement (mandatory on all 5 screens)

Delete the screen's old header container **and all of its children** (`cntDashboardHeader`, `cntRequestHeader`, `cntRequestDetailHeader`, `cntDepartmentWorkHeader`, `cntCloseoutHeader`). Move any behavior those header buttons carried into the header instance events (table in each screen spec). Then restructure the screen root as:

```yaml
Screens:
  Dashboard:
    Properties:
      Fill: =ColorNeutralBg
      LoadingSpinnerColor: =ColorBrand
      OnVisible: |-
        =<unchanged OnVisible>
    Children:
      - cntDashboardShell:
          Control: GroupContainer
          Variant: AutoLayout
          Properties:
            Fill: =ColorNeutralBg
            Height: =Parent.Height
            LayoutAlignItems: =LayoutAlignItems.Stretch
            LayoutDirection: =LayoutDirection.Vertical
            LayoutGap: =0
            Width: =Parent.Width
          Children:
            - cmpDashboardHeader:        # cmpAppHeader instance (see snippet)
            - cntDashboardBody:
                Control: GroupContainer
                Variant: AutoLayout
                Properties:
                  FillPortions: =1
                  LayoutAlignItems: =LayoutAlignItems.Stretch
                  LayoutDirection: =LayoutDirection.Horizontal
                  LayoutGap: =0
                  LayoutMinHeight: =0
                Children:
                  - cmpDashboardNavRail:   # cmpSideNav Placement "Rail" (see snippet)
                  - cntDashboardContent:
                      Control: GroupContainer
                      Variant: AutoLayout
                      Properties:
                        FillPortions: =1
                        LayoutAlignItems: =LayoutAlignItems.Stretch
                        LayoutDirection: =LayoutDirection.Vertical
                        LayoutGap: =SpaceMd
                        LayoutMinWidth: =0
                        LayoutOverflowY: =LayoutOverflow.Scroll
                        PaddingBottom: =SpaceLg
                        PaddingLeft: =PagePadding
                        PaddingRight: =PagePadding
                        PaddingTop: =PagePadding
                      Children:
                        # ... all existing NON-shell content of the old cntXxxRoot goes here, in the same order ...
            - cmpDashboardNavBottom:     # cmpSideNav Placement "Bottom" (see snippet)
```

Rename per screen: `cntNewRequestShell/Body/Content`, `cntRequestDetailShell/Body/Content`, `cntDepartmentWorkShell/Body/Content`, `cntResponseCloseoutShell/Body/Content`; header/nav instances `cmpNewRequestHeader`, `cmpNewRequestNavRail`, `cmpNewRequestNavBottom`, etc. The old `cntXxxRoot` container is replaced by this structure (do not keep an extra nested scroll root). All content below uses `Parent.Width` of `cntXxxContent` (already minus nav rail and padding).

### P2 — AutoLayout child sizing rules (fixes the App Checker layout warnings)

1. A child sets **either** `FillPortions >= 1` (and no `Width` in a Horizontal parent / no `Height` in a Vertical parent) **or** `FillPortions: =0` with an explicit `Width`/`Height`. Never both.
2. Inside a container with `LayoutWrap: =true`, **every** child uses `FillPortions: =0` and a formula `Width` (see P4) plus a `Height`.
3. `GroupContainer` children default to `LayoutMinWidth 250` / `LayoutMinHeight 112`. Override to the intended minimum on every small or flexible container (dividers `=1`, flexible columns `=0`, field groups `=200`). Text/button/icon/badge children have smaller defaults but still set `LayoutMinWidth` on buttons (= their `Width`).
4. **Direction-switching containers** (`LayoutDirection: =If(IsPhone, LayoutDirection.Vertical, LayoutDirection.Horizontal)`): children that flex horizontally set `FillPortions: =If(IsPhone, 0, 1)` and `AlignInContainer: =AlignInContainer.Stretch`; fixed children set `FillPortions: =0`, `Width`, and `AlignInContainer: =AlignInContainer.Stretch` (so they go full-width when stacked). The container sets `LayoutAlignItems: =If(IsPhone, LayoutAlignItems.Stretch, LayoutAlignItems.Center)` and `Height: =If(IsPhone, <stacked height>, <row height>)`.
5. Every Vertical container sets `LayoutAlignItems: =LayoutAlignItems.Stretch` so `ModernText` children span the width — then **remove `Width`** from those text controls and set `AutoHeight: =true`.
6. Any container that is a `FillPortions: =0` child of a Vertical parent **must** have an explicit `Height` formula (otherwise it renders at the 225 default). Use P3 for content-driven heights.
7. Buttons: `FillPortions: =0`, `Height: =ControlMinTouch` (header/nav use 40–44), `Size: =FontSizeBody`, `Width` = `Len(Text) * 9 + SpaceLg * 2` (+24 with icon) or a fixed value ≥ that, and `LayoutMinWidth` equal to `Width`. In stacked (phone) action bars use `AlignInContainer: =AlignInContainer.Stretch` so the button spans the width.
8. Galleries as AutoLayout children: `FillPortions: =0`, `LayoutMinHeight: =0`, `Height` from item count (`=If(Self.AllItemsCount = 0, 0, Self.AllItemsCount * (<TemplateSize> + Self.TemplatePadding * 2))`, capped with `Min(...)` where the spec says), `Width: =Parent.Width`. Gallery `OnSelect` was **not** returned by `describe_control` → do not use it; put selection/navigation on a `ModernButton` inside the template.

### P3 — Content-driven container height

A container's `Height` may reference its own children's rendered heights (AutoHeight text reports `Height`). Pattern:

```yaml
Height: =lblSectionHeading.Height + SpaceSm + lblBody.Height + PaddingTop + PaddingBottom   # literal numbers for paddings
```
No cycle exists as long as children do not reference `Parent.Height`. Use this for every text-heavy section (request description, validation blocks, banners, two-column detail cards). For two side-by-side auto-height cards in a Horizontal parent: parent `LayoutAlignItems: =If(IsPhone, LayoutAlignItems.Stretch, LayoutAlignItems.Start)`, each card has its own P3 `Height`, parent `Height: =If(IsPhone, cardA.Height + SpaceMd + cardB.Height, Max(cardA.Height, cardB.Height))`.

### P4 — Wrap-row column widths

For N equal columns in a `LayoutWrap: =true` Horizontal container with `LayoutGap: =SpaceMd`:

| Columns on desktop | Child `Width` formula | Rows formula (for container `Height`) |
|---|---|---|
| 4 | `=If(IsPhone, Parent.Width, If(IsTablet, (Parent.Width - SpaceMd) / 2 - 1, (Parent.Width - SpaceMd * 3) / 4 - 1))` | `If(IsPhone, 4, If(IsTablet, 2, 1))` |
| 3 | `=If(IsPhone, Parent.Width, If(IsTablet, (Parent.Width - SpaceMd) / 2 - 1, (Parent.Width - SpaceMd * 2) / 3 - 1))` | `If(IsPhone, 3, If(IsTablet, 2, 1))` |
| 2 | `=If(IsPhone, Parent.Width, (Parent.Width - SpaceMd) / 2 - 1)` | `If(IsPhone, 2, 1)` |

Container `Height: =<rows> * <childHeight> + (<rows> - 1) * SpaceMd` (+ container padding). `Parent.Width` here is the wrap container's inner width (its own padding already excluded by the container).

### P5 — Tile (replaces every KPI / summary `ModernCard`)

```yaml
- cntTileTotal:
    Control: GroupContainer
    Variant: AutoLayout
    Properties:
      BorderColor: =ColorNeutralStroke
      BorderStyle: =BorderStyle.Solid
      BorderThickness: =1
      DropShadow: =DropShadow.None
      Fill: =ColorSurface
      FillPortions: =0
      Height: =TileHeight
      LayoutAlignItems: =LayoutAlignItems.Stretch
      LayoutDirection: =LayoutDirection.Vertical
      LayoutGap: =SpaceXs
      LayoutMinHeight: =TileHeight
      LayoutMinWidth: =200
      PaddingBottom: =SpaceMd
      PaddingLeft: =SpaceMd
      PaddingRight: =SpaceMd
      PaddingTop: =SpaceMd
      RadiusBottomLeft: =RadiusSm
      RadiusBottomRight: =RadiusSm
      RadiusTopLeft: =RadiusSm
      RadiusTopRight: =RadiusSm
      Width: =<P4 width formula>
    Children:
      - cntTileTotalHead:
          Control: GroupContainer
          Variant: AutoLayout
          Properties:
            FillPortions: =0
            Height: =20
            LayoutAlignItems: =LayoutAlignItems.Center
            LayoutDirection: =LayoutDirection.Horizontal
            LayoutGap: =SpaceSm
            LayoutMinHeight: =20
          Children:
            - icoTileTotal:
                Control: ModernIcon
                Properties:
                  AccessibleLabel: ="Total requests"
                  FillPortions: =0
                  Height: =20
                  Icon: ="Document"
                  IconColor: =ColorTextSecondary
                  LayoutMinHeight: =20
                  LayoutMinWidth: =20
                  Width: =20
            - lblTileTotalLabel:
                Control: ModernText
                Properties:
                  AccessibleLabel: =Self.Text
                  AutoHeight: =true
                  Color: =ColorTextSecondary
                  FillPortions: =1
                  LayoutMinWidth: =0
                  PaddingBottom: =0
                  PaddingLeft: =0
                  PaddingRight: =0
                  PaddingTop: =0
                  Size: =FontSizeCaption
                  Text: ="Total requests"
      - lblTileTotalValue:
          Control: ModernText
          Properties:
            AccessibleLabel: ="Total requests: " & Self.Text
            AutoHeight: =true
            Color: =ColorTextPrimary
            FontWeight: =FontWeight.Semibold
            PaddingBottom: =0
            PaddingLeft: =0
            PaddingRight: =0
            PaddingTop: =0
            Size: =FontSizeKpi
            Text: =Text(CountRows('FOIA Pilot Requests'))
      - lblTileTotalNote:
          Control: ModernText
          Properties:
            AccessibleLabel: =Self.Text
            AutoHeight: =true
            Color: =ColorTextSecondary
            PaddingBottom: =0
            PaddingLeft: =0
            PaddingRight: =0
            PaddingTop: =0
            Size: =FontSizeCaption
            Text: ="All submitted requests"
```
Semantic tiles (due soon / closed / remaining) set `IconColor` **and** `lblTileXxxValue.Color` to `ColorWarning`/`ColorSuccess` and use a matching icon (`Warning`, `CheckmarkCircle`) — icon + color + label text together. A tile whose value is a status uses a `cmpStatusBadge` instance (Height 28, Width 128, `AlignInContainer: =AlignInContainer.Start`) in place of `lblTileXxxValue`.

### P6 — Gallery Row (replaces `ModernCard` rows inside galleries)

Template child is one Horizontal container filling the template; text column flexes; a trailing `ModernButton` carries the action (gallery `OnSelect` is not used — see P2.8):

```yaml
- cntRequestRow:
    Control: GroupContainer
    Variant: AutoLayout
    Properties:
      BorderColor: =ColorNeutralStroke
      BorderStyle: =BorderStyle.Solid
      BorderThickness: =1
      DropShadow: =DropShadow.None
      Fill: =ColorSurface
      Height: =Parent.TemplateHeight
      LayoutAlignItems: =LayoutAlignItems.Center
      LayoutDirection: =LayoutDirection.Horizontal
      LayoutGap: =SpaceMd
      PaddingBottom: =SpaceSm
      PaddingLeft: =SpaceMd
      PaddingRight: =SpaceSm
      PaddingTop: =SpaceSm
      RadiusBottomLeft: =RadiusSm
      RadiusBottomRight: =RadiusSm
      RadiusTopLeft: =RadiusSm
      RadiusTopRight: =RadiusSm
      Width: =Parent.TemplateWidth
      X: =0
      Y: =0
    Children:
      - cntRequestRowText:
          Control: GroupContainer
          Variant: AutoLayout
          Properties:
            FillPortions: =1
            LayoutAlignItems: =LayoutAlignItems.Stretch
            LayoutDirection: =LayoutDirection.Vertical
            LayoutGap: =0
            LayoutJustifyContent: =LayoutJustifyContent.Center
            LayoutMinHeight: =0
            LayoutMinWidth: =120
          Children:
            - lblRequestRowTitle:   # ModernText, AutoHeight, FontSizeBody, Semibold, ColorTextPrimary, Padding 0
            - lblRequestRowMeta:    # ModernText, AutoHeight, FontSizeCaption, ColorTextSecondary, Padding 0
      - cmpRequestRowStatus:      # cmpStatusBadge instance (Width 112, Height 24, Visible: =!IsPhone)
      - btnRequestRowOpen:
          Control: ModernButton
          Properties:
            AccessibleLabel: ="Open request " & ThisItem.Title
            Appearance: =ButtonAppearance.Subtle
            FillPortions: =0
            Height: =ControlMinTouch
            Icon: ="ChevronRight"
            Layout: =ButtonLayout.IconOnly
            LayoutMinWidth: =ControlMinTouch
            OnSelect: |-
              =Set(gblSelectedRequest, ThisItem);
              Navigate(RequestDetail, ScreenTransition.Fade)
            Size: =FontSizeBody
            Text: ="Open"
            Tooltip: ="Open request"
            Width: =ControlMinTouch
```

### P7 — Form field group (NewRequest, DepartmentWork, ResponseCloseout)

Vertical container, `FillPortions: =0`, `Height: =FieldHeight`, `LayoutMinHeight: =FieldHeight`, `LayoutMinWidth: =200`, `LayoutAlignItems: =LayoutAlignItems.Stretch`, `LayoutGap: =6`, `Width` from P4. Label: `ModernText` `AutoHeight: =true`, `Size: =FontSizeCaption`, `Color: =ColorTextSecondary`, `PaddingTop: =0`, `PaddingBottom: =0`, no `Width`. Input: `Height: =InputHeight`, no `Width` (stretches). Multiline inputs keep their taller `Height` and the group `Height` = label (22) + 6 + input height.

### P8 — Section card

Vertical `GroupContainer` with the Fluent surface styling (Fill `ColorSurface`, 1 px `ColorNeutralStroke`, radius `RadiusSm`, `DropShadow.None`, padding `SpaceMd`), `LayoutAlignItems: =LayoutAlignItems.Stretch`, `FillPortions: =0`, `Height` by P3 (sum of children) or an explicit per-breakpoint formula when children are fixed-height inputs.

## Per-Screen Edit Specifications

### Components (New)
- **File:** Components.pa.yaml
- **Purpose:** Hosts the three component definitions exactly as specified above (single `ComponentDefinitions:` root, order `cmpAppHeader`, `cmpSideNav`, `cmpStatusBadge`). Write out all five `cmpSideNav` nav buttons in full.
- **Layout:** each component's first child is a full-size `GroupContainer` (`X/Y 0`, `Width/Height = Parent`).
- **Data Binding:** none. No data sources, no global variables.
- **Navigation:** `cmpSideNav` buttons navigate with `ScreenTransition.None`; `cmpAppHeader` only raises events.
- **State:** none.

### App (Existing)
- **File:** App.pa.yaml
- **Current State:** navy/gold palette + breakpoints/spacing tokens.
- **Changes Required:** 1) Replace `Formulas` with the Fluent token block verbatim. 2) Keep `StartScreen: =Dashboard`, `Theme: =PowerAppsTheme`. 3) Nothing else.

### Dashboard (Existing)
- **File:** Dashboard.pa.yaml
- **Current State:** `cntDashboardRoot` scroll root → navy `cntDashboardHeader` (title, subtitle, `btnNewRequest`, `btnQueueRefresh`), `lblQueueHeading`, `cntQueueCards` (4 `ModernCard`), `cntQueueFilters` (search + 2 dropdowns), `lblRecentRequests`, `cntQueueBody` (state labels + `galRecentRequests` with `ModernCard` rows).
- **Changes Required:**
  1. Apply P1. Header instance: `Title ="FOIA requests"`, `Subtitle ="Village of Flossmoor · Request queue and response readiness"`, `ShowBack =false`, `PrimaryLabel ="New request"`, `PrimaryIcon ="Add"`, `OnPrimary =Navigate(NewRequest, ScreenTransition.Fade)`, `SecondaryLabel ="Refresh"`, `SecondaryIcon ="ArrowClockwise"`, `OnSecondary` = the old `btnQueueRefresh.OnSelect` body (`Set(gblIsLoading, true); Set(gblLoadError, false); Refresh('FOIA Pilot Requests'); Set(gblIsLoading, false)`), `OnBack =false`. Nav instances `ActiveScreen ="Dashboard"`.
  2. `lblQueueHeading`, `lblRecentRequests`: remove `Width`, keep `AutoHeight`, `Size: =FontSizeSection`, `Color: =ColorTextPrimary`, `PaddingLeft: =0`.
  3. `cntQueueCards`: `LayoutWrap: =true`, `LayoutGap: =SpaceMd`, `FillPortions: =0`, `Height: =If(IsPhone, 4, If(IsTablet, 2, 1)) * TileHeight + (If(IsPhone, 4, If(IsTablet, 2, 1)) - 1) * SpaceMd`, `LayoutMinHeight: =TileHeight`. Replace the four `ModernCard`s with P5 tiles (4-column P4 width):
     - `cntTileTotal` — icon `Document` (`ColorTextSecondary`), label "Total requests", value `=Text(CountRows('FOIA Pilot Requests'))`, note "All submitted requests".
     - `cntTileOpen` — icon `Clock` (`ColorInfo`), label "Open", value `=Text(CountRows(Filter('FOIA Pilot Requests', OverallStatus.Value <> "Closed")))` (value color `ColorInfo`), note "Open / in progress".
     - `cntTileDueSoon` — icon `Warning` (`ColorWarning`), label "Due within 7 days", value `=Text(CountRows(Filter('FOIA Pilot Requests', DueDateConfirmed = true && DueDate <= DateAdd(Today(), 7, TimeUnit.Days))))` (value color `ColorWarning`), note "Confirmed working due dates only".
     - `cntTileClosed` — icon `CheckmarkCircle` (`ColorSuccess`), label "Closed", value `=Text(CountRows(Filter('FOIA Pilot Requests', OverallStatus.Value = "Closed")))` (value color `ColorSuccess`), note "Closed requests".
  4. `cntQueueFilters`: convert to P2.4 direction-switching (no `LayoutWrap`): Fluent surface styling (P8), `Height: =If(IsPhone, InputHeight * 3 + SpaceSm * 2 + SpaceMd * 2, InputHeight + SpaceMd * 2)`, padding `SpaceMd`, `LayoutGap: =If(IsPhone, SpaceSm, SpaceMd)`. `txtQueueSearch`: `FillPortions: =If(IsPhone, 0, 1)`, `AlignInContainer: =AlignInContainer.Stretch`, `LayoutMinWidth: =200`, `Height: =InputHeight`, remove `Width`. `cmbStatusFilter`: `FillPortions: =0`, `Width: =180`, `LayoutMinWidth: =180`, `AlignInContainer: =AlignInContainer.Stretch`, `Height: =InputHeight`. `cmbDepartmentFilter`: same with `Width: =220`. Keep `Items`/`Default`/`OnChange` formulas unchanged.
  5. Remove the `cntQueueBody` wrapper; make `lblQueueLoading`, `lblQueueError`, `lblQueuePermission`, `lblQueueEmpty`, `galRecentRequests` direct children of `cntDashboardContent` (same order). State labels: remove `Width`, keep `AutoHeight`, `Align: =Align.Left`, `Size: =FontSizeBody`. Keep all `Visible` formulas (they reference `galRecentRequests.AllItemsCount`).
  6. `galRecentRequests`: keep `Items`, `Visible`, `AccessibleLabel`, `LoadingSpinner`, `TabIndex`; set `FillPortions: =0`, `LayoutMinHeight: =0`, `Width: =Parent.Width`, `TemplatePadding: =SpaceXs`, `TemplateSize: =If(IsPhone, 92, 76)`, `Height: =If(Self.AllItemsCount = 0, 0, Self.AllItemsCount * (If(IsPhone, 92, 76) + SpaceXs * 2))`, `ShowScrollbar: =false`. Replace `cardRequestRow` with P6 row: `lblRequestRowTitle.Text =ThisItem.Title`; `lblRequestRowMeta.Text =ThisItem.RequesterFirstName & " " & ThisItem.RequesterLastName & " · Received " & If(IsBlank(ThisItem.ReceivedDate), "—", Text(ThisItem.ReceivedDate, "[$-en-US]mmm d, yyyy")) & If(IsPhone, " · " & Coalesce(ThisItem.OverallStatus.Value, "Not set"), "")`; `cmpRequestRowStatus.Status =Coalesce(ThisItem.OverallStatus.Value, "Not set")`, `Visible: =!IsPhone`; `btnRequestRowOpen.OnSelect` = `Set(gblSelectedRequest, ThisItem); Navigate(RequestDetail, ScreenTransition.Fade)`.
- **Controls to Add:** `cmpDashboardHeader`, `cmpDashboardNavRail`, `cmpDashboardNavBottom`, `cntDashboardShell/Body/Content`, 4 tiles (P5), row controls (P6).
- **Controls to Remove:** `cntDashboardRoot` (replaced by shell), `cntDashboardHeader`, `lblDashboardTitle`, `lblDashboardSubtitle`, `btnNewRequest`, `btnQueueRefresh`, `cardTotalRequests`, `cardOpenRequests`, `cardDueSoon`, `cardClosedRequests`, `cntQueueBody`, `cardRequestRow`.
- **Properties to Update:** screen `Fill → =ColorNeutralBg`, `LoadingSpinnerColor → =ColorBrand`; all listed above. `OnVisible` unchanged.

### NewRequest (Existing)
- **File:** NewRequest.pa.yaml
- **Current State:** `cntRequestRoot` scroll root → navy `cntRequestHeader` (title, subtitle, `btnRequestBack`), `cntRequestFormShell` (hidden `frmRequestIntake`, 3 section headings, 4 wrap rows of field groups, message labels), `cntRequestActions` (Cancel / Save).
- **Changes Required:**
  1. Apply P1 **with one variation**: `cntNewRequestContent` has **no** `LayoutOverflowY` and `LayoutGap: =SpaceMd`; `cntRequestFormShell` becomes the scroller (`FillPortions: =1`, `LayoutMinHeight: =0`, `LayoutOverflowY: =LayoutOverflow.Scroll`, P8 styling, `LayoutAlignItems: =LayoutAlignItems.Stretch`, `LayoutGap: =SpaceMd`, padding `SpaceLg` desktop / `SpaceMd` phone via `=If(IsPhone, SpaceMd, SpaceLg)`), and `cntRequestActions` stays pinned below it (`FillPortions: =0`). Header instance: `Title ="New request"`, `Subtitle ="Manual intake · confirm the working due date before saving"`, `ShowBack =true`, `OnBack =Navigate(Dashboard, ScreenTransition.None)`, `PrimaryLabel =""`, `SecondaryLabel =""`, `OnPrimary =false`, `OnSecondary =false`. Nav `ActiveScreen ="NewRequest"`.
  2. Remove `frmRequestIntake` (unused hidden Form; save is via `Patch`). Nothing else references it.
  3. Section headings `lblRequesterSection`, `lblRequestSection`, `lblDatesSection`: `Color: =ColorTextPrimary`, `Size: =FontSizeSection`, `AutoHeight: =true`, `PaddingLeft: =0`, remove `Width`.
  4. Field groups → P7. `cntRequesterFields` (4 fields) and `cntRoutingFields` (4 fields): `LayoutWrap: =true`, `LayoutGap: =SpaceMd`, `FillPortions: =0`, `LayoutAlignItems: =LayoutAlignItems.Start`, child `Width` = P4 4-col, container `Height: =If(IsPhone, 4, If(IsTablet, 2, 1)) * FieldHeight + (If(IsPhone, 4, If(IsTablet, 2, 1)) - 1) * SpaceMd`. `cntRequestDetails` (description): `FillPortions: =0`, `Height: =22 + 6 + 120`, `LayoutAlignItems: =LayoutAlignItems.Stretch`; `txtRequestDescription` keeps `Height: =120`, remove `Width`. `cntDateFields` (3 groups: received, due, confirm): P4 3-col widths, `Height: =If(IsPhone, 3, If(IsTablet, 2, 1)) * 80 + (If(IsPhone, 3, If(IsTablet, 2, 1)) - 1) * SpaceMd`; `cntDueDateConfirm` `Height: =80` (checkbox 44 + help caption AutoHeight), other two `Height: =FieldHeight`. `cntOptionalFlags`: direction-switching P2.4, `Height: =If(IsPhone, InputHeight * 2 + SpaceSm, InputHeight)`, checkboxes `FillPortions: =0`, `Width: =260`, `LayoutMinWidth: =260`, `AlignInContainer: =AlignInContainer.Stretch`.
  5. All field labels (`lblRequesterFirstName`, `lblRequesterLastName`, `lblRequesterEmail`, `lblRequesterPhone`, `lblRequestDescription`, `lblPrimaryDepartment`, `lblIntakeMethod`, `lblRequestRoute`, `lblDeliveryFormat`, `lblReceivedDate`, `lblDueDate`, `lblDueDateHelp`) → add `AutoHeight: =true`, `PaddingTop: =0`, `PaddingBottom: =0`, `PaddingLeft: =0`, remove `Width`. All inputs (`txt*`, `cmb*`, `dat*`, `chk*`) → `Height: =InputHeight` (multiline description keeps 120), remove `Width` (parent stretches).
  6. Message labels `lblRequestValidation`, `lblRequestError`, `lblRequestPermission`, `lblRequestSuccess`: add `AutoHeight: =true`, remove `Width`, `Size: =FontSizeBody`. Keep `Text`/`Visible` formulas unchanged.
  7. `cntRequestActions`: P2.4 direction-switching, `LayoutJustifyContent: =LayoutJustifyContent.End`, P8 styling, `Height: =If(IsPhone, ControlMinTouch * 2 + SpaceSm + SpaceMd * 2, ControlMinTouch + SpaceMd * 2)`, padding `SpaceMd`. `btnCancelRequest`: `Appearance: =ButtonAppearance.Secondary`, remove `Color`, `Width: =120`, `LayoutMinWidth: =120`, `Height: =ControlMinTouch`, `Size: =FontSizeBody`, `AlignInContainer: =AlignInContainer.Stretch`. `btnSaveRequest`: `BasePaletteColor: =ColorBrand`, `Width: =150`, `LayoutMinWidth: =150`, `Height: =ControlMinTouch`, `Size: =FontSizeBody`, `AlignInContainer: =AlignInContainer.Stretch`; keep `DisplayMode` and the full `OnSelect` `Patch` **unchanged** (scope guard).
- **Controls to Add:** shell + header/nav instances.
- **Controls to Remove:** `cntRequestRoot`, `cntRequestHeader`, `lblRequestTitle`, `lblRequestSubtitle`, `btnRequestBack`, `frmRequestIntake`.
- **Properties to Update:** screen `Fill → =ColorNeutralBg`, `LoadingSpinnerColor → =ColorBrand`; `OnVisible` unchanged except delete nothing (it never referenced the form).

### RequestDetail (Existing)
- **File:** RequestDetail.pa.yaml
- **Current State:** `cntRequestDetailRoot` → navy header (`btnBackDashboard`, identity labels), `cntRequestDetailEmpty`, `cntRequestDetailContent` (`cntRequestSummaryCards` 4 `ModernCard`, `cntRequestStageStatus` badges + progress, `cntRequestInformationColumns` 2 columns, `lblAssignmentsHeading`, `galAssignments`, `cntRequestExtensions`, `cntRequestDetailActions`).
- **Changes Required:**
  1. Apply P1. Header: `Title =If(IsBlank(gblSelectedRequest), "Request detail", Coalesce(gblSelectedRequest.Title, "Request detail"))`, `Subtitle =If(IsBlank(gblSelectedRequest), "No request selected", "Request ID " & Text(gblSelectedRequest.ID))`, `ShowBack =true`, `OnBack =Navigate(Dashboard, ScreenTransition.None)`, no primary/secondary. Nav `ActiveScreen ="RequestDetail"`.
  2. `cntRequestDetailEmpty`: `FillPortions: =0`, `Height: =180`, `LayoutAlignItems: =LayoutAlignItems.Center`; `lblRequestDetailEmpty` `AutoHeight: =true`, remove fixed `Height`/`Width`; `btnRequestDetailEmptyBack` `BasePaletteColor: =ColorBrand`, `Width/LayoutMinWidth: =180`, `Height: =ControlMinTouch`, `Size: =FontSizeBody`.
  3. `cntRequestDetailContent`: `FillPortions: =0`, `LayoutAlignItems: =LayoutAlignItems.Stretch`, `Height: =cntRequestSummaryCards.Height + cntRequestStageStatus.Height + cntRequestInformationColumns.Height + lblAssignmentsHeading.Height + galAssignments.Height + cntRequestExtensions.Height + cntRequestDetailActions.Height + SpaceMd * 6` (P3), `LayoutMinHeight: =0`.
  4. `cntRequestSummaryCards` → P4/P5 4 tiles, `LayoutWrap: =true`, `Height` as Dashboard tiles: `cntTileStage` (icon `Flag`, label "Current stage", value `=Coalesce(gblSelectedRequest.RequestRoute.Value, "Intake")` at `Size: =FontSizeSection`), `cntTileStatus` (icon `Info`, label "Status", value = `cmpStatusBadge` instance `Status =Coalesce(gblSelectedRequest.OverallStatus.Value, "Not set")`), `cntTileDueDate` (icon `Calendar`, label "Working due date", value `=If(IsBlank(gblSelectedRequest.DueDate), "Not entered", Text(gblSelectedRequest.DueDate, "[$-en-US]mmm d, yyyy"))` at `FontSizeSection`, note `=If(gblSelectedRequest.DueDateConfirmed, "Confirmed by staff", "Confirmation required")` with `Color: =If(gblSelectedRequest.DueDateConfirmed, ColorSuccess, ColorWarning)` and tile icon `=If(gblSelectedRequest.DueDateConfirmed, "CheckmarkCircle", "Warning")`), `cntTileRecords` (icon `Document`, label "Records", value `=Text(CountRows(Filter('FOIA Pilot Records', Request.Id = gblSelectedRequest.ID)))`, note "Source records linked").
  5. `cntRequestStageStatus`: P8 styling, `Height: =cntRequestStageStatusHeader.Height + SpaceSm + 16 + SpaceMd * 2`. `cntRequestStageStatusHeader`: `LayoutWrap: =true`, `FillPortions: =0`, `Height: =If(IsPhone, 28 * 2 + SpaceSm, 28)`, `LayoutMinHeight: =28`; children all `FillPortions: =0`: `lblRequestStage` `Width: =140`, `AutoHeight`, `Size: =FontSizeSection`; `bdgRequestStage` keep `ModernBadge` (`Intent Informative`, add `Icon: ="Flag"`, `Shape: =BadgeShape.Rounded`, `Size: =FontSizeCaption`, `Width: =160`, `Height: =28`); replace `bdgRequestOverallStatus` with `cmpStatusBadge` instance (`Width: =128`, `Height: =28`). `pgbRequestStageProgress`: `FillColor: =ColorBrand`, `TrackColor: =ColorNeutralStroke`, remove `Width` (stretch), keep `Value`/`Max`.
  6. `cntRequestInformationColumns`: P3 two-card pattern — `LayoutDirection: =If(IsPhone, LayoutDirection.Vertical, LayoutDirection.Horizontal)`, no `LayoutWrap`, `LayoutAlignItems: =If(IsPhone, LayoutAlignItems.Stretch, LayoutAlignItems.Start)`, `FillPortions: =0`, `Height: =If(IsPhone, cntRequesterDetails.Height + SpaceMd + cntDetailRequestDetails.Height, Max(cntRequesterDetails.Height, cntDetailRequestDetails.Height))`. Each card: P8 styling, `FillPortions: =If(IsPhone, 0, 1)`, `LayoutMinWidth: =200`, `AlignInContainer: =AlignInContainer.Stretch`, remove `Width`, `Height` = sum of its label heights + `SpaceSm * (n-1)` + `SpaceMd * 2`. Headings `lblRequesterDetailsHeading`/`lblRequestDetailsHeading`: `Color: =ColorTextPrimary`, `Size: =FontSizeSection`. All detail labels: keep `AutoHeight`, remove fixed `Height` and `Width`, `Size: =FontSizeBody`, `PaddingLeft: =0`.
  7. `lblAssignmentsHeading`: `Color: =ColorTextPrimary`, `Size: =FontSizeSection`, remove `Height`/`Width`.
  8. `galAssignments`: `FillPortions: =0`, `LayoutMinHeight: =0`, `TemplateSize: =If(IsPhone, 84, 68)`, `TemplatePadding: =SpaceXs`, `Height: =If(Self.AllItemsCount = 0, 0, Min(4, Self.AllItemsCount) * (If(IsPhone, 84, 68) + SpaceXs * 2))`, `ShowScrollbar: =true`. Replace `cntAssignmentRow` children with P6: text column (`lblAssignmentDepartment` title `=Coalesce(ThisItem.Department.Value, "Department")`; meta `="Due: " & If(IsBlank(ThisItem.AssignmentDueDate), "Not set", Text(ThisItem.AssignmentDueDate, "[$-en-US]mmm d, yyyy"))`), `cmpAssignmentStatus` (`Status =Coalesce(ThisItem.AssignmentStatus.Value, "Not set")`, Width 112), `btnAssignmentOpen` (`Icon "ChevronRight"`, `OnSelect =Set(gblSelectedAssignment, ThisItem); Navigate(DepartmentWork, ScreenTransition.None)`, `AccessibleLabel ="Open department work for " & Coalesce(ThisItem.Department.Value, "assignment")`). Remove `bdgAssignmentStatus`, `lblAssignmentDueDate` (merged into meta).
  9. Add `lblAssignmentsEmpty` (`ModernText`, `AutoHeight`, caption color, `Text ="No active department assignments for this request."`, `Visible =galAssignments.AllItemsCount = 0 && !IsBlank(gblSelectedRequest)`) directly after `galAssignments`; include its `Height` in step 3's sum.
  10. `cntRequestExtensions`: P8 styling, `Height: =lblExtensionHeading.Height + lblExtensionExplanation.Height + cntExtensionInputs.Height + lblExtensionValidation.Height + ControlMinTouch + SpaceSm * 4 + SpaceMd * 2`. Heading `Color: =ColorTextPrimary`, `Size: =FontSizeSection`. `cntExtensionInputs`: P2.4 direction-switching, `FillPortions: =0`, `Height: =If(IsPhone, InputHeight * 3 + SpaceSm * 2, InputHeight)`, `LayoutGap: =If(IsPhone, SpaceSm, SpaceMd)`; `datExtensionDate` `FillPortions: =0`, `Width: =200`, `LayoutMinWidth: =200`, `Height: =InputHeight`, `AlignInContainer: =AlignInContainer.Stretch`; `txtExtensionNotes` `FillPortions: =If(IsPhone, 0, 1)`, `LayoutMinWidth: =200`, `Height: =InputHeight`, remove `Width`, `AlignInContainer: =AlignInContainer.Stretch`; `chkExtensionConfirmed` `FillPortions: =0`, `Width: =240`, `LayoutMinWidth: =240`, `Height: =InputHeight`, `AlignInContainer: =AlignInContainer.Stretch`. `btnReviewExtension`: `Appearance: =ButtonAppearance.Secondary`, remove `BasePaletteColor`, `Width/LayoutMinWidth: =190`, `Height: =ControlMinTouch`, `Size: =FontSizeBody`, `AlignInContainer: =AlignInContainer.Start`; keep `DisplayMode`/`OnSelect` unchanged (no due-date change).
  11. `cntRequestDetailActions`: P2.4 direction-switching, `FillPortions: =0`, `Height: =If(IsPhone, ControlMinTouch * 2 + SpaceSm, ControlMinTouch)`, `LayoutJustifyContent: =LayoutJustifyContent.End`. `btnDepartmentWork`: `Appearance: =ButtonAppearance.Secondary`, remove `BasePaletteColor`, `Width/LayoutMinWidth: =210`, `Height: =ControlMinTouch`, `Size: =FontSizeBody`, `AlignInContainer: =AlignInContainer.Stretch`, `DisplayMode: =If(IsBlank(gblSelectedRequest) || galAssignments.AllItemsCount = 0, DisplayMode.Disabled, DisplayMode.Edit)`, `OnSelect: =Set(gblSelectedAssignment, If(IsBlank(galAssignments.Selected), First(galAssignments.AllItems), galAssignments.Selected)); Navigate(DepartmentWork, ScreenTransition.None)`. `btnResponseCloseout`: `BasePaletteColor: =ColorBrand`, `Width/LayoutMinWidth: =210`, `Height: =ControlMinTouch`, `Size: =FontSizeBody`, `AlignInContainer: =AlignInContainer.Stretch`; keep `DisplayMode`/`OnSelect`.
- **Controls to Add:** shell + header/nav instances, 4 tiles, `cmpStatusBadge` instances (tile, stage row, assignment rows), `btnAssignmentOpen`, `lblAssignmentsEmpty`.
- **Controls to Remove:** `cntRequestDetailRoot`, `cntRequestDetailHeader`, `btnBackDashboard`, `cntRequestDetailIdentity`, `lblRequestDetailTitle`, `lblRequestDetailId`, `crdRequestStage`, `crdRequestStatus`, `crdRequestDueDate`, `crdRequestRecords`, `bdgRequestOverallStatus`, `bdgAssignmentStatus`, `lblAssignmentDueDate`.
- **Properties to Update:** screen `Fill → =ColorNeutralBg`, `LoadingSpinnerColor → =ColorBrand`; everything listed above. `OnVisible` unchanged.

### DepartmentWork (Existing)
- **File:** DepartmentWork.pa.yaml
- **Current State:** `cntDepartmentWorkRoot` → navy header (title, request label, `btnBackRequestDetail`), `lblDepartmentWorkState`, `cntDepartmentWorkSelector` (heading + horizontal `galDepartmentAssignments` of `ModernCard`), `cntDepartmentWorkEditor` (title, `cntAssignmentEditorRow` dropdown/date/toggle, guidance, `txtResponseNotes`, `cntAssignmentActions` Save / Mark complete), `cntDepartmentRecords` (heading, meta, `galDepartmentRecords`).
- **Changes Required:**
  1. Apply P1. Header: `Title ="Department work"`, `Subtitle =If(IsBlank(gblSelectedRequest), "No request selected", "Request " & gblSelectedRequest.Title)`, `ShowBack =true`, `OnBack =Navigate(RequestDetail, ScreenTransition.None)`, no primary/secondary. Nav `ActiveScreen ="DepartmentWork"`.
  2. `lblDepartmentWorkState`: keep `Text`/`Visible`/`Color` formulas; remove `Width`; `Size: =FontSizeBody`; add `Fill` tint `=If(gblLoadError || gblPermissionDenied, ColorCriticalBg, If(gblSaveSuccess, ColorSuccessBg, ColorWarningBg))`, padding `SpaceSm`, radius `RadiusSm`.
  3. `cntDepartmentWorkSelector`: P8 styling (`Fill: =ColorSurface` instead of `Color.White`), `FillPortions: =0`, `Height: =lblAssignmentSelector.Height + SpaceSm + 112 + SpaceMd * 2`. `lblAssignmentSelector`: remove `Width`, `Size: =FontSizeSection`, `PaddingLeft: =0`. `galDepartmentAssignments` (Horizontal): `FillPortions: =0`, `Height: =112`, `LayoutMinHeight: =112`, remove `Width` (stretch), `Fill: =RGBA(0, 0, 0, 0)`, `TemplateSize: =If(IsPhone, 240, 272)`, `TemplatePadding: =SpaceXs`, `ShowScrollbar: =true`, `ShowNavigation: =!IsPhone`. Replace `crdDepartmentAssignment` with a P6-style card (Vertical inside, `Height: =Parent.TemplateHeight`, `Width: =Parent.TemplateWidth`): `Fill: =If(ThisItem.ID = gblSelectedAssignment.ID, ColorBrandTint, ColorSurface)`, `BorderColor: =If(ThisItem.ID = gblSelectedAssignment.ID, ColorBrand, ColorNeutralStroke)`, `BorderThickness: =1`; children: `lblAssignmentCardTitle` (`=ThisItem.Title`, Semibold, `FontSizeBody`, AutoHeight), `lblAssignmentCardDept` (`=If(IsBlank(ThisItem.Department), "Department not assigned", ThisItem.Department.Value)`, caption), a Horizontal footer row (`FillPortions: =0`, `Height: =ControlMinTouch - 8`, `LayoutMinHeight: =ControlMinTouch - 8`) with `cmpAssignmentCardStatus` (`cmpStatusBadge`, `Status =Coalesce(ThisItem.AssignmentStatus.Value, "Not set")`, Width 112, Height 24) and `btnAssignmentCardSelect` (`ModernButton`, `Appearance: =If(ThisItem.ID = gblSelectedAssignment.ID, ButtonAppearance.Primary, ButtonAppearance.Secondary)`, `BasePaletteColor: =ColorBrand`, `Icon: =If(ThisItem.ID = gblSelectedAssignment.ID, "Checkmark", "")`, `Layout: =If(ThisItem.ID = gblSelectedAssignment.ID, ButtonLayout.IconBefore, ButtonLayout.TextOnly)`, `Text: =If(ThisItem.ID = gblSelectedAssignment.ID, "Selected", "Select")`, `Width/LayoutMinWidth: =110`, `Height: =36`, `Size: =FontSizeBody`, `AccessibleLabel: ="Select assignment " & ThisItem.Title`, `OnSelect` = the old card `OnSelect` body: `Set(gblSelectedAssignment, ThisItem); Set(gblSelectedDepartment, ThisItem.Department); Set(gblSaveSuccess, false)`).
  4. `cntDepartmentWorkEditor`: P8 styling, `FillPortions: =0`, `Height: =lblAssignmentEditorTitle.Height + cntAssignmentEditorRow.Height + lblAssignmentGuidance.Height + 96 + cntAssignmentActions.Height + SpaceMd * 4 + SpaceMd * 2`, `LayoutGap: =SpaceMd`, padding `SpaceMd`. `lblAssignmentEditorTitle`: remove `Width`, `Size: =FontSizeSection`, `PaddingLeft: =0`. `cntAssignmentEditorRow`: P7 field groups wrapping each input with a caption label ("Assignment status", "Assignment due date", "Redaction required") — `LayoutWrap: =true`, 3-col P4 widths, `Height: =If(IsPhone, 3, If(IsTablet, 2, 1)) * FieldHeight + (If(IsPhone, 3, If(IsTablet, 2, 1)) - 1) * SpaceMd`; keep `cmbAssignmentStatus`/`datAssignmentDueDate`/`tglRedactionRequired` `Default`/`Items` formulas unchanged, `Height: =InputHeight`, remove `Width`. `lblAssignmentGuidance`: remove `Width`, `PaddingLeft: =0`. `txtResponseNotes`: remove `Width`, keep `Height: =96` and all formulas. `cntAssignmentActions`: P2.4 direction-switching, `FillPortions: =0`, `Height: =If(IsPhone, ControlMinTouch * 2 + SpaceSm, ControlMinTouch)`, remove `Width`; `btnSaveAssignment` `BasePaletteColor: =ColorBrand`, `Width/LayoutMinWidth: =180`, `Height: =ControlMinTouch`, `Size: =FontSizeBody`, `AlignInContainer: =AlignInContainer.Stretch`; `btnMarkComplete` `Appearance: =ButtonAppearance.Secondary`, remove `BasePaletteColor`, add `Icon: ="CheckmarkCircle"`, `Layout: =ButtonLayout.IconBefore`, `Width/LayoutMinWidth: =190`, `Height: =ControlMinTouch`, `Size: =FontSizeBody`, `AlignInContainer: =AlignInContainer.Stretch`. Keep both `DisplayMode` and `OnSelect` `Patch` formulas **unchanged**.
  5. `cntDepartmentRecords`: P8 styling, `FillPortions: =0`, `Height: =lblDepartmentRecordsTitle.Height + lblDepartmentRecordsMeta.Height + galDepartmentRecords.Height + SpaceSm * 2 + SpaceMd * 2`. Heading/meta: remove `Width`, `PaddingLeft: =0`, heading `Size: =FontSizeSection`. `galDepartmentRecords`: `FillPortions: =0`, `LayoutMinHeight: =0`, `Fill: =RGBA(0, 0, 0, 0)`, `TemplateSize: =52`, `TemplatePadding: =SpaceXs`, `Height: =If(Self.AllItemsCount = 0, 32, Min(6, Self.AllItemsCount) * (52 + SpaceXs * 2))`, remove `Width`. Row: wrap `lblDepartmentRecordTitle` + badge in a P6 Horizontal container (`cntDepartmentRecordRow`), title `FillPortions: =1`, `LayoutMinWidth: =100`, `AutoHeight`; `badgeDepartmentRecordStatus` keep `ModernBadge`, remove custom `Fill`, add `Icon: =If(ThisItem.IsFinalResponse, "CheckmarkCircle", "Document")`, `Shape: =BadgeShape.Rounded`, `Size: =FontSizeCaption`, `FillPortions: =0`, `Width: =140`, `Height: =24`. Add `lblDepartmentRecordsEmpty` (`Visible =galDepartmentRecords.AllItemsCount = 0 && !IsBlank(gblSelectedAssignment)`, caption, `Text ="No records are linked to this department yet."`), include in step 5 height.
  6. Replace every `Color.White` with `ColorSurface` and `ColorNavy`/`ColorGold` with `ColorBrand`.
- **Controls to Add:** shell + header/nav instances, assignment card controls (`lblAssignmentCardTitle`, `lblAssignmentCardDept`, `cntAssignmentCardFooter`, `cmpAssignmentCardStatus`, `btnAssignmentCardSelect`), P7 wrappers + labels for the editor row, `cntDepartmentRecordRow`, `lblDepartmentRecordsEmpty`.
- **Controls to Remove:** `cntDepartmentWorkRoot`, `cntDepartmentWorkHeader`, `lblDepartmentWorkTitle`, `lblDepartmentWorkRequest`, `btnBackRequestDetail`, `crdDepartmentAssignment`.
- **Properties to Update:** screen `Fill → =ColorNeutralBg`; everything above. `OnVisible` unchanged.

### ResponseCloseout (Existing)
- **File:** ResponseCloseout.pa.yaml
- **Current State:** `cntResponseCloseoutRoot` → navy header (title, request context, `btnBackDetail`), `cntNoSelectedRequest`, `cntCloseoutContent` (`cntReadinessCards` 3 `ModernCard`, `cntReadinessBanner`, `cntCloseoutEditor`, `cntCloseoutValidation`, `cntCloseoutActions`).
- **Changes Required:**
  1. Apply P1. Header: `Title ="Response closeout"`, `Subtitle =If(IsBlank(gblSelectedRequest), "No request selected", "Request #" & Text(gblSelectedRequest.ID) & " · " & gblSelectedRequest.Title)`, `ShowBack =true`, `OnBack =Navigate(RequestDetail, ScreenTransition.None)`, no primary/secondary. Nav `ActiveScreen ="ResponseCloseout"`.
  2. `cntNoSelectedRequest`: `FillPortions: =0`, `Height: =160`, labels `AutoHeight`, remove `Width`.
  3. `cntCloseoutContent`: `FillPortions: =0`, `LayoutMinHeight: =0`, `Height: =cntReadinessCards.Height + cntReadinessBanner.Height + cntCloseoutEditor.Height + cntCloseoutValidation.Height + cntCloseoutActions.Height + SpaceMd * 4` (P3; invisible `cntCloseoutValidation` still reports a height — acceptable).
  4. `cntReadinessCards` → 3 P5 tiles with P4 3-col widths, `LayoutWrap: =true`, `Height: =If(IsPhone, 3, If(IsTablet, 2, 1)) * TileHeight + (If(IsPhone, 3, If(IsTablet, 2, 1)) - 1) * SpaceMd`: `cntTileReadiness` (icon `Flag`, label "Response readiness", value = `cmpStatusBadge` `Status =Coalesce(gblSelectedRequest.OverallStatus.Value, "Not set")`, note `=Coalesce(gblSelectedRequest.CurrentStageNotes, "No stage notes recorded")`); `cntTileAssignments` (label "Assignments", value `=Text(CountRows(Filter('FOIA Pilot Assignments', Request.Id = gblSelectedRequest.ID && Active = true && AssignmentStatus.Value <> "Complete")))`, note "active assignment(s) remain", icon `=If(Value(lblTileAssignmentsValue.Text) = 0, "CheckmarkCircle", "Warning")`, `IconColor` and value `Color` `=If(Value(lblTileAssignmentsValue.Text) = 0, ColorSuccess, ColorWarning)`); `cntTileFinalDocs` (label "Final documents", value `=Text(CountRows(Filter('FOIA Pilot Records', Request.Id = gblSelectedRequest.ID && IsFinalResponse = true)))`, note "final-response document(s) found", icon `=If(Value(lblTileFinalDocsValue.Text) > 0, "CheckmarkCircle", "Document")`, colors `=If(Value(lblTileFinalDocsValue.Text) > 0, ColorSuccess, ColorWarning)`).
  5. `cntReadinessBanner`: `FillPortions: =0`, `Fill: =If(CountRows(Filter('FOIA Pilot Assignments', Request.Id = gblSelectedRequest.ID && Active = true && AssignmentStatus.Value <> "Complete")) = 0, ColorSuccessBg, ColorWarningBg)`, `BorderColor: =ColorNeutralStroke`, `BorderThickness: =1`, radius `RadiusSm`, no `LayoutWrap`, `LayoutDirection: =If(IsPhone, LayoutDirection.Vertical, LayoutDirection.Horizontal)`, `Height: =If(IsPhone, 32 + SpaceSm + lblReadinessBanner.Height, Max(32, lblReadinessBanner.Height)) + SpaceMd * 2`. `badgeResponseStatus`: keep `ModernBadge`, remove `BasePaletteColor`/`Fill`, add `Icon: =If(<same condition>, "CheckmarkCircle", "Warning")`, `Shape: =BadgeShape.Rounded`, `Size: =FontSizeCaption`, `FillPortions: =0`, `Width/LayoutMinWidth: =170`, `Height: =32`, `AlignInContainer: =AlignInContainer.Start`. `lblReadinessBanner`: add `AutoHeight: =true`, `FillPortions: =If(IsPhone, 0, 1)`, `LayoutMinWidth: =0`, remove `Width`, `Size: =FontSizeBody`, `PaddingLeft: =0`.
  6. `cntCloseoutEditor`: P8 styling, `FillPortions: =0`, `Height: =lblCloseoutEditorHeading.Height + cntFinalDateStatusRow.Height + lblCloseoutNotes.Height + 112 + InputHeight + SpaceMd * 4 + SpaceMd * 2`. `lblCloseoutEditorHeading`: `AutoHeight`, remove `Width`, `Size: =FontSizeSection`, `PaddingLeft: =0`. `cntFinalDateStatusRow`: P2.4 direction-switching (no wrap), `LayoutAlignItems: =LayoutAlignItems.Start`, `Height: =If(IsPhone, cntFinalDate.Height + SpaceMd + cntFinalStatus.Height, Max(cntFinalDate.Height, cntFinalStatus.Height))`; `cntFinalDate` `FillPortions: =0`, `Width: =If(IsPhone, Parent.Width, 320)`, `Height: =FieldHeight`, `AlignInContainer: =AlignInContainer.Stretch`; `cntFinalStatus` `FillPortions: =If(IsPhone, 0, 1)`, `LayoutMinWidth: =240`, `Height: =22 + 6 + If(IsPhone, 120, 44)`, `AlignInContainer: =AlignInContainer.Stretch`; `radCloseoutStatus` `Layout: =If(IsPhone, Layout.Vertical, Layout.Horizontal)`, `Height: =If(IsPhone, 120, 44)`, remove `Width`; `datFinalResponseDate` `FillPortions: =0`, `Height: =InputHeight`, remove `Width`. Field labels (`lblFinalResponseDate`, `lblCloseoutStatus`, `lblCloseoutNotes`): `AutoHeight`, `Size: =FontSizeCaption`, `Color: =ColorTextSecondary`, `FontWeight: =FontWeight.Normal`, `PaddingTop/Bottom/Left: =0`, remove `Width`. `txtCloseoutNotes`: remove `Width`, keep `Height: =112` and all formulas. `chkFinalResponseDocument`: `Height: =InputHeight`, remove `Width`, keep formulas.
  7. `cntCloseoutValidation`: `FillPortions: =0`, `Fill: =If(gblSaveSuccess, ColorSuccessBg, ColorCriticalBg)`, `BorderColor: =ColorNeutralStroke`, `BorderThickness: =1`, radius `RadiusSm`, `Height: =lblCloseoutValidation.Height + SpaceXs + lblCloseoutValidationDetail.Height + SpaceMd * 2`; `lblCloseoutValidation` add `AutoHeight: =true`, remove `Width`, `Size: =FontSizeBody`, `PaddingLeft: =0`; `lblCloseoutValidationDetail` remove `Width`, `PaddingLeft: =0`. Keep `Visible` and `Text` formulas unchanged.
  8. `cntCloseoutActions`: `FillPortions: =0`, `Height: =If(IsPhone, ControlMinTouch * 2 + SpaceSm, ControlMinTouch)`, `LayoutAlignItems: =If(IsPhone, LayoutAlignItems.Stretch, LayoutAlignItems.Center)`. `btnValidateCloseout`: `Appearance: =ButtonAppearance.Secondary`, remove `BasePaletteColor`, `Width/LayoutMinWidth: =170`, `Height: =ControlMinTouch`, `Size: =FontSizeBody`, `AlignInContainer: =AlignInContainer.Stretch`. `btnCloseoutRequest`: `Appearance: =ButtonAppearance.Primary`, `BasePaletteColor: =ColorBrand`, add `Icon: ="CheckmarkCircle"`, `Layout: =ButtonLayout.IconBefore`, `Width/LayoutMinWidth: =190`, `Height: =ControlMinTouch`, `Size: =FontSizeBody`, `AlignInContainer: =AlignInContainer.Stretch`. Keep both `DisplayMode`/`OnSelect` formulas **unchanged** (the `IfError(Patch(...))` block).
- **Controls to Add:** shell + header/nav instances, 3 tiles, `cmpStatusBadge` instance in the readiness tile.
- **Controls to Remove:** `cntResponseCloseoutRoot`, `cntCloseoutHeader`, `lblResponseCloseoutTitle`, `lblCloseoutRequestContext`, `btnBackDetail`, `cardRequestStatus`, `cardAssignmentStatus`, `cardFinalDocuments`.
- **Properties to Update:** screen `Fill → =ColorNeutralBg`, `LoadingSpinnerColor → =ColorBrand`; everything above. `OnVisible` unchanged.

### _EditorState (Existing, optional)
- **File:** _EditorState.pa.yaml
- **Changes Required:** add `ComponentDefinitionsOrder:` with `cmpAppHeader`, `cmpSideNav`, `cmpStatusBadge` under `EditorState`. Skip if the compiler rejects the key.

## Control Definitions (describe_control output, verbatim)

Only properties listed here (plus those already present in the existing YAML for controls not listed) may be used. Audit performed 2026-10-17 against the live session.

### GroupContainer
```
Part of the control family Classic.
Control: GroupContainer
Variant: <variant name> # (required) AutoLayout | GridLayout | ManualLayout

Input Properties:
  - BorderColor: Color (Default RGBA(0, 0, 0, 1))
  - BorderStyle: Enum BorderStyle — Dashed, Dotted, None, Solid (Default Solid)
  - BorderThickness: Number (Default 0)
  - ContentLanguage: Text
  - DropShadow: Enum DropShadow — Bold, ExtraBold, Light, None, Regular, Semibold, Semilight (Default Light)
  - EnableChildFocus: Boolean (Default true)
  - Fill: Color (Default RGBA(0, 0, 0, 0))
  - Height: Number (Default 225)
  - RadiusBottomLeft / RadiusBottomRight / RadiusTopLeft / RadiusTopRight: Number (Default 4)
  - Visible: Boolean (Default true)
  - Width: Number (Default 500)
  - X: Number, Y: Number

Additional input properties for variant AutoLayout:
  - LayoutAlignItems: Enum LayoutAlignItems — Center, End, Start, Stretch (Default Start)
  - LayoutDirection: Enum LayoutDirection — Horizontal, Vertical (Required; Default Horizontal)
  - LayoutGap: Number (Default 0)
  - LayoutJustifyContent: Enum LayoutJustifyContent — Center, End, SpaceBetween, Start (Default Start)
  - LayoutOverflowX / LayoutOverflowY: Enum LayoutOverflow — Hide, Scroll (Default Hide)
  - LayoutWrap: Boolean (Default false)
  - PaddingBottom / PaddingLeft / PaddingRight / PaddingTop: Number (Default 0)

Additional input properties for variant GridLayout: ChildTabPriority, LayoutGap (8), LayoutGridColumnMinWidth, LayoutGridColumns (4), LayoutGridRowMinHeight, LayoutGridRows (2), LayoutOverflowX/Y, Padding* (8)
Additional input properties for variant ManualLayout: ChildTabPriority, Padding*

Additional input properties if a child of a Vertical or Horizontal GroupContainer:
  - AlignInContainer: Enum AlignInContainer — Center, End, SetByContainer, Start, Stretch (Default Stretch)
  - FillPortions: Number (Default 1)
  - LayoutMaxHeight: Number (Default 0)
  - LayoutMaxWidth: Number (Default 0)
  - LayoutMinHeight: Number (Default 112)
  - LayoutMinWidth: Number (Default 250)

Additional input properties if a child of a Grid GroupContainer: LayoutGridColumnEnd, LayoutGridColumnStart, LayoutGridRowEnd, LayoutGridRowStart

Output Properties: BorderColor, BorderStyle, BorderThickness, ChildTabPriority, ContentLanguage, DropShadow, EnableChildFocus, Fill, Height, LayoutGridColumnMinWidth, LayoutGridColumns, LayoutGridRowMinHeight, LayoutGridRows, PaddingBottom, PaddingLeft, PaddingRight, PaddingTop, RadiusBottomLeft, RadiusBottomRight, RadiusTopLeft, RadiusTopRight, Visible, Width, X, Y
```
Note: `GroupContainer` has **no** `OnSelect`.

### ModernText
```
Part of the control family React.
Control: ModernText

Input Properties:
  - AccessibleLabel: Text
  - Align: Enum Align — Center, Justify, Left, Right (Default Left)
  - AutoHeight: Boolean (Default false)
  - BorderColor: Color
  - BorderStyle: Enum BorderStyle — Dashed, Dotted, None, Solid
  - BorderThickness: Number
  - Color: Color
  - ContentLanguage: Text
  - DisplayMode: Enum DisplayMode — Disabled, Edit, View
  - Fill: Color
  - Font: Enum Font — Arial, Courier New, Dancing Script, Georgia, Great Vibes, Lato, Lato Black, Lato Hairline, Lato Light, Open Sans, Open Sans Condensed, Patrick Hand, Segoe UI, Verdana
  - FontWeight: Enum FontWeight — Bold, Lighter, Normal, Semibold (Default Normal)
  - Height: Number (Default 50)
  - Italic: Boolean
  - OnSelect: Boolean
  - PaddingBottom / PaddingLeft / PaddingRight / PaddingTop: Number (Default 5)
  - RadiusBottomLeft / RadiusBottomRight / RadiusTopLeft / RadiusTopRight: Number
  - Size: Number (Default 26)
  - Strikethrough: Boolean
  - Text: Text (Default "Text")
  - Underline: Boolean
  - VerticalAlign: Enum VerticalAlign — Bottom, Middle, Top (Default Middle)
  - Visible: Boolean
  - Width: Number (Default 200)
  - Wrap: Boolean (Default true)
  - X, Y: Number

If child of Vertical/Horizontal GroupContainer: AlignInContainer (Default SetByContainer), FillPortions (Default 0), LayoutMaxHeight, LayoutMaxWidth, LayoutMinHeight (Default 50), LayoutMinWidth (Default 200)
If child of Grid GroupContainer: LayoutGridColumnEnd/Start, LayoutGridRowEnd/Start

Output Properties: AccessibleLabel, Align, AutoHeight, BorderColor, BorderStyle, BorderThickness, Color, ContentLanguage, DisplayMode, Fill, Font, FontWeight, Height, Italic, PaddingBottom, PaddingLeft, PaddingRight, PaddingTop, Radius*, Size, Strikethrough, Text, Underline, VerticalAlign, Visible, Width, Wrap, X, Y
```

### ModernButton
```
Part of the control family React.
Control: ModernButton

Input Properties:
  - AccessibleLabel: Text
  - Align: Enum Align — Center, Justify, Left, Right
  - Appearance: Enum ButtonAppearance — Outline, Primary, Secondary, Subtle, Transparent (Default Primary)
  - BasePaletteColor: Color
  - BorderColor: Color
  - BorderStyle: Enum BorderStyle — Dashed, Dotted, None, Solid
  - BorderThickness: Number
  - Color: Color
  - ContentLanguage: Text
  - DisplayMode: Enum DisplayMode — Disabled, Edit, View
  - Font: Enum Font (same list as ModernText)
  - FontWeight: Enum FontWeight — Bold, Lighter, Normal, Semibold
  - Height: Number (Default 64)
  - Icon: Text (Default "")
  - IconRotation: Number
  - IconStyle: Enum IconStyle — Filled, Outline (Default Outline)
  - Italic: Boolean
  - Layout: Enum ButtonLayout — IconAfter, IconBefore, IconOnly, TextOnly (Default IconBefore)
  - OnSelect: Boolean
  - PaddingBottom / PaddingLeft / PaddingRight / PaddingTop: Number
  - RadiusBottomLeft / RadiusBottomRight / RadiusTopLeft / RadiusTopRight: Number
  - Size: Number (Default 24)
  - Strikethrough: Boolean
  - Text: Text (Default "Button")
  - Tooltip: Text
  - Underline: Boolean
  - VerticalAlign: Enum VerticalAlign — Bottom, Middle, Top
  - Visible: Boolean
  - Width: Number (Default 280)
  - X, Y: Number

If child of Vertical/Horizontal GroupContainer: AlignInContainer (Default SetByContainer), FillPortions (Default 0), LayoutMaxHeight, LayoutMaxWidth, LayoutMinHeight (Default 64), LayoutMinWidth (Default 280)
If child of Grid GroupContainer: LayoutGridColumnEnd/Start, LayoutGridRowEnd/Start

Output Properties: AccessibleLabel, Align, BasePaletteColor, BorderColor, BorderStyle, BorderThickness, Color, ContentLanguage, DisplayMode, Font, FontWeight, Height, Italic, Padding*, Radius*, Size, Strikethrough, Text, Tooltip, Underline, VerticalAlign, Visible, Width, X, Y
```

### ModernIcon
```
Part of the control family React.
Control: ModernIcon

Input Properties:
  - AccessibleLabel: Text
  - BasePaletteColor: Color
  - BorderColor: Color
  - BorderStyle: Enum BorderStyle — Dashed, Dotted, None, Solid
  - BorderThickness: Number
  - ContentLanguage: Text
  - DisplayMode: Enum DisplayMode — Disabled, Edit, View
  - Fill: Color
  - Height: Number (Default 42)
  - Icon: Text (Default "Add")
  - IconColor: Color
  - IconStyle: Enum IconStyle — Filled, Outline (Default Outline)
  - OnSelect: Boolean
  - PaddingBottom / PaddingLeft / PaddingRight / PaddingTop: Number (Default 0)
  - RadiusBottomLeft / RadiusBottomRight / RadiusTopLeft / RadiusTopRight: Number
  - Rotation: Number
  - Tooltip: Text
  - Visible: Boolean
  - Width: Number (Default 42)
  - X, Y: Number

If child of Vertical/Horizontal GroupContainer: AlignInContainer (Default SetByContainer), FillPortions (Default 0), LayoutMaxHeight, LayoutMaxWidth, LayoutMinHeight (Default 42), LayoutMinWidth (Default 42)
If child of Grid GroupContainer: LayoutGridColumnEnd/Start, LayoutGridRowEnd/Start

Output Properties: AccessibleLabel, BasePaletteColor, BorderColor, BorderStyle, BorderThickness, ContentLanguage, DisplayMode, Fill, Height, Padding*, Radius*, Tooltip, Visible, Width, X, Y
```

### ModernBadge
```
Part of the control family React.
Control: ModernBadge

Input Properties:
  - AccessibleLabel: Text
  - Align: Enum Align — Center, Justify, Left, Right (Default Center)
  - Appearance: Enum BadgeAppearance — Filled, Ghost, Outline, Tint (Default Tint)
  - BasePaletteColor: Color
  - BorderColor: Color
  - BorderStyle: Enum BorderStyle — Dashed, Dotted, None, Solid
  - BorderThickness: Number
  - Color: Color
  - Content: Text (Default "AB")
  - ContentLanguage: Text
  - DisplayMode: Enum DisplayMode — Disabled, Edit, View
  - Fill: Color
  - Font: Enum Font (same list as ModernText)
  - FontWeight: Enum FontWeight — Bold, Lighter, Normal, Semibold
  - Height: Number (Default 44)
  - Icon: Text (Default "")
  - IconPosition: Enum BadgeIconPosition — After, Before (Default Before)
  - Intent: Enum BadgeIntent — Attention, Caution, Critical, Highlight, Informative, Neutral, Positive, Urgent (Default Positive)
  - Italic: Boolean
  - OnSelect: Boolean
  - PaddingBottom / PaddingLeft / PaddingRight / PaddingTop: Number
  - RadiusBottomLeft / RadiusBottomRight / RadiusTopLeft / RadiusTopRight: Number
  - Shape: Enum BadgeShape — Circular, Rounded, Square (Default Circular)
  - Size: Number (Default 24)
  - Strikethrough: Boolean
  - Tooltip: Text
  - Underline: Boolean
  - VerticalAlign: Enum VerticalAlign — Bottom, Middle, Top (Default Middle)
  - Visible: Boolean
  - Width: Number (Default 88)
  - X, Y: Number

If child of Vertical/Horizontal GroupContainer: AlignInContainer (Default SetByContainer), FillPortions (Default 0), LayoutMaxHeight, LayoutMaxWidth, LayoutMinHeight (Default 44), LayoutMinWidth (Default 88)
If child of Grid GroupContainer: LayoutGridColumnEnd/Start, LayoutGridRowEnd/Start

Output Properties: AccessibleLabel, Align, BasePaletteColor, BorderColor, BorderStyle, BorderThickness, Color, ContentLanguage, DisplayMode, Fill, Font, FontWeight, Height, Italic, Padding*, Radius*, Size, Strikethrough, Tooltip, Underline, VerticalAlign, Visible, Width, X, Y
```

### ModernCard (for reference only — being REMOVED from the app)
```
Part of the control family React.
Control: ModernCard

Input Properties: AccessibleLabel, BorderRadius (12), ContentLanguage, Description, DescriptionColor, DescriptionSize (12), DisplayMode, DropShadow (Regular), Fill,
  HeaderImage: Image (Default SampleCardHeaderImage), HeaderImageAccessibleLabel, Height (420),
  Image: Image (Default SampleCardImage), ImageAccessibleLabel, ImagePlacement (BeforeHeader), ImagePosition (Fill), ImageRatio,
  LayoutDirection (Vertical), OnSelect, Subtitle, SubtitleColor, SubtitleSize (14), Title, TitleColor, TitleSize (16), Visible, Width (560), X, Y
If child of Vertical/Horizontal GroupContainer: AlignInContainer (SetByContainer), FillPortions (0), LayoutMaxHeight, LayoutMaxWidth, LayoutMinHeight (420), LayoutMinWidth (560)
```
The `Image`/`HeaderImage` defaults (`SampleCardImage`) are the source of the purple placeholder defect. No `ModernCard` remains after this edit.

### Gallery
```
Part of the control family Classic.
Control: Gallery
Variant: <variant name> # (required) Horizontal | VariableHeight | Vertical

Input Properties (all variants):
  - BorderStyle: Enum BorderStyle — Dashed, Dotted, None, Solid (Default Solid)
  - ContentLanguage: Text
  - Default: Record
  - DisplayMode: Enum DisplayMode — Disabled, Edit, View
  - Fill: Color (Default RGBA(0, 0, 0, 0))
  - FocusedBorderColor: Color (Default Self.BorderColor)
  - FocusedBorderThickness: Number (Default 4)
  - LoadingSpinnerColor: Color
  - NavigationStep: Number (Default 1)
  - Selectable: Boolean (Default true)
  - ShowNavigation: Boolean (Default false)
  - TabIndex: Number (Default -1)
  - Transition: Enum Transition — None, Pop, Push
  - Visible: Boolean

Variant Horizontal: AccessibleLabel, BorderColor, BorderThickness (0), DelayItemLoading (true), Height (575), Items: Table, LoadingSpinner: Enum LoadingSpinner — Controls, Data, None (Default Data), ShowScrollbar (true), TemplatePadding (5), TemplateSize, Width (640), WrapCount (1), X, Y
Variant VariableHeight: AccessibleLabel, BorderColor, BorderThickness, DelayItemLoading, Height, Items, LoadingSpinner, MaxTemplateSize (5000), ShowScrollbar, TemplatePadding, TemplateSize (280), Width, X, Y
Variant Vertical: AccessibleLabel, BorderColor, BorderThickness, DelayItemLoading, Height, Items, LoadingSpinner, ShowScrollbar, TemplatePadding, TemplateSize, Width, WrapCount, X, Y

If child of Vertical/Horizontal GroupContainer: AlignInContainer (Default Stretch), FillPortions (Default 1), LayoutMaxHeight, LayoutMaxWidth, LayoutMinHeight (Default 287), LayoutMinWidth (Default 320)
If child of Grid GroupContainer: LayoutGridColumnEnd/Start, LayoutGridRowEnd/Start

Output Properties: AccessibleLabel, AllItems: Table, AllItemsCount: Number, BorderColor, BorderStyle, BorderThickness, ContentLanguage, DisplayMode, Fill, FocusedBorderColor, FocusedBorderThickness, Height, Selected: Record, TabIndex, TemplateHeight: Number, TemplatePadding, TemplateWidth: Number, Valid, Visible, VisibleIndex, Width, X, Y
```
`OnSelect` is **not** in this output → do not set `Gallery.OnSelect`. Inside templates use `Parent.TemplateHeight` / `Parent.TemplateWidth` for the row container and `ThisItem` in child formulas.

### CanvasComponent instance (from describe_control on the live stub `cmpAppHeader`)
```
Control: CanvasComponent
ComponentName: <name>

Input Properties: ChildTabPriority (true), ContentLanguage, EnableChildFocus (true), Fill (RGBA(0,0,0,0)), Height (component default), Visible (true), Width (component default), X, Y, plus every custom Input/Event property declared in the definition
If child of Vertical/Horizontal GroupContainer: AlignInContainer (Default SetByContainer), FillPortions (Default 0), LayoutMaxHeight, LayoutMaxWidth, LayoutMinHeight (Default = component Height), LayoutMinWidth (Default = component Width)
Output Properties: ChildTabPriority, ContentLanguage, EnableChildFocus, Fill, Height, Visible, Width, X, Y, plus custom Output properties
```
Because `LayoutMinHeight`/`LayoutMinWidth` default to the component's definition size, **every instance must set `LayoutMinHeight`/`LayoutMinWidth` explicitly** (shown in the snippets).

### Existing controls not re-described
`ModernTextInput`, `ModernCombobox`, `ModernDropdown`, `ModernDatePicker`, `ModernCheckbox`, `ModernToggle`, `ModernRadio`, `ModernProgressBar` already exist in the YAML — reuse only the property names already present in the current files for them (`Height`, `Width`, `Default`, `DefaultDate`, `Items`, `ItemDisplayText`, `OnChange`, `Placeholder`, `InputTextPlaceholder`, `IsSearchable`, `IsEditable`, `Format`, `Required`, `MaxLength`, `Type`, `Label`, `OnCheck`, `OnUncheck`, `Checked`, `ToggleSize`, `Layout`, `Selected`, `SelectedDate`, `Text`, `ValidationState`, `Tooltip`, `CheckboxSize`, `FontWeight`, `FillColor`, `ProgressColor`, `TrackColor`, `Max`, `Value`, `AccessibleLabel`, `DisplayMode`, `Visible`, and the AutoLayout child set `FillPortions`, `AlignInContainer`, `LayoutMinWidth`, `LayoutMinHeight`).

## TechnicalGuide Key Conventions (screen editors must follow)

- Every property value is a Power Fx formula prefixed with `=`. Non-formula keys: `Control`, `Variant`, `ComponentName`, `DefinitionType`, `Description`, `AccessAppScope` (YAML boolean), `PropertyKind`, `DisplayName`, `DataType`, `ReturnType`.
- Multi-line formulas use `|-`; the `=` goes on the first content line.
- Quote any plain-scalar value containing `: ` — especially Power Fx record literals: `Default: '={Value: "Yes"}'` or `"={Value: ""Yes""}"`. Existing `Patch` bodies with `{Value: ...}` inside `|-` blocks are fine (block scalars are not parsed as mappings).
- Enum references: `LayoutDirection.Vertical`, `LayoutAlignItems.Stretch`, `ButtonAppearance.Secondary`, `ButtonLayout.IconOnly`, `BadgeIntent.Positive`, `BadgeShape.Rounded`, `IconStyle.Filled`, `DropShadow.None`, `BorderStyle.Solid`, `AlignInContainer.Stretch`, `LayoutOverflow.Scroll`, `ScreenTransition.None`. Escape with `'…'` only when a name has spaces/special chars.
- Choice/lookup columns: compare with `.Value` / `.Id` (`OverallStatus.Value = "Closed"`, `Request.Id = gblSelectedRequest.ID`). Data source names are quoted: `'FOIA Pilot Requests'`.
- Date formatting: `Text(date, "[$-en-US]mmm d, yyyy")` (lower-case format codes).
- Component definitions: root key `ComponentDefinitions:`; inside a definition reference its own properties as `cmpName.Prop` and raise events as `cmpName.Event()`. Instances: `Control: CanvasComponent` + `ComponentName:`; set event handlers like any property (`OnBack: =Navigate(...)`). Component `Properties` must not include `X`, `Y`, `Visible`.
- Screen-level `OnVisible` formulas, all `Patch`/`Filter`/`LookUp`/`Choices` data formulas, and all `DisplayMode` validation gates are **copied unchanged** unless a per-screen step explicitly rewrites them (only `btnDepartmentWork` on RequestDetail is rewritten).
- Do not call `compile_canvas`; the orchestrator compiles after all files are written. Do not publish.
- Naming: keep the `scr/cnt/lbl/btn/txt/cmb/gal/ico/cmp/gbl` prefixes; every new control name states its purpose (no `Button1`).
- Required user states remain visible: loading, empty, permission-denied, error, validation, success labels exist on every data-bound screen (keep their `Visible` formulas).
