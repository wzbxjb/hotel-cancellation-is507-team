# 期中排练与分工指南

Group 16：Zhe Wang、Zhengxuan Du。正式报告和幻灯片均为英文。

正文10页，计划7分45秒，另留约15秒切换与停顿。隐藏备份5页只在问答时使用。计划时长不是实际排练结果，至少完整计时一次。

## 已确定的职责安排

两人都参与每个环节，包括研究问题、数据核对、预处理、模型评价、结果解释、报告撰写、幻灯片制作和演讲准备。Zhe Wang更侧重代码，Zhengxuan Du更侧重幻灯片；两人共同核对证据，并理解完整流程和错误分析。

两人都能解释完整项目。实际贡献按具体工作和核验记录填写，不按代码提交次数或发言时长机械衡量。

## 发言顺序与时间

建议 Zhengxuan Du讲1–3页，Zhe Wang讲4–9页，Zhengxuan Du讲第10页。Zhe约5分10秒，Zhengxuan约2分35秒。分工可交换，两人都应能解释全部页面。

| 页 | 内容 | 秒 | 建议讲者 |
|---|---|---:|---|
| 1 | Hotel Cancellation Prediction | 15 | Zhengxuan Du |
| 2 | Why this question? Booking outcomes affect planning | 50 | Zhengxuan Du |
| 3 | What data? One row is one reservation | 40 | Zhengxuan Du |
| 4 | What do we predict? X, Y and a probability | 45 | Zhe Wang |
| 5 | Challenge: booking-time information is uncertain | 50 | Zhe Wang |
| 6 | Evaluation: our inclusion rule changes the sample | 55 | Zhe Wang |
| 7 | Preparation and two training-data findings | 50 | Zhe Wang |
| 8 | Analysis: a constant baseline and logistic regression | 50 | Zhe Wang |
| 9 | Initial results: modest improvement over the baseline | 60 | Zhe Wang |
| 10 | Conclusion and next steps | 50 | Zhengxuan Du |

## 教授五问与页面

| 教授问题 | 正文页面 |
|---|---|
| Why this question? | 2：问题、兴趣方向与业务背景 |
| What data? | 3：来源、行数、每行单位、时间与酒店范围 |
| What predict: X, Y, loss? | 4、8：目标、输入、概率、log loss与baseline |
| What challenges? | 5–7：时点、筛选、缺失和重复 |
| How analyze? | 6、8–11：划分、比较、误报漏报、结论与下一步 |

## 英文讲稿（与 PPT 备注一致）

### Slide 1: Hotel Cancellation Prediction (15 seconds)

We are Group 16, Zhe Wang and Zhengxuan Du. Our midterm question is whether recorded hotel booking details can help identify cancellations and no-shows. We focus on initial analysis and what the evidence can support.

### Slide 2: Why this question? Booking outcomes affect planning (40 seconds)

A booking reserves a room for a future stay. A cancellation calls off the reservation. A no-show means the guest does not arrive. We call both outcomes noncompletion. For example, a Friday reservation that cancels leaves the hotel less certain about occupancy. We chose this applied prediction question to connect customer behavior with service planning. A score might help prioritize booking reviews. Our study measures prediction quality, without measuring money saved or cancellations prevented.

### Slide 3: What data? One row is one reservation (40 seconds)

The original paper describes operational records from two Portuguese hotels, extracted from property management systems and booking change logs. We use the TidyTuesday combined file: 119,390 bookings and 32 columns. Arrivals span July 2015 to August 2017. One row is a booking, not a unique person. A guest or group can generate multiple records. These two hotels do not represent the entire hotel industry.

### Slide 4: What do we predict? X, Y and a probability (45 seconds)

Y is the eventual recorded outcome. One includes cancellation or no-show; zero means a completed stay recorded as Check-Out. Lead time means days between booking and arrival. X includes the hotel, lead time, planned stay, guest counts and booking choices. Logistic regression returns a probability. A value of 0.8 would mean an estimated 80 percent risk. This example explains the output. Our primary loss is log loss, which checks probabilities against outcomes and penalizes confident mistakes. Lower is better. We do not predict a fixed 30-day outcome.

### Slide 5: Challenge: booking-time information is uncertain (50 seconds)

Ideally we would predict at reservation creation. At that time, the final status is unknown, so using it would reveal the answer. This is data leakage. We also exclude later room assignments, accumulated changes and transaction-derived fields. However, the source supplies attributes extracted relative to the day before arrival. Even retained room or stay information might have changed. Removing obvious leakage cannot recover initial values. Our actual experiment evaluates recorded past bookings. Performance at original booking creation remains unverified.

### Slide 6: Evaluation: our inclusion rule changes the sample (65 seconds)

We derive an estimated booking date by subtracting lead time from arrival. Training uses July 2015 through June 2016. Validation uses July through December 2016. Both final status and planned departure must precede each cutoff. A December cancellation for a February stay has a known outcome but fails our departure rule. The rule limits preferential admission of early cancellations for future stays, while defining a selected population. It excludes about 47 percent of validation candidates. A status-only rule would add 4,080 positives, raising the positive fraction from 26.19 to 42.76 percent. Neither rule guarantees an unbiased sample. The existing later test has already been scored; details are in the backup.

### Slide 7: Preparation and two training-data findings (50 seconds)

All learned preparation comes from training. We fill four missing children counts with the training median, encode categories and scale numeric inputs. Different group bookings can look identical, so we keep repeated rows and examine alternatives. Training lead time has median 38 days and a middle half from 8 to 94 days. The city hotel has a 35.05 percent noncompletion fraction, versus 22.35 percent at the resort. These are associations in two selected establishments, not a causal hotel-type effect. Missing guest and group IDs prevent verifying independence.

### Slide 8: Analysis: a constant baseline and logistic regression (50 seconds)

Our baseline assigns every booking the training positive fraction, 30.75 percent. It uses no individual details and no validation outcomes. Logistic regression combines booking inputs into log-odds, then converts them to a probability. Regularization discourages extreme coefficients. We fit once on training, with fixed settings and no parameter search. Both models face exactly the same validation rows. We evaluate probabilities with log loss and ordering with AUC. AUC asks how often a positive receives a higher score than a negative. A constant baseline has AUC 0.5.

### Slide 9: Initial results: modest improvement over the baseline (60 seconds)

On 14,088 validation bookings, logistic log loss is 0.5517 versus 0.5800 for the baseline, a 4.88 percent relative reduction. AUC improves from 0.5 to 0.6584, suggesting some ranking information. The default rule flags probabilities at or above 50 percent. It detects only 11 of 3,689 actual cases. Accuracy is around 74 percent, even though nearly every cancellation or no-show is missed. The baseline achieves similar accuracy by alerting nobody. These results separate useful probability or ranking information from a useful alert system.

### Slide 10: Alert thresholds: more detections mean more false alerts (90 seconds)

A probability becomes an alert only after choosing a rule. At a 50 percent threshold we detect 11 cases and raise 24 false alerts. At 30 percent we detect 1,058 cases, but raise 1,398 false alerts. At 20 percent recall reaches about 74 percent with 5,353 false alerts. These development checks do not select a business policy: the acceptable cost and review capacity are unknown. Separately, the highest-scored ten percent contains 679 cases among 1,409 bookings, about 48 percent compared with 26 percent overall. It still finds only 18 percent of all cases. The error audit shows that the few default alerts tend to have longer lead times. Those small groups suggest where to investigate, without explaining guest motives.

### Slide 11: Conclusion and next steps (45 seconds)

Our initial analysis finds limited retrospective ranking and probability improvement. The default alert rule performs poorly, and lower thresholds require explicit choices about false alerts. Original booking-time inputs and a more representative cohort remain unresolved. Our next steps are to examine cohort and error patterns on development data, collect original timestamped inputs and define review capacity before evaluating a practical rule on new bookings. Both members participate in every stage. Zhe places greater emphasis on coding and Zhengxuan on slides, while both understand and explain the full analysis. We are not proposing deployment based on these results.

### Slide 12: Backup: model settings and sensitivity checks （仅问答）

L2 logistic regression uses C=1, lbfgs, max_iter=3000 and seed 507. It has 39 encoded columns and converges in 46 iterations. The inputs are lead time, weekday/weekend nights, adults, children, babies, cyclic month, hotel, meal, market segment, channel and reserved room. The same validation rows compare primary, deduplicated-training and minimal-feature models. Unique validation evaluation changes the population, so its Brier improvement alone cannot show a better model.

### Slide 13: Backup: the later period has already been evaluated （仅问答）

On October 8 the frozen protocol evaluated January-May 2017 bookings. There are 22,541 included rows. We retain the unchanged train-only model and disclose all results. The test has already been inspected and cannot become a fresh unknown test after tuning. Of the original 26,565 holdout rows, 3,696 later proxy dates are unused and 328 window candidates are ineligible. This supports another selected-period comparison rather than original booking-time deployment.

### Slide 14: Backup: stability and dependence （仅问答）

We resample 27 booking-week clusters 400 times with the fitted model fixed. A week resample preserves some within-week dependence, unlike independently drawing every row. It cannot identify repeated guests across weeks. The AUC range is conditional on the fitted model and exchangeable weeks. It does not include training uncertainty, unknown guest dependence, source timing or cohort selection bias. No population coverage guarantee is made. Train deduplication changes learning weights, while unique validation changes the evaluated population.

### Slide 15: Backup: team participation and sources （仅问答）

Both members participate in every stage, including question formulation, data review, preprocessing, model evaluation, interpretation, report writing and presentation preparation. Zhe Wang places greater emphasis on coding, while Zhengxuan Du places greater emphasis on slides. Both check claims against outputs and understand the complete workflow. The team submits one report and both members join the correct Project Teams group. The code requires an accessible GitHub link.

## 两人共同掌握的中文核对要点

- **研究对象**：每行是一笔预订；取消与未到店共同构成noncompletion；不是每行一个独立客人。
- **信息时点**：数据提取的是较晚记录。删掉最终状态不能恢复创建时的初始输入，所以实际研究是回顾性分析。
- **筛选的代价**：已取消的未来入住订单虽然标签已知，仍可不符合departure规则。验证候选约47%被排除，status-only会把正类比例从26.19%改为42.76%。双日期不是无偏保证。
- **baseline**：训练正类比例30.75%，人人同一概率；0.5规则下不报警，accuracy高、recall为零。
- **概率与报警不同**：log loss衡量概率；AUC衡量排序；threshold决定报警；不能由AUC推断业务收益。
- **阈值取舍**：0.3能识别1,058例，同时误报1,398例。先确定容量和成本，才能选实际规则。
- **重复与bootstrap**：训练去重改变学习权重，验证去重改变评价人群。按周抽样保留部分周内相关性，仍不解决跨周重复客人。
- **已有测试**：2017年结果已经看过。可以复算，但调参后不能继续把同一集当全新测试。

## 实际工作留痕与互相复核

| 环节 | 两人共同参与 | 侧重点 |
|---|---|---|
| 问题与数据 | 两人共同确定问题、核对字段和样本 | Zhe更侧重代码核对 |
| 预处理与模型评价 | 两人共同检查方法、指标与错误 | Zhe更侧重实现与复算 |
| 报告与幻灯片 | 两人共同组织论述、检查数字和图表 | Zhengxuan更侧重幻灯片 |
| 演讲与问答 | 两人共同排练并解释完整项目 | 根据内容安排发言 |

以上概括两人的合作方式。个人组件应由本人用自己的理由说明一个分析选择、证据及未解决风险。

## 提交前事项

1. 两人先加入正确的Project Teams组，由一人上传一份团队报告。
2. 只提交deliverables中的新期中报告和PPT，report目录是历史资料。Markdown是可编辑同文版；PDF已排为5页A4。
3. 代码上传GitHub，确认教师能访问，并提交实际链接。现有包不包含已发布仓库证明。
4. 实际排练到10分钟以内；若超时，缩短解释，优先保留筛选限制与误报漏报取舍。