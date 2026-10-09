# Complete-project understanding and individual component

The student clarified on 2026-09-30 that the instructor expects each person to complete and understand the entire project. This working copy therefore covers the student's end-to-end analysis; no stage is assigned to another teammate. The supplied [syllabus](../docs/IS507-syllabus.md) explicitly requires every student to explain the complete project and permits AI assistance with verification. It retains team deliverables and a separate individual component.

## Prepare to explain the whole project

| Stage | What you should be able to explain | Evidence |
|---|---|---|
| Question and scope | Why retrospective ranking/association; why not proven creation-time prediction | Report sections 1–5 |
| Data and outcome | How PMS records become the observed sample; booking unit; canceled + no-show | Source and target cross-tab |
| Data quality | Structural NULL versus missing values; why identical rows are retained | Audit and duplicate sensitivities |
| Feature policy | Why each field is included conditionally or excluded | Feature audit and pipeline guard |
| Dates and maturity | Why both status/departure are used; cost of excluding already-known cancellations | Maturity and date audits |
| Preprocessing | Which transforms learn from training only | Pipeline and preprocessing checks |
| Models | Dummy baseline, logistic assumptions and fixed specification | Baseline comparison |
| Evaluation | AUC versus probability quality versus threshold recall | Metrics, calibration and confusion matrix |
| Errors and sensitivity | Where the model fails; what deduplication can and cannot establish | Error, subgroup and sensitivity results |
| Claims and next steps | Supported claims, uncertainty, non-use conditions and locked final holdout | Claim–evidence table |

## Individual midterm component

Select one decision from your complete analysis and explain it in your own reasoning:

1. What decision did you make, and what alternative did you consider?
2. Which executed evidence supports it?
3. What risk remains, and what would you do next?

A suitable choice is the maturity rule: retaining the original combined gate costs sample size, whereas status-only eligibility adds 4,080 validation bookings, all canceled or no-show. Explain both selection mechanisms; do not describe either rule as automatically unbiased.

Other choices include retaining exact duplicate rows, defining the combined outcome, limiting uncertain features, or explaining why 73.72% accuracy with 0.30% recall does not establish a useful alert system.

This focused component is additional to whole-project understanding. The contribution statement should describe your actual end-to-end work and verification. AI-assisted implementation/drafting is compatible with the supplied course policy; independent explanation and verification remain your responsibility. Final submission grouping follows the instructor's current instructions.
