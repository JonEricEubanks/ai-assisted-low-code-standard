# Visual Verification Standard

Applies to Power Apps, Power Automate, SharePoint, and any other surface an end user sees.

## Principle

Every bounded change has two halves that are both mandatory:

| Half | Done through | Proves |
|---|---|---|
| **Backend change** | Authoring service MCP, YAML sync/compile, Graph/REST, approved CLI | The definition is syntactically valid and saved |
| **Visual verification** | The shared integrated browser viewing the real rendered surface | The thing a human will actually see is correct |

A clean compile, a successful API response, or a passing App Checker is **not** acceptance. Only inspecting the rendered surface is.

## Why this exists

The first Flossmoor FOIA build compiled clean with zero App Checker errors while the rendered Dashboard showed a portrait phone frame on a desktop target, header buttons wrapping mid-word, KPI cards with broken image placeholders, and five layout warnings. None of that is visible in YAML. It was visible in a single screenshot.

## Required loop

```
edit → compile/sync → open rendered surface → capture → inspect → record → (fix and repeat)
```

1. Make the backend change through the authoring tool.
2. Compile, sync, or save as the platform supports.
3. Open the real rendered surface in the shared browser — Studio canvas, Player, flow designer, flow run, SharePoint list/page/library.
4. Capture at each supported breakpoint. Default: phone 390, tablet 820, desktop 1366 CSS px wide.
5. Inspect the capture for the defect classes below.
6. Record findings with the capture reference, breakpoint, and disposition.
7. Fix and repeat until each breakpoint is clean or the remaining item has a named owner and recorded reason.

## Defect classes to inspect for

| Class | Examples |
|---|---|
| Layout | Clipping, overflow, wrong orientation, fixed-size containers that do not reflow, overlapping controls |
| Text | Truncation, mid-word wrapping on buttons, unreadable size, missing `AutoHeight` on wrapping labels |
| Imagery | Broken or placeholder images, stock images that did not resolve, missing icons |
| State | Empty state not rendering, loading state stuck, error state hidden, success not reflected |
| Density | Touch targets under 44 px on phone or tablet, controls crowding at narrow widths |
| Consistency | Shell elements that differ between screens because they were duplicated rather than componentized |
| Fluent | Non-Fluent colors, type, or spacing where Fluent tokens were required |
| Flow designer | Unresolved dynamic content, missing connection reference, action with configuration warning badge |
| SharePoint | Column formatting not applied, view missing columns, page web part rendering empty |

## Platform-specific surface

| Platform | Backend tool | Surface to open | Capture |
|---|---|---|---|
| Power Apps | Canvas MCP sync/compile | Studio canvas for each screen; Player for runtime | Each screen at each breakpoint |
| Power Automate | flowagent MCP or CLI | Flow designer for structure; a run detail for behavior | Designer full page; run summary with action results |
| SharePoint | Graph/REST or PnP/CLI | List default view, form, and any page using it | View; new-item form; page at desktop and phone |

## Evidence

Captures are retained under the pilot's evidence folder with filename `{surface}-{breakpoint}-{yyyymmdd-hhmm}.png`. Each capture is referenced from the change's test record together with the finding and disposition. Captures that contain client data are internal-only; public examples are re-created with synthetic data per `governance/evidence-boundary.md`.

## What the agent must not do

- Claim visual acceptance from compile or App Checker output alone.
- Skip a breakpoint because another one passed.
- Fix a defect by hiding the control at that breakpoint without recording it.
- Capture a stale tab; reload or re-sync before capturing.
- Capture the designer when the defect only appears at runtime, or vice versa.

## Related

- `standards/power-apps.md`
- `standards/power-automate.md`
- `standards/sharepoint.md`
- `qa/qa-strategy.md`
- `qa/screenshot-plan.md`
