# Hotel Cancellation Prediction — IS 507 Midterm Revision

A retrospective benchmark of **booking noncompletion (cancellation / no-show)** in two Portuguese hotels. One row is a booking, not a unique guest. Later snapshots prevent certifying a prediction at reservation creation.

## Submitted document (per latest instructor requirements)

- [Preliminary project proposal (PDF, 5 pages)](deliverables/Hotel_Cancellation_Report_Group16.pdf) — Group 16: motivation, problem, related work, data and challenges, baseline/model plan.
- [Proposal presentation (11 slides)](deliverables/Hotel_Cancellation_Presentation_Group16.pptx) — 8-minute talk with speaker notes.

## Midterm deliverables

- [English presentation](deliverables/IS507_Midterm_Presentation.pptx): 11 main slides, 4 hidden backups, speaker notes. Speaking targets total 9 minutes 10 seconds; a timed rehearsal is still needed.
- [Five-page A4 report PDF](deliverables/IS507_Midterm_Report.pdf) and [editable Markdown](deliverables/IS507_Midterm_Report.md).
- [Rehearsal and role guide](deliverables/Rehearsal_and_Team_Guide.md).
- [Detailed bilingual handbook](deliverables/IS507_讲稿与问答理解手册.md) and [plain text](deliverables/IS507_讲稿与问答理解手册.txt): 15 slide explanations, 35 Q&As, glossary and numeric reference.
- Six previously executed notebooks and source code, with saved results independently reverified for this revision.

Group 16: Zhe Wang and Zhengxuan Du. Both members participate in every stage, including analysis, report writing and presentation preparation. Zhe places greater emphasis on coding and Zhengxuan on slides. Both understand and explain the complete project. Actual completed contributions need an honest record. Submit one team report, after all members join the correct Project Teams group.

This revision centers the midterm narrative on validation initial analysis. It also discloses the already-scored October 8 later test. No model, features, split, eligibility rule or frozen protocol was changed for better test results.

## Reproduce

Tested with Python **3.11.5**. Start in this repository's root:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python run_all.py
python run_notebooks.py
python verify_outputs.py
```

On Windows activate with `.venv\Scripts\activate` instead. `run_all.py` is the non-notebook path; Jupyter execution additionally requires permission to open local kernel ports. No GPU is needed. Raw data are included; `download_data.py` downloads only if absent and rejects a changed checksum. Processed CSVs/models are regenerated and excluded from Git. Notebook results and public aggregate tables/figures are committed. Dependencies are pinned to the environment actually used; a separate clean installation on another machine has not been tested.

The submitted report/PPTX are checked-in summaries of the recorded run. Reproduction regenerates empirical tables/figures, not presentation typography. Small floating-point differences across platforms may occur. The frozen final-test guard deliberately stops if the saved protocol/model/results differ: investigate, do not tune or delete the guard to improve test performance.

## Study design

Read the [frozen final-evaluation protocol](docs/FINAL_EVALUATION_PROTOCOL.md), [corrected prior specification](Project_spec.md) and [feature audit](tables/prediction_time_leakage_audit.csv).

1. Preserve raw tokens and verify SHA-256; construct `booking_date = arrival_date - lead_time`, explicitly a proxy.
2. Reuse train (39,865 rows, July 2015–June 2016) and validation (14,088, July–December 2016); both terminal status and planned departure precede each origin.
3. Fit preprocessing and logistic regression only on training; baseline is constant training prevalence 0.30749. C=1, L2, lbfgs, seed=507; no tuning, class weighting or recalibration.
4. Freeze January–May 2017 test and require both dates before September 1, 2017. Test n=22,541; 328 window candidates excluded; 3,696 later holdout rows unused. No refit on validation.
5. Primary: mean log loss. Secondary: ROC-AUC, average precision, Brier; fixed 0.5 classification; fixed top-10% cohort ranking. Validation-only sensitivities are not final-test model selection.

| Later-period test | Training-prior baseline | Logistic regression |
|---|---:|---:|
| Log loss ↓ | 0.6328 | 0.5968 |
| ROC-AUC ↑ | 0.5000 | 0.6644 |
| Average precision ↑ | 0.3269 | 0.4714 |
| Brier ↓ | 0.2204 | 0.2051 |
| Recall at 0.5 | 0.00% | 6.62% |

Top 10%: 2,255 bookings, 1,304 positives; precision 57.83%, recall 17.70%. This is static retrospective ranking, not a daily queue or proven intervention. **Conclusion:** modest ranking / probability improvement; hold operational use.

## Sources and limitations

- Antonio, de Almeida & Nunes (2019), [Hotel booking demand datasets](https://doi.org/10.1016/j.dib.2018.11.126), original data article, CC BY 4.0.
- [TidyTuesday Hotels, 2020-02-11](https://github.com/rfordatascience/tidytuesday/tree/main/data/2020/2020-02-11), combined mirror and dictionary.
- Raw SHA-256: `7c2ae42a7353905ea136e5c2287f17c92c5435826598bfbb8491c6f0c7b1fc06`.
- 119,390 rows, 32 columns; arrivals July 2015–August 2017. Structural consistency is checked; publisher supplementary files were not compared byte by byte.
- Source snapshots, selected maturity/arrival cohorts, two hotels, unknown guest/group dependence, and low recall restrict inference. No causal effects, revenue gains, global generalization or certified creation-time performance are claimed.
- [Provenance/reuse record](docs/REUSE_AND_COURSE_AUDIT.md) distinguishes old validation results from newly executed final-test results.

## GitHub submission

The local GitHub CLI was installed, but its existing account credential failed authentication on October 8, 2026. **No remote repository was created or uploaded.** Follow [the exact upload steps](deliverables/GitHub_Upload_Guide.md), then paste the real repository URL in the course submission. The zip is an upload-ready package, not a published repository.

## Team participation

Both members participate in all stages and understand the complete analysis. Zhe places greater emphasis on coding, while Zhengxuan places greater emphasis on slides. Each member checks the submitted claims and explains the methods, evidence and errors.
