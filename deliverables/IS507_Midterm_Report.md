## Hotel Cancellation Prediction

Midterm Project Report | IS 507, Fall 2026 | October 8, 2026

Group 16: Zhe Wang and Zhengxuan Du

### 1. Question and motivation

Can recorded booking information distinguish hotel reservations that complete from those that cancel or end in a no-show? We chose this applied prediction question because it connects customer behavior with service planning and lets us examine when a seemingly useful prediction is actually credible.

A booking reserves a room for a future stay. A cancellation calls off the reservation; a no-show means the guest does not arrive. Both create uncertainty about occupancy. We call their combined outcome noncompletion. A useful risk score could help prioritize booking reviews, but we do not measure cancellations prevented or money saved.

**Related work.** Antonio, de Almeida and Nunes (2017) studied cancellation classification on four resort hotels for demand management [3], establishing that cancellation prediction is feasible and operationally relevant. Their data, feature scope and evaluation differ from ours, so their reported performance is not a benchmark for our restricted retrospective setup. Our focus is narrower: probability quality against a simple baseline, with explicit attention to prediction timing and leakage.

### 2. Data generation, population and observation unit

Antonio, de Almeida and Nunes (2019) released records from the property management systems and booking change logs of two Portuguese hotels [1]. We use the TidyTuesday combined CSV [2]: 119,390 rows and 32 columns, comprising 79,330 city-hotel and 40,060 resort-hotel bookings. Scheduled arrivals span July 2015 to August 2017. One row represents one booking, not one unique guest. The same guest or group may generate multiple rows.

The data cover bookings scheduled to arrive within a fixed window. They are neither a random sample of hotels nor a complete register of all bookings created in that period. Our reported performance applies to the date-eligible recorded bookings defined below. We cannot infer performance for all hotels or future new bookings.

### 3. Statistical task: X, Y and loss

| Element | Project definition |
| --- | --- |
| Task and Y | Binary probability estimation and risk ranking. is_canceled = 1 includes Canceled and No-Show; 0 is Check-Out. The target is eventual recorded outcome. |
| X: inputs | Hotel, lead time (days booked ahead), planned weekday/weekend nights, adults/children/babies, meal, reserved room, market segment, distribution channel and cyclic arrival month. |
| Output and loss | p estimates the probability of noncompletion. Mean log loss = -mean[y log(p) + (1-y) log(1-p)]. Lower is better; confident wrong predictions receive a larger penalty. |

The intended business decision time is reservation creation. The actual analysis is retrospective: later stored attributes do not verify the values known at creation. An illustrative p = 0.8 means an estimated 80% risk, rather than an alert rule or a measured example.

<!-- PDF page break -->

## 4. Challenges and preparation

### Information timing and leakage

Data leakage occurs when a model uses information unavailable at the intended prediction time. Final reservation status reveals the answer. The source describes extracting booking attributes relative to the day before arrival [1]; room, meal or stay details may have changed since creation. Excluding obvious later information reduces risk, but cannot recover original booking-time values.

| Fields | Treatment and reason |
| --- | --- |
| reservation_status and its date | Exclude from X. Use status date only to define eligibility, never to predict. |
| assigned_room_type, booking_changes, waiting days | Exclude later assignment, accumulated changes and waiting. |
| adr, deposit_type, parking, special requests | Exclude transaction-derived rates/payments and potentially updated requests. |
| Prior outcomes, repeated-guest flag, customer_type | Omit because original availability cannot be independently reconstructed. This does not prove that every omitted field leaks. |
| country, agent, company | Omit from modeling to keep scope manageable. Audit their missing-value semantics separately. |

### Missing, duplicated and repeated observations

The raw file has four missing children counts, 488 country NULLs, 16,340 agent NULLs and 112,593 company NULLs. Unknown children differs from zero children. Agent/company NULL means not applicable in the source dictionary. Country NULL becomes Unknown. Only children enters X: the training pipeline fills it with the training median and adds a missingness indicator. No validation outcomes determine preparation rules.

Training contains 11,395 extra identical full rows and validation 1,635, counted after the first copy. Different group bookings can look identical, so the primary model retains them. We separately remove training duplicates and evaluate unique validation rows. No exact full row crosses train/validation, but absent guest/group IDs prevent establishing independence.

Development data include 91 zero-guest rows, 520 zero-night rows and one ADR above 1,000. We retain them because unusual does not establish erroneous. A separate validation check excludes flagged guest/stay anomalies while keeping the model fixed; its AUC is 0.6565 versus 0.6584 for the primary analysis.

### Preprocessing

The training pipeline learns numeric medians and scales, and encodes categories as indicator columns. It ignores unfamiliar evaluation categories. Fixed sine/cosine arrival-month terms make December and January neighbors. The model receives 39 encoded columns. These transformations do not resolve the snapshot or repeated-observation limitations.

<!-- PDF page break -->

## 5. Evaluation design and initial findings

### Earlier periods train; later periods evaluate

We derive a booking-date proxy as recorded arrival minus lead time. For example, an October 20 arrival with 10 days of lead time implies October 10. This arithmetic illustrates the rule; the release has no independent immutable creation timestamp to verify it. Planned departure is arrival plus recorded nights.

| Use | Booking-date proxy window | Eligibility cutoff | Rows |
| --- | --- | --- | --- |
| Training | Jul 2015-Jun 2016 | Before Jul 1, 2016 | 39,865 |
| Validation | Jul-Dec 2016 | Before Jan 1, 2017 | 14,088 |
| Existing later test* | Jan-May 2017 | Before Sep 1, 2017 | 22,541 |

Each included row requires both terminal-status date and planned departure before its cutoff, and status cannot precede the booking proxy. The model and learned transformations fit training only. Validation supports initial analysis and diagnostic choices. *The later test has already been evaluated under the October 8 frozen protocol; we disclose it in Section 8, rather than represent it as an untouched future test.

### Why the cohort rule matters

An already canceled booking can have a known outcome before planned departure. Our additional departure rule limits preferential admission of early cancellations for future stays, but defines a selected cohort rather than an unbiased sample. It excludes 12,484 of 26,572 validation candidates (47.0%). A status-only rule adds 4,080 positives, raising prevalence from 26.19% to 42.76%. This substantial change is a central limitation, not a minor cleaning detail.

For example, a booking canceled in December for a February stay has a known label before January 1, but fails the departure rule. This is an illustration. We retain the inherited rule, disclose its effect and avoid choosing an alternative using observed test performance. The 119,390 rows reconcile as 39,865 training, 17,610 training exclusions, 14,088 validation, 12,484 validation exclusions, 26,565 inherited holdout and 8,778 left-boundary exclusions.

### Training distributions and associations

| Training description | Observed value | Interpretation |
| --- | --- | --- |
| Lead time | Median 38 days; middle half 8-94; mean 63.22 | A long right tail makes the mean alone incomplete. |
| Hotel noncompletion fraction | City: 35.05% (n=26,357); resort: 22.35% (n=13,508) | Two individual establishments differ; this is not a hotel-type effect. |
| Market segment | Direct: 12.89% (n=4,484); Groups: 48.24% (n=6,601) | Recorded channels differ within the eligible cohort; reasons remain unknown. |

The positive fraction changes from 30.75% in training to 26.19% in validation. Season, booking mix and eligibility can contribute; we do not isolate a causal explanation for the change.

<!-- PDF page break -->

## 6. Baseline, model and validation results

The baseline assigns every booking the training noncompletion fraction, 0.30749. Logistic regression combines X into linear log-odds and converts them to a probability. L2 regularization limits coefficient size (C=1). We use lbfgs, max_iter=3000 and seed 507; fitting converges in 46 iterations. There is no class weighting, hyperparameter search or recalibration. The constant baseline is a minimum comparison, not evidence that this is the best available model.

| Validation metric | Constant baseline | Logistic regression |
| --- | --- | --- |
| Log loss (lower) | 0.5800 | 0.5517 |
| ROC-AUC (higher) | 0.5000 | 0.6584 |
| Average precision (higher) | 0.2619 | 0.3954 |
| Brier score (lower) | 0.1954 | 0.1841 |
| Accuracy at 0.5 | 73.81% | 73.72% |
| Recall at 0.5 | 0.00% | 0.30% |

Validation log loss improves by 4.88% relative to the baseline. AUC measures whether a randomly selected positive receives a higher score than a negative (half credit for ties). Average precision summarizes positive-case ranking across score cutoffs. Brier is mean squared probability error. Ranking quality, probability accuracy and useful alerts are different questions.

### Default alerts and the cost of lower thresholds

At p >= 0.5, logistic regression detects 11 of 3,689 positives and misses 3,678. It also produces 24 false alerts and 10,375 true negatives. The baseline alerts nobody but has high accuracy because most bookings complete. Its precision is undefined with no alerts; the code reports zero by convention.

| Validation alert rule | Detected / 3,689 | False alerts | Precision | Recall |
| --- | --- | --- | --- | --- |
| p >= 0.5 | 11 | 24 | 31.43% | 0.30% |
| p >= 0.3 | 1,058 | 1,398 | 43.08% | 28.68% |
| p >= 0.2 | 2,724 | 5,353 | 33.73% | 73.84% |

Lowering the threshold finds more cases and adds false alerts. These are development diagnostics, not selected operational policies: review capacity and error costs remain unspecified. Ranking the highest-scored 10% selects 1,409 rows with 679 positives: precision 48.19% and recall 18.41%. This concentrates observed risk but misses most cases and does not simulate a daily queue.

### What the error audit adds

At 0.5, false negatives have median lead time 37 days; the 11 detected positives have median 125 days, and the 24 false positives 157 days. The few alerts tend to involve longer lead times. These small groups suggest a failure pattern for further investigation; they cannot explain guest motives. Both hotels have near-zero validation recall at this threshold.

<!-- PDF page break -->

## 7. Supported claims, limits and next steps

| Claim | Evidence and boundary |
| --- | --- |
| Some retrospective ranking information | Validation AUC 0.6584 and lower log loss support modest predictive value within the selected cohort. |
| Effective cancellation alerts | The 0.5 rule is weak: 11/3,689 detected. Lower thresholds trade detection for false alerts; no business policy is validated. |
| Valid predictions at booking creation | Unestablished: the release supplies later snapshots and derived dates, not verified initial inputs. |
| Causes or financial benefit | Unestablished: associations do not show why guests cancel or whether contact changes outcomes. |

Validation sensitivities give AUC 0.6517 after training deduplication and 0.6425 for hotel/lead time/month only, versus 0.6584 for the full model. Extra fields add limited observed discrimination. Evaluating unique validation rows also gives AUC 0.6425 and Brier 0.1739, but changes the evaluated population; the lower Brier alone does not indicate model improvement.

The existing paired bootstrap resamples 27 booking-week clusters 400 times with the fitted model fixed. Its central 95% AUC range is 0.6376-0.6822. This is conditional stability under exchangeable weeks, not guaranteed population coverage. It omits training uncertainty and cannot recover unknown guest/group dependence or remove timing and selection bias.

Next, examine the cohort rule and threshold tradeoffs on development data, then collect timestamped original booking inputs and follow every booking to its outcome. Guest/group IDs would support dependence checks. Define review capacity and error costs before evaluating a practical rule on genuinely new data. Models under consideration include a random forest comparison to capture nonlinear effects and interactions, using the same restricted features and a small prespecified tuning grid; any added complexity will be judged by held-out log loss against the current baseline, not by in-sample fit. Added model complexity cannot restore missing historical inputs.

### 8. Previously evaluated later period

The October 8 frozen protocol evaluated 22,541 January-May 2017 records using the unchanged training-only model. Log loss was 0.5968 versus baseline 0.6328; AUC was 0.6644; recall at 0.5 was 6.62%. Of the 26,565 inherited holdout rows, 3,696 later proxy dates remained unused and 328 window candidates failed eligibility. This supports modest performance in another selected period. We have already seen these results and will not reuse the same set as an unknown test after tuning.

### References

[1] Antonio, N., de Almeida, A., & Nunes, L. (2019). Hotel booking demand datasets. Data in Brief, 22, 41-49. https://doi.org/10.1016/j.dib.2018.11.126

[2] TidyTuesday (2020-02-11). Hotels data and field dictionary. https://github.com/rfordatascience/tidytuesday/tree/main/data/2020/2020-02-11

[3] Antonio, N., de Almeida, A., & Nunes, L. (2017). Predicting hotel booking cancellations to decrease uncertainty and increase revenue. Tourism & Management Studies, 13(2), 25-39. https://doi.org/10.18089/tms.2017.13203
