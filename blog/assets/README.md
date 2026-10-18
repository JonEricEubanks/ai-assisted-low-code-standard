# Blog Visual Capture Set

Captured with Playwright on 2026-10-17 from [the local capture board](capture-board.html). These are browser-rendered **synthetic editorial illustrations**, not screenshots of Power Apps, Power Automate, SharePoint, or a deployed pilot. No platform validation, adoption, release, or measured improvement is demonstrated.

## Asset index

| Evidence ID | Article | Image | Caption |
|---|---|---|---|
| EVD-BLOG-001 | [Governed standard](../article-01-governed-standard.md) | [Before/after](2026-10-17_blog_synthetic_governed-standard_draft.png) | Fictional intake paths make checks and human ownership explicit; no measured improvement is asserted. |
| EVD-BLOG-002 | [Lifecycle](../article-02-delivery-lifecycle.md) | [Stage decisions](2026-10-17_blog_synthetic_delivery-lifecycle_draft.png) | Proposed lifecycle from acceptance criteria to verification, handoff, and human release authority. |
| EVD-BLOG-003 | [Reusable skills](../article-03-reusable-skills.md) | [Bounded contract](2026-10-17_blog_synthetic_reusable-skills_draft.png) | Generic skill contract with explicit inputs, bounded assistance, and verified output. |
| EVD-BLOG-004 | [SharePoint design](../article-04-sharepoint-design.md) | [Data-to-view path](2026-10-17_blog_synthetic_data-contract_draft.png) | Conceptual synthetic data path; not a SharePoint product screenshot or deployment design. |
| EVD-BLOG-005 | [Layered QA](../article-05-qa-system.md) | [QA responsibilities](2026-10-17_blog_synthetic_layered-qa_draft.png) | Deterministic checks, accessibility/visual review, and human release authority remain distinct. |
| EVD-BLOG-006 | [Measurement](../article-06-measurement.md) | [Claim controls](2026-10-17_blog_synthetic_measurement_draft.png) | Comparison, reporting, and claim classification controls; no outcome values are asserted. |

Alt text is embedded with each image in its article. Captions and source classifications remain part of the publication package.

## Source and transformation

Original fictional concepts from [the synthetic visual set](../../portfolio/synthetic-visuals.md) and the six synthetic article drafts were recreated as local HTML/CSS. No internal media, platform session, client record, or existing pilot screen was used. Each image carries its own synthetic/draft label and publication warning so it remains identifiable when copied separately.

## Capture and checks

- Source: `capture-board.html`; no remote scripts, fonts, images, or network dependencies.
- Browser: standalone Playwright browser, viewport 1320 x 820 CSS pixels.
- Method: element screenshots of the six `figure` elements, with animations disabled and CSS pixel scale.
- Output: six 1200 x 675 PNGs, one complete figure per file.
- Inspected all six saved images for legibility, complete captions, and correct crop.
- Checked figure dimensions and absence of content overflow.
- An initial integrated-browser capture included neighboring figures; those files were replaced by the standalone Playwright captures.
- These are asset/layout checks only, not a completed accessibility review or release-gate evidence pack.

To recapture, serve only this folder on loopback:

```powershell
python -m http.server 8767 --bind 127.0.0.1 --directory .\blog\assets
```

Open `http://127.0.0.1:8767/capture-board.html` with Playwright. Set the viewport above, then capture these selectors individually using `locator.screenshot` with `animations: "disabled"` and `scale: "css"`:

| Selector | Filename subject |
|---|---|
| `#governed-standard` | `governed-standard` |
| `#delivery-lifecycle` | `delivery-lifecycle` |
| `#reusable-skills` | `reusable-skills` |
| `#data-contract` | `data-contract` |
| `#layered-qa` | `layered-qa` |
| `#measurement` | `measurement` |

Preserve the filename convention `YYYY-MM-DD_blog_synthetic_SUBJECT_draft.png`. Stop the temporary server when capture is complete.

## Remaining gates

All assets are **not approved for external publication**. Independent content, privacy/security, proprietary-content, accessibility, and publication review remain pending in [the approval record](../publication-review.md). Final venue layout and scaled-image readability still need review. Entries in [the screenshot register](../../qa/screenshot-register.csv) track illustration provenance, not successful platform tests.

Actual product screenshots require a separate approved synthetic demonstration environment and an agreed journey. Keep real/internal pilot captures in approved internal storage, not this asset set.
