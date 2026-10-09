# Verification — October 8, 2026

- All eight inherited scientific integrity tests passed.
- All six notebooks executed in clean kernels using Python 3.11.5; no error outputs.
- `verify_outputs.py`: 65 checks passed, including independently recomputed validation/test metrics, saved-model probability reproduction, disjoint row IDs, temporal/maturity rules, source checksum, target semantics, top-10% accounting and deliverable metrics.
- Report parsed as exactly five A4 pages and all five page renders inspected.
- PPTX: 15 total slides, 10 visible and five hidden backups; all 15 have speaker notes. All slides inspected visually. Native tables and both editable charts verified; chart workbooks embedded. Final packaged chart/results slides reimported and rendered.
- PowerPoint application execution was not tested; structural/import/render checks do not establish native application behavior.
- Full analysis rerun with the final run_all.py entry point; empirically frozen test outputs reproduced without tuning.
- Clean dependency installation on a separate computer was not tested. See README for the tested environment and package pins.
- GitHub CLI authentication failed because the existing credential was invalid; no remote repository was created/uploaded.

Revision: Group 16 and both user-confirmed members added; report explains booking terms and evaluation results for readers without hotel background. All five revised pages and edited cover/date slide inspected; PDF remains five A4 pages. Empirical results and code unchanged.


## Audience-focused PPT revision (2026-10-08)

The 10 main slides now explain hotel terms before using them, map to the five course questions, explain X/Y/probability with an explicitly illustrative example, and interpret baseline, log loss, AUC and recall in plain English. Exact parameters and secondary metrics remain in hidden backup slides. All 15 notes match the synchronized rehearsal guide. Speaking targets total 465 seconds (7:45); actual timing requires rehearsal. The deck was reimported and rendered for review; package/layout checks pass. Analysis outputs, source hash and frozen protocol are unchanged.
