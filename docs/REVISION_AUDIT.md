> **Update 2026-09-30:** The student has now supplied [the syllabus](IS507-syllabus.md), which has been reviewed. Earlier missing-source statements below describe the 2026-09-29 audit only. Current requirements and the student's whole-project scope are in [COURSE_REQUIREMENTS.md](COURSE_REQUIREMENTS.md). This update changes documentation, not the analysis or holdout policy.

# Revision audit — 2026-09-29

This revision starts from the user's Desktop project, not a replacement implementation. Original model, features, calendar splits, primary maturity gate, structural NULL handling and duplicate sensitivities are retained.

## Changes

- `src/utils.py`: enforced approved feature set and expanded exclusions. A new regression test first failed for all ten previously accepted unapproved fields; after repair all eight tests passed. Boundary-date and holdout-missing-status tests also pass.
- `src/analysis.py`: corrected source-based reasons for country, repeated-guest and history exclusions, with risk categories and source attribution. Added development-candidate-only maturity and status/departure audits; added combined endpoint assertion. Confusion matrix now labels the positive class cancellation/no-show.
- `src/reporting.py`: generated report follows the requested 13 sections; first screen gives question, outcome and revised estimand. Existing evidence, baseline, errors, uncertainty and sensitivity results retained. Claim–evidence artifacts are clickable.
- README and FINAL_CHECKLIST restored as new files; Project_spec updated; inherited source/course/verification notes explicitly marked when source evidence is absent. Notebook audit introduction updated. File manifest regenerated from actual files.
- `verify_outputs.py`: extra checks reconcile maturity tables, enforce audit/feature agreement, confirm outcome semantics, section order and local links.

## Maturity interpretation

Training: original combined gate admits 39,865 rows. Status-only admits 45,603, adding 5,738 (5,730 canceled, 6 no-shows and 2 check-outs). Validation: combined gate admits 14,088; status-only admits 18,168, adding 4,080 (4,077 canceled and 3 no-shows). These comparisons use development candidates only.

The extra departure condition is unnecessary for an already recorded cancellation's label availability. It defines a restricted cohort and avoids preferentially admitting resolved cancellations from future stays; it also alters lead-time/season composition. Retain the original primary rule, report this tradeoff and do not choose a replacement on model performance. The legacy `unmatured` suffix does not imply every excluded outcome was unknown.

Date audit: no development candidate has status before reconstructed booking. In train candidates, 16 Check-Out rows have status earlier than snapshot-derived departure; two become extra status-only cases. This discrepancy could reflect amendment/early-departure semantics; the public release cannot establish the cause. Validation Check-Out dates all equal derived departure. Cancellations before arrival are expected, not automatically date errors. Strict `< cutoff` remains because intraday ordering is unavailable.

## Source verification

Rechecked the original paper's Table 1 and operational caution in Section 2 through the public full text: https://pmc.ncbi.nlm.nih.gov/articles/PMC6297060/ . The source supports profile-date checks for repeated guests, payment-derived deposit categories and nationality uncertainty at check-in. Conservative exclusions of uncertain history/customer-type fields are project judgments, not proof of future information. The mirror dictionary is preserved unchanged.

## Remaining human decisions

Confirm the revised estimand with the instructor; obtain the absent syllabus and exact assignment/rubric; verify deadline, formatting and AI-use policy; supply actual names/contributions. Original feature snapshots, guest identifiers, exact historical revisions and publisher-ZIP equivalence remain unavailable. The 0.5 model recall is about 0.30%; do not claim an effective live alert system.

## Execution evidence

Current test, notebook and output-verification logs are saved alongside this file. Notebook execution initially failed because the sandbox prohibited local kernel sockets, then was retried with local execution permission. Final holdout outcomes are never summarized, scored or used for model selection. Raw source and holdout file byte identity are checked before applying changes.

Final verification: **8 tests passed; 5 notebooks executed; 40 output checks passed.** The raw CSV, locked holdout CSV, row manifest and model metrics match original bytes. Confusion-matrix labels visually inspected without clipping.
