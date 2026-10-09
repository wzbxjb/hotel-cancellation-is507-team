# Frozen evaluation protocol — 2026-10-08

Written before final-holdout outcome inspection or prediction in this project.
The September 30 corrected project is the development source. Its fixed primary
model, feature policy, train/validation partitions and maturity gate are retained.

## Question and prediction time

Intended decision: at reservation creation, estimate eventual noncompletion.
Identified question: retrospective discrimination and probability quality using
released snapshots in explicitly selected booking cohorts. These two questions
are not interchangeable. No source creation-time snapshot is available.

## Frozen model and outcomes

- Endpoint: original `is_canceled`; verify Canceled/No-Show = 1, Check-Out = 0.
- Primary model: existing train-only logistic regression, L2 C=1, lbfgs,
  max_iter=3000, seed 507, approved 13 engineered/raw predictors.
- Baseline: constant training positive fraction. Neither model is refitted on
  validation. The same fitted model is compared across both evaluation periods.
- No new models, parameter tuning, feature selection or post-hoc calibration.
- Primary comparison: mean log loss (lower is better).
- Secondary: ROC-AUC, average precision, Brier; classification at fixed 0.5;
  fixed top-10% cohort ranking, ties resolved by ascending source row_id.
- Training deduplication and smaller-feature specifications remain validation
  sensitivities only; they are not competing final-test model candidates.

## Final test eligibility

Start with the previously locked booking-date-proxy >= 2017-01-01 partition.
Evaluate only proxy dates in [2017-01-01, 2017-06-01), with BOTH planned departure
and last-status date strictly before 2017-09-01, and status_date >= booking_date.
The five-month booking window leaves at least three calendar months before
source arrival coverage ends (2017-08-31). It reduces, but cannot remove,
right-boundary truncation of long-lead bookings. Later proxy dates are unused.
The maturity gate is selected-cohort restriction, not proof of unbiased label
availability. Do not interpret `unmatured` as always unknown outcomes.

Report candidate, excluded and eligible counts, target semantics, date boundaries,
exact full-row development/test overlap, selected cohort prevalence, subgroup
diagnostics and all primary results, including unfavorable results.

The test may be scored once after this freeze. Re-execution for deterministic
reproducibility and checksum verification is permitted; no resulting design
changes may be selected based on test performance. It is a later calendar test
of a retrospective benchmark, not a simulated live deployment or untouched
population sample. No causal or revenue impact is estimated.

## Course requirements

Ten-minute English presentation; Markdown/PDF research report at most five A4
pages; GitHub code and shareable repository URL. Use the five questions supplied
in the referenced conversation (Lecture 9 pp.75–80 of the 87-slide version).
The local 61-page v2 PDF covers model evaluation but omits those project slides.
Presentation date: October 13 or 15, 2026; group unknown. Do not invent a separate
report/code submission deadline, team number, identities or contributions.
