# Canvas App Plan — Flossmoor FOIA v3 (design-system uplift)

## Mode
EDIT (complex) — visual/system uplift of a working app. No data-model, navigation-graph, or write-logic changes other than `Notify()` → `cmpToastHost.SendToast(...)`.

## Edit Requirements
User's bar (verbatim): **"Make sure you make this more elevated, next level, feel like a Microsoft app that really impresses everyone."** Plain-but-functional is a failure. The target look is codified in `skills\power-apps-delivery\references\design-system.md` (ELM / Early Check language): white carded header with centered Lato title, 50-px icon rail with GridDots expander, phone bottom tab bar, KPI metric tiles with tinted icon chips, list rows with 5-px status accent bars + tint pills, section cards (radius 10, light shadow), approval-flow stepper, and `cmpToast` as the only user-facing feedback surface.

Scope (approved — do not redesign):
- `App.pa.yaml` — tokens + OnStart (**already written by the planner**; builders do not touch it).
- **Create** 4 components: `cmpToast`, `cmpMetricTile`, `cmpEmptyState`, `cmpPhoneNav`.
- **Modify** 3 components (property-level + appended children only): `cmpAppHeader`, `cmpSideNav`, `cmpStatusBadge`.
- **Modify** 5 screens: `Home`, `NewRequest`, `RequestDetail`, `DepartmentWork`, `ResponseCloseout`.
- `cmpRequestDetailPane` is **not** modified.

## Working Directory
`C:\Users\tejas\OneDrive - MGP Inc\ManagedApps\AI_Process\pilots\flossmoor-foia\canvas-app-v3`
(already synced from the live app). **Do not run `sync_canvas` or `compile_canvas`** — the orchestrating skill owns both.

## Files and actions

| Action | File | Summary |
|---|---|---|
| Modify (done) | `App.pa.yaml` | §2 tokens added (old names kept as aliases), `OnStart` seeds `colToasts`, `varCurrentTime`, `gblNavExpanded`. |
| Create | `Components\cmpToast.pa.yaml` | Fluent 2 toast stack recreated from `toast-component.pa.yaml`, retokenised, a11y labels, Modern* controls. |
| Create | `Components\cmpMetricTile.pa.yaml` | KPI tile: tinted 50-px icon chip + caption + value (+ note); `Compact` strip mode. |
| Create | `Components\cmpEmptyState.pa.yaml` | Centered icon · headline · hint · one primary action. |
| Create | `Components\cmpPhoneNav.pa.yaml` | Bottom tab bar driven by an `Items` table; icon above label; 2-px brand indicator. |
| Modify | `Components\cmpAppHeader.pa.yaml` | New three-portion (1 · 2 · 1) header row appended; old row children hidden. White, `DropShadow.Light`, `RadiusMedium`, Lato title. |
| Modify | `Components\cmpSideNav.pa.yaml` | New `Expanded` input; new GridDots expander + 4 tinted nav-item containers appended; old buttons/dividers hidden. 50 ↔ 220 px. |
| Modify | `Components\cmpStatusBadge.pa.yaml` | Property-only: Tint appearance, `RadiusMedium`, Lato, caption size. |
| Modify | `Home.pa.yaml` | Shell retokenised; 4 `cmpMetricTile` instances (old tiles hidden); accent-bar rows + chevron; `Status:`/`Department:` dropdown labels + Reset; `cmpEmptyState`; `cmpPhoneNav`; `cmpToast` host; Notify → SendToast. |
| Modify | `NewRequest.pa.yaml` | Section cards retokenised (radius 10, light shadow, no border); `locShowValidation` inline validation (`ValidationState` + red labels); Save → SendToast both branches; sticky bar retokenised; `cmpPhoneNav`; `cmpToast` host. |
| Modify | `RequestDetail.pa.yaml` | New `cntDetailStack` (stepper + fresh pane instance) appended; old pane host hidden; Notify → SendToast; `cmpPhoneNav`; `cmpToast` host. |
| Modify | `DepartmentWork.pa.yaml` | Accent bars on assignment cards + record rows; cards retokenised; 6 Notify → SendToast; `cmpEmptyState` for assignments; `cmpPhoneNav`; `cmpToast` host. |
| Modify | `ResponseCloseout.pa.yaml` | Section cards retokenised; Notify → SendToast; success toast then navigate; `cmpPhoneNav`; `cmpToast` host. |
| Modify | `_EditorState.pa.yaml` | Append the 4 new component names to `ComponentDefinitionsOrder` (alphabetical: cmpAppHeader, cmpEmptyState, cmpMetricTile, cmpPhoneNav, cmpRequestDetailPane, cmpSideNav, cmpStatusBadge, cmpToast). |

## Current App Summary
- Screens: `Home` (KPIs, distribution strip, master-detail on desktop, filtered gallery), `NewRequest` (3 section cards + sticky action bar + desktop guidance panel), `RequestDetail` (hosts `cmpRequestDetailPane`), `DepartmentWork` (assignment cards + editor + records), `ResponseCloseout` (readiness card + closeout form + sticky actions).
- Layout: pure AutoLayout. Every screen = `cnt<Screen>Shell` (vertical) → `cmp<Screen>Header` (cmpAppHeader) → `cnt<Screen>Body` (horizontal: `cmp<Screen>NavRail` + `cnt<Screen>ContentOuter` → `cnt<Screen>Content`) → [NewRequest: `cntNewRequestActions`] → `cmp<Screen>NavBottom` (cmpSideNav Placement "Bottom").
- Control families in use: `GroupContainer` (AutoLayout), `Gallery` (Vertical), `ModernText`, `ModernButton`, `ModernIcon`, `ModernBadge`, `ModernTabList`, `ModernTextInput`, `ModernCombobox`, `ModernDropdown`, `ModernDatePicker`, `ModernCheckbox`, `ModernToggle`, `ModernRadio`, `CanvasComponent`. **Use these names** (not the FluentV9 `Text`/`Button`/`Icon` names that appear in design-system.md snippets — translate: `Text`→`ModernText` (`Weight`→`FontWeight`, `FontColor`→`Color`), `Button`→`ModernButton` (`'ButtonCanvas.Appearance'.X`→`ButtonAppearance.X`, `'ButtonCanvas.Layout'.IconOnly`→`ButtonLayout.IconOnly`), `Icon`→`ModernIcon`, `Badge`→`ModernBadge`, `Progress`→`ModernProgressBar`).
- Current palette (pre-uplift, now superseded by App.pa.yaml): brand `RGBA(0,120,212,1)`, page `RGBA(250,250,250,1)`, surface white, text `RGBA(36,36,36,1)` / `RGBA(97,97,97,1)`.
- Globals: `gblIsLoading`, `gblLoadError`, `gblPermissionDenied`, `gblSaveSuccess`, `gblSearchText`, `gblStatusFilter`, `gblDepartmentFilter`, `gblSelectedRequest` (Record), `gblSelectedAssignment` (Record), `gblSelectedDepartment` (Record), `gblDueDateConfirmed`, `gblExtensionValidationMessage`. **New:** `colToasts` (collection), `varCurrentTime` (DateTime), `gblNavExpanded` (Boolean) — all seeded in `App.OnStart`. Screen-local new: `locShowValidation` (NewRequest).
- Data sources: `FOIA Pilot Requests`, `FOIA Pilot Assignments`, `FOIA Pilot Departments`, `FOIA Pilot Records` (SharePoint; schemas unchanged — see `..\canvas-app-v2-plan.md` "Data Source Schemas" if a column name is needed; no new columns are bound in this edit).

## Token block (already in App.pa.yaml — reference only)
Old names remain valid aliases (`SpaceSm = Space2`, `RadiusSm = RadiusSmall`, `ColorNeutralBg = ColorCanvas`, `ColorNeutralStroke = ColorBorder`, `ColorCritical = ColorDanger`, `ControlMinTouch = TouchTarget`, `NavRailWidthTablet = RailWidth`, `NavRailWidthDesktop = RailWidthExpanded`, `BottomNavHeight = PhoneNavHeight`). New code uses the §2 names.

| Token | Value | Token | Value |
|---|---|---|---|
| `ColorBrand` | `RGBA(27,74,137,1)` | `ColorBrandHover` | `RGBA(21,60,112,1)` |
| `ColorBrandTint` | `RGBA(27,74,137,0.10)` | `ColorBrandAlt` | `RGBA(55,73,114,1)` |
| `ColorSurface` | white | `ColorCanvas` | `RGBA(245,245,245,1)` |
| `ColorBorder` | `RGBA(225,223,221,1)` | `ColorTextPrimary` | `RGBA(36,36,36,1)` |
| `ColorTextSecondary` | `RGBA(97,97,97,1)` | `ColorTextTertiary` | `RGBA(150,148,146,1)` |
| `ColorSuccess` / `ColorSuccessTint` | `RGBA(16,124,16,1)` / `…0.12` | `ColorWarning` / `ColorWarningTint` | `RGBA(157,93,0,1)` / `RGBA(255,185,0,0.18)` |
| `ColorDanger` / `ColorDangerTint` | `RGBA(196,49,75,1)` / `…0.12` | `ColorInfo` / `ColorInfoTint` | `RGBA(0,120,212,1)` / `…0.12` |
| `ColorNeutralTint` | `RGBA(97,97,97,0.12)` | `FontApp` | `Font.Lato` |
| `FontSizeCaption/Body/BodyPhone/Section` | 12 / 14 / 15 / 16 | `FontSizeTitlePhone/Tablet/Desktop` | 20 / 22 / 24 |
| `FontSizeKpiPhone/Tablet/Desktop` | 28 / 30 / 32 | `FontSizeAppTitle` | 28 |
| `Space1…Space6` | 4 8 12 16 24 32 | `RadiusSmall/Medium/Large` | 4 / 8 / 10 |
| `TouchTarget` | 44 | `InputHeight` / `FieldHeight` | 44 / 72 |
| `HeaderHeight` | 64 | `RailWidth` / `RailWidthExpanded` | 50 / 220 |
| `PhoneNavHeight` | 64 | `StatusAccentWidth` | 5 |
| `TileHeight` / `TileMaxWidth` / `StatStripHeight` | 104 / 360 / 64 | `IconChipSize` | 50 |
| `StepperCircleSize` / `StepperConnectorWidth` | 20 / 80 | `ContentMaxWidth` / `ListPaneRatio` | 1600 / 0.38 |
| `BreakpointPhone` / `BreakpointDesktop` | 600 / 1200 (compare **inline**: `App.Width < BreakpointPhone`) | | |

`App.OnStart` (written):
```powerfx
ClearCollect(colToasts, Filter(Table({Header:"", Icon:"", IconColor:Color.Gray, IconFilled:false, Body:"", Duration:7000, ShowDismiss:true, ShowTime:false, ShowProgress:false, CurrentTime:Now(), RemoveTime:Now()}), false));
Set(varCurrentTime, Now());
Set(gblNavExpanded, App.Width >= BreakpointDesktop)
```

## Sync-rule compliance (read before editing anything)

The authoring service merges same-named controls onto their existing instances. **Changing a control's parent corrupts it** (rule 1); a recreated parent needs all-new descendants (rule 3). This plan therefore uses only three kinds of change:

1. **Property-only edits** to existing controls (same name, same parent). Includes `Visible: =false` to retire a control.
2. **New controls appended as the LAST children of an existing parent.** Every retired sibling is hidden (invisible AutoLayout children take no space), so the new controls render in the right place without relying on sibling re-ordering. Names of new controls never collide with existing ones (suffix `2` where a conceptual duplicate exists, e.g. `btnHeaderBack2`).
3. **New sub-trees** (new parent + all-new descendants), appended last. Used where a wrapper is needed: `cntDetailStack` on RequestDetail (contains a *second* `cmpRequestDetailPane` instance because the existing one cannot be moved).
4. **New overlay controls inside gallery templates** (`recAccent*` Rectangles) are placed directly in the gallery's `Children` with absolute `X/Y` (gallery templates are not AutoLayout). Appended last ⇒ topmost z-order, which is what an accent bar wants.

Explicitly **never** done in this plan: deleting controls, renaming controls, moving a control into a new container, changing a `Variant`, changing a `ComponentName` on an existing instance. Old bottom-nav instances (`cmp*NavBottom`) and old KPI tiles stay in the file, hidden.

Other rules applied: components never inside gallery templates (rows use `ModernBadge` + `Rectangle`); every `PropertyKind: Event` has a `Default`; breakpoint tests inline; `ModernBadge.Intent` uses `BadgeIntent.Neutral`; `TemplateSize` is never read — row heights repeat the literal; any scalar formula containing `: ` is single-quoted; `Select(Parent)` is not used inside template containers (inner controls repeat the gallery's `OnSelect` body).

Also note the stock app-shell deviation: **`cmpToastHost` is a direct child of the Screen** (sibling after `cnt<Screen>Shell`), not of the shell. The shell is a vertical AutoLayout container, where `X`/`Y` are ignored; only a Screen-level child can float over content. This is a new control under an existing parent (the screen) and is sync-safe.

Hidden-control inventory (so QA knows they are intentional): `cmp*NavBottom` ×5, `cntTileTotal/Open/DueSoon/Closed` (Home), `lblQueueEmpty` (Home), `lblRequestSuccess` (NewRequest), `cmpRequestDetailPaneHost` (RequestDetail), `lblAssignmentsEmpty` (DepartmentWork), `cmpAppHeader`: `btnHeaderBack`, `cntHeaderTitles`, `btnHeaderSecondary`, `btnHeaderPrimary`, `cntHeaderDivider`; `cmpSideNav`: `btnNavHome`, `btnNavNewRequest`, `btnNavDepartmentWork`, `btnNavResponseCloseout`, `cntNavDividerTop`, `cntNavDividerSide`.

## Toast intent table (use verbatim at every call site)

| Intent | Call |
|---|---|
| Success | `cmpToastHost.SendToast("<≤40 chars>", "CheckmarkCircle", ColorSuccess, true, "<detail>")` (7 000 ms default) |
| Error | `cmpToastHost.SendToast("<≤40 chars>", "DismissCircle", ColorDanger, true, "<FirstError.Message>", 600000, true, false, false)` |
| Warning | `cmpToastHost.SendToast("<≤40 chars>", "Warning", ColorWarning, true, "<detail>", 10000)` |
| Info | `cmpToastHost.SendToast("<≤40 chars>", "Info", ColorInfo, false, "<detail>", 5000, true, true, true)` |

Every screen names its host **`cmpToastHost`** so call sites are identical across screens. `colToasts` is global, so a toast raised immediately before `Navigate()` is shown by the destination screen's host.

## New component definitions (paste-ready)

Each goes in its own file under `Components\`. Component Properties reference custom properties as `cmpX.Prop` (the proven v2 style); `Self.AutoHeight` is used only where the reference toast proved it.

### Components\cmpToast.pa.yaml

Differences from the reference (`toast-component.pa.yaml`): `@version` suffixes dropped; `Fluent 2 Toast` → `cmpToast`; FluentV9 controls → Modern* equivalents (`Text`→`ModernText`, `Icon`→`ModernIcon`, `Button`→`ModernButton`, `Progress`→`ModernProgressBar`); `IconFIlled` typo normalised to `IconFilled`; colours → tokens; `conToast` gets `DropShadow.Regular` + `RadiusMedium`; a11y labels added. `ModernText` has no `Live` property and `GroupContainer` has no `AccessibleLabel`, so the live-region label lives on `txtHeader` (recorded exception).

```yaml
ComponentDefinitions:
  cmpToast:
    DefinitionType: CanvasComponent
    Description: Fluent 2 toast stack - the app's only user-facing notification surface. Collection-driven (colToasts), per-row auto-dismiss, queue capped at 4. App-scope deps - colToasts, varCurrentTime (seeded in App.OnStart).
    AccessAppScope: true
    CustomProperties:
      AddToast:
        PropertyKind: Event
        DisplayName: Add Toast
        Description: Adds a toast record to the collection (drops the oldest when 4 are queued).
        ReturnType: None
        Default: =If(CountRows(colToasts) = 4, Remove(colToasts, First(colToasts))); Collect(colToasts, ToastRecord)
        Parameters:
          - ToastRecord:
              Description: Record built by SendToast
              DataType: Record
              Default: |-
                ={
                Header: "",
                Icon: "",
                IconColor: Color.Gray,
                IconFilled: false,
                Body: "",
                Duration: 7000,
                ShowDismiss: true,
                ShowTime: false,
                ShowProgress: false,
                CurrentTime: Now(),
                RemoveTime: Now()
                }
      AutoHeight:
        PropertyKind: Output
        DisplayName: Auto Height
        Description: 0 when no toasts are queued, otherwise the rendered stack height. Bind the instance Height to it.
        DataType: Number
      RemoveToast:
        PropertyKind: Event
        DisplayName: Remove Toast
        Description: Removes a toast record from the collection.
        ReturnType: None
        Default: =Remove(colToasts, ToastRecord)
        Parameters:
          - ToastRecord:
              Description: Record to remove
              DataType: Record
              Default: |-
                ={
                Header: "",
                Icon: "",
                IconColor: Color.Gray,
                IconFilled: false,
                Body: "",
                Duration: 7000,
                ShowDismiss: true,
                ShowTime: false,
                ShowProgress: false,
                CurrentTime: Now(),
                RemoveTime: Now()
                }
      SendToast:
        PropertyKind: Action
        DisplayName: Send Toast
        Description: Raise a toast. Header, Icon required; IconColor, IconFilled, Body, Duration (ms), ShowDismiss, ShowTime, ShowProgress optional.
        ReturnType: None
        Parameters:
          - Header:
              Description: Toast header (does not wrap - keep under 40 characters)
              DataType: Text
              Default: ="Header Text"
          - Icon:
              Description: Fluent icon name (CheckmarkCircle, DismissCircle, Warning, Info)
              DataType: Text
              Default: =""
          - IconColor:
              Description: Icon colour token
              IsOptional: true
              DataType: Color
              Default: =Color.Gray
          - IconFilled:
              Description: Filled icon style when true
              IsOptional: true
              DataType: Boolean
              Default: =false
          - Body:
              Description: Body text (wraps)
              IsOptional: true
              DataType: Text
              Default: =""
          - Duration:
              Description: Milliseconds before auto-dismiss
              IsOptional: true
              DataType: Number
              Default: =7000
          - ShowDismiss:
              Description: Show the dismiss button
              IsOptional: true
              DataType: Boolean
              Default: =true
          - ShowTime:
              Description: Show the time the toast was raised
              IsOptional: true
              DataType: Boolean
              Default: =false
          - ShowProgress:
              Description: Show the countdown progress bar
              IsOptional: true
              DataType: Boolean
              Default: =false
      SortOrder:
        PropertyKind: Input
        DisplayName: Sort Order
        Description: SortOrder.Ascending = oldest on top.
        DataType: Text
        Default: =SortOrder.Ascending
      ToastTable:
        PropertyKind: Input
        DisplayName: Toast Table
        Description: Table of toast records (defaults to colToasts).
        DataType: Table
        Default: =colToasts
    Properties:
      AutoHeight: =If(galToast.AllItemsCount = 0, 0, conToastComponent.Height)
      Height: =Self.AutoHeight
      SendToast: |-
        =cmpToast.AddToast(
            {
                Header: Header,
                Icon: Icon,
                IconColor: IconColor,
                IconFilled: IconFilled,
                Body: Body,
                Duration: Duration,
                ShowDismiss: ShowDismiss,
                ShowTime: ShowTime,
                ShowProgress: ShowProgress,
                CurrentTime: Now(),
                RemoveTime: DateAdd(Now(), Duration, TimeUnit.Milliseconds)
            }
        )
      Width: =300
    Children:
      - conToastComponent:
          Control: GroupContainer
          Variant: AutoLayout
          Properties:
            DropShadow: =DropShadow.None
            Height: =galToast.Height
            LayoutDirection: =LayoutDirection.Vertical
            LayoutMinHeight: =0
            LayoutMinWidth: =0
            RadiusBottomLeft: =0
            RadiusBottomRight: =0
            RadiusTopLeft: =0
            RadiusTopRight: =0
            Width: =Parent.Width
          Children:
            - galToast:
                Control: Gallery
                Variant: VariableHeight
                Properties:
                  AccessibleLabel: ="Notifications"
                  FillPortions: =0
                  Height: =Sum(Self.AllItems, txtGaluAutoHeight.Text) + Self.TemplatePadding
                  Items: |-
                    =If(IsBlank(App.ActiveScreen.Name),
                      Table({Header: "Request saved", Icon: "CheckmarkCircle", IconColor: ColorSuccess, IconFilled: true, Body: "Sample toast shown only in the designer.", Duration: 7000, ShowDismiss: true, ShowTime: false, ShowProgress: false, CurrentTime: Now(), RemoveTime: Now()}),
                      Sort(cmpToast.ToastTable, CurrentTime, cmpToast.SortOrder))
                  LayoutMinHeight: =0
                  LayoutMinWidth: =0
                  ShowScrollbar: =false
                  TemplatePadding: =Space4
                  TemplateSize: =100
                Children:
                  - txtGaluAutoHeight:
                      Control: ModernText
                      Properties:
                        Text: =conToast.Height + Parent.TemplatePadding
                        Visible: =false
                        X: =40
                        Y: =40
                  - conToast:
                      Control: GroupContainer
                      Variant: AutoLayout
                      Properties:
                        DropShadow: =DropShadow.Regular
                        Fill: =ColorSurface
                        Height: =conAutoHeight.Y + Self.PaddingBottom
                        LayoutDirection: =LayoutDirection.Vertical
                        LayoutGap: =Space1
                        PaddingBottom: =Space2
                        PaddingLeft: =Space2
                        PaddingRight: =Space2
                        PaddingTop: =Space2
                        RadiusBottomLeft: =RadiusMedium
                        RadiusBottomRight: =RadiusMedium
                        RadiusTopLeft: =RadiusMedium
                        RadiusTopRight: =RadiusMedium
                        Width: =Parent.TemplateWidth
                      Children:
                        - conToastHeader:
                            Control: GroupContainer
                            Variant: AutoLayout
                            Properties:
                              DropShadow: =DropShadow.None
                              FillPortions: =0
                              Height: =32
                              LayoutAlignItems: =LayoutAlignItems.Center
                              LayoutDirection: =LayoutDirection.Horizontal
                              LayoutGap: =Space2
                              LayoutMinHeight: =0
                              LayoutMinWidth: =0
                              RadiusBottomLeft: =0
                              RadiusBottomRight: =0
                              RadiusTopLeft: =0
                              RadiusTopRight: =0
                            Children:
                              - icoToast:
                                  Control: ModernIcon
                                  Properties:
                                    AccessibleLabel: =ThisItem.Header
                                    AlignInContainer: =AlignInContainer.Center
                                    Height: =20
                                    Icon: =ThisItem.Icon
                                    IconColor: =ThisItem.IconColor
                                    IconStyle: =If(ThisItem.IconFilled, IconStyle.Filled, IconStyle.Outline)
                                    LayoutMinHeight: =20
                                    LayoutMinWidth: =20
                                    Visible: =!IsBlank(ThisItem.Icon)
                                    Width: =20
                              - txtHeader:
                                  Control: ModernText
                                  Properties:
                                    AccessibleLabel: '=ThisItem.Header & ". " & ThisItem.Body'
                                    AlignInContainer: =AlignInContainer.Center
                                    Color: =ColorTextPrimary
                                    FillPortions: =1
                                    Font: =FontApp
                                    FontWeight: =FontWeight.Semibold
                                    LayoutMinHeight: =0
                                    LayoutMinWidth: =0
                                    PaddingBottom: =0
                                    PaddingLeft: =0
                                    PaddingRight: =0
                                    PaddingTop: =0
                                    Size: =FontSizeBody
                                    Text: =ThisItem.Header
                                    VerticalAlign: =VerticalAlign.Middle
                                    Wrap: =false
                              - txtTime:
                                  Control: ModernText
                                  Properties:
                                    AccessibleLabel: =Self.Text
                                    Align: =Align.Right
                                    AlignInContainer: =AlignInContainer.Center
                                    Color: =ColorTextSecondary
                                    FillPortions: =1
                                    Font: =FontApp
                                    LayoutMinHeight: =0
                                    LayoutMinWidth: =56
                                    PaddingBottom: =0
                                    PaddingLeft: =0
                                    PaddingRight: =0
                                    PaddingTop: =0
                                    Size: =FontSizeCaption
                                    Text: =Text(ThisItem.CurrentTime, "hh:mm AM/PM")
                                    VerticalAlign: =VerticalAlign.Middle
                                    Visible: =ThisItem.ShowTime
                                    Wrap: =false
                              - btnToastDismiss:
                                  Control: ModernButton
                                  Properties:
                                    AccessibleLabel: ="Dismiss notification"
                                    AlignInContainer: =AlignInContainer.Center
                                    Appearance: =ButtonAppearance.Transparent
                                    Height: =32
                                    Icon: ="Dismiss"
                                    Layout: =ButtonLayout.IconOnly
                                    LayoutMinHeight: =32
                                    LayoutMinWidth: =32
                                    OnSelect: =cmpToast.RemoveToast(ThisItem)
                                    Text: ="Dismiss"
                                    Tooltip: ="Dismiss"
                                    Visible: =ThisItem.ShowDismiss
                                    Width: =32
                        - txtToastBody:
                            Control: ModernText
                            Properties:
                              AccessibleLabel: =Self.Text
                              AlignInContainer: =AlignInContainer.Stretch
                              AutoHeight: =true
                              Color: =ColorTextSecondary
                              Font: =FontApp
                              LayoutMinHeight: =0
                              LayoutMinWidth: =0
                              PaddingBottom: =0
                              PaddingLeft: =0
                              PaddingRight: =0
                              PaddingTop: =0
                              Size: =FontSizeBody
                              Text: =ThisItem.Body
                              Visible: =!IsBlank(ThisItem.Body)
                        - prgToast:
                            Control: ModernProgressBar
                            Properties:
                              AccessibleLabel: ="Time remaining"
                              AlignInContainer: =AlignInContainer.Stretch
                              Height: =8
                              LayoutMinHeight: =8
                              LayoutMinWidth: =0
                              Max: =ThisItem.Duration
                              ProgressColor: =ProgressColor.Brand
                              Shape: =ProgressShape.Rounded
                              Thickness: =ProgressThickness.Medium
                              Value: =DateDiff(ThisItem.CurrentTime, varCurrentTime, TimeUnit.Milliseconds)
                              Visible: =ThisItem.ShowProgress
                        - conAutoHeight:
                            Control: GroupContainer
                            Variant: AutoLayout
                            Properties:
                              DropShadow: =DropShadow.None
                              FillPortions: =0
                              Height: =1
                              LayoutDirection: =LayoutDirection.Vertical
                              LayoutMinHeight: =0
                              LayoutMinWidth: =0
                              RadiusBottomLeft: =0
                              RadiusBottomRight: =0
                              RadiusTopLeft: =0
                              RadiusTopRight: =0
                  - tmrDuration:
                      Control: Timer
                      Properties:
                        AutoPause: =false
                        AutoStart: =true
                        Duration: =100
                        Height: =40
                        OnTimerEnd: =If(Now() > ThisItem.RemoveTime, cmpToast.RemoveToast(ThisItem), Set(varCurrentTime, Now()))
                        Repeat: =true
                        Visible: =false
                        Width: =160
                        X: =224
                        Y: =24
```

**Instance (every screen, direct child of the Screen, after `cnt<Screen>Shell`):**
```yaml
      - cmpToastHost:
          Control: CanvasComponent
          ComponentName: cmpToast
          Properties:
            Height: =Self.AutoHeight
            SortOrder: =SortOrder.Ascending
            ToastTable: =colToasts
            Width: =If(App.Width < BreakpointPhone, App.Width - 2 * Space4, 300)
            X: =If(App.Width < BreakpointPhone, Space4, Parent.Width - Self.Width - Space4)
            Y: =If(App.Width < BreakpointPhone, HeaderHeight + Space4 + Space2, Parent.Height - Self.Height - Space4)
```

### Components\cmpMetricTile.pa.yaml

Contract: inputs `Label`, `Value` (Text — pass `Text(n)`), `Icon`, `Intent` (`"Brand" | "Success" | "Warning" | "Danger" | "Info" | "Neutral"`), `Compact` (desktop strip: icon · value · caption in one row), `Note` (footnote, hidden in Compact). Event `OnSelect` (raised from the icon chip and the value). Instance sizes itself: `Height = If(App.Width >= BreakpointDesktop, StatStripHeight, TileHeight)`.

```yaml
ComponentDefinitions:
  cmpMetricTile:
    DefinitionType: CanvasComponent
    Description: KPI metric tile - tinted 50px icon chip, caption, large value, optional note. Compact=true renders the horizontal desktop strip.
    AccessAppScope: true
    CustomProperties:
      Compact:
        PropertyKind: Input
        DisplayName: Compact
        Description: True renders icon - value - caption in one row (desktop stat strip).
        DataType: Boolean
        Default: =false
      Icon:
        PropertyKind: Input
        DisplayName: Icon
        Description: Fluent icon name.
        DataType: Text
        Default: ="Document"
      Intent:
        PropertyKind: Input
        DisplayName: Intent
        Description: Brand, Success, Warning, Danger, Info or Neutral - drives chip tint and icon colour.
        DataType: Text
        Default: ="Brand"
      Label:
        PropertyKind: Input
        DisplayName: Label
        Description: Caption shown above (or beside) the value.
        DataType: Text
        Default: ="Metric"
      Note:
        PropertyKind: Input
        DisplayName: Note
        Description: Optional footnote under the value. Hidden when Compact.
        DataType: Text
        Default: =""
      OnSelect:
        PropertyKind: Event
        DisplayName: OnSelect
        Description: Raised when the icon chip or the value is selected.
        ReturnType: None
        Default: =false
      Value:
        PropertyKind: Input
        DisplayName: Value
        Description: Display value (already formatted text).
        DataType: Text
        Default: ="0"
    Properties:
      Height: =TileHeight
      Width: =320
    Children:
      - cntTileRoot:
          Control: GroupContainer
          Variant: AutoLayout
          Properties:
            DropShadow: =DropShadow.Light
            Fill: =ColorSurface
            Height: =Parent.Height
            LayoutAlignItems: =LayoutAlignItems.Center
            LayoutDirection: =LayoutDirection.Horizontal
            LayoutGap: =Space3
            PaddingBottom: =If(cmpMetricTile.Compact, Space2, Space3)
            PaddingLeft: =Space4
            PaddingRight: =Space4
            PaddingTop: =If(cmpMetricTile.Compact, Space2, Space3)
            RadiusBottomLeft: =RadiusLarge
            RadiusBottomRight: =RadiusLarge
            RadiusTopLeft: =RadiusLarge
            RadiusTopRight: =RadiusLarge
            Width: =Parent.Width
          Children:
            - cntTileIconChip:
                Control: GroupContainer
                Variant: AutoLayout
                Properties:
                  AlignInContainer: =AlignInContainer.Center
                  DropShadow: =DropShadow.None
                  Fill: =Switch(cmpMetricTile.Intent, "Success", ColorSuccessTint, "Warning", ColorWarningTint, "Danger", ColorDangerTint, "Info", ColorInfoTint, "Neutral", ColorNeutralTint, ColorBrandTint)
                  FillPortions: =0
                  Height: =If(cmpMetricTile.Compact, 40, IconChipSize)
                  LayoutAlignItems: =LayoutAlignItems.Center
                  LayoutDirection: =LayoutDirection.Vertical
                  LayoutJustifyContent: =LayoutJustifyContent.Center
                  LayoutMinHeight: =0
                  LayoutMinWidth: =0
                  RadiusBottomLeft: =RadiusMedium
                  RadiusBottomRight: =RadiusMedium
                  RadiusTopLeft: =RadiusMedium
                  RadiusTopRight: =RadiusMedium
                  Width: =If(cmpMetricTile.Compact, 40, IconChipSize)
                Children:
                  - icoTile:
                      Control: ModernIcon
                      Properties:
                        AccessibleLabel: =cmpMetricTile.Label
                        AlignInContainer: =AlignInContainer.Center
                        Height: =24
                        Icon: =cmpMetricTile.Icon
                        IconColor: =Switch(cmpMetricTile.Intent, "Success", ColorSuccess, "Warning", ColorWarning, "Danger", ColorDanger, "Info", ColorInfo, "Neutral", ColorTextSecondary, ColorBrand)
                        IconStyle: =IconStyle.Filled
                        LayoutMinHeight: =24
                        LayoutMinWidth: =24
                        OnSelect: =cmpMetricTile.OnSelect()
                        Width: =24
            - cntTileText:
                Control: GroupContainer
                Variant: AutoLayout
                Properties:
                  DropShadow: =DropShadow.None
                  FillPortions: =1
                  LayoutAlignItems: =If(cmpMetricTile.Compact, LayoutAlignItems.Center, LayoutAlignItems.Stretch)
                  LayoutDirection: =If(cmpMetricTile.Compact, LayoutDirection.Horizontal, LayoutDirection.Vertical)
                  LayoutGap: =If(cmpMetricTile.Compact, Space2, Space1)
                  LayoutJustifyContent: =LayoutJustifyContent.Center
                  LayoutMinHeight: =0
                  LayoutMinWidth: =0
                  RadiusBottomLeft: =0
                  RadiusBottomRight: =0
                  RadiusTopLeft: =0
                  RadiusTopRight: =0
                Children:
                  - lblTileValue:
                      Control: ModernText
                      Properties:
                        AccessibleLabel: '=cmpMetricTile.Label & ": " & cmpMetricTile.Value'
                        AlignInContainer: =If(cmpMetricTile.Compact, AlignInContainer.Center, AlignInContainer.Stretch)
                        AutoHeight: =true
                        Color: =ColorTextPrimary
                        FillPortions: =0
                        Font: =FontApp
                        FontWeight: =FontWeight.Semibold
                        LayoutMinHeight: =0
                        LayoutMinWidth: =0
                        OnSelect: =cmpMetricTile.OnSelect()
                        PaddingBottom: =0
                        PaddingLeft: =0
                        PaddingRight: =0
                        PaddingTop: =0
                        Size: =If(cmpMetricTile.Compact, FontSizeTitleDesktop, App.Width < BreakpointPhone, FontSizeKpiPhone, App.Width < BreakpointDesktop, FontSizeKpiTablet, FontSizeKpiDesktop)
                        Text: =cmpMetricTile.Value
                        Wrap: =false
                  - lblTileCaption:
                      Control: ModernText
                      Properties:
                        AccessibleLabel: =Self.Text
                        AlignInContainer: =If(cmpMetricTile.Compact, AlignInContainer.Center, AlignInContainer.Stretch)
                        AutoHeight: =true
                        Color: =If(cmpMetricTile.Compact, ColorTextSecondary, ColorTextTertiary)
                        FillPortions: =If(cmpMetricTile.Compact, 1, 0)
                        Font: =FontApp
                        LayoutMinHeight: =0
                        LayoutMinWidth: =0
                        PaddingBottom: =0
                        PaddingLeft: =0
                        PaddingRight: =0
                        PaddingTop: =0
                        Size: =If(cmpMetricTile.Compact, FontSizeBody, FontSizeCaption)
                        Text: =cmpMetricTile.Label
                        Wrap: =false
                  - lblTileNote:
                      Control: ModernText
                      Properties:
                        AccessibleLabel: =Self.Text
                        AlignInContainer: =AlignInContainer.Stretch
                        AutoHeight: =true
                        Color: =ColorTextSecondary
                        FillPortions: =0
                        Font: =FontApp
                        LayoutMinHeight: =0
                        LayoutMinWidth: =0
                        PaddingBottom: =0
                        PaddingLeft: =0
                        PaddingRight: =0
                        PaddingTop: =0
                        Size: =FontSizeCaption
                        Text: =cmpMetricTile.Note
                        Visible: =!cmpMetricTile.Compact && !IsBlank(cmpMetricTile.Note)
                        Wrap: =false
```

Note the child order in `cntTileText` is **value, caption, note** (value first reads best in both modes: stacked "12 / Open requests" and strip "12 Open requests"). This matches the Early Check metric cards' visual weight.

### Components\cmpEmptyState.pa.yaml

```yaml
ComponentDefinitions:
  cmpEmptyState:
    DefinitionType: CanvasComponent
    Description: Centered empty / no-results / permission state - 48px icon, headline, hint, optional primary action.
    AccessAppScope: true
    CustomProperties:
      ActionIcon:
        PropertyKind: Input
        DisplayName: ActionIcon
        Description: Fluent icon for the action button.
        DataType: Text
        Default: ="Add"
      ActionText:
        PropertyKind: Input
        DisplayName: ActionText
        Description: Button text. Button hidden when blank.
        DataType: Text
        Default: =""
      Headline:
        PropertyKind: Input
        DisplayName: Headline
        Description: One-line headline.
        DataType: Text
        Default: ="Nothing here yet"
      Hint:
        PropertyKind: Input
        DisplayName: Hint
        Description: One-line hint about what will appear or what to do.
        DataType: Text
        Default: =""
      Icon:
        PropertyKind: Input
        DisplayName: Icon
        Description: Fluent icon name.
        DataType: Text
        Default: ="DocumentSearch"
      OnAction:
        PropertyKind: Event
        DisplayName: OnAction
        Description: Raised when the action button is selected.
        ReturnType: None
        Default: =false
    Properties:
      Height: =240
      Width: =400
    Children:
      - cntEmptyRoot:
          Control: GroupContainer
          Variant: AutoLayout
          Properties:
            DropShadow: =DropShadow.Light
            Fill: =ColorSurface
            Height: =Parent.Height
            LayoutAlignItems: =LayoutAlignItems.Center
            LayoutDirection: =LayoutDirection.Vertical
            LayoutGap: =Space2
            LayoutJustifyContent: =LayoutJustifyContent.Center
            PaddingBottom: =Space5
            PaddingLeft: =Space5
            PaddingRight: =Space5
            PaddingTop: =Space5
            RadiusBottomLeft: =RadiusLarge
            RadiusBottomRight: =RadiusLarge
            RadiusTopLeft: =RadiusLarge
            RadiusTopRight: =RadiusLarge
            Width: =Parent.Width
          Children:
            - cntEmptyIconChip:
                Control: GroupContainer
                Variant: AutoLayout
                Properties:
                  AlignInContainer: =AlignInContainer.Center
                  DropShadow: =DropShadow.None
                  Fill: =ColorBrandTint
                  FillPortions: =0
                  Height: =64
                  LayoutAlignItems: =LayoutAlignItems.Center
                  LayoutDirection: =LayoutDirection.Vertical
                  LayoutJustifyContent: =LayoutJustifyContent.Center
                  LayoutMinHeight: =0
                  LayoutMinWidth: =0
                  RadiusBottomLeft: =32
                  RadiusBottomRight: =32
                  RadiusTopLeft: =32
                  RadiusTopRight: =32
                  Width: =64
                Children:
                  - icoEmpty:
                      Control: ModernIcon
                      Properties:
                        AccessibleLabel: =cmpEmptyState.Headline
                        AlignInContainer: =AlignInContainer.Center
                        Height: =32
                        Icon: =cmpEmptyState.Icon
                        IconColor: =ColorBrand
                        LayoutMinHeight: =32
                        LayoutMinWidth: =32
                        Width: =32
            - lblEmptyHeadline:
                Control: ModernText
                Properties:
                  AccessibleLabel: =Self.Text
                  Align: =Align.Center
                  AlignInContainer: =AlignInContainer.Stretch
                  AutoHeight: =true
                  Color: =ColorTextPrimary
                  FillPortions: =0
                  Font: =FontApp
                  FontWeight: =FontWeight.Semibold
                  LayoutMinHeight: =0
                  LayoutMinWidth: =0
                  PaddingBottom: =0
                  PaddingLeft: =0
                  PaddingRight: =0
                  PaddingTop: =Space1
                  Size: =FontSizeSection
                  Text: =cmpEmptyState.Headline
            - lblEmptyHint:
                Control: ModernText
                Properties:
                  AccessibleLabel: =Self.Text
                  Align: =Align.Center
                  AlignInContainer: =AlignInContainer.Stretch
                  AutoHeight: =true
                  Color: =ColorTextSecondary
                  FillPortions: =0
                  Font: =FontApp
                  LayoutMinHeight: =0
                  LayoutMinWidth: =0
                  PaddingBottom: =0
                  PaddingLeft: =0
                  PaddingRight: =0
                  PaddingTop: =0
                  Size: =FontSizeBody
                  Text: =cmpEmptyState.Hint
                  Visible: =!IsBlank(cmpEmptyState.Hint)
            - btnEmptyAction:
                Control: ModernButton
                Properties:
                  AccessibleLabel: =cmpEmptyState.ActionText
                  AlignInContainer: =AlignInContainer.Center
                  BasePaletteColor: =ColorBrand
                  Font: =FontApp
                  Height: =TouchTarget
                  Icon: =cmpEmptyState.ActionIcon
                  Layout: =If(IsBlank(cmpEmptyState.ActionIcon), ButtonLayout.TextOnly, ButtonLayout.IconBefore)
                  LayoutMinHeight: =TouchTarget
                  LayoutMinWidth: =0
                  OnSelect: =cmpEmptyState.OnAction()
                  Size: =FontSizeBody
                  Text: =cmpEmptyState.ActionText
                  Tooltip: =cmpEmptyState.ActionText
                  Visible: =!IsBlank(cmpEmptyState.ActionText)
                  Width: =Len(cmpEmptyState.ActionText) * 9 + Space5 * 2 + If(IsBlank(cmpEmptyState.ActionIcon), 0, 24)
```

### Components\cmpPhoneNav.pa.yaml

Bottom tab bar. `Items` is a table `(Key, Label, Icon)`; the component navigates itself (same pattern as `cmpSideNav`, which already owns navigation through app scope) **and** raises `OnSelect(Key)` so a host can react. A horizontal `Gallery` renders the tabs; the template is not AutoLayout, so icon/label/hit-target are positioned with `X/Y` and the transparent `btnNavTab` sits on top as the 44-px+ target (full tab height 64).

```yaml
ComponentDefinitions:
  cmpPhoneNav:
    DefinitionType: CanvasComponent
    Description: Phone bottom tab bar (Items table of Key/Label/Icon). Icon above short label, 2px brand top indicator on the active tab. Navigates itself and raises OnSelect(Key).
    AccessAppScope: true
    CustomProperties:
      ActiveKey:
        PropertyKind: Input
        DisplayName: ActiveKey
        Description: Key of the active tab (Home, NewRequest, DepartmentWork, ResponseCloseout).
        DataType: Text
        Default: ="Home"
      Items:
        PropertyKind: Input
        DisplayName: Items
        Description: Table of Key, Label, Icon.
        DataType: Table
        Default: '=Table({Key: "Home", Label: "Home", Icon: "Home"}, {Key: "NewRequest", Label: "New", Icon: "Add"}, {Key: "DepartmentWork", Label: "Dept work", Icon: "People"}, {Key: "ResponseCloseout", Label: "Closeout", Icon: "CheckmarkCircle"})'
      OnSelect:
        PropertyKind: Event
        DisplayName: OnSelect
        Description: Raised with the selected tab Key after navigation.
        ReturnType: None
        Default: =false
        Parameters:
          - Key:
              Description: Key of the selected tab
              DataType: Text
              Default: =""
    Properties:
      Fill: =ColorSurface
      Height: =PhoneNavHeight
      Width: =App.Width
    Children:
      - cntPhoneNavRoot:
          Control: GroupContainer
          Variant: AutoLayout
          Properties:
            DropShadow: =DropShadow.Light
            Fill: =ColorSurface
            Height: =Parent.Height
            LayoutAlignItems: =LayoutAlignItems.Stretch
            LayoutDirection: =LayoutDirection.Vertical
            RadiusBottomLeft: =RadiusMedium
            RadiusBottomRight: =RadiusMedium
            RadiusTopLeft: =RadiusMedium
            RadiusTopRight: =RadiusMedium
            Width: =Parent.Width
          Children:
            - galPhoneNav:
                Control: Gallery
                Variant: Horizontal
                Properties:
                  AccessibleLabel: ="Primary navigation"
                  FillPortions: =1
                  Items: =cmpPhoneNav.Items
                  LayoutMinHeight: =0
                  LayoutMinWidth: =0
                  ShowScrollbar: =false
                  TabIndex: =-1
                  TemplatePadding: =0
                  TemplateSize: =Parent.Width / Max(1, CountRows(cmpPhoneNav.Items))
                Children:
                  - recNavIndicator:
                      Control: Rectangle
                      Properties:
                        BorderThickness: =0
                        Fill: =If(ThisItem.Key = cmpPhoneNav.ActiveKey, ColorBrand, RGBA(0, 0, 0, 0))
                        Height: =2
                        Width: =Parent.TemplateWidth - Space4
                        X: =Space2
                        Y: =0
                  - icoNavTab:
                      Control: ModernIcon
                      Properties:
                        AccessibleLabel: =ThisItem.Label
                        Height: =24
                        Icon: =ThisItem.Icon
                        IconColor: =If(ThisItem.Key = cmpPhoneNav.ActiveKey, ColorBrand, ColorTextSecondary)
                        IconStyle: =If(ThisItem.Key = cmpPhoneNav.ActiveKey, IconStyle.Filled, IconStyle.Outline)
                        Width: =24
                        X: =(Parent.TemplateWidth - 24) / 2
                        Y: =Space2 + 2
                  - lblNavTab:
                      Control: ModernText
                      Properties:
                        AccessibleLabel: =ThisItem.Label
                        Align: =Align.Center
                        AutoHeight: =false
                        Color: =If(ThisItem.Key = cmpPhoneNav.ActiveKey, ColorBrand, ColorTextSecondary)
                        Font: =FontApp
                        FontWeight: =If(ThisItem.Key = cmpPhoneNav.ActiveKey, FontWeight.Semibold, FontWeight.Normal)
                        Height: =18
                        PaddingBottom: =0
                        PaddingLeft: =0
                        PaddingRight: =0
                        PaddingTop: =0
                        Size: =FontSizeCaption
                        Text: =ThisItem.Label
                        Width: =Parent.TemplateWidth
                        Wrap: =false
                        X: =0
                        Y: =Space2 + 2 + 24 + Space1
                  - btnNavTab:
                      Control: ModernButton
                      Properties:
                        AccessibleLabel: '="Go to " & ThisItem.Label'
                        Appearance: =ButtonAppearance.Transparent
                        Height: =Parent.TemplateHeight
                        Layout: =ButtonLayout.TextOnly
                        OnSelect: |-
                          =Switch(ThisItem.Key,
                            "Home", Navigate(Home, ScreenTransition.None),
                            "NewRequest", Navigate(NewRequest, ScreenTransition.None),
                            "DepartmentWork", Navigate(DepartmentWork, ScreenTransition.None),
                            "ResponseCloseout", Navigate(ResponseCloseout, ScreenTransition.None));
                          cmpPhoneNav.OnSelect(ThisItem.Key)
                        Text: =""
                        Tooltip: =ThisItem.Label
                        Width: =Parent.TemplateWidth
                        X: =0
                        Y: =0
```

**Instance (every screen, appended as the LAST child of `cnt<Screen>Shell`, after the hidden `cmp<Screen>NavBottom`):**
```yaml
            - cmp<Screen>PhoneNav:
                Control: CanvasComponent
                ComponentName: cmpPhoneNav
                Properties:
                  ActiveKey: ="<Home | NewRequest | DepartmentWork | ResponseCloseout>"
                  AlignInContainer: =AlignInContainer.Stretch
                  FillPortions: =0
                  Height: =PhoneNavHeight
                  LayoutMinHeight: =PhoneNavHeight
                  LayoutMinWidth: =0
                  OnSelect: =false
                  Visible: =App.Width < BreakpointPhone
```
`RequestDetail` uses `ActiveKey: ="Home"` (it is a child of the Home journey, like the existing rail instance). On `NewRequest` the phone nav sits **below** `cntNewRequestActions` (sticky bar) — both are shell children; this is the intended phone stacking (form → action bar → tab bar).

## Modified components

### Components\cmpAppHeader.pa.yaml (Modify)

Goal (§5.1): white card, `DropShadow.Light`, `RadiusMedium`, **truly-centered Lato title** via three portions (1 · 2 · 1). The old flat row (`btnHeaderBack`, `cntHeaderTitles`, `btnHeaderSecondary`, `btnHeaderPrimary`) cannot be regrouped without reparenting, so **a new three-container row is appended to `cntHeaderBar`** and the four old children + `cntHeaderDivider` are hidden. Custom properties are unchanged (`Title`, `Subtitle`, `ShowBack`, `PrimaryLabel/Icon`, `SecondaryLabel/Icon`, `OnBack`, `OnPrimary`, `OnSecondary`) so no screen instance changes are required.

Property updates (existing controls):

| Control | Property | New value |
|---|---|---|
| `cmpAppHeader` (component) | `Fill` | `=RGBA(0, 0, 0, 0)` (card look comes from `cntHeaderRoot`) |
| `cntHeaderRoot` | `DropShadow` | `=DropShadow.Light` |
| `cntHeaderRoot` | `RadiusTopLeft/TopRight/BottomLeft/BottomRight` | `=RadiusMedium` |
| `cntHeaderBar` | `LayoutGap` | `=Space2` |
| `cntHeaderBar` | `PaddingLeft`, `PaddingRight` | `=If(App.Width < BreakpointPhone, Space3, Space4)` |
| `btnHeaderBack` | `Visible` | `=false` |
| `cntHeaderTitles` | `Visible` | `=false` |
| `btnHeaderSecondary` | `Visible` | `=false` |
| `btnHeaderPrimary` | `Visible` | `=false` |
| `cntHeaderDivider` | `Visible` | `=false` |

New children appended to `cntHeaderBar` (after `btnHeaderPrimary`):

```yaml
                  - cntHeaderLeft:
                      Control: GroupContainer
                      Variant: AutoLayout
                      Properties:
                        AlignInContainer: =AlignInContainer.Stretch
                        DropShadow: =DropShadow.None
                        FillPortions: =If(App.Width < BreakpointPhone, 0, 1)
                        LayoutAlignItems: =LayoutAlignItems.Center
                        LayoutDirection: =LayoutDirection.Horizontal
                        LayoutGap: =Space3
                        LayoutMinHeight: =0
                        LayoutMinWidth: =0
                        RadiusBottomLeft: =0
                        RadiusBottomRight: =0
                        RadiusTopLeft: =0
                        RadiusTopRight: =0
                        Width: =If(App.Width < BreakpointPhone, If(cmpAppHeader.ShowBack, TouchTarget, 36), 0)
                      Children:
                        - btnHeaderBack2:
                            Control: ModernButton
                            Properties:
                              AccessibleLabel: ="Go back"
                              AlignInContainer: =AlignInContainer.Center
                              Appearance: =ButtonAppearance.Subtle
                              Font: =FontApp
                              Height: =TouchTarget
                              Icon: ="ArrowLeft"
                              Layout: =If(App.Width < BreakpointPhone, ButtonLayout.IconOnly, ButtonLayout.IconBefore)
                              LayoutMinHeight: =TouchTarget
                              LayoutMinWidth: =If(App.Width < BreakpointPhone, TouchTarget, 96)
                              OnSelect: =cmpAppHeader.OnBack()
                              Size: =FontSizeBody
                              Text: ="Back"
                              Tooltip: ="Back"
                              Visible: =cmpAppHeader.ShowBack
                              Width: =If(App.Width < BreakpointPhone, TouchTarget, 96)
                        - cntHeaderLogoChip:
                            Control: GroupContainer
                            Variant: AutoLayout
                            Properties:
                              AlignInContainer: =AlignInContainer.Center
                              DropShadow: =DropShadow.None
                              Fill: =ColorBrand
                              FillPortions: =0
                              Height: =36
                              LayoutAlignItems: =LayoutAlignItems.Center
                              LayoutDirection: =LayoutDirection.Vertical
                              LayoutJustifyContent: =LayoutJustifyContent.Center
                              LayoutMinHeight: =0
                              LayoutMinWidth: =0
                              RadiusBottomLeft: =RadiusMedium
                              RadiusBottomRight: =RadiusMedium
                              RadiusTopLeft: =RadiusMedium
                              RadiusTopRight: =RadiusMedium
                              Visible: =!cmpAppHeader.ShowBack || App.Width >= BreakpointPhone
                              Width: =36
                            Children:
                              - icoHeaderLogo:
                                  Control: ModernIcon
                                  Properties:
                                    AccessibleLabel: ="FOIA"
                                    AlignInContainer: =AlignInContainer.Center
                                    Height: =20
                                    Icon: ="Document"
                                    IconColor: =ColorTextOnBrand
                                    IconStyle: =IconStyle.Filled
                                    LayoutMinHeight: =20
                                    LayoutMinWidth: =20
                                    Width: =20
                        - lblHeaderWordmark:
                            Control: ModernText
                            Properties:
                              AccessibleLabel: =Self.Text
                              AlignInContainer: =AlignInContainer.Center
                              AutoHeight: =true
                              Color: =ColorBrand
                              FillPortions: =0
                              Font: =FontApp
                              FontWeight: =FontWeight.Bold
                              LayoutMinHeight: =0
                              LayoutMinWidth: =0
                              PaddingBottom: =0
                              PaddingLeft: =0
                              PaddingRight: =0
                              PaddingTop: =0
                              Size: =FontSizeSection
                              Text: ="FOIA"
                              Visible: =App.Width >= BreakpointDesktop
                              Wrap: =false
                  - cntHeaderCenter:
                      Control: GroupContainer
                      Variant: AutoLayout
                      Properties:
                        AlignInContainer: =AlignInContainer.Stretch
                        DropShadow: =DropShadow.None
                        FillPortions: =If(App.Width < BreakpointPhone, 1, 2)
                        LayoutAlignItems: =LayoutAlignItems.Stretch
                        LayoutDirection: =LayoutDirection.Vertical
                        LayoutJustifyContent: =LayoutJustifyContent.Center
                        LayoutMinHeight: =0
                        LayoutMinWidth: =0
                        RadiusBottomLeft: =0
                        RadiusBottomRight: =0
                        RadiusTopLeft: =0
                        RadiusTopRight: =0
                      Children:
                        - lblHeaderTitle2:
                            Control: ModernText
                            Properties:
                              AccessibleLabel: =Self.Text
                              Align: =If(App.Width < BreakpointPhone, Align.Left, Align.Center)
                              AlignInContainer: =AlignInContainer.Stretch
                              AutoHeight: =true
                              Color: =ColorTextPrimary
                              FillPortions: =0
                              Font: =FontApp
                              FontWeight: =FontWeight.Semibold
                              LayoutMinHeight: =0
                              LayoutMinWidth: =0
                              PaddingBottom: =0
                              PaddingLeft: =0
                              PaddingRight: =0
                              PaddingTop: =0
                              Size: =If(App.Width < BreakpointPhone, FontSizeTitlePhone, App.Width < BreakpointDesktop, FontSizeTitleTablet, FontSizeTitleDesktop)
                              Text: =cmpAppHeader.Title
                              Wrap: =false
                        - lblHeaderSubtitle2:
                            Control: ModernText
                            Properties:
                              AccessibleLabel: =Self.Text
                              Align: =Align.Center
                              AlignInContainer: =AlignInContainer.Stretch
                              AutoHeight: =true
                              Color: =ColorTextSecondary
                              FillPortions: =0
                              Font: =FontApp
                              LayoutMinHeight: =0
                              LayoutMinWidth: =0
                              PaddingBottom: =0
                              PaddingLeft: =0
                              PaddingRight: =0
                              PaddingTop: =0
                              Size: =FontSizeCaption
                              Text: =cmpAppHeader.Subtitle
                              Visible: =App.Width >= BreakpointPhone && !IsBlank(cmpAppHeader.Subtitle)
                              Wrap: =false
                  - cntHeaderRight:
                      Control: GroupContainer
                      Variant: AutoLayout
                      Properties:
                        AlignInContainer: =AlignInContainer.Stretch
                        DropShadow: =DropShadow.None
                        FillPortions: =If(App.Width < BreakpointPhone, 0, 1)
                        LayoutAlignItems: =LayoutAlignItems.Center
                        LayoutDirection: =LayoutDirection.Horizontal
                        LayoutGap: =Space2
                        LayoutJustifyContent: =LayoutJustifyContent.End
                        LayoutMinHeight: =0
                        LayoutMinWidth: =0
                        RadiusBottomLeft: =0
                        RadiusBottomRight: =0
                        RadiusTopLeft: =0
                        RadiusTopRight: =0
                        Width: =If(App.Width < BreakpointPhone, If(!IsBlank(cmpAppHeader.SecondaryLabel), TouchTarget + Space2, 0) + If(!IsBlank(cmpAppHeader.PrimaryLabel), TouchTarget, 0), 0)
                      Children:
                        - btnHeaderSecondary2:
                            Control: ModernButton
                            Properties:
                              AccessibleLabel: =cmpAppHeader.SecondaryLabel
                              AlignInContainer: =AlignInContainer.Center
                              Appearance: =ButtonAppearance.Subtle
                              Font: =FontApp
                              Height: =TouchTarget
                              Icon: =cmpAppHeader.SecondaryIcon
                              Layout: |-
                                =If(IsBlank(cmpAppHeader.SecondaryIcon), ButtonLayout.TextOnly,
                                    App.Width < BreakpointPhone, ButtonLayout.IconOnly,
                                    ButtonLayout.IconBefore)
                              LayoutMinHeight: =TouchTarget
                              LayoutMinWidth: |-
                                =If(App.Width < BreakpointPhone && !IsBlank(cmpAppHeader.SecondaryIcon), TouchTarget,
                                    Len(cmpAppHeader.SecondaryLabel) * 9 + Space5 * 2 + If(IsBlank(cmpAppHeader.SecondaryIcon), 0, 24))
                              OnSelect: =cmpAppHeader.OnSecondary()
                              Size: =FontSizeBody
                              Text: =cmpAppHeader.SecondaryLabel
                              Tooltip: =cmpAppHeader.SecondaryLabel
                              Visible: =!IsBlank(cmpAppHeader.SecondaryLabel)
                              Width: |-
                                =If(App.Width < BreakpointPhone && !IsBlank(cmpAppHeader.SecondaryIcon), TouchTarget,
                                    Len(cmpAppHeader.SecondaryLabel) * 9 + Space5 * 2 + If(IsBlank(cmpAppHeader.SecondaryIcon), 0, 24))
                        - btnHeaderPrimary2:
                            Control: ModernButton
                            Properties:
                              AccessibleLabel: =cmpAppHeader.PrimaryLabel
                              AlignInContainer: =AlignInContainer.Center
                              Appearance: =ButtonAppearance.Primary
                              BasePaletteColor: =ColorBrand
                              Font: =FontApp
                              Height: =TouchTarget
                              Icon: =cmpAppHeader.PrimaryIcon
                              Layout: |-
                                =If(IsBlank(cmpAppHeader.PrimaryIcon), ButtonLayout.TextOnly,
                                    App.Width < BreakpointPhone, ButtonLayout.IconOnly,
                                    ButtonLayout.IconBefore)
                              LayoutMinHeight: =TouchTarget
                              LayoutMinWidth: |-
                                =If(App.Width < BreakpointPhone && !IsBlank(cmpAppHeader.PrimaryIcon), TouchTarget,
                                    Len(cmpAppHeader.PrimaryLabel) * 9 + Space5 * 2 + If(IsBlank(cmpAppHeader.PrimaryIcon), 0, 24))
                              OnSelect: =cmpAppHeader.OnPrimary()
                              Size: =FontSizeBody
                              Text: =cmpAppHeader.PrimaryLabel
                              Tooltip: =cmpAppHeader.PrimaryLabel
                              Visible: =!IsBlank(cmpAppHeader.PrimaryLabel)
                              Width: |-
                                =If(App.Width < BreakpointPhone && !IsBlank(cmpAppHeader.PrimaryIcon), TouchTarget,
                                    Len(cmpAppHeader.PrimaryLabel) * 9 + Space5 * 2 + If(IsBlank(cmpAppHeader.PrimaryIcon), 0, 24))
```

### Components\cmpSideNav.pa.yaml (Modify)

Goal (§4 / §5.2): 50-px icon rail, 42-px items, active item = `ColorBrandTint` rounded square + `ColorBrand` filled icon, GridDots expander at the top toggling a 220-px labelled rail. `ModernButton` has no `Fill`, so each new item is a tinted `GroupContainer` wrapping a Subtle button — new sub-trees appended to `cntNavItems`; the four old buttons and both dividers are hidden. The `Placement = "Bottom"` branch stays in the formulas (instances are hidden, not deleted).

Add custom property:
```yaml
      Expanded:
        PropertyKind: Input
        DisplayName: Expanded
        Description: True shows icon + label at RailWidthExpanded; false is the 50px icon rail. Hosts pass gblNavExpanded.
        DataType: Boolean
        Default: =false
```
App-scope dependency: `gblNavExpanded` (toggled by `btnNavExpand`, seeded in `App.OnStart`) — justified as shell state shared by every screen, same class as `colToasts`.

Property updates (existing controls):

| Control | Property | New value |
|---|---|---|
| `cmpSideNav` (component) | `Width` | `=If(cmpSideNav.Placement = "Bottom", App.Width, If(cmpSideNav.Expanded, RailWidthExpanded, RailWidth))` |
| `cmpSideNav` (component) | `Fill` | `=RGBA(0, 0, 0, 0)` |
| `cntNavRoot` | `DropShadow` | `=If(cmpSideNav.Placement = "Rail", DropShadow.Light, DropShadow.None)` |
| `cntNavRoot` | `RadiusTopLeft/TopRight/BottomLeft/BottomRight` | `=RadiusMedium` |
| `cntNavDividerTop` | `Visible` | `=false` |
| `cntNavDividerSide` | `Visible` | `=false` |
| `cntNavItems` | `LayoutGap` | `=Space1` |
| `cntNavItems` | `PaddingLeft`, `PaddingRight` | `=Space1` |
| `cntNavItems` | `PaddingTop` | `=Space2` |
| `cntNavItems` | `LayoutAlignItems` | `=If(cmpSideNav.Placement = "Bottom", LayoutAlignItems.Center, LayoutAlignItems.Start)` |
| `btnNavHome`, `btnNavNewRequest`, `btnNavDepartmentWork`, `btnNavResponseCloseout` | `Visible` | `=false` |

New children appended to `cntNavItems` (after `btnNavResponseCloseout`). `btnNavExpand` first, then one `cntNavItem*` per destination. Only `cntNavItemHome` is spelled out; the other three are identical with the substitutions in the table below.

```yaml
                  - btnNavExpand:
                      Control: ModernButton
                      Properties:
                        AccessibleLabel: =If(cmpSideNav.Expanded, "Collapse navigation", "Expand navigation")
                        AlignInContainer: =AlignInContainer.Start
                        Appearance: =ButtonAppearance.Subtle
                        Color: =ColorTextSecondary
                        Height: =RailWidth - Space2
                        Icon: ="GridDots"
                        Layout: =ButtonLayout.IconOnly
                        LayoutMinHeight: =RailWidth - Space2
                        LayoutMinWidth: =RailWidth - Space2
                        OnSelect: =Set(gblNavExpanded, !gblNavExpanded)
                        Size: =FontSizeBody
                        Text: ="Menu"
                        Tooltip: =If(cmpSideNav.Expanded, "Collapse", "Expand")
                        Visible: =cmpSideNav.Placement = "Rail"
                        Width: =RailWidth - Space2
                  - cntNavItemHome:
                      Control: GroupContainer
                      Variant: AutoLayout
                      Properties:
                        AlignInContainer: =AlignInContainer.Start
                        DropShadow: =DropShadow.None
                        Fill: =If(cmpSideNav.ActiveScreen = "Home", ColorBrandTint, RGBA(0, 0, 0, 0))
                        FillPortions: =0
                        Height: =RailWidth - Space2
                        LayoutAlignItems: =LayoutAlignItems.Center
                        LayoutDirection: =LayoutDirection.Horizontal
                        LayoutMinHeight: =0
                        LayoutMinWidth: =0
                        RadiusBottomLeft: =RadiusMedium
                        RadiusBottomRight: =RadiusMedium
                        RadiusTopLeft: =RadiusMedium
                        RadiusTopRight: =RadiusMedium
                        Visible: =cmpSideNav.Placement = "Rail"
                        Width: =If(cmpSideNav.Expanded, Parent.Width - Space1 * 2, RailWidth - Space2)
                      Children:
                        - btnNavHome2:
                            Control: ModernButton
                            Properties:
                              AccessibleLabel: ="Go to Home"
                              Align: =Align.Left
                              AlignInContainer: =AlignInContainer.Stretch
                              Appearance: =ButtonAppearance.Subtle
                              Color: =If(cmpSideNav.ActiveScreen = "Home", ColorBrand, ColorTextSecondary)
                              FillPortions: =1
                              Font: =FontApp
                              FontWeight: =If(cmpSideNav.ActiveScreen = "Home", FontWeight.Semibold, FontWeight.Normal)
                              Height: =RailWidth - Space2
                              Icon: ="Home"
                              IconStyle: =If(cmpSideNav.ActiveScreen = "Home", IconStyle.Filled, IconStyle.Outline)
                              Layout: =If(cmpSideNav.Expanded, ButtonLayout.IconBefore, ButtonLayout.IconOnly)
                              LayoutMinHeight: =0
                              LayoutMinWidth: =0
                              OnSelect: =Navigate(Home, ScreenTransition.None)
                              Size: =FontSizeBody
                              Text: ="Home"
                              Tooltip: ="Home"
```

| Container / button | `ActiveScreen` value | `Icon` | `Text` / `Tooltip` | `AccessibleLabel` | `OnSelect` |
|---|---|---|---|---|---|
| `cntNavItemHome` / `btnNavHome2` | `"Home"` | `"Home"` | `"Home"` | `"Go to Home"` | `Navigate(Home, ScreenTransition.None)` |
| `cntNavItemNewRequest` / `btnNavNewRequest2` | `"NewRequest"` | `"Add"` | `"New request"` | `"Go to New request"` | `Navigate(NewRequest, ScreenTransition.None)` |
| `cntNavItemDepartmentWork` / `btnNavDepartmentWork2` | `"DepartmentWork"` | `"People"` | `"Department work"` | `"Go to Department work"` | `Navigate(DepartmentWork, ScreenTransition.None)` |
| `cntNavItemResponseCloseout` / `btnNavResponseCloseout2` | `"ResponseCloseout"` | `"CheckmarkCircle"` | `"Closeout"` | `"Go to Closeout"` | `Navigate(ResponseCloseout, ScreenTransition.None)` |

### Components\cmpStatusBadge.pa.yaml (Modify — property-only)

| Control | Property | New value |
|---|---|---|
| `bdgStatus` | `Appearance` | `=BadgeAppearance.Tint` |
| `bdgStatus` | `Font` | `=FontApp` |
| `bdgStatus` | `RadiusTopLeft/TopRight/BottomLeft/BottomRight` | `=RadiusMedium` |
| `bdgStatus` | `Height` | `=24` |
| `bdgStatus` | `Intent` | keep the existing Switch, but change `"In Progress"` → `BadgeIntent.Caution` and `"On Hold"` → `BadgeIntent.Attention` (matches the §4 map: In Progress = Warning). |

The leading status icon already provides the non-colour cue ("leading dot/icon"). No structural change.

## Per-screen edit specifications

### Shared edits (apply to all five screens first)

1. **Shell retokenise** — `cnt<Screen>Shell`: `Fill: =ColorCanvas`, `LayoutGap: =Space2`, `PaddingLeft/Right/Top/Bottom: =Space2`. Screen `Fill: =ColorCanvas`.
2. **Body gap** — `cnt<Screen>Body`: `LayoutGap: =Space2`, `Fill: =ColorCanvas`. `cnt<Screen>ContentOuter` and `cnt<Screen>Content`: `Fill: =ColorCanvas`.
3. **Rail instance** — `cmp<Screen>NavRail`: `Width: =If(gblNavExpanded, RailWidthExpanded, RailWidth)`, `LayoutMinWidth: =RailWidth`, add `Expanded: =gblNavExpanded`. (`Placement`, `ActiveScreen`, `Visible` unchanged.)
4. **Old bottom nav** — `cmp<Screen>NavBottom`: `Visible: =false` (keep all other properties).
5. **Phone nav** — append `cmp<Screen>PhoneNav` (instance block above) as the **last child of the shell**.
6. **Toast host** — append `cmpToastHost` (instance block above) as the **last child of the Screen** (sibling after the shell).
7. **Content padding** — `cnt<Screen>Content`: `PaddingLeft/Right: =If(App.Width < BreakpointPhone, Space4, App.Width < BreakpointDesktop, Space5, Max(Space5, (Parent.Width - ContentMaxWidth) / 2))`, `PaddingTop/Bottom: =If(App.Width < BreakpointPhone, Space3, Space4)`.
8. **Cards** — every white card container listed per screen: `BorderThickness: =0`, `DropShadow: =DropShadow.Light`, `Radius*: =RadiusLarge`.
9. **Fonts** — add `Font: =FontApp` to every `ModernText`, `ModernButton`, `ModernBadge`, `ModernTextInput`, `ModernDropdown`, `ModernCombobox`, `ModernDatePicker`, `ModernTabList` you touch (do not hunt for every label; titles, captions, buttons and inputs on the edited paths are enough — the shared components already carry Lato).
10. **Notify → SendToast** — replace every `Notify(...)` per the intent table; keep the surrounding `IfError` and `Set(...)` statements intact.

### Home (Existing)
- **File:** `Home.pa.yaml`
- **Current state:** shell → header → body (rail + content) → bottom nav. Content: `cntHomeKpis` (4 bespoke tiles), `cntHomeDistribution` (desktop strip), `cntHomeMasterDetail` (`cntHomeListPane` with `cntHomeFilters` + status labels + `galRequests`; `cntHomeDetailPane` with `cntHomeDetailEmpty` + `cmpHomeDetailPane`).
- **Changes required:**
  1. Shared edits 1–10.
  2. **Metric tiles** — set `Visible: =false` on `cntTileTotal`, `cntTileOpen`, `cntTileDueSoon`, `cntTileClosed`. Append four `cmpMetricTile` instances to `cntHomeKpis` (block below). `cntHomeKpis.Height` stays as is (`TileHeight * 4 + …` / `TileHeight * 2 + …` / `StatStripHeight`).
  3. **Distribution strip** — `cntHomeDistribution`: wrap look = `Fill: =ColorSurface`, `DropShadow: =DropShadow.Light`, `Radius*: =RadiusLarge`, `PaddingLeft/Right: =Space4`, `PaddingTop/Bottom: =Space3`, `Height: =Space3 * 2 + Space2 + Space1 + 20`. Segment fills: `cntSegNew` `ColorInfo`, `cntSegInProgress` `ColorWarning`, `cntSegOnHold` `ColorTextTertiary`, `cntSegClosed` `ColorSuccess` (verify/replace the current literals). Legend labels: `Font: =FontApp`, `Color: =ColorTextSecondary`.
  4. **Filters** — `txtSearch`: `Placeholder: ="Search requests…"`, `Radius*: =RadiusLarge`, `Appearance: =Appearance.FilledLighter`, `Font: =FontApp`. `cmbStatusFilter`: `ItemDisplayText: '="Status: " & ThisItem.Value'`, `Default: =LookUp(["All", "New", "In Progress", "On Hold", "Closed"], Value = gblStatusFilter)`, `Radius*: =RadiusLarge`, `Font: =FontApp`. `cmbDepartmentFilter`: `ItemDisplayText: '="Department: " & ThisItem.Value'`, `Default: =LookUp(Ungroup(Table({Options: Table({Value: "All"})}, {Options: Distinct(Filter('FOIA Pilot Departments', Active = true), Title)}), Options), Value = gblDepartmentFilter)`, `Radius*: =RadiusLarge`, `Font: =FontApp`, keep `Visible`. `cntHomeFilters.Height`: phone `InputHeight * 3 + Space2 * 2`, tablet `InputHeight`, desktop `InputHeight * 4 + Space2 * 3` (one extra row for Reset). Append `btnResetFilters` to `cntHomeFilters`:
     ```yaml
                                                - btnResetFilters:
                                                    Control: ModernButton
                                                    Properties:
                                                      AccessibleLabel: ="Reset filters"
                                                      AlignInContainer: =AlignInContainer.Stretch
                                                      Appearance: =ButtonAppearance.Subtle
                                                      Font: =FontApp
                                                      Height: =InputHeight
                                                      Icon: ="ArrowReset"
                                                      Layout: =ButtonLayout.IconBefore
                                                      LayoutMinHeight: =InputHeight
                                                      LayoutMinWidth: =0
                                                      OnSelect: |-
                                                        =Set(gblStatusFilter, "All");
                                                        Set(gblDepartmentFilter, "All");
                                                        Set(gblSearchText, "");
                                                        Reset(txtSearch);
                                                        Reset(cmbStatusFilter);
                                                        Reset(cmbDepartmentFilter)
                                                      Size: =FontSizeBody
                                                      Text: ="Reset"
                                                      Tooltip: ="Clear search and filters"
                                                      Visible: =gblStatusFilter <> "All" || gblDepartmentFilter <> "All" || !IsBlank(gblSearchText)
                                                      Width: =If(App.Width >= BreakpointPhone && App.Width < BreakpointDesktop, 110, Parent.Width)
     ```
     (If `"ArrowReset"` is rejected by the checker use `"ArrowUndo"`, then `"Dismiss"`.)
  5. **Gallery rows** — `galRequests`: `TemplateSize: =If(App.Width < BreakpointPhone, 92, 80)` and update the two height formulas that repeat it (`galRequests.Height`, `cntHomeMasterDetail.Height`, `cntHomeListPane.Height`: replace `76` with `80`). Desktop branch of `galRequests.Height`: wrap with `If(Self.AllItemsCount = 0, 0, <existing Max(...)>)` so the empty state can take the space. `cntRequestRow`: `BorderThickness: =0`, `DropShadow: =DropShadow.Light`, `RadiusTopLeft: =0`, `RadiusBottomLeft: =0`, `RadiusTopRight: =RadiusMedium`, `RadiusBottomRight: =RadiusMedium`, `PaddingLeft: =Space4 + StatusAccentWidth`, `Fill: =If(ThisItem.ID = gblSelectedRequest.ID, ColorBrandTint, ColorSurface)` (selected tint at every tier). `bdgRequestRowStatus`: `Appearance: =BadgeAppearance.Tint`, `Font: =FontApp`, `Radius*: =RadiusMedium`, change `"In Progress"` → `BadgeIntent.Caution`, `"On Hold"` → `BadgeIntent.Attention`. `btnRequestRowOpen`: `Visible: =true`, `Appearance: =ButtonAppearance.Transparent`, `Color: =ColorTextTertiary`, `Width: =32`, `LayoutMinWidth: =32`. Append to `galRequests.Children` (after `cntRequestRow`):
     ```yaml
                                                - recRequestAccent:
                                                    Control: Rectangle
                                                    Properties:
                                                      BorderThickness: =0
                                                      Fill: |-
                                                        =Switch(ThisItem.OverallStatus.Value,
                                                          "New", ColorInfo,
                                                          "In Progress", ColorWarning,
                                                          "On Hold", ColorTextTertiary,
                                                          "Ready", ColorBrand,
                                                          "Delivered", ColorSuccess,
                                                          "Closed", ColorSuccess,
                                                          "Complete", ColorSuccess,
                                                          "Overdue", ColorDanger,
                                                          ColorBorder)
                                                      Height: =Parent.TemplateHeight
                                                      TabIndex: =-1
                                                      Width: =StatusAccentWidth
                                                      X: =0
                                                      Y: =0
     ```
  6. **Empty state** — `lblQueueEmpty`: `Visible: =false`. Append `cmpHomeEmpty` to `cntHomeListPane` (after `galRequests`):
     ```yaml
                                          - cmpHomeEmpty:
                                              Control: CanvasComponent
                                              ComponentName: cmpEmptyState
                                              Properties:
                                                ActionIcon: ="Add"
                                                ActionText: =If(gblStatusFilter <> "All" || gblDepartmentFilter <> "All" || !IsBlank(gblSearchText), "Reset filters", "New request")
                                                AlignInContainer: =AlignInContainer.Stretch
                                                FillPortions: =If(App.Width >= BreakpointDesktop, 1, 0)
                                                Headline: =If(gblStatusFilter <> "All" || gblDepartmentFilter <> "All" || !IsBlank(gblSearchText), "No requests match these filters", "No FOIA requests yet")
                                                Height: =If(App.Width >= BreakpointDesktop, Parent.Height, 240)
                                                Hint: ="Requests appear here as they are received. Summary, assignments and activity open on the right on desktop."
                                                Icon: ="DocumentSearch"
                                                LayoutMinHeight: =0
                                                LayoutMinWidth: =0
                                                OnAction: |-
                                                  =If(gblStatusFilter <> "All" || gblDepartmentFilter <> "All" || !IsBlank(gblSearchText),
                                                    Set(gblStatusFilter, "All"); Set(gblDepartmentFilter, "All"); Set(gblSearchText, ""); Reset(txtSearch); Reset(cmbStatusFilter); Reset(cmbDepartmentFilter),
                                                    Navigate(NewRequest, ScreenTransition.Fade))
                                                Visible: =!gblIsLoading && !gblLoadError && !gblPermissionDenied && galRequests.AllItemsCount = 0
     ```
     Update the non-desktop height sums in `cntHomeMasterDetail.Height` and `cntHomeListPane.Height`: replace `If(lblQueueEmpty.Visible, lblQueueEmpty.Height, 0)` with `If(cmpHomeEmpty.Visible, 240 + Space2, 0)`.
  7. **Detail pane card** — `cntHomeDetailEmpty`: shared edit 8 plus `Fill: =ColorSurface`. `cmpHomeDetailPane.OnConfirmDueDate`: replace the two `Notify` calls with `cmpToastHost.SendToast("Due date confirmed", "CheckmarkCircle", ColorSuccess, true, "Statutory deadline locked for " & Coalesce(gblSelectedRequest.Title, "this request") & ".")` and `cmpToastHost.SendToast("Couldn't confirm the due date", "DismissCircle", ColorDanger, true, FirstError.Message, 600000, true, false, false)`.
  8. **Header instance** — `cmpHomeHeader.OnSecondary` (Refresh): after `Set(gblIsLoading, false)` add `; cmpToastHost.SendToast("Queue refreshed", "Info", ColorInfo, false, "", 5000, true, true, true)`.
- **Controls to add:** `cmpTileTotal`, `cmpTileOpen`, `cmpTileDueSoon`, `cmpTileClosed` (→ `cntHomeKpis`), `btnResetFilters` (→ `cntHomeFilters`), `recRequestAccent` (→ `galRequests`), `cmpHomeEmpty` (→ `cntHomeListPane`), `cmpHomePhoneNav` (→ `cntHomeShell`), `cmpToastHost` (→ Screen).
- **Controls to remove:** none (hidden: `cntTile*` ×4, `lblQueueEmpty`, `cmpHomeNavBottom`).

Metric-tile instances (all four share this shape; only `Label/Value/Icon/Intent/Note` differ):
```yaml
                                    - cmpTileTotal:
                                        Control: CanvasComponent
                                        ComponentName: cmpMetricTile
                                        Properties:
                                          AlignInContainer: =AlignInContainer.Start
                                          Compact: =App.Width >= BreakpointDesktop
                                          FillPortions: =0
                                          Height: =If(App.Width >= BreakpointDesktop, StatStripHeight, TileHeight)
                                          Icon: ="Document"
                                          Intent: ="Brand"
                                          Label: ="Total requests"
                                          LayoutMaxWidth: =If(App.Width >= BreakpointDesktop, TileMaxWidth, 0)
                                          LayoutMinHeight: =0
                                          LayoutMinWidth: =0
                                          Note: ="All requests on record"
                                          OnSelect: =Set(gblStatusFilter, "All"); Reset(cmbStatusFilter)
                                          Value: =Text(CountRows('FOIA Pilot Requests'))
                                          Width: =If(App.Width < BreakpointPhone, Parent.Width, App.Width < BreakpointDesktop, (Parent.Width - Space4) / 2 - 1, (Parent.Width - Space4 * 3) / 4 - 1)
```

| Instance | Label | Value | Icon | Intent | Note | OnSelect |
|---|---|---|---|---|---|---|
| `cmpTileTotal` | `"Total requests"` | `Text(CountRows('FOIA Pilot Requests'))` | `"Document"` | `"Brand"` | `"All requests on record"` | `Set(gblStatusFilter, "All"); Reset(cmbStatusFilter)` |
| `cmpTileOpen` | `"Open"` | `Text(CountRows(Filter('FOIA Pilot Requests', OverallStatus.Value <> "Closed")))` | `"DocumentSearch"` | `"Info"` | `"New, in progress or on hold"` | `Set(gblStatusFilter, "All"); Reset(cmbStatusFilter)` |
| `cmpTileDueSoon` | `"Due within 7 days"` | `Text(CountRows(Filter('FOIA Pilot Requests', DueDateConfirmed = true && DueDate <= DateAdd(Today(), 7, TimeUnit.Days))))` | `"Warning"` | `"Warning"` | `"Confirmed due dates only"` | `Set(gblStatusFilter, "In Progress"); Reset(cmbStatusFilter)` |
| `cmpTileClosed` | `"Closed"` | `Text(CountRows(Filter('FOIA Pilot Requests', OverallStatus.Value = "Closed")))` | `"CheckmarkCircle"` | `"Success"` | `"Final response sent"` | `Set(gblStatusFilter, "Closed"); Reset(cmbStatusFilter)` |

### NewRequest (Existing)
- **File:** `NewRequest.pa.yaml`
- **Current state:** shell → header (ShowBack) → body (rail + content → `cntNewRequestColumns` → `cntNewRequestForm` [`cntCardRequester`, `cntCardRequest`, `cntCardDates`, 4 status labels] + `cntIntakeGuidance` desktop panel) → `cntNewRequestActions` (sticky: `btnCancelRequest`, `btnSaveRequest`) → bottom nav. Save is `IfError(Set(gblSelectedRequest, Patch(...)); …Navigate(RequestDetail…), …Notify(error))`. Save is currently disabled until every required field is valid.
- **Changes required:**
  1. Shared edits 1–10.
  2. **Screen OnVisible** — append `; UpdateContext({locShowValidation: false})`.
  3. **Section cards** — `cntCardRequester`, `cntCardRequest`, `cntCardDates`, `cntIntakeGuidance`: shared edit 8 (`BorderThickness 0`, `DropShadow.Light`, `RadiusLarge`), `PaddingLeft/Right/Top/Bottom: =Space5` on desktop/tablet (`=If(App.Width < BreakpointPhone, Space4, Space5)`), and update each card's `Height` formula to use the same padding token twice (e.g. `cntCardRequester.Height: =If(App.Width < BreakpointPhone, Space4, Space5) * 2 + lblRequesterSection.Height + Space2 + cntRequesterFields.Height`; do the equivalent for `cntCardRequest`, `cntCardDates`, `cntIntakeGuidance`). Section titles (`lblRequesterSection`, `lblRequestSection`, `lblDatesSection`, `lblGuidanceTitle`): `Font: =FontApp`, `Size: =FontSizeSection`, `Color: =ColorBrandAlt`.
  4. **Required-field labels** — the eight labels whose text ends in ` *` (`lblRequesterFirstName`, `lblRequesterLastName`, `lblRequestDescription`, `lblPrimaryDepartment`, `lblIntakeMethod`, `lblRequestRoute`, `lblReceivedDate`, `lblDueDate`): `Color: =If(locShowValidation && <field blank test>, ColorDanger, ColorTextSecondary)` and `AccessibleLabel: =Self.Text & " (required)"`. Blank tests: `IsBlank(txtRequesterFirstName.Text)`, `IsBlank(txtRequesterLastName.Text)`, `IsBlank(txtRequestDescription.Text)`, `IsBlank(cmbPrimaryDepartment.Selected)`, `IsBlank(cmbIntakeMethod.Selected)`, `IsBlank(cmbRequestRoute.Selected)`, `IsBlank(datReceivedDate.SelectedDate)`, `IsBlank(datDueDate.SelectedDate)`.
  5. **Inline validation on inputs** — `txtRequesterFirstName`, `txtRequesterLastName`, `txtRequestDescription`, `cmbPrimaryDepartment`, `cmbIntakeMethod`, `cmbRequestRoute`: `ValidationState: =If(locShowValidation && <blank test>, ValidationState.Error, ValidationState.None)`. (`ModernDatePicker` has no `ValidationState`; the red label is its cue.) All inputs: `Radius*: =RadiusMedium`, `Font: =FontApp`.
  6. **Due-date confirmation cue** — `lblDueDateHelp`: `Color: =If(locShowValidation && !gblDueDateConfirmed, ColorDanger, ColorTextSecondary)`.
  7. **Validation summary** — `lblRequestValidation`: `Text: ="Complete the fields marked in red and confirm the working due date."`, `Color: =ColorDanger`, `Visible: =locShowValidation && (<full invalid test>)` where the full invalid test is the existing Save `DisplayMode` condition minus `gblPermissionDenied`. `lblRequestSuccess`: `Visible: =false` (toast replaces it). Update `cntNewRequestForm.Height` only if you change which labels are visible (it already sums `lblRequestValidation.Visible`).
  8. **Save button** — `btnSaveRequest`: `DisplayMode: =If(gblPermissionDenied || gblIsLoading, DisplayMode.Disabled, DisplayMode.Edit)`, `Text: =If(gblIsLoading, "Saving…", "Save request")`, `Appearance: =ButtonAppearance.Primary`, `Font: =FontApp`, `Radius*: =RadiusMedium`, `Icon: ="Save"`, `Layout: =ButtonLayout.IconBefore`. `OnSelect`:
     ```powerfx
     UpdateContext({locShowValidation: true});
     If(
       IsBlank(txtRequesterFirstName.Text) || IsBlank(txtRequesterLastName.Text) || IsBlank(txtRequestDescription.Text) || IsBlank(cmbPrimaryDepartment.Selected) || IsBlank(cmbRequestRoute.Selected) || IsBlank(cmbIntakeMethod.Selected) || IsBlank(datReceivedDate.SelectedDate) || IsBlank(datDueDate.SelectedDate) || !gblDueDateConfirmed,
       cmpToastHost.SendToast("Complete the required fields", "Warning", ColorWarning, true, "Fields marked in red are required and the working due date must be confirmed.", 10000),
       Set(gblIsLoading, true);
       Set(gblLoadError, false);
       Set(gblSaveSuccess, false);
       IfError(
         Set(gblSelectedRequest, Patch( <existing Patch unchanged> ));
         Set(gblIsLoading, false);
         Set(gblSaveSuccess, true);
         cmpToastHost.SendToast("Request saved", "CheckmarkCircle", ColorSuccess, true, Coalesce(gblSelectedRequest.Title, "New request") & " is now New and ready for assignment.");
         Navigate(RequestDetail, ScreenTransition.Fade),
         Set(gblIsLoading, false);
         Set(gblLoadError, true);
         cmpToastHost.SendToast("Couldn't save the request", "DismissCircle", ColorDanger, true, FirstError.Message, 600000, true, false, false)
       )
     )
     ```
     Keep the Patch body byte-for-byte (it is the proven v2 write).
  9. **Sticky bar** — `cntNewRequestActions`: `BorderThickness: =0`, `DropShadow: =DropShadow.Light`, `Radius*: =RadiusMedium`, `Fill: =ColorSurface`, `PaddingLeft/Right: =If(App.Width < BreakpointPhone, Space4, Space5)`. `btnCancelRequest`: `Appearance: =ButtonAppearance.Secondary`, `Font: =FontApp`, `Radius*: =RadiusMedium`.
  10. **Guidance panel** — `cntIntakeGuidance` is the desktop supplementary panel; keep it, add a tinted chip feel: `Fill: =ColorSurface`, and set `lblGuidanceTitle.Color: =ColorBrandAlt`.
- **Controls to add:** `cmpNewRequestPhoneNav` (→ shell, last), `cmpToastHost` (→ Screen).
- **Controls to remove:** none (hidden: `lblRequestSuccess`, `cmpNewRequestNavBottom`).

### RequestDetail (Existing)
- **File:** `RequestDetail.pa.yaml`
- **Current state:** shell → header (Back, primary "Closeout") → body (rail + content → `cntRequestDetailEmpty` + `cmpRequestDetailPaneHost`) → bottom nav. The pane host carries the three event handlers (`OnConfirmDueDate` with Notify, `OnOpenCloseout`, `OnOpenDepartmentWork`).
- **Changes required:**
  1. Shared edits 1–10.
  2. **Retire the old host** — `cmpRequestDetailPaneHost`: `Visible: =false`, `OnConfirmDueDate: =false` (so no stale Notify remains).
  3. **Empty card** — `cntRequestDetailEmpty`: shared edit 8.
  4. **Append `cntDetailStack`** as the last child of `cntRequestDetailContent`. It holds the approval-flow stepper (inline native controls per §4 `cmpStepper`) and a **fresh** `cmpRequestDetailPane` instance (`cmpRequestDetailPane2`) with the same three handlers (Notify → SendToast). Stage index: `New`=1, `Assigned`=2 (any active assignment exists), `In Progress`=3, `Closed`=4 — computed inline as
     `locStage` is **not** a variable; use the expression `If(gblSelectedRequest.OverallStatus.Value = "Closed", 4, gblSelectedRequest.OverallStatus.Value = "In Progress", 3, CountRows(Filter('FOIA Pilot Assignments', Request.Id = gblSelectedRequest.ID && Active = true)) > 0, 2, 1)` wherever `<stage>` appears below (repeat it; do not create a named formula because it reads a global).

```yaml
                              - cntDetailStack:
                                  Control: GroupContainer
                                  Variant: AutoLayout
                                  Properties:
                                    AlignInContainer: =AlignInContainer.Stretch
                                    DropShadow: =DropShadow.None
                                    FillPortions: =1
                                    LayoutAlignItems: =LayoutAlignItems.Stretch
                                    LayoutDirection: =LayoutDirection.Vertical
                                    LayoutGap: =Space4
                                    LayoutMinHeight: =0
                                    LayoutMinWidth: =0
                                    RadiusBottomLeft: =0
                                    RadiusBottomRight: =0
                                    RadiusTopLeft: =0
                                    RadiusTopRight: =0
                                    Visible: =!IsBlank(gblSelectedRequest)
                                  Children:
                                    - cntDetailStepperCard:
                                        Control: GroupContainer
                                        Variant: AutoLayout
                                        Properties:
                                          DropShadow: =DropShadow.Light
                                          Fill: =ColorSurface
                                          FillPortions: =0
                                          Height: =If(App.Width < BreakpointPhone, Space4 * 2 + 4 * (StepperCircleSize + Space3) + Space2, Space4 * 2 + StepperCircleSize + Space2 + 18)
                                          LayoutAlignItems: =If(App.Width < BreakpointPhone, LayoutAlignItems.Stretch, LayoutAlignItems.Start)
                                          LayoutDirection: =If(App.Width < BreakpointPhone, LayoutDirection.Vertical, LayoutDirection.Horizontal)
                                          LayoutGap: =If(App.Width < BreakpointPhone, Space3, 0)
                                          LayoutJustifyContent: =LayoutJustifyContent.Center
                                          LayoutMinHeight: =0
                                          LayoutMinWidth: =0
                                          PaddingBottom: =Space4
                                          PaddingLeft: =Space5
                                          PaddingRight: =Space5
                                          PaddingTop: =Space4
                                          RadiusBottomLeft: =RadiusLarge
                                          RadiusBottomRight: =RadiusLarge
                                          RadiusTopLeft: =RadiusLarge
                                          RadiusTopRight: =RadiusLarge
                                        Children:
                                          # repeat the following step block 4x: Step 1 "New", Step 2 "Assigned", Step 3 "In Progress", Step 4 "Closed"
                                          # (connector `cntStepConn<N>`/`recStepLine<N>` is omitted after step 4). Steps align to the TOP of the card row so the 2px line (centered in a circle-height container) runs through the circle centres.
                                          - cntStep1:
                                              Control: GroupContainer
                                              Variant: AutoLayout
                                              Properties:
                                                DropShadow: =DropShadow.None
                                                FillPortions: =0
                                                Height: =If(App.Width < BreakpointPhone, StepperCircleSize + Space1, StepperCircleSize + Space1 + 18)
                                                LayoutAlignItems: =LayoutAlignItems.Center
                                                LayoutDirection: =If(App.Width < BreakpointPhone, LayoutDirection.Horizontal, LayoutDirection.Vertical)
                                                LayoutGap: =Space1
                                                LayoutMinHeight: =0
                                                LayoutMinWidth: =0
                                                RadiusBottomLeft: =0
                                                RadiusBottomRight: =0
                                                RadiusTopLeft: =0
                                                RadiusTopRight: =0
                                                Width: =If(App.Width < BreakpointPhone, Parent.Width - Space5 * 2, 96)
                                              Children:
                                                - cntStepCircle1:
                                                    Control: GroupContainer
                                                    Variant: AutoLayout
                                                    Properties:
                                                      AlignInContainer: =AlignInContainer.Center
                                                      BorderColor: =If(<stage> >= 1, ColorBrand, ColorBorder)
                                                      BorderThickness: =2
                                                      DropShadow: =DropShadow.None
                                                      Fill: =If(<stage> > 1, ColorBrand, ColorSurface)
                                                      FillPortions: =0
                                                      Height: =StepperCircleSize
                                                      LayoutAlignItems: =LayoutAlignItems.Center
                                                      LayoutDirection: =LayoutDirection.Vertical
                                                      LayoutJustifyContent: =LayoutJustifyContent.Center
                                                      LayoutMinHeight: =0
                                                      LayoutMinWidth: =0
                                                      RadiusBottomLeft: =StepperCircleSize / 2
                                                      RadiusBottomRight: =StepperCircleSize / 2
                                                      RadiusTopLeft: =StepperCircleSize / 2
                                                      RadiusTopRight: =StepperCircleSize / 2
                                                      Width: =StepperCircleSize
                                                    Children:
                                                      - icoStepCheck1:
                                                          Control: ModernIcon
                                                          Properties:
                                                            AccessibleLabel: ="Completed"
                                                            AlignInContainer: =AlignInContainer.Center
                                                            Height: =12
                                                            Icon: ="Checkmark"
                                                            IconColor: =ColorTextOnBrand
                                                            IconStyle: =IconStyle.Filled
                                                            LayoutMinHeight: =12
                                                            LayoutMinWidth: =12
                                                            Visible: =<stage> > 1
                                                            Width: =12
                                                - lblStep1:
                                                    Control: ModernText
                                                    Properties:
                                                      AccessibleLabel: '="Step 1 of 4, New: " & If(<stage> > 1, "completed", <stage> = 1, "current", "upcoming")'
                                                      Align: =If(App.Width < BreakpointPhone, Align.Left, Align.Center)
                                                      AlignInContainer: =If(App.Width < BreakpointPhone, AlignInContainer.Center, AlignInContainer.Stretch)
                                                      AutoHeight: =true
                                                      Color: =If(<stage> >= 1, ColorTextPrimary, ColorTextTertiary)
                                                      FillPortions: =If(App.Width < BreakpointPhone, 1, 0)
                                                      Font: =FontApp
                                                      FontWeight: =If(<stage> = 1, FontWeight.Semibold, FontWeight.Normal)
                                                      LayoutMinHeight: =0
                                                      LayoutMinWidth: =0
                                                      PaddingBottom: =0
                                                      PaddingLeft: =0
                                                      PaddingRight: =0
                                                      PaddingTop: =0
                                                      Size: =FontSizeCaption
                                                      Text: ="New"
                                                      Wrap: =false
                                          - cntStepConn1:
                                              Control: GroupContainer
                                              Variant: AutoLayout
                                              Properties:
                                                AlignInContainer: =AlignInContainer.Start
                                                DropShadow: =DropShadow.None
                                                FillPortions: =0
                                                Height: =StepperCircleSize
                                                LayoutAlignItems: =LayoutAlignItems.Stretch
                                                LayoutDirection: =LayoutDirection.Vertical
                                                LayoutJustifyContent: =LayoutJustifyContent.Center
                                                LayoutMinHeight: =0
                                                LayoutMinWidth: =0
                                                RadiusBottomLeft: =0
                                                RadiusBottomRight: =0
                                                RadiusTopLeft: =0
                                                RadiusTopRight: =0
                                                Visible: =App.Width >= BreakpointPhone
                                                Width: =StepperConnectorWidth
                                              Children:
                                                - recStepLine1:
                                                    Control: Rectangle
                                                    Properties:
                                                      AlignInContainer: =AlignInContainer.Stretch
                                                      BorderThickness: =0
                                                      Fill: =If(<stage> > 1, ColorBrand, ColorBorder)
                                                      FillPortions: =0
                                                      Height: =2
                                                      LayoutMinHeight: =0
                                                      LayoutMinWidth: =0
                                                      TabIndex: =-1
                                          # ... cntStep2 / cntStepConn2 / cntStep3 / cntStepConn3 / cntStep4 follow the same shape
                                    - cmpRequestDetailPane2:
                                        Control: CanvasComponent
                                        ComponentName: cmpRequestDetailPane
                                        Properties:
                                          AlignInContainer: =AlignInContainer.Stretch
                                          FillPortions: =1
                                          Height: =Parent.Height - cntDetailStepperCard.Height - Space4
                                          LayoutMinHeight: =0
                                          LayoutMinWidth: =0
                                          OnConfirmDueDate: |-
                                            =IfError(
                                              Patch('FOIA Pilot Requests', gblSelectedRequest, {DueDateConfirmed: true});
                                              Set(gblSelectedRequest, LookUp('FOIA Pilot Requests', ID = gblSelectedRequest.ID));
                                              cmpToastHost.SendToast("Due date confirmed", "CheckmarkCircle", ColorSuccess, true, "Statutory deadline locked for " & Coalesce(gblSelectedRequest.Title, "this request") & "."),
                                              cmpToastHost.SendToast("Couldn't confirm the due date", "DismissCircle", ColorDanger, true, FirstError.Message, 600000, true, false, false)
                                            )
                                          OnOpenCloseout: =Navigate(ResponseCloseout, ScreenTransition.None)
                                          OnOpenDepartmentWork: |-
                                            =If(IsBlank(gblSelectedAssignment) || gblSelectedAssignment.Request.Id <> gblSelectedRequest.ID,
                                              Set(gblSelectedAssignment, First(Filter('FOIA Pilot Assignments', Request.Id = gblSelectedRequest.ID && Active = true))));
                                            Set(gblSelectedDepartment, gblSelectedAssignment.Department);
                                            Navigate(DepartmentWork, ScreenTransition.None)
                                          ShowQuickActions: =true
                                          Width: =Parent.Width
```

Step table (substitute in the four blocks):

| Block | Label | "completed" test | "current" test | circle Fill | circle BorderColor |
|---|---|---|---|---|---|
| `cntStep1` / `lblStep1` / `icoStepCheck1` | `"New"` | `<stage> > 1` | `<stage> = 1` | `If(<stage> > 1, ColorBrand, ColorSurface)` | `If(<stage> >= 1, ColorBrand, ColorBorder)` |
| `cntStep2` … | `"Assigned"` | `<stage> > 2` | `<stage> = 2` | `If(<stage> > 2, ColorBrand, ColorSurface)` | `If(<stage> >= 2, ColorBrand, ColorBorder)` |
| `cntStep3` … | `"In Progress"` | `<stage> > 3` | `<stage> = 3` | `If(<stage> > 3, ColorBrand, ColorSurface)` | `If(<stage> >= 3, ColorBrand, ColorBorder)` |
| `cntStep4` … | `"Closed"` | `<stage> > 4` (never) | `<stage> = 4` | `If(<stage> = 4, ColorBrand, ColorSurface)` (closed = filled) | `If(<stage> >= 4, ColorBrand, ColorBorder)` |

Connector lines `recStepLine1..3` fill `If(<stage> > N, ColorBrand, ColorBorder)`. Phone: steps stack vertically (horizontal row of circle + label), connectors hidden. Non-colour cue: check icon in completed circles + Semibold current label + the AccessibleLabel text.

  5. **Quick-action strip** already exists inside the pane (`cntPaneQuickActions`); nothing to add.
- **Controls to add:** `cntDetailStack` sub-tree (stepper + `cmpRequestDetailPane2`), `cmpRequestDetailPhoneNav` (→ shell, last, `ActiveKey "Home"`), `cmpToastHost` (→ Screen).
- **Controls to remove:** none (hidden: `cmpRequestDetailPaneHost`, `cmpRequestDetailNavBottom`).

### DepartmentWork (Existing)
- **File:** `DepartmentWork.pa.yaml`
- **Current state:** shell → header → body (rail + content → `cntDeptEmpty`; `cntDeptTopRow` [`cntDeptAssignmentsCard` (title, `galAssignments` wrap-cards, `lblAssignmentsEmpty`) + `cntDepartmentWorkEditor` (status/due/redaction fields, notes, `cntAssignmentActions` with `btnSaveAssignment` / `btnMarkComplete`, `lblAssignmentSaved`)]; `cntDepartmentRecords` (title, meta, `galDepartmentRecords`, `lblDepartmentRecordsEmpty`)) → bottom nav. Six `Notify` calls at lines ~708–739.
- **Changes required:**
  1. Shared edits 1–10.
  2. **Cards** — `cntDeptEmpty`, `cntDeptAssignmentsCard`, `cntDepartmentWorkEditor`, `cntDepartmentRecords`: shared edit 8 (+ `Fill: =ColorSurface` where missing). Titles `lblDeptAssignmentsTitle`, `lblAssignmentEditorTitle`, `lblDepartmentRecordsTitle`: `Font: =FontApp`, `Color: =ColorBrandAlt`.
  3. **Assignment cards (gallery template)** — `cntAssignmentCard`: `BorderThickness: =0`, `DropShadow: =DropShadow.Light`, `RadiusTopLeft: =0`, `RadiusBottomLeft: =0`, `RadiusTopRight: =RadiusMedium`, `RadiusBottomRight: =RadiusMedium`, `PaddingLeft: =Space3 + StatusAccentWidth`, `Fill: =If(ThisItem.ID = gblSelectedAssignment.ID, ColorBrandTint, ColorSurface)`. `bdgAssignmentCardStatus`: `Appearance: =BadgeAppearance.Tint`, `Font: =FontApp`, `Radius*: =RadiusMedium`. Append to `galAssignments.Children` (after `cntAssignmentCard`):
     ```yaml
                                                - recAssignmentAccent:
                                                    Control: Rectangle
                                                    Properties:
                                                      BorderThickness: =0
                                                      Fill: |-
                                                        =Switch(ThisItem.AssignmentStatus.Value,
                                                          "Complete", ColorSuccess,
                                                          "In Progress", ColorWarning,
                                                          "On Hold", ColorTextTertiary,
                                                          "Overdue", ColorDanger,
                                                          ColorInfo)
                                                      Height: =Parent.TemplateHeight
                                                      TabIndex: =-1
                                                      Width: =StatusAccentWidth
                                                      X: =0
                                                      Y: =0
     ```
  4. **Record rows (gallery template)** — `cntDepartmentRecordRow`: `BorderThickness: =0`, `DropShadow: =DropShadow.Light`, left radii `0`, right radii `RadiusMedium`, `PaddingLeft: =Space4 + StatusAccentWidth`. `bdgRecordSensitivity`: `Appearance: =BadgeAppearance.Tint`, `Font: =FontApp`, `Radius*: =RadiusMedium`. Append to `galDepartmentRecords.Children`:
     ```yaml
                                          - recRecordAccent:
                                              Control: Rectangle
                                              Properties:
                                                BorderThickness: =0
                                                Fill: =If(IsBlank(ThisItem.Sensitivity.Value) || ThisItem.Sensitivity.Value = "Public", ColorSuccess, ThisItem.Sensitivity.Value = "Internal", ColorWarning, ColorDanger)
                                                Height: =Parent.TemplateHeight
                                                TabIndex: =-1
                                                Width: =StatusAccentWidth
                                                X: =0
                                                Y: =0
     ```
     (Read the actual `Sensitivity` choice values from the existing `bdgRecordSensitivity.Intent` Switch in the file and mirror its mapping; the names above are placeholders if they differ.)
  5. **Empty state for assignments** — `lblAssignmentsEmpty`: `Visible: =false`. Append `cmpDeptAssignmentsEmpty` to `cntDeptAssignmentsCard` (after `lblAssignmentsEmpty`):
     ```yaml
                                          - cmpDeptAssignmentsEmpty:
                                              Control: CanvasComponent
                                              ComponentName: cmpEmptyState
                                              Properties:
                                                ActionIcon: ="ArrowLeft"
                                                ActionText: ="Back to request"
                                                AlignInContainer: =AlignInContainer.Stretch
                                                FillPortions: =0
                                                Headline: ="No active department assignments"
                                                Height: =220
                                                Hint: ="Assignments created for this request will appear here with their status and due date."
                                                Icon: ="People"
                                                LayoutMinHeight: =0
                                                LayoutMinWidth: =0
                                                OnAction: =Navigate(RequestDetail, ScreenTransition.None)
                                                Visible: =!gblIsLoading && !IsBlank(gblSelectedRequest) && galAssignments.AllItemsCount = 0
     ```
     If `cntDeptAssignmentsCard.Height` sums `lblAssignmentsEmpty.Height`, replace that term with `If(cmpDeptAssignmentsEmpty.Visible, 220 + Space2, 0)`.
  6. **Editor inputs** — `cmbAssignmentStatus`, `datAssignmentDueDate`, `txtResponseNotes`: `Radius*: =RadiusMedium`, `Font: =FontApp`. `btnSaveAssignment`: `Appearance: =ButtonAppearance.Primary`, `Font: =FontApp`, `Radius*: =RadiusMedium`, `Text: =If(gblIsLoading, "Saving…", "Save assignment")`. `btnMarkComplete`: `Font: =FontApp`, `Radius*: =RadiusMedium`. `lblAssignmentSaved`: `Visible: =false` (toast replaces it).
  7. **Notify → SendToast** (exact replacements):
     - `btnSaveAssignment.OnSelect`: validation branch → `cmpToastHost.SendToast("Missing required fields", "Warning", ColorWarning, true, "Status, due date and response notes are required.", 10000)`; success → `cmpToastHost.SendToast("Assignment saved", "CheckmarkCircle", ColorSuccess, true, Coalesce(gblSelectedAssignment.Department.Value, "Department") & " assignment updated.")`; failure → `cmpToastHost.SendToast("Couldn't save the assignment", "DismissCircle", ColorDanger, true, FirstError.Message, 600000, true, false, false)`.
     - `btnMarkComplete.OnSelect`: validation → `cmpToastHost.SendToast("Add response notes first", "Warning", ColorWarning, true, "Response notes are required before marking the assignment complete.", 10000)`; success → `cmpToastHost.SendToast("Assignment marked complete", "CheckmarkCircle", ColorSuccess, true, "Department work is done. Closeout can proceed when all assignments are complete.")`; failure → `cmpToastHost.SendToast("Couldn't mark the assignment complete", "DismissCircle", ColorDanger, true, FirstError.Message, 600000, true, false, false)`.
- **Controls to add:** `recAssignmentAccent` (→ `galAssignments`), `recRecordAccent` (→ `galDepartmentRecords`), `cmpDeptAssignmentsEmpty` (→ `cntDeptAssignmentsCard`), `cmpDepartmentWorkPhoneNav` (→ shell, last), `cmpToastHost` (→ Screen).
- **Controls to remove:** none (hidden: `lblAssignmentsEmpty`, `lblAssignmentSaved`, `cmpDepartmentWorkNavBottom`).

### ResponseCloseout (Existing)
- **File:** `ResponseCloseout.pa.yaml`
- **Current state:** shell → header → body (rail + content → `cntCloseoutEmpty`; `cntCloseoutColumns` [`cntCloseoutReadiness` (title, `cmpCloseoutStatusBadge`, readiness rows) + `cntCloseoutForm` (date, status radio, notes, final-document checkbox, `cntCloseoutValidation`)]; `cntCloseoutActions` sticky (`btnValidateCloseout`, `btnCloseoutRequest`)) → bottom nav. One `Notify` (close failure). Success currently navigates with `ScreenTransition.Cover` and no confirmation.
- **Changes required:**
  1. Shared edits 1–10.
  2. **Cards** — `cntCloseoutEmpty`, `cntCloseoutReadiness`, `cntCloseoutForm`, `cntCloseoutValidation`: shared edit 8 (+ `Fill: =ColorSurface`). `cntCloseoutValidation` keeps its warning tint if it has one (`ColorWarningBg`). Titles `lblReadinessTitle`, `lblCloseoutFormTitle`: `Font: =FontApp`, `Color: =ColorBrandAlt`. Readiness row icons (`icoReadinessAssignments/Docs/DueDate`): `IconStyle: =IconStyle.Filled`.
  3. **Inputs** — `datFinalResponseDate`, `txtCloseoutNotes`: `Radius*: =RadiusMedium`, `Font: =FontApp`; `radCloseoutStatus`, `chkFinalResponseDocument`: `Font: =FontApp`.
  4. **Sticky bar** — `cntCloseoutActions`: `BorderThickness: =0`, `DropShadow: =DropShadow.Light`, `Radius*: =RadiusMedium`. `btnValidateCloseout`: `Font: =FontApp`, `Radius*: =RadiusMedium`, and append to its `OnSelect` a toast on each outcome: `If(<invalid test>, Set(gblSaveSuccess, false); cmpToastHost.SendToast("Not ready to close", "Warning", ColorWarning, true, "Complete every department assignment, attach the final response document, and fill the closeout fields.", 10000), Set(gblSaveSuccess, true); cmpToastHost.SendToast("Ready to close", "Info", ColorInfo, false, "All readiness checks passed.", 5000, true, true, true))` — keep the existing `<invalid test>` expression verbatim.
  5. **Close request** — `btnCloseoutRequest`: `Appearance: =ButtonAppearance.Primary`, `Font: =FontApp`, `Radius*: =RadiusMedium`, `Text: =If(gblIsLoading, "Closing…", "Close request")`. `OnSelect` becomes:
     ```powerfx
     Set(gblIsLoading, true);
     IfError(
       Patch('FOIA Pilot Requests', gblSelectedRequest, {FinalResponseDate: datFinalResponseDate.SelectedDate, OverallStatus: radCloseoutStatus.Selected, CloseoutNotes: txtCloseoutNotes.Text});
       Set(gblSaveSuccess, true);
       Refresh('FOIA Pilot Requests');
       Set(gblSelectedRequest, LookUp('FOIA Pilot Requests', ID = gblSelectedRequest.ID));
       Set(gblIsLoading, false);
       cmpToastHost.SendToast("Request closed", "CheckmarkCircle", ColorSuccess, true, Coalesce(gblSelectedRequest.Title, "Request") & " closed as " & Coalesce(radCloseoutStatus.Selected.Value, "Closed") & ".");
       Back(),
       Set(gblIsLoading, false);
       Set(gblLoadError, true);
       Set(gblSaveSuccess, false);
       cmpToastHost.SendToast("Couldn't close the request", "DismissCircle", ColorDanger, true, FirstError.Message, 600000, true, false, false)
     )
     ```
     (`Back()` returns to wherever closeout was opened from — RequestDetail on phone/tablet, Home on desktop — which replaces the previous `Navigate(If(App.Width >= BreakpointDesktop, Home, RequestDetail), ScreenTransition.Cover)`. If the screen can be reached without a history entry — it cannot today; every path is a `Navigate` — keep `Back()`.)
- **Controls to add:** `cmpCloseoutPhoneNav` (→ shell, last), `cmpToastHost` (→ Screen).
- **Controls to remove:** none (hidden: `cmpCloseoutNavBottom`).

### _EditorState.pa.yaml (Modify)
Replace `ComponentDefinitionsOrder` with the eight names in alphabetical order: `cmpAppHeader`, `cmpEmptyState`, `cmpMetricTile`, `cmpPhoneNav`, `cmpRequestDetailPane`, `cmpSideNav`, `cmpStatusBadge`, `cmpToast`. `ScreensOrder` unchanged.

## Control Definitions (new control types only)

Property names for every control already in the app are authoritative in the existing YAML files (and dumped in `..\canvas-app-v2-plan.md` → "Control Definitions"). Three control types are new in this edit; full `describe_control` output follows. Audit done: every property used in this plan for these controls appears below.

### Rectangle
```
# Control Rectangle
Part of the control family Classic.

Control creation keywords:
Control: Rectangle

Input Properties:
  - AccessibleLabel: Text             Default: ""
  - BorderColor: Color                Default: App.Theme.Colors.Darker40
  - BorderStyle: Enum                 Default: BorderStyle.Solid   (BorderStyle: Dashed, Dotted, None, Solid)
  - BorderThickness: Number           Default: 0
  - ContentLanguage: Text             Default: ""
  - DisabledFill: Color               Default: Self.Fill
  - DisplayMode: Enum                 Default: DisplayMode.Edit    (DisplayMode: Disabled, Edit, View)
  - Fill: Color                       Default: App.Theme.Colors.Primary
  - FocusedBorderColor: Color         Default: Self.BorderColor
  - FocusedBorderThickness: Number    Default: 2
  - Height: Number                    Default: 100
  - HoverFill: Color                  Default: Self.Fill
  - OnSelect: Boolean                 Default: false
  - PressedFill: Color                Default: Self.Fill
  - TabIndex: Number                  Default: -1
  - Tooltip: Text                     Default: ""
  - Visible: Boolean                  Default: true
  - Width: Number                     Default: 150
  - X: Number                         Default: 0
  - Y: Number                         Default: 0

Additional input properties if a child of a Vertical or Horizontal GroupContainer:
  - AlignInContainer: Enum            Default: AlignInContainer.SetByContainer (Center, End, SetByContainer, Start, Stretch)
  - FillPortions: Number              Default: 0
  - LayoutMaxHeight: Number           Default: 0
  - LayoutMaxWidth: Number            Default: 0
  - LayoutMinHeight: Number           Default: 100
  - LayoutMinWidth: Number            Default: 150

Additional input properties if a child of a Grid GroupContainer:
  - LayoutGridColumnEnd, LayoutGridColumnStart, LayoutGridRowEnd, LayoutGridRowStart: Number

Output Properties:
  AccessibleLabel, BorderColor, BorderStyle, BorderThickness, ContentLanguage, DisabledFill, DisplayMode, Fill, FocusedBorderColor,
  FocusedBorderThickness, Height, HoverFill, PressedFill, TabIndex, Tooltip, Visible, Width, X, Y
```
Note: no `Radius*`, no `Padding*`. Inside an AutoLayout container always set `LayoutMinHeight: =0` / `LayoutMinWidth: =0` (defaults are 100/150).

### Timer
```
# Control Timer
Part of the control family Classic.

Control creation keywords:
Control: Timer

Input Properties:
  - Align: Enum                       Default: Align.Center        (Align: Center, Justify, Left, Right)
  - AutoPause: Boolean                Default: true
  - AutoStart: Boolean                Default: false
  - BorderColor: Color                Default: App.Theme.Colors.Primary
  - BorderStyle: Enum                 Default: BorderStyle.Solid   (BorderStyle: Dashed, Dotted, None, Solid)
  - BorderThickness: Number           Default: 2
  - Color: Color                      Default: App.Theme.Colors.PrimaryForeground
  - ContentLanguage: Text             Default: ""
  - DisabledBorderColor: Color        Default: RGBA(244, 244, 244, 1)
  - DisabledColor: Color              Default: RGBA(166, 166, 166, 1)
  - DisabledFill: Color               Default: RGBA(244, 244, 244, 1)
  - DisplayMode: Enum                 Default: DisplayMode.Edit    (DisplayMode: Disabled, Edit, View)
  - Duration: Number                  Default: 60000
  - Fill: Color                       Default: App.Theme.Colors.Primary
  - FocusedBorderColor: Color         Default: Self.BorderColor
  - FocusedBorderThickness: Number    Default: 4
  - Font: Enum                        Default: App.Theme.Font      (Font: Arial, Courier New, Dancing Script, Georgia, Great Vibes, Lato, Lato Black, Lato Hairline, Lato Light, Open Sans, Open Sans Condensed, Patrick Hand, Segoe UI, Verdana)
  - FontWeight: Enum                  Default: FontWeight.Normal   (FontWeight: Bold, Lighter, Normal, Semibold)
  - Height: Number                    Default: 40
  - HoverBorderColor: Color           Default: App.Theme.Colors.Darker10
  - HoverColor: Color                 Default: App.Theme.Colors.PrimaryForeground
  - HoverFill: Color                  Default: App.Theme.Colors.Darker10
  - Italic: Boolean                   Default: false
  - OnSelect: Boolean                 Default: false
  - OnTimerEnd: Boolean               Default: false
  - OnTimerStart: Boolean             Default: false
  - PaddingBottom/Left/Right/Top: Number  Default: 5
  - PressedBorderColor: Color         Default: App.Theme.Colors.Darker40
  - PressedColor: Color               Default: Self.Color
  - PressedFill: Color                Default: App.Theme.Colors.Darker40
  - RadiusBottomLeft/BottomRight/TopLeft/TopRight: Number  Default: 10
  - Repeat: Boolean                   Default: false
  - Reset: Boolean                    Default: false
  - Size: Number                      Default: 13
  - Start: Boolean                    Default: false
  - Strikethrough: Boolean            Default: false
  - TabIndex: Number                  Default: 0
  - Text: Text                        Default: Text(Time(0, 0, Self.Value/1000), "hh:mm:ss")
  - Tooltip: Text                     Default: ""
  - Underline: Boolean                Default: false
  - VerticalAlign: Enum               Default: VerticalAlign.Middle (VerticalAlign: Bottom, Middle, Top)
  - Visible: Boolean                  Default: true
  - Width: Number                     Default: 160
  - X: Number                         Default: 0
  - Y: Number                         Default: 0

Additional input properties if a child of a Vertical or Horizontal GroupContainer:
  - AlignInContainer: Enum (SetByContainer), FillPortions: Number (0), LayoutMaxHeight: Number (0), LayoutMaxWidth: Number (0),
    LayoutMinHeight: Number (40), LayoutMinWidth: Number (160)

Additional input properties if a child of a Grid GroupContainer:
  - LayoutGridColumnEnd, LayoutGridColumnStart, LayoutGridRowEnd, LayoutGridRowStart: Number

Output Properties:
  Align, AutoPause, AutoStart, BorderColor, BorderStyle, BorderThickness, Color, ContentLanguage, DisabledBorderColor, DisabledColor,
  DisabledFill, DisplayMode, Duration, Fill, FocusedBorderColor, FocusedBorderThickness, Font, FontWeight, Height, HoverBorderColor,
  HoverColor, HoverFill, Italic, PaddingBottom, PaddingLeft, PaddingRight, PaddingTop, PressedBorderColor, PressedColor, PressedFill,
  RadiusBottomLeft, RadiusBottomRight, RadiusTopLeft, RadiusTopRight, Repeat, Reset, Size, Start, Strikethrough, TabIndex, Text, Tooltip,
  Underline, Value: Number, VerticalAlign, Visible, Width, X, Y
```

### ModernProgressBar
```
# Control ModernProgressBar
Part of the control family React.

Control creation keywords:
Control: ModernProgressBar

Input Properties:
  - AccessibleLabel: Text             Default: "Progress bar"
  - BasePaletteColor: Color
  - ContentLanguage: Text             Default: ""
  - DisplayMode: Enum                 Default: DisplayMode.Edit    (DisplayMode: Disabled, Edit, View)
  - FillColor: Color
  - Height: Number                    Default: 45
  - Indeterminate: Boolean            Default: false
  - Max: Number                       Default: 100
  - ProgressColor: Enum               Default: ProgressColor.Brand (ProgressColor: Brand, Error, Success, Warning)
  - Shape: Enum                       Default: ProgressShape.Rounded (ProgressShape: Rounded, Square)
  - Thickness: Enum                   Default: ProgressThickness.Medium (ProgressThickness: Large, Medium)
  - Tooltip: Text                     Default: ""
  - TrackColor: Color
  - Value: Number                     Default: 50
  - Visible: Boolean                  Default: true
  - Width: Number                     Default: 450
  - X: Number                         Default: 0
  - Y: Number                         Default: 0

Additional input properties if a child of a Vertical or Horizontal GroupContainer:
  - AlignInContainer: Enum (SetByContainer), FillPortions: Number (0), LayoutMaxHeight: Number (0), LayoutMaxWidth: Number (0),
    LayoutMinHeight: Number (45), LayoutMinWidth: Number (450)

Additional input properties if a child of a Grid GroupContainer:
  - LayoutGridColumnEnd, LayoutGridColumnStart, LayoutGridRowEnd, LayoutGridRowStart: Number

Output Properties:
  AccessibleLabel, BasePaletteColor, ContentLanguage, DisplayMode, Height, Tooltip, Value, Visible, Width, X, Y
```
(The FluentV9 `Progress` control used by the reference toast also exists — enum names there are `'Progress.ProgressColor'.Brand` etc. — but this app standardises on the React `Modern*` family, so `ModernProgressBar` is used.)

### Gallery — `Horizontal` and `VariableHeight` variants (new to this app)
Same property set as `Vertical` (see v2 plan): `AccessibleLabel`, `BorderColor`, `BorderThickness`, `DelayItemLoading`, `Height`, `Items`, `LoadingSpinner`, `ShowScrollbar`, `TemplatePadding`, `TemplateSize`, `Width`, `WrapCount` (`Horizontal` only), `MaxTemplateSize` (`VariableHeight` only), `X`, `Y`, plus `TabIndex`, `Selectable`, `Transition`, `Visible`, `OnSelect`. Outputs include `AllItems`, `AllItemsCount`, `Selected`, `TemplateHeight`, `TemplateWidth`, `VisibleIndex`. In a `Horizontal` gallery `TemplateSize` is the **template width** and `Parent.TemplateHeight` equals the gallery height. `TemplateSize` is **not** readable (rule 11).

## TechnicalGuide key conventions (must-follow)
- Every property value starts with `=`. Multi-line formulas use `|-` with `=` on the first content line.
- **Any plain scalar containing `: ` must be quoted** — record literals (`'=Table({Key: "Home", …})'`), labels like `'="Status: " & x'`, AccessibleLabels with colons. Inside `|-` blocks nothing needs quoting.
- Enum escaping: `ButtonAppearance.Subtle`, `ButtonLayout.IconOnly`, `IconStyle.Filled`, `BadgeAppearance.Tint`, `BadgeIntent.Caution`, `ProgressColor.Brand`, `ValidationState.Error`, `Appearance.FilledLighter`, `TextInputType.Search`, `TriggerOutput.Delayed`, `DropShadow.Light`, `LayoutDirection.Vertical`, `AlignInContainer.Stretch`, `FontWeight.Semibold`, `Font.Lato`, `Align.Center`, `VerticalAlign.Middle`, `ScreenTransition.None`, `SortOrder.Ascending`, `TimeUnit.Milliseconds`.
- AutoLayout children: set `FillPortions: =0` whenever you give a fixed `Width`/`Height`; always set `LayoutMinHeight: =0` and `LayoutMinWidth: =0` on containers, galleries, rectangles and progress bars (their defaults are large). `AlignInContainer` default for Modern controls is `SetByContainer`.
- `GroupContainer` has no `OnSelect`, no `AccessibleLabel`, no `Font`. `ModernText` has no `Tooltip`/`Live`. `ModernButton`/`ModernIcon` have no `AutoHeight`/`Fill`. `ModernDropdown` has no `Placeholder` (hence the `"Status: " &` display-text prefix).
- Breakpoints inline only: `App.Width < BreakpointPhone`, `App.Width >= BreakpointDesktop`. Never `IsPhone` as a named formula.
- Inside gallery templates: no `CanvasComponent`; `Parent.TemplateHeight` / `Parent.TemplateWidth`; repeat the gallery `OnSelect` body on inner controls instead of `Select(Parent)`.
- Component custom property references: `cmpX.Prop` for inputs, `cmpX.Event()` / `cmpX.Event(arg)` for events, `cmpX.Action(args)` for actions. Instances: `Control: CanvasComponent` + `ComponentName: cmpX`; event handlers are set on the instance as properties (`OnSelect: =…`); unused events `=false`.
- Component definition files: one `ComponentDefinitions:` root per file with a single component; `DefinitionType: CanvasComponent`, `AccessAppScope: true`, `Description` present; every `PropertyKind: Event` has a `Default`; `Action` properties declare `Parameters` with `DataType` + `Default` (and `IsOptional: true` where optional).
- Do not rename, delete, move, or re-variant any existing control. Do not touch `App.pa.yaml`.
- Date formats lower-case (`"mmm d, yyyy"`, `"hh:mm AM/PM"`).

## Builder acceptance checklist (per file, before handing back)
- [ ] No existing control changed parent; no existing control renamed or removed.
- [ ] Every new control name is unique across the whole app (grep the folder).
- [ ] Shell: `Fill ColorCanvas`, padding/gap `Space2`; header card shadow+radius visible; rail 50 px with GridDots; old bottom nav hidden; `cmp<Screen>PhoneNav` last in shell; `cmpToastHost` last on the Screen.
- [ ] Zero `Notify(` left in the file.
- [ ] Every card: `BorderThickness 0`, `DropShadow.Light`, `RadiusLarge`. Every row: accent Rectangle + tint badge (or status word on phone).
- [ ] One Primary button visible per screen (NewRequest: Save; DepartmentWork: Save assignment; ResponseCloseout: Close request; Home/RequestDetail: header primary).
- [ ] Icon-only buttons carry `AccessibleLabel` + `Tooltip`; tile values and badges include their label in `AccessibleLabel`.
- [ ] Any `: ` inside a plain-scalar formula is quoted.
