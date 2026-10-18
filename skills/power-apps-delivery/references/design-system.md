# MGP Canvas App Design System — Elevated UI/UX Reference

This is the **quality bar** for every Canvas app built with the `power-apps-delivery` skill. It codifies the visual language of the two internal apps the team holds up as the standard (the Team Onboarding / ELM app and the Early Check Request app) so an agent can reproduce that bar without seeing them. The goal is an app that feels like a first-party Microsoft product: calm, dense where it should be, generous where it should be, fully responsive, and obviously "designed".

Use it together with `standards/power-apps.md` (responsive tiers, MCP sync rules) and `standards/visual-verification.md` (screenshot acceptance). Where this file and the standard disagree, the standard wins; this file adds the *how it should look*.

---

## 1. Design principles (what "elevated" means here)

| Principle | What it looks like | What it is **not** |
|---|---|---|
| **Microsoft-native** | Fluent 2 modern controls, Lato or Segoe UI, neutral surfaces, one accent, subtle shadows, 4–10 px radii | Rainbow palettes, gradients, classic controls, hard black borders |
| **Mobile-first, desktop-rich** | Phone tier is a complete product with a bottom tab bar; every wider tier *adds* context (master-detail, side panels, timelines, stat strips) | Phone layout stretched to 1920 px; tiny 11-px text on desktop |
| **Information hierarchy** | One title, one primary action per screen; KPI → filters → list; detail panes use tabs | Five buttons of equal weight in a header |
| **Everything is a component** | Header, sidebar/rail, phone nav, status pill, KPI tile, empty state, toast, stepper, detail pane | Copy-pasted shell controls on every screen |
| **State is designed, not defaulted** | Loading skeleton, empty illustration + CTA, inline validation, toast on success/error | A blank gallery or a `Notify()` as the only feedback |
| **Delight with purpose** | Approval-flow stepper, status accent bar on rows, metric tiles with tinted icon chips, hover/press feedback, toggles that change layout mode | Animation or decoration that adds no information |

---

## 2. Design tokens (declare once in `App.Formulas`)

Declare every literal below as a named formula. Never inline a color, radius, or font size in a control. (`App.Width`/`App.Height` comparisons must stay inline — see standard rule 6.)

```yaml
App:
  Properties:
    Formulas: |-
      // ---- Breakpoints (literals only; compare inline) ----
      BreakpointPhone = 600;
      BreakpointDesktop = 1200;

      // ---- Brand & semantic colors (Fluent 2 neutral ramp + one accent) ----
      ColorBrand = RGBA(27, 74, 137, 1);         // primary accent (ELM blue)
      ColorBrandHover = RGBA(21, 60, 112, 1);
      ColorBrandTint = RGBA(27, 74, 137, 0.10);  // icon chips, selected row
      ColorBrandAlt = RGBA(55, 73, 114, 1);      // secondary accent (Early Check navy)

      ColorSurface = RGBA(255, 255, 255, 1);     // cards, header
      ColorCanvas = RGBA(245, 245, 245, 1);      // page background (Fluent neutralBackground3)
      ColorBorder = RGBA(225, 223, 221, 1);
      ColorTextPrimary = RGBA(36, 36, 36, 1);
      ColorTextSecondary = RGBA(97, 97, 97, 1);
      ColorTextTertiary = RGBA(150, 148, 146, 1); // metric captions
      ColorTextOnBrand = RGBA(255, 255, 255, 1);

      ColorSuccess = RGBA(16, 124, 16, 1);  ColorSuccessTint = RGBA(16, 124, 16, 0.12);
      ColorWarning = RGBA(157, 93, 0, 1);   ColorWarningTint = RGBA(255, 185, 0, 0.18);
      ColorDanger  = RGBA(196, 49, 75, 1);  ColorDangerTint  = RGBA(196, 49, 75, 0.12);
      ColorInfo    = RGBA(0, 120, 212, 1);  ColorInfoTint    = RGBA(0, 120, 212, 0.12);
      ColorNeutralTint = RGBA(97, 97, 97, 0.12);

      // ---- Typography (Lato preferred; Segoe UI fallback) ----
      FontApp = Font.Lato;
      FontSizeCaption = 12;
      FontSizeBody = 14;
      FontSizeBodyPhone = 15;
      FontSizeSection = 16;
      FontSizeTitlePhone = 20;  FontSizeTitleTablet = 22;  FontSizeTitleDesktop = 24;
      FontSizeKpiPhone = 28;    FontSizeKpiTablet = 30;    FontSizeKpiDesktop = 32;
      FontSizeAppTitle = 28;    // header wordmark (ELM uses 35 on a 60-px header)

      // ---- Spacing & shape ----
      Space1 = 4;  Space2 = 8;  Space3 = 12;  Space4 = 16;  Space5 = 24;  Space6 = 32;
      RadiusSmall = 4;  RadiusMedium = 8;  RadiusLarge = 10;
      TouchTarget = 44;

      // ---- Shell dimensions ----
      HeaderHeight = 60;
      RailWidth = 50;          // icon-only left rail (ELM/Early Check Sidebar)
      RailWidthExpanded = 220;
      PhoneNavHeight = 64;
      ContentMaxWidth = 1600;
      TileHeight = 104;
      StatStripHeight = 64;
      StatusAccentWidth = 5;   // left accent bar on list rows
```

**Shadows** (modern controls expose `DropShadow`; containers expose `DropShadow` as an enum): cards use `DropShadow.Light` (≈ `0 1px 2px`), elevated/hover surfaces use `DropShadow.Regular` (≈ `0 4px 8px`), the header uses `DropShadow.Light` bottom shadow. Never use `DropShadow.Bold` except for modals.

---

## 3. Screen skeleton (every screen, every tier)

Observed in both reference apps: a single full-screen vertical AutoLayout container with 8-px padding and 8-px gap, a white header row, then a horizontal body with a 50-px icon rail and a `FillPortions` main area. Phone replaces the rail with a bottom tab bar.

```
scrX  (Fill = ColorCanvas)
└─ cntPage          GroupContainer · Vertical · Padding Space2 · Gap Space2 · Width/Height = Parent
   ├─ cmpAppHeader  CanvasComponent · Height HeaderHeight · FillPortions 0
   ├─ cntBody       GroupContainer · Horizontal · FillPortions 1 · Gap Space2 · LayoutWrap false
   │  ├─ cmpSideNav   CanvasComponent · Width RailWidth · Visible = App.Width >= BreakpointPhone
   │  └─ cntMain      GroupContainer · Vertical · FillPortions 1 · Gap Space4 · Padding tier-based
   │     ├─ cntMetrics      (KPI tiles or stat strip — see §5.3)
   │     ├─ cntToolbar      (search / filters / toggles — see §5.5)
   │     └─ cntContent      (gallery, master-detail, or form — FillPortions 1)
   └─ cmpPhoneNav   CanvasComponent · Height PhoneNavHeight · Visible = App.Width < BreakpointPhone
```

Tier rules for `cntMain`:

| | Phone `< 600` | Tablet `600–1199` | Desktop `≥ 1200` |
|---|---|---|---|
| `PaddingLeft/Right` | `Space4` (16) | `Space5` (24) | `Max(Space5, (Parent.Width - ContentMaxWidth) / 2)` — centers content |
| Rail | hidden; `cmpPhoneNav` shown | icon-only rail | icon + label rail (`RailWidthExpanded`) or icon rail with GridDots expander |
| Content | single column | bounded 2-column groups | master-detail / multi-column |

---

## 4. Component catalog (build these first; everything else composes them)

Each is a `ComponentDefinitions` entry with the contract below. Instances use `Control: CanvasComponent` + `ComponentName`. Components may **not** be placed inside a gallery template (standard rule 4) — use native controls with the same tokens there.

| Component | Purpose | Inputs | Outputs / Events | Notes |
|---|---|---|---|---|
| `cmpAppHeader` | White 60-px bar: logo (left), app title (centered Lato 28–35 Semibold), right action cluster (search icon, notifications, user avatar/initials) | `Title: Text`, `ShowBack: Boolean`, `ShowSearch: Boolean`, `UserDisplayName: Text`, `Tier: Text` | `OnBack`, `OnSearch`, `OnProfile` | ELM pattern: three `FillPortions` spacer containers to truly center the title. `DropShadow.Light`. Phone: title left-aligned at `FontSizeTitlePhone`, actions icon-only. |
| `cmpSideNav` | Left icon rail; 32-px Fluent `Icon` buttons stacked vertically; GridDots at top toggles expanded labels; active item has `ColorBrandTint` background + `ColorBrand` icon | `Items: Table(Key, Label, Icon, Screen)`, `ActiveKey: Text`, `Expanded: Boolean` | `OnSelect(Key)` | Width `If(Expanded, RailWidthExpanded, RailWidth)`. Tooltip = Label when collapsed. |
| `cmpPhoneNav` | Bottom tab bar, 3–5 items, icon above short label, 44-px targets, active item in brand color + 2-px top indicator | same as `cmpSideNav` | `OnSelect(Key)` | Fixed at bottom of `cntPage`; content above it scrolls. |
| `cmpStatusBadge` | Pill: tinted background + bold 12-px text, radius `RadiusMedium`, optional leading dot/icon | `Status: Text`, `Size: Text` | — | Mapping table lives **once** here (Submitted→Info, In Progress→Warning, Completed→Success, Denied→Danger, Draft→Neutral). Inside galleries use `ModernBadge` with the same map. |
| `cmpMetricTile` | KPI card: 50-px icon chip (tinted fill, radius `RadiusMedium`) + caption (`FontSizeCaption`, `ColorTextTertiary`) + value (KPI size, Semibold) + optional delta/footnote | `Label`, `Value`, `Icon`, `Intent`, `Compact: Boolean` | `OnSelect` | `Compact=true` renders the horizontal icon·value·label strip used on desktop. |
| `cmpSectionCard` | White surface, radius `RadiusLarge`, `DropShadow.Light`, optional title row + "See all" action | `Title`, `ActionText`, `ShowAction` | `OnAction` | Wrap any content group that needs a card boundary. |
| `cmpEmptyState` | Centered 48-px icon, one-line headline, one-line hint, one primary button | `Icon`, `Headline`, `Hint`, `ActionText` | `OnAction` | Used for no-results **and** permission-denied with different copy. |
| `cmpToast` | **Default notification surface for every app.** Imported from the reference "Fluent 2 Toast": collection-driven variable-height stack (icon · Semibold header · optional time · dismiss · body · optional progress), per-row timer auto-dismiss, queue capped at 4 | `ToastTable` (default `colToasts`), `SortOrder`; **Action** `SendToast(Header, Icon, IconColor, IconFilled, Body, Duration, ShowDismiss, ShowTime, ShowProgress)` | Output `AutoHeight`; events `AddToast`, `RemoveToast` | Full YAML in `toast-component.pa.yaml`; usage in §5.9. Bare `Notify()` is not permitted for user-facing outcomes. |
| `cmpStepper` | Approval-flow progress: 20-px circles joined by 80-px connector lines; past = brand filled, current = brand ring, future = border grey; labels under circles | `Steps: Table(Label, State)`, `Orientation` | — | Vertical orientation on phone. Non-color cue = check icon in completed circles. |
| `cmpDetailPane` | Record detail with inline tabs (Summary / Assignments / Activity), sticky action bar | `RecordId`, `Tier` | `OnClose`, `OnSaved` | Reused by desktop master-detail **and** the phone/tablet detail screen (standard rule). |
| `cmpConfirmDialog` | Modal overlay 40 % scrim + centered 480-px card, title, body, Cancel/Confirm | `Title`, `Body`, `ConfirmText`, `Destructive: Boolean`, `Visible` | `OnConfirm`, `OnCancel` | `DropShadow.Bold`. Only modal allowed to use bold shadow. |

---

## 5. Signature patterns (with YAML)

### 5.1 Header with truly-centered title (ELM)

```yaml
- cntHeader:
    Control: GroupContainer
    Variant: HorizontalAutoLayoutContainer
    Properties:
      Height: =HeaderHeight
      FillPortions: =0
      Fill: =ColorSurface
      DropShadow: =DropShadow.Light
      RadiusTopLeft: =RadiusMedium
      RadiusTopRight: =RadiusMedium
      RadiusBottomLeft: =RadiusMedium
      RadiusBottomRight: =RadiusMedium
      LayoutAlignItems: =LayoutAlignItems.Center
      PaddingLeft: =Space4
      PaddingRight: =Space4
    Children:
      - cntHeaderLeft:
          Control: GroupContainer
          Variant: HorizontalAutoLayoutContainer
          Properties: { FillPortions: =1, LayoutAlignItems: =LayoutAlignItems.Center, LayoutGap: =Space3 }
          Children:
            - imgLogo: { Control: Image, Properties: { Height: =40, Width: =40, Image: =AppLogo } }
      - lblAppTitle:
          Control: Text
          Properties:
            Text: =AppTitle
            Font: =FontApp
            Size: '=If(App.Width < BreakpointPhone, FontSizeTitlePhone, FontSizeAppTitle)'
            Weight: ='TextCanvas.Weight'.Semibold
            Color: =ColorTextPrimary
            Align: ='TextCanvas.Align'.Center
            FillPortions: =2
            AutoHeight: =true
      - cntHeaderRight:
          Control: GroupContainer
          Variant: HorizontalAutoLayoutContainer
          Properties: { FillPortions: =1, LayoutJustifyContent: =LayoutJustifyContent.End, LayoutGap: =Space2 }
          Children:
            - btnNotify: { Control: Button, Properties: { Icon: ='ButtonCanvas.Icon'.Alert, Appearance: ='ButtonCanvas.Appearance'.Subtle, Width: =TouchTarget, Height: =TouchTarget, AccessibleLabel: ="Notifications" } }
```

### 5.2 Icon rail item (Sidebar component body)

```yaml
- btnNavItem:
    Control: Button
    Properties:
      Icon: =ThisItem.Icon
      Appearance: ='ButtonCanvas.Appearance'.Subtle
      Width: =RailWidth - Space2
      Height: =RailWidth - Space2
      Fill: '=If(ThisItem.Key = cmpSideNav.ActiveKey, ColorBrandTint, Color.Transparent)'
      Color: '=If(ThisItem.Key = cmpSideNav.ActiveKey, ColorBrand, ColorTextSecondary)'
      Tooltip: =ThisItem.Label
      AccessibleLabel: =ThisItem.Label
```

### 5.3 Metric tile (Early Check metric cards)

```yaml
- cntTile:
    Control: GroupContainer
    Variant: HorizontalAutoLayoutContainer
    Properties:
      Height: =TileHeight
      Fill: =ColorSurface
      DropShadow: =DropShadow.Light
      RadiusTopLeft: =RadiusLarge   # repeat for all four corners
      LayoutGap: =Space3
      PaddingLeft: =Space4
      PaddingRight: =Space4
      LayoutAlignItems: =LayoutAlignItems.Center
    Children:
      - cntIconChip:
          Control: GroupContainer
          Variant: VerticalAutoLayoutContainer
          Properties: { Width: =50, Height: =50, Fill: =ColorBrandTint, RadiusTopLeft: =RadiusMedium, LayoutAlignItems: =LayoutAlignItems.Center, LayoutJustifyContent: =LayoutJustifyContent.Center }
          Children:
            - icoTile: { Control: Icon, Properties: { Icon: ='Icon'.Document, Color: =ColorBrand, Width: =24, Height: =24 } }
      - cntTileText:
          Control: GroupContainer
          Variant: VerticalAutoLayoutContainer
          Properties: { FillPortions: =1, LayoutGap: =Space1 }
          Children:
            - lblTileCaption: { Control: Text, Properties: { Text: ="Open requests", Size: =FontSizeCaption, Color: =ColorTextTertiary, AutoHeight: =true } }
            - lblTileValue:
                Control: Text
                Properties:
                  Text: =Text(CountRows(colOpen))
                  Size: '=If(App.Width < BreakpointPhone, FontSizeKpiPhone, App.Width < BreakpointDesktop, FontSizeKpiTablet, FontSizeKpiDesktop)'
                  Weight: ='TextCanvas.Weight'.Semibold
                  Color: =ColorTextPrimary
                  AutoHeight: =true
                  AccessibleLabel: '="Open requests: " & Self.Text'
```

### 5.4 List row with status accent bar + pill (Early Check gallery)

Inside a gallery template (no components allowed):

```yaml
- cntRow:
    Control: GroupContainer
    Variant: HorizontalAutoLayoutContainer
    Properties:
      Fill: =ColorSurface
      RadiusTopLeft: =RadiusMedium   # all corners
      DropShadow: =DropShadow.Light
      LayoutGap: =Space3
      LayoutAlignItems: =LayoutAlignItems.Center
      PaddingRight: =Space4
    Children:
      - recAccent:
          Control: Rectangle
          Properties:
            Width: =StatusAccentWidth
            Height: =Parent.Height
            Fill: '=Switch(ThisItem.Status.Value, "Completed", ColorSuccess, "Denied", ColorDanger, "In Progress", ColorWarning, ColorInfo)'
      - cntRowText:
          Control: GroupContainer
          Variant: VerticalAutoLayoutContainer
          Properties: { FillPortions: =1, LayoutGap: =Space1, PaddingTop: =Space3, PaddingBottom: =Space3 }
          Children:
            - lblRowTitle: { Control: Text, Properties: { Text: =ThisItem.Title, Size: =FontSizeBody, Weight: ='TextCanvas.Weight'.Semibold, AutoHeight: =true } }
            - lblRowMeta:  { Control: Text, Properties: { Text: '=ThisItem.Requester & " · " & Text(ThisItem.Created, "mmm d")', Size: =FontSizeCaption, Color: =ColorTextSecondary, AutoHeight: =true } }
      - bdgStatus:
          Control: Badge
          Properties:
            Text: =ThisItem.Status.Value
            Appearance: ='BadgeCanvas.Appearance'.Tint
            Intent: '=Switch(ThisItem.Status.Value, "Completed", ''BadgeCanvas.Intent''.Success, "Denied", ''BadgeCanvas.Intent''.Danger, "In Progress", ''BadgeCanvas.Intent''.Warning, ''BadgeCanvas.Intent''.Informative)'
            Visible: =App.Width >= BreakpointPhone
      - icoChevron: { Control: Icon, Properties: { Icon: ='Icon'.ChevronRight, Color: =ColorTextTertiary, Width: =20, Height: =20 } }
```

Phone: hide `bdgStatus` and rely on `recAccent` + a status word in `lblRowMeta` (non-color cue preserved).

### 5.5 Toolbar: search + filters + layout toggles

Desktop/tablet: one horizontal container — `TextInput` (search, `FillPortions 2`, radius `RadiusLarge`, leading Search icon) · `Dropdown` status · `Dropdown` department · `Button` Reset (subtle) · spacer · `Toggle` "Hide metrics" · `Toggle` "Compact". Phone: search full-width; filters collapse into a single "Filters" button that opens a bottom-sheet container (`cntFilterSheet`, `Visible = locShowFilters`).

The Early Check `Hide Metrics` / `Hide Filters` toggles are the pattern for **user-controlled density** — expose them on desktop, default them off, store in `gbl` variables so they persist across screens.

### 5.6 Master-detail (desktop)

```
cntContent (Horizontal, FillPortions 1, Gap Space4)
├─ cntListPane    FillPortions 0 · Width = Parent.Width * 0.38 · LayoutMinWidth 360
│  └─ galRequests (Vertical, TemplateSize 84, rows per §5.4; selected row Fill = ColorBrandTint)
└─ cmpDetailPane  FillPortions 1 · RecordId = galRequests.Selected.ID · Tier = "Desktop"
```

On tablet/phone `cmpDetailPane` is the only control on `scrRequestDetail`, which `Navigate()`s in with `ScreenTransition.Cover` (phone) / `Fade` (tablet).

### 5.7 Form layout

- Group fields into `cmpSectionCard`s (Requester · Request · Fulfillment).
- Desktop: 2–3 columns via `LayoutWrap: true` with children `Width = (Parent.Width - gaps) / columns`; tablet 2 columns; phone 1 column.
- Required fields: label suffix ` *` in `ColorDanger` plus `AccessibleLabel` "… (required)".
- Inline validation text under the field (`FontSizeCaption`, `ColorDanger`, `AutoHeight`), shown only after first submit attempt (`locShowValidation`).
- Sticky action bar at the bottom of the form container (phone: full-width primary button; desktop: right-aligned Cancel + Save). Save is `Disabled` while required fields are blank or `locIsSaving`.
- Save path wraps `Patch` in `IfError`; success → `cmpToast` + `Back()`; failure → `cmpToast` Danger and keep input.

### 5.8 Desktop-only supplementary panels (earn the real estate)

Add **only** when the panel conveys information not already on screen:

| Panel | Content | Where |
|---|---|---|
| Status distribution strip | Horizontal stacked bar of counts by status, 8 px tall, with legend pills | Under metrics on the list screen |
| Activity timeline | Vertical list of status changes/comments with relative time | Detail pane "Activity" tab or right side panel |
| Due-date heat | Badge "Due in 2 days" / "Overdue" computed from statutory deadline | Row meta + detail header |
| Quick-action strip | Assign to me · Add note · Mark complete (icon + label) | Detail pane sticky bar |
| Keyboard hints | `/` focus search, `N` new request | Footer caption on desktop only |

### 5.9 Toast notifications — the default feedback surface (Early Check "Fluent 2 Toast")

The reference component's full YAML is stored verbatim at `toast-component.pa.yaml` in this folder. It is the team's **default notification surface**; the skill imports/recreates it as `cmpToast` in every app rather than designing a new one.

**How it works (so you can debug it)**

- Transparent 300-px component whose `Height = Self.AutoHeight` (an **Output** property: `0` when empty, else the container height) — so the host screen never reserves space for it.
- `galToast` is a `VariableHeight` gallery over `Sort(ToastTable, CurrentTime, SortOrder)`. Row height is measured by a hidden `txtGaluAutoHeight` text (`conToast.Height + TemplatePadding`) and the gallery sums them; `conToast.Height` is derived from a 1-px `conAutoHeight` sentinel at the bottom of the card — the standard "measure an AutoLayout container" trick.
- Each card: white, 8-px padding, 4-px gap → header row (32 px: 20-px `Icon` with `IconStyle` Filled/Outline, Semibold `Header` that does not wrap, optional right-aligned 12-px timestamp, transparent icon-only `Dismiss` button 32 px) → optional `Body` (AutoHeight, grey `RGBA(106,122,127)`) → optional 8-px `Progress` bar counting down `Duration`.
- A hidden `Timer` per row (`Duration 100`, `Repeat true`) ticks `Set(varCurrentTime, Now())` for the progress bar and calls `RemoveToast(ThisItem)` once `Now() > RemoveTime`.
- Queue is capped at **4**; `AddToast` drops the oldest first. In the designer (no active screen) it renders one sample toast so the component is visible while editing.

**Contract**

| Property | Kind | Purpose |
|---|---|---|
| `SendToast(Header, Icon, [IconColor], [IconFilled], [Body], [Duration=7000], [ShowDismiss=true], [ShowTime=false], [ShowProgress=false])` | **Action** | The only call sites use. Builds the record with `CurrentTime`/`RemoveTime` and raises `AddToast`. |
| `AddToast(ToastRecord)` / `RemoveToast(ToastRecord)` | Event | Default bodies `Collect`/`Remove` on `colToasts`; override on the instance if the app uses a different collection. |
| `ToastTable` | Input (Table) | Defaults to `colToasts`. |
| `SortOrder` | Input | `SortOrder.Ascending` = oldest on top. |
| `AutoHeight` | Output (Number) | Bind the instance `Height` to it. |

**App-scope dependencies (justified under the component-contract rule):** `colToasts` and `varCurrentTime`. Initialise both in `App.OnStart`:

```powerfx
ClearCollect(colToasts, Filter(Table({Header:"", Icon:"", IconColor:Color.Gray, IconFilled:false, Body:"", Duration:7000,
    ShowDismiss:true, ShowTime:false, ShowProgress:false, CurrentTime:Now(), RemoveTime:Now()}), false));
Set(varCurrentTime, Now());
```

**Instance — last child of `cntPage` on every screen**

```yaml
- cmpToastHost:
    Control: CanvasComponent
    ComponentName: cmpToast
    Properties:
      ToastTable: =colToasts
      SortOrder: =SortOrder.Ascending
      Width: '=If(App.Width < BreakpointPhone, App.Width - 2 * Space4, 300)'
      Height: =Self.AutoHeight
      X: '=If(App.Width < BreakpointPhone, Space4, Parent.Width - Self.Width - Space2)'
      Y: '=If(App.Width < BreakpointPhone, HeaderHeight + Space4, Parent.Height - Self.Height - PhoneNavHeight * 0)'
```

Desktop/tablet: bottom-right (reference uses `X = Parent.Width - Self.Width - 8`, `Y = Parent.Height - Self.Height`). Phone: top, full-width, below the header so it never covers the bottom tab bar.

**Call sites — intent mapping is fixed; always pass icon + colour from tokens**

```powerfx
// success branch of IfError(Patch(...))
cmpToastHost.SendToast("Request saved", "CheckmarkCircle", ColorSuccess, true,
    "FOIA-" & Text(locNewId) & " is now In Progress.");

// failure branch — sticky (no auto-dismiss), with progress hidden
cmpToastHost.SendToast("Couldn't save the request", "DismissCircle", ColorDanger, true,
    "Check the required fields and try again.", 600000, true, false, false);

// warning / info
cmpToastHost.SendToast("Due in 2 days", "Warning", ColorWarning, true, "Statutory deadline is " & Text(locDue, "mmm d"));
cmpToastHost.SendToast("Assignment sent", "Info", ColorInfo, false, "", 5000, true, true, true);
```

| Intent | Icon | Colour token | Filled | Duration |
|---|---|---|---|---|
| Success | `CheckmarkCircle` | `ColorSuccess` | true | 7 000 |
| Error | `DismissCircle` | `ColorDanger` | true | 600 000 (effectively sticky; user dismisses) |
| Warning | `Warning` | `ColorWarning` | true | 10 000 |
| Info | `Info` | `ColorInfo` | false | 5 000 |

**Rules**

- `Notify()` is **not** used for user-facing outcomes; it is permitted only for developer diagnostics behind a debug flag.
- Every save, delete, assignment, send, approval, or failure raises `SendToast`. Screens never build toast UI themselves.
- Colour is reinforced by icon and header text (non-colour cue). Keep `Header` ≤ ~40 characters (it does not wrap); put detail in `Body`.
- Retokenise on import: `Fill` → `ColorSurface`, grey text → `ColorTextSecondary`, add `DropShadow.Regular` and `RadiusMedium` to `conToast` (the reference card is flat; our bar is carded).
- Accessibility additions on import: `conToast.AccessibleLabel = ThisItem.Header & ". " & ThisItem.Body`, `btnToastDismiss.AccessibleLabel = "Dismiss notification"`, `txtHeader.Live = Live.Polite`.
- Canvas MCP sync notes: drop the `@version` suffixes; `PropertyKind: Event` needs `Default` (present); `Action` properties with `Parameters` compile as shown. The sentinel-height pattern depends on reading `conAutoHeight.Y` and `conToast.Height` — both are readable, unlike `TemplateSize` (standard rule 11).

**Reuse shortcut:** export from the reference app (*Tree view → Components → Export components*), import into the new app, rename to `cmpToast`, apply the retokenise/accessibility steps above, and record the import in the component inventory.

---

## 6. Motion and feedback

- Screen transitions: `ScreenTransition.Fade` on desktop/tablet; `Cover`/`UnCover` on phone for list→detail.
- Buttons: use `Appearance` Primary (one per screen), Secondary, Subtle; never two Primary buttons visible at once.
- Hover/press are handled by modern controls — do not hand-roll `HoverFill` on classic controls.
- Loading: show a `cntSkeleton` (grey rounded rectangles matching row shapes) while `locIsLoading`; never an empty gallery.
- Saves: disable the button, swap its text to "Saving…", then raise a `cmpToast` (§5.9). Minimum perceived feedback 300 ms. `Notify()` is not a user-facing feedback surface.

---

## 7. Accessibility baked in

- Every icon-only button has `AccessibleLabel` and `Tooltip`.
- Tile values and badges include their label in `AccessibleLabel` (`"Open requests: 12"`).
- Status is always color **and** text/icon.
- Focus order follows visual order; `TabIndex` is left default inside AutoLayout.
- Contrast: `ColorTextTertiary` on white is caption-only; body text uses `ColorTextSecondary` or darker.
- Minimum 44-px touch targets at the phone tier; 32-px targets permitted on the desktop rail.

---

## 8. Elevated-UI acceptance checklist

Add to the skill's after-editing checklist. Each item needs a screenshot at the relevant tier.

- [ ] All colors, sizes, radii, fonts come from `App.Formulas` tokens; no literals in controls.
- [ ] Header, rail/phone nav, status badge, metric tile, empty state, and toast are **components** (or recorded exception).
- [ ] Phone: bottom tab bar present, single column, 44-px targets, no horizontal scroll, text ≥ 15 px body.
- [ ] Tablet: icon rail, 2-column tiles/forms, nothing clipped.
- [ ] Desktop: content capped and centered, master-detail or supplementary panel present, metrics in a strip or 4-up.
- [ ] Every list row has an accent bar or badge **and** a text status.
- [ ] Loading, empty, validation, error, success states each captured once.
- [ ] Every write outcome surfaces through `cmpToast` (success + error captured); no user-facing `Notify()` remains.
- [ ] One Primary button per screen; icon-only buttons have labels/tooltips.
- [ ] App Checker: zero errors, zero layout warnings (`FillPortions` + `Width` conflicts resolved).
- [ ] Side-by-side with the reference apps: header, rail, tiles, rows, and pills are visually indistinguishable in structure.

---

## 9. Reference evidence

Store sanitized screenshots of the reference apps and of each pilot at `visuals/power-apps/reference/` (names and data blurred). Capture, for each app: Home/Dashboard at desktop, tablet, phone; a detail screen; a form with validation shown; an empty state. These are the "before/after" images for the blog and portfolio.
