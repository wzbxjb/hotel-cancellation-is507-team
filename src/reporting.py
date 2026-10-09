"""Generate report numbers directly from saved, executed analysis tables."""
import json
from .utils import *

def write_report():
    get=lambda name:pd.read_csv(ROOT/'tables'/name)
    metrics=get('validation_metrics.csv'); m=metrics.set_index('model').loc['Logistic primary']; b=metrics.set_index('model').loc['Dummy prior']
    tr=read_partition('train'); va=read_partition('validation')
    split=get('split_counts.csv'); audit=get('development_audit.csv').set_index('check')['count']
    ci=get('week_cluster_bootstrap.csv').set_index('metric')
    ranks=get('ranking_capacity.csv'); r=ranks.iloc[1]
    sg=get('subgroup_metrics.csv'); hotel=sg[sg.grouping.eq('hotel')]
    miss=get('raw_missing_tokens.csv'); spec=get('model_specification.csv').iloc[0]
    f=lambda v:f'{v:.3f}'
    pct=lambda v:f'{100*v:.2f}%'
    metric_table=metrics[['model','n','roc_auc','average_precision','accuracy','recall','precision','brier','log_loss']].to_markdown(index=False,floatfmt='.4f')
    claims=pd.DataFrame([
        ['Logistic scores show modest discrimination on the eligible retrospective validation cohort.',f"AUC {m.roc_auc:.4f}; Dummy {b.roc_auc:.4f}; approximate week-bootstrap interval [{ci.loc['roc_auc','lower_2_5']:.4f}, {ci.loc['roc_auc','upper_97_5']:.4f}].",'Supported for this cohort only.','tables/validation_metrics.csv; tables/week_cluster_bootstrap.csv'],
        ['The default 0.5 threshold is unsuitable for a high-recall non-completion alert.',f"TP={int(m.tp)}, FN={int(m.fn)}, recall={pct(m.recall)}; accuracy={pct(m.accuracy)}.",'Supported descriptive failure; operational cost still unknown.','figures/04_confusion_matrix.png'],
        ['Ranking may be more useful than the default hard decisions.',f"Top 10% precision={pct(r.precision_at_k)}, recall={pct(r.recall_at_k)}, overall prevalence={pct(m.prevalence)}.",'Exploratory retrospective result; capacity and utility unvalidated.','tables/ranking_capacity.csv'],
        ['This is a valid deployed reservation-time model.','No original feature snapshots or confirmed creation timestamps.','Not supported; HOLD deployment.','tables/prediction_time_leakage_audit.csv'],
        ['A feature causes customers to cancel.','Observational records, no intervention or identification design.','Not supported.','report/MIDTERM_REPORT_DRAFT.md'],
        ['The same performance applies to all hotels, countries, or future years.','Two specific Portuguese hotels; arrival-window selection; no external validation.','Not supported.','docs/SOURCES.md'],
        ['Deduplication resolves repeated-guest dependence.','Exact-row sensitivity is available; guest/group IDs are absent.','Not supported; dependence persists.','tables/development_audit.csv'],
        ['Final-test performance is known.','Final holdout not scored.','Not evaluated.','data/processed/HOLDOUT_POLICY.md'],
    ],columns=['claim','evidence','status_or_limit','artifact'])
    table(claims,'claim_evidence.csv')
    (ROOT/'report/CLAIM_EVIDENCE.md').write_text('# Claim–evidence table\n\n'+claims.assign(artifact=claims.artifact.map(lambda paths: '; '.join(f'[{x}](../{x})' for x in paths.split('; ')))).to_markdown(index=False)+'\n')
    report=f'''# Retrospective Ranking and Association Analysis of Hotel Booking Non-Completion

**IS507 Midterm report draft — analysis date 2026-09-29; course requirements checked 2026-09-30.** This working copy covers the student's complete end-to-end project: problem formulation, data audit, preprocessing, modeling, evaluation and interpretation. Every stage is within the student's responsibility and preparation scope. The supplied syllabus has been reviewed; the specific Midterm Assignment screenshot remains unavailable. No final holdout predictions were made.

### 1. Research Question & Revised Estimand

**Research Question:** Which observable booking characteristics are associated with hotel booking non-completion, and how well can they distinguish completed bookings from cancellations or no-shows in the eligible retrospective cohort?

**Outcome:** `is_canceled = 1` includes Canceled + No-Show; `is_canceled = 0` corresponds to recorded Check-Out. The unit is one booking, not one guest. This does not measure guest intent or an intervention effect.

**Revised estimand:** Retrospective discrimination, probability quality and predictive associations on the calendar- and maturity-selected sample. This is not strict booking-creation-time prediction: the released data do not preserve complete point-in-time feature snapshots. The horizon is the recorded terminal booking outcome, not a fixed number of days.

**Current recommendation: HOLD operational use; continue the educational retrospective analysis.** The primary logistic model achieved validation ROC-AUC {f(m.roc_auc)} versus {f(b.roc_auc)} for a constant-probability baseline. Yet the 0.5 decision threshold recovered only {int(m.tp):,} of {int(m.tp+m.fn):,} positives. More fundamentally, the public dataset does not provide original creation-time snapshots. Prospective operational performance is outside the supported estimand. The executable benchmark concerns a restricted retrospective cohort and conditionally plausible predictors, not a certified reservation-time deployment.

### 2. Data Source & Generation

Antonio, de Almeida and Nunes (2019) describe anonymized records from two Portuguese hotel property-management systems (PMS): one resort in Algarve and one city hotel in Lisbon. The public data include bookings with scheduled arrivals from July 2015 through August 2017. TidyTuesday combines the two source tables and standardizes field names. We retrieved its CSV and verified 119,390 rows, 32 columns, hotel counts (40,060 resort; 79,330 city), and the published arrival-date range. The checksum and source URL are saved in `data/raw/PROVENANCE.json`. This verifies structural consistency, not byte identity with the publisher's supplementary ZIPs.

### 3. Outcome Definition

The development-only status/target cross-tab below verifies the combined endpoint. No final-holdout outcome cross-tab was produced. The source paper Tables 3 and 6 also distinguish cancellations from no-shows [1].

{get('target_semantics_development.csv').to_markdown(index=False)}

### 4. Target Population & Observed Sample

The source systems record bookings, amendments and eventual status; extraction uses booking tables and change logs, with many values taken relative to the day before arrival. The observed sample is thus selected through two hotels, their recording systems, and an arrival window. It is not a random sample of hotels or of all bookings created during these years. The target population for this revised analysis is the eligible observed booking cohort at these two hotels. Newly created bookings at the same hotels are a possible future operational population, not the population identified here. Even that extension needs caution because arrivals outside the source window are absent, especially long-lead bookings near the right boundary.

A second selection layer is our calendar and maturation eligibility rule. It favors bookings with recorded outcomes and planned departure before each analysis origin; it is **not** a representative sample of every booking created during the validation months. No inference to a national/global hotel population, causal effect, or effective independent sample size is justified. `hotel` identifies two establishments; a difference between them cannot establish an effect of hotel type.

### 5. Temporal Provenance & Leakage Audit

The central limitation is temporal measurement: a value that *could* exist at booking time is not proven to be the value that existed then. We exclude status/status date, assigned room, booking-change count, waiting days, transaction-derived ADR, deposit status, parking and accumulated special requests. Prior-outcome history and repeated-guest status are also omitted as predictors because history availability at creation is not independently verified. Country is excluded primarily because nationality may only be corrected at check-in [1]. The repeated-guest definition checks profile creation before booking creation [1]; exclusion is conservative, not proof of future information. Prior-booking outcome availability remains uncertain. See the [complete column audit](../tables/prediction_time_leakage_audit.csv). The pipeline enforces an explicit approved feature set, including for sensitivity models.

The primary feature list is: {', '.join(FEATURES)}. Hotel identity is stable; other inputs remain conditional on their recorded values matching initial booking information. Planned dates, length of stay, party composition, room, meal and channel may have changed. Removing the most obvious outcome proxies reduces risk but does not certify freedom from leakage. A smaller hotel/lead-time/seasonality sensitivity has the same remaining timestamp assumptions.

`booking_date = arrival_date - lead_time` is a **reconstructed proxy**, not an observed creation timestamp. We validate arithmetic and calendar boundaries; we cannot establish its original transactional provenance. Status date is used only to restrict administrative label availability, never as a predictor. All transformations that learn from data fit on training rows only.

### 6. Data Quality & Preprocessing

Raw bytes are preserved. Agent and company `NULL` values are structural non-applicability according to source documentation; they become a named category rather than an invented numeric zero. Country `NULL` becomes Unknown, while children `NA` becomes numeric missingness. Raw token counts are retained, so literal missing tokens are not confused with true zero children or numeric ID magnitudes. Agent, company and country are excluded from the primary model; children use training-median imputation inside the pipeline. We do not claim to identify MCAR, MAR or MNAR from this table, and single imputation does not propagate missing-data uncertainty.

{miss[miss[['literal_NULL','literal_NA','empty']].sum(axis=1)>0][['column','literal_NULL','literal_NA','empty']].to_markdown(index=False)}

Eligible training data contain {int(audit['train_exact_redundant_rows']):,} exact redundant rows; eligible validation contains {int(audit['validation_exact_redundant_rows']):,}. These are extra copies after the first occurrence within each partition. There is no booking identifier proving that identical records are erroneous: bookings for a group can legitimately coincide. The primary analysis retains rows. A sensitivity analysis deduplicates only the training table and evaluates on the same validation rows; a separate analysis evaluates the unchanged primary model on unique validation rows. Their different estimands must not be mixed. Exact full-row hashes do not cross the train/validation boundary ({int(audit['exact_hash_overlap_train_validation'])} overlaps), but that does not rule out repeated guests or group dependence.

The development cohort contains {int(audit['repeated_guest_rows']):,} rows flagged as repeated guests. Guest and group IDs are unavailable, so entity-disjoint validation and person-level clustering cannot be established. `agent` and `company` are not guest IDs. We avoid ordinary independent-row confidence claims.

There are {int(audit['zero_total_guests'])} zero-total-guest and {int(audit['zero_nights'])} zero-night records in eligible development data, plus {int(audit['adr_above_1000'])} ADR above 1,000. These are flagged, not automatically deleted or called errors without business verification. ADR is excluded from the model. An outcome-blind eligibility sensitivity excludes zero-guest/zero-night/extreme-party validation rows while leaving the fitted model unchanged; see `anomaly_sensitivity.csv`. No clipping thresholds were learned from validation.

### 7. EDA

Training-only empirical distributions appear below; validation is reserved for evaluation and declared diagnostics. These are selected-cohort patterns, not causal effects or overall hotel demand.

![Training monthly composition and outcome](../figures/01_training_time.png)

![Training lead time and hotel outcome distributions](../figures/02_training_distributions.png)

See [numeric distributions](../tables/train_distributions.csv) and [hotel summary](../tables/eda_hotel.csv). Association interpretations remain conditional on mutable snapshots and unknown guest/group dependence.

### 8. Baseline

The baseline is `DummyClassifier(strategy="prior")`, assigning each row the training positive fraction. Logistic regression uses an intercept, L2 regularization with C=1, lbfgs, maximum 3,000 iterations, and seed 507. It fits {int(spec.encoded_features)} transformed columns and converged after {int(spec.iterations)} iterations. Numerical fields undergo median imputation and standard scaling; categorical fields use constant missing-category imputation and one-hot encoding with unknown validation levels ignored. Sine/cosine month features are fixed arithmetic, not fitted using future data. No oversampling, class weighting, hyperparameter search, post-hoc calibration or automatic threshold optimization is applied.

Logistic regression assumes a linear additive log-odds relationship in the encoded representation; this is an approximation, not a verified generative law. Correlated predictors and regularization limit individual coefficient interpretations. Coefficients are conditional predictive associations, not causal effects or valid unregularized significance tests.

### 9. Initial Analysis

All numbers below are generated from executed code. Threshold-dependent metrics use 0.5. ROC-AUC measures pairwise discrimination; average precision summarizes positive-class ranking; Brier score and log loss assess probability quality. Accuracy alone is misleading under imbalance.

{metric_table}

At 0.5, the primary confusion matrix is TN={int(m.tn):,}, FP={int(m.fp):,}, FN={int(m.fn):,}, TP={int(m.tp):,}. The baseline achieves {pct(b.accuracy)} accuracy by predicting no positives. The primary model's {pct(m.accuracy)} accuracy therefore is not evidence of useful alerting. Its recall is only {pct(m.recall)}. Lower-threshold diagnostics are saved, but no business-optimal threshold is claimed without costs or capacity. For instance, 0.3 trades recall for many more false alerts; this is validation exploration, not unbiased final evaluation of a selected rule.

At a retrospective top-10% review capacity ({int(r.k):,} rows), primary-model precision is {pct(r.precision_at_k)} and recall is {pct(r.recall_at_k)}. Ties break by original row index for reproducibility. This static cohort ranking does not simulate a daily live queue and does not show that outreach would prevent cancellations.

A paired bootstrap resamples {int(ci.loc['roc_auc','week_clusters'])} booking-week clusters, using 400 fixed-seed replicates and a fixed fitted model. The approximate percentile interval for AUC is [{f(ci.loc['roc_auc','lower_2_5'])}, {f(ci.loc['roc_auc','upper_97_5'])}]; for Brier improvement over Dummy it is [{f(ci.loc['brier_gain','lower_2_5'])}, {f(ci.loc['brier_gain','upper_97_5'])}]. These are conditional stability diagnostics. They do not include training/model-selection uncertainty, unknown guest clustering, feature leakage or systematic future shift. Week exchangeability is questionable, and this interval is not a population-level coverage guarantee.

### 10. Temporal Evaluation & Outcome Maturity

Calendar boundaries were fixed before fitting models. Booking-date proxies before 2015-07-01 are excluded because the arrival-window start gives those cohorts particularly incomplete coverage. Train candidates are 2015-07-01 through 2016-06-30; validation candidates are 2016-07-01 through 2016-12-31; final holdout is 2017-01-01 onward. For training, both planned departure and terminal status must precede 2016-07-01; validation uses the corresponding 2017-01-01 origin. Status must not precede reconstructed booking date. Requiring planned departure before the origin reduces preferential inclusion of quickly canceled future arrivals, but planned departure itself is a snapshot proxy. It cannot completely eliminate selection bias.

{split.to_markdown(index=False)}

The legacy partition suffix `unmatured` means failure of the combined gate; some excluded labels were already known. It does not mean all those outcomes were unknown or records corrupt. The {len(tr):,} eligible training rows have target prevalence {pct(tr.is_canceled.mean())}; the {len(va):,} validation rows have prevalence {pct(va.is_canceled.mean())}. The unequal windows and maturity cutoff alter the lead-time/season mix, particularly near each cutoff. The monthly plots show this selected-cohort composition, not unconstrained booking demand or a causal seasonal effect.

Training-only EDA reports numeric ranges/quantiles, hotel/channel distributions, lead times and monthly outcome fractions. Validation is used only for declared evaluation and diagnostics. Final holdout target prevalence, EDA, metrics and predictions are not computed. A procedural lock and read/scoring guards reinforce this separation; the raw public source still physically contains its labels, so the lock is not encryption.

**Maturity ruling:** Keep the original combined gate as the primary cohort definition. For an already canceled booking, waiting for planned departure is unnecessary for label availability. The extra gate reduces preferential admission of early cancellations for future stays, but selects a different lead-time/season mix. A status-only rule also selects on resolution speed; neither is automatically unbiased. This is retrospective cohort eligibility, not a fixed-length embargo. Dates on the cutoff are excluded because intraday ordering is unavailable.

{get('maturity_rule_audit.csv').to_markdown(index=False,floatfmt='.4f')}

The status-only rows above are descriptive selection sensitivity, not a newly selected model or a replacement benchmark. `reservation_status_date` records the last status, not a full event history. `planned_departure` uses recorded arrival plus recorded nights, which may reflect amendments. The [development date audit](../tables/development_date_audit.csv) reports status/departure agreement by terminal status; canceled statuses preceding arrival are expected, whereas status before reconstructed booking is excluded. No final-holdout status values inform this diagnostic.

### 11. Sensitivity Analyses

{hotel[['group','n','prevalence','roc_auc','recall','brier']].to_markdown(index=False,floatfmt='.4f')}

Additional tables stratify market segment, booking month, lead-time band, recorded repeated-guest flag and family composition. These are overlapping exploratory slices, not independent confirmatory tests or proof of fairness; groups below 100 rows are explicitly flagged. The repeated-guest flag is diagnostic only. The saved confident-error examples identify high-score false positives and low-score false negatives without inventing reasons for the guests' actions.

Training deduplication changes both weighting and the fitted probability distribution; unique-row validation changes the evaluated population. Modest changes in AUC across these checks do not resolve entity dependence. Calibration bins and the reliability plot compare predicted and observed fractions without recalibrating on evaluation data. The very low recall, selected-cohort drift and limited probability quality justify holding operational use even when AUC exceeds the constant baseline.

{metrics.loc[metrics.model.isin(['Logistic primary','Logistic train deduplicated','Primary on unique validation rows','Logistic minimal proxy']), ['model','n','roc_auc','average_precision','brier']].to_markdown(index=False,floatfmt='.4f')}

The maturity-rule comparison in Section 10 changes cohort eligibility only. Deduplication, minimal-feature and anomaly checks retain their existing implementations and remain exploratory.

### 12. Supported & Limited Claims

Supported: this fixed logistic specification provides modest retrospective ranking information relative to the declared Dummy baseline on the eligible validation cohort. Unsupported: accurate real-time prediction at initial reservation; prevention of cancellations; causal interpretation; transfer to all hotels; final-test performance. Full claim–evidence mappings appear in [claim–evidence table](CLAIM_EVIDENCE.md).

### 13. Next Steps

Before final work: confirm the revised retrospective estimand with the instructor; obtain original snapshots before considering deployment; confirm label semantics, original date consistency and intended decision horizon; justify a prospective cohort with complete arrival/outcome coverage; obtain guest/group identifiers if possible; define intervention costs and capacity; predeclare rolling temporal validation and any threshold/calibration selection; freeze all choices before a single final holdout evaluation. The current public holdout is also subject to arrival-window selection and cannot repair the data's timestamp limitation.

The supplied syllabus requires every student to explain the complete project, methods and error analysis, and permits AI assistance with student verification. Following the student's clarification of the instructor's expectations, this working copy is organized as the student's full analysis, with no division of analytical stages among teammates. The individual midterm component focuses on one important analytical choice, its supporting evidence and one unresolved risk or next step; it does not replace understanding the whole project. The syllabus still specifies a team submission and a contribution assessment. It lists presentations on October 13 and 15, subject to schedule updates, but gives no exact report deadline, length or submission format. AI-assisted code and drafting were used; the student must be able to independently explain and verify the submitted analysis.

### References

1. Antonio, N., de Almeida, A., & Nunes, L. (2019). *Hotel booking demand datasets*. Data in Brief, 22, 41–49. [original paper](https://doi.org/10.1016/j.dib.2018.11.126); [open full text, Table 1 and Section 2](https://pmc.ncbi.nlm.nih.gov/articles/PMC6297060/).
2. TidyTuesday (2020-02-11), [Hotels data and field dictionary](https://github.com/rfordatascience/tidytuesday/tree/main/data/2020/2020-02-11).
3. [IS507 Fall 2026 Section BC syllabus](../docs/IS507-syllabus.md), last updated August 25, 2026; supplied by the student and reviewed September 30, 2026. See Team Project, Midterm Project Report and Presentation, Use of Artificial Intelligence, and Teamwork and Individual Accountability. [Requirements mapping](../docs/COURSE_REQUIREMENTS.md). Specific assignment screenshot not available.
'''
    (ROOT/'report/MIDTERM_REPORT_DRAFT.md').write_text(report)
    summary=dict(train_n=len(tr),validation_n=len(va),train_prevalence=float(tr.is_canceled.mean()),validation_prevalence=float(va.is_canceled.mean()),auc=float(m.roc_auc),recall=float(m.recall),accuracy=float(m.accuracy),holdout_n=int(split.set_index('partition').loc['final_holdout','n']),recommendation='HOLD',course_assignment_screenshot_verified=False)
    (ROOT/'tables/KEY_RESULTS.json').write_text(json.dumps(summary,indent=2))
    return summary

if __name__=='__main__': print(write_report())
