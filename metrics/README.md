# Metrics outcome reporting

`analyze_outcomes.py` is a standard-library CLI for descriptive comparisons of the
`baseline-and-outcomes.csv` contract. It does not edit the source CSV or infer
organization outcomes.

## Run

```sh
python metrics/analyze_outcomes.py --input path/to/observations.csv --output path/to/report.json
```

Both paths are required and must differ. The output file is written only after
the entire input validates. Invalid input prints row-specific diagnostics to
stderr, exits nonzero, and does not write a report.

## Input rules and comparison

- The CSV header is the contract in `baseline-and-outcomes.csv`; every contract
  header is required. Additional columns are accepted and ignored.
- Each non-empty row is one task observation with a unique `Measurement ID` and
  `Sample Size` exactly `1`. Split pre-aggregated data into task-level rows;
  the CLI will not invent weighted medians or ranges.
- `Actual or Estimate` accepts `Actual` or `Estimate` (case-insensitive). Those
  claim classes are always reported in separate groups.
- Groups are comparable only when `Project`, `Activity`, `Standard Version`,
  `Start Definition`, `Stop Definition`, and claim class all match exactly.
- `Baseline Minutes` is the baseline duration for one task measured from the
  row's start definition to its stop definition, captured before introducing
  the skill or automation. `AI Assisted Minutes` is the corresponding duration
  for the same task unit and definitions with AI assistance.
- Paired duration change is `Baseline Minutes - AI Assisted Minutes`, computed
  only when both values are present. Positive values indicate a shorter
  assisted duration; negative values indicate a longer one. No percentage
  improvement is calculated, so a zero baseline cannot produce a division by
  zero or a misleading percentage.
- Review, rework, waiting, deployment, and independent assistance times are
  summarized separately. They are not added to either duration because
  components may overlap. Zero is measured zero; a blank numeric cell is
  unknown. No blank component is inferred to be zero.
- Durations and counts must be finite and non-negative; counts must be integer
  values. Documentation completeness must be from 0 through 100. Critical tests
  passed cannot exceed planned when both are known. Invalid rows reject the
  complete input rather than being discarded.

## JSON output contract (schema version 1)

- `schema_version`: integer output contract version.
- `status`: `reported` when at least one paired duration exists, otherwise
  `insufficient_data`. The latter includes empty and header-only input and is
  never a realized-savings result.
- `dataset_classification`: `synthetic` when every row's `Data Source` starts
  with `synthetic:`, `mixed` when only some rows do, or `unclassified` when
  none do. This describes fixture provenance, not the `Actual or Estimate`
  claim class. Mark invented fixture sources explicitly; `Actual` in a
  synthetic fixture remains invented input, not an organization outcome.
- `observation_count`, `group_count`, and `groups`: number of task observations,
  comparison groups, and their reports.
- Each group's `comparison` contains the six exact comparison keys and
  `claim_class`; `sample_size` counts task observations in that group.
- `metrics` has a summary for every duration, count, and percentage column.
  Each summary contains `status`, `observation_count`, `median`, `minimum`, and
  `maximum`. `status` is `available` when values exist and `unknown` when all
  values are missing; unknown summaries have a zero count and null statistics.
- `paired_duration_change_minutes` uses the same summary shape, but counts only
  rows with both baseline and assisted durations.
- `sources` and `exclusions` list the distinct non-empty values recorded in
  that group. Exclusions describe the input observations and do not silently
  remove any row from analysis.
- Group and report `limitations` explicitly caution that the comparison is
  descriptive, not causal or organization-wide, and that component durations
  may overlap. The reported range is descriptive; no uncertainty interval is
  estimated.

The CLI makes no causal, organization-wide, deployment, approval, or benefit
claim. The report is not an automatic determination that any benefit is
realized. Evidence review and the scorecard's measurement rules remain
necessary.

## Synthetic fixture

`fixtures/synthetic-outcomes.csv` contains five wholly invented task rows:
three actual-class rows in one comparable group with baseline values 100, 120,
and 80 minutes and assisted values 80, 90, and 100; one separate estimate-class
row; and one actual-class row with a different activity. Every source begins
with `synthetic:` and every note says the value is invented, not an organization
outcome. The fixture exists only to exercise actual/estimate separation,
grouping, median/range arithmetic, duration change, and source labeling. It is
not evidence about a pilot or organization.

## Validation and handoff

Commands run from the repository root:

```sh
python -m unittest discover -s metrics -p 'test_*.py' -v
python scripts/validate_repo.py
```

Results: the unit-test command passed all 9 metric CLI tests, and the repository
validation command printed `VALIDATION PASSED`.

Files changed for this work: `metrics/analyze_outcomes.py`,
`metrics/test_analyze_outcomes.py`, `metrics/fixtures/synthetic-outcomes.csv`,
and this README. The existing baseline CSV and all files outside `metrics/`
remain unchanged. Downstream use depends on the CSV contract and consumers
respecting the JSON v1 null/unknown states and grouping semantics. No downstream
report consumer or automated benefit approval is included.

The repository PR template was inspected; retain its `Summary`, `Changes made`,
`Validation`, and `Handoff notes` headings and applicable checklist prompts in
the draft PR description.
