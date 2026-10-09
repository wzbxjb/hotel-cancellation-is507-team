> **Update 2026-09-30:** The student has now supplied [the syllabus](IS507-syllabus.md), which has been reviewed. Earlier missing-source statements below describe the 2026-09-29 audit only. Current requirements and the student's whole-project scope are in [COURSE_REQUIREMENTS.md](COURSE_REQUIREMENTS.md). This update changes documentation, not the analysis or holdout policy.

> **Revision note (2026-09-29):** The syllabus file cited by the inherited text below is absent from this project. Its review history, course dates and requirements are not independently verified in this revision. The assignment screenshot is also unavailable. Current execution evidence is in [REVISION_AUDIT.md](REVISION_AUDIT.md).

# IS507 analysis execution plan

Scope: execute the user's specified Midterm analysis in this standalone output folder; do not publish or submit. The full previous prompt and assignment screenshot could not be retrieved. A local syllabus dated 2026-08-25 is available and copied here. Its identity with IS507-syllabus(1).md is unconfirmed.

1. Freeze source bytes and SHA256, verify published row/hotel counts and schema; document provenance and course requirements.
2. Write and run integrity tests for date reconstruction, partition boundaries, label maturation, unknown categories, and holdout evaluation refusal.
3. Freeze calendar splits before model fitting: reconstructed booking date before 2015-07-01 = left-boundary exclusion; 2015-07-01 to 2016-06-30 = train candidates; 2016-07-01 to 2016-12-31 = validation candidates; 2017-01-01 onward = sealed final holdout.
4. For train and validation require planned departure and recorded terminal status before the next partition origin, and status date not before reconstructed booking date. This conservative retrospective eligibility rule reduces outcome-availability leakage but changes the eligible population; document exclusions. Status dates never enter X. Do not analyze holdout targets or generate holdout predictions.
5. Primary analysis retains identical rows: no booking ID proves they are errors. Sensitivity fits after train-only exact deduplication, with unchanged validation evaluation, and separately reports unique-row validation weighting. Unknown guest/group dependence remains.
6. Fit all learned transforms on eligible training rows. Predeclared Dummy prior, logistic C=1, threshold=.5; no tuning search. Reduced feature sensitivity and extended provisional features are descriptive sensitivity analyses only. No deployment claim from mutable snapshots.
7. Train-only EDA; validation metrics, confusion matrix, ROC/PR, calibration, error/subgroup analyses, paired week-cluster bootstrap intervals as approximate stability diagnostics.
8. Generate and execute five notebooks, report, README, claim-evidence table and checklist. Audit package consistency, inspect figures, obtain independent review, repair defects and rerun affected checks.

Main methodological risks: snapshot time differs from intended prediction time; reconstructed dates can be inconsistent; arrival-window selection distorts booking cohorts; row equality does not identify entities; both hotels are convenience sources; terminal label includes no-shows. Do not disguise these with high AUC.
