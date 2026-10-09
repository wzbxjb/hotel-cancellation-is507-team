# IS 507: Data, Statistical Models, and Information

**Fall 2026 — Section BC**
**Last updated:** August 25, 2026

## Full Course Information

**Course number:** IS 507
**Course title:** Data, Statistical Models, and Information
**Term:** Fall 2026
**Credit hours:** 4
**Class meeting time:** Tuesday and Thursday, 2:00–3:20 PM
**Class location:** 165 Noyes Laboratory
**Course dates:** August 24–December 9, 2026
**First scheduled meeting:** August 25, 2026
**Last scheduled meeting:** December 8, 2026
**Weekly classroom time:** 2 hours and 40 minutes

This syllabus may be provided in an alternative format upon request. Please contact the instructor.

# Instructor Information

## Instructor

**Name:** Yonghan Jung
**Email:** [yonghan@illinois.edu](mailto:yonghan@illinois.edu)
**Website:** https://yonghanjung.me/
**Office hours:** TBD
**Preferred contact method:** `[TBD; email with [IS507] in the subject line proposed]`

## Teaching Assistants

- **Roman Matthew Zapata**
  - Email: [rzapata2@illinois.edu](mailto:rzapata2@illinois.edu)
  - Office hours: Monday and Wednesday, 1:00–2:00 PM
  - Office: Room 322, 501 E. Daniel St. (old iSchool building)
- **Andrew Nam**
  - Email: [donginn2@illinois.edu](mailto:donginn2@illinois.edu)
  - Office hours: Tuesday, 9:00–11:00 AM
  - Office: Room 318, 501 E. Daniel St. (old iSchool building)

# Course Information

## Course Description

An introduction to statistical and probabilistic models as they pertain to quantifying information, assessing information quality, and principled application of information to decision making, with a focus on model selection and gauging model quality. The course reviews relevant results from probability theory, parametric and non-parametric predictive models, as well as extensions of these models for unsupervised learning. Applications of statistical and probabilistic models to tasks in information management, such as prediction, ranking, and data reduction, are emphasized.

## Course Purpose

IS 507 prepares students to work as practical data scientists who can select, use, interpret, evaluate statistical and AI methods and audit statistical analysis. 

Students will learn the basic statistics and AI models that data scientists should know. The course uses the same statistical questions to study classical models and modern AI models: what problem is being formulated, what evidence is relevant, how model quality is evaluated, and what conclusions the evidence supports.

IS 507 deliberately introduces many statistical methods and theories at a broad level. The goal is recognition: students should leave able to say, “I have heard of this method. I know what kind of problem it addresses, and I know where to begin.” That prior exposure gives students a starting point for learning additional details with AI. Students remain responsible for verifying assumptions and results and for interpreting what the evidence supports.

Implementation is not the final goal of the course. Students will learn to determine:

1. what kind of statistical or data-science problem is being posed;
2. what population, information, and outcome are relevant;
3. which baseline and model families are appropriate;
4. what assumptions support a method;
5. how uncertainty and model quality should be evaluated;
6. when a result supports a decision; and
7. under what conditions a method should not be used.

## Course Context

IS 507 is a required core course in the Master of Science in Information Management program. It connects probability theory and statistical modeling to contemporary information-management tasks, including prediction, ranking, dimensionality reduction, clustering, text modeling, time-series prediction, generative AI evaluation, and causal analysis.

The course preserves the statistical foundation of IS 507 while examining modern model families such as neural networks, Transformers, foundation models, and TabPFN. Modern methods will be compared with simpler baselines using the same target population, data split, metrics, and test set.

Causal analysis is included as a modern extension of principled decision making. Students will learn the boundary between prediction, association, and causal effects; this is not a full graduate sequence in causal inference.

## Pre- and Co-requisites

**Official prerequisite:** Graduate standing.

Basic experience with Python or another programming language is recommended. The course uses Python but does not teach general programming from the beginning. Students without prior introductory statistics should expect to review foundational probability and statistics during the first part of the semester.

## General Education Category

Not applicable. This is a graduate course.

# Student Learning Objectives

By the end of the course, each student will be able to:

1. Articulate the role of marginal, joint, and conditional probability in modeling processes involving information.
2. Select, parameterize, fit, and compare probability distributions using their support, data-generating interpretation, parameters, and empirical fit.
3. Specify, estimate, and evaluate elementary parametric statistical models.
4. Specify, estimate, and evaluate flexible or non-parametric predictive models, including kernel methods.
5. Use honest validation, cross-validation, regularization, and the bias–variance tradeoff to compare baselines and candidate models.
6. Evaluate prediction, ranking, calibration, time-dependent prediction, data reduction, and clustering using appropriate statistics and uncertainty assessments.
7. Distinguish association, prediction, and causal effects; design a simple randomized experiment; and state the assumptions required for an observational causal claim.
8. Evaluate how sampling, measurement, missingness, dependence, subgroup failure, distribution shift, and AI-generated output affect the credibility of a statistical claim.
9. Exercise professional responsibility when creating, describing, evaluating, and using models built from data.
10. Justify a final recommendation of `use`, `conditional use`, `hold`, or `reject` using an explicit claim–evidence chain.

# Program and Institutional Learning Context

## Program Learning Outcomes

This course supports program-level abilities to:

- apply quantitative and computational methods to information-management problems;
- evaluate the quality, limitations, and appropriate use of data;
- produce reproducible and interpretable analytical results;
- communicate technical evidence to decision makers; and
- practice responsible data and AI work.

## iSchool Goal

Maintain global leadership in education for the information professions.

## University of Illinois Campus-Wide Learning Goals

- Intellectual Reasoning and Knowledge
- Creative Inquiry and Discovery
- Effective Leadership and Community Engagement
- Social Awareness and Cultural Understanding
- Global Consciousness

# Course Materials

## Required Materials

Course notes, demonstrations, notebooks, datasets, readings, quizzes, and project instructions will be provided through the course LMS or repository.

Students will need:

- a laptop capable of running Python notebooks;
- Python 3.11 or a course-approved hosted notebook environment;
- Jupyter or JupyterLab;
- reliable access to the course LMS; and
- the Python packages specified in individual course notebooks.

The course is Python-centered. SQL syntax, database design, and query construction are not learning objectives. Database operations may appear only when they create a statistical problem, such as duplicated observations, selection, or leakage.

## Textbooks and References

N/A. There is no required or recommended reading list.

# Course Format and Expectations

## Typical Class Structure

Each class meeting lasts 80 minutes.

- **10–15 minutes:** recap of the previous lecture
- **50 minutes:** teaching, statistical reasoning, and worked examples
- **15 minutes:** quiz, when one is given

When a quiz is not given, the remaining time may be used for continued teaching, worked examples, demonstrations, or project feedback. Presentation meetings will use a different structure.

Quizzes begin in Week 2 and will occur frequently throughout the semester. Quiz dates will not follow a fixed announced schedule.

## Depth of Coverage

Methods will be taught at different levels of depth.

### Core

Students must be able to:

- identify an appropriate use;
- execute or modify a supplied Python workflow;
- interpret the output;
- evaluate the assumptions and evidence; and
- state conditions under which the method should not be used.

### Recognition

Students must explain the purpose, central assumptions, output, and common failure modes. Full implementation or mathematical derivation is not required.

### Project-Specific

Students may use these methods when appropriate for a team project, but they will not be assumed on every quiz.

## Implementation Expectations

Students are not expected to implement every optimizer or algorithm from first principles. Students are expected to:

- run and modify prepared Python notebooks;
- identify the observation unit, population, target, split, model, metric, and output;
- detect leakage and invalid evaluation;
- compare baselines and candidate models under a common evaluation protocol;
- reproduce reported results;
- explain what submitted code does;
- determine whether a claim is supported; and
- document the limits of the analysis.

# Quizzes

Quizzes begin in Week 2 and will occur frequently throughout the semester. Quiz dates will not follow a fixed announced schedule.

When a quiz is given, it will normally take 15 minutes at the end of class and may assess the current lecture and the preceding one or two lectures.

Questions will emphasize reasoning and interpretation rather than isolated recall. Formats may include:

- selecting exactly five correct statements from ten options;
- ordering the steps of an analysis;
- explaining reasoning in one or two sentences;
- matching a situation to a method, assumption, or interpretation;
- interpreting numerical output or a plot;
- identifying leakage or an invalid comparison; and
- distinguishing supported from unsupported claims.

The following policies remain to be determined:

- whether quizzes are open-resource or closed-resource;
- how many quiz scores count toward the final grade;
- whether the lowest quiz scores are dropped.

The default policy is that make-up quizzes are not allowed. An exception is permitted only when all four conditions are met:

1. the student provides formal documentation or proof of the absence;
2. the instructor approves the make-up;
3. the make-up is completed within one week of the missed quiz; and
4. the student schedules the make-up with an available teaching assistant.

# Team Project

There is no midterm examination and no final examination. Students will work in teams of two or three.

Teams may freely choose their problem, topic, data, and methods. The team will formulate the problem, select appropriate methods, evaluate the evidence, and present the analysis. Model complexity is not itself a grading criterion. The selected method must be appropriate for the question and evaluated honestly.

Every student must be able to explain the complete project and the methods used. Error analysis is a required part of the project. Challenging topics are welcome; evaluation will emphasize how deeply the team understands and investigates the problem rather than whether the project uses a fashionable method or obtains a positive result.

## Topic and Data Proposal

The team proposal will identify:

- the practical or research question;
- the type of statistical task;
- the proposed dataset;
- the relevant population and unit of analysis;
- the intended outcome or target;
- foreseeable sampling, measurement, missing-data, privacy, licensing, or access limitations; and
- the evidence needed to support the intended claim or decision.

**Due date:** `[TBD]`
**Grading status:** N/A. The proposal is not separately graded.

## Midterm Project Report and Presentation

The midterm project is worth 15% of the course grade. The detailed allocation among the report, presentation, individual component, and contribution assessment is TBD.

The team report will establish a defensible initial analysis.

It will include, as applicable:

- the practical or research problem;
- the type of statistical task;
- how the data were generated or observed;
- the target population and observed sample;
- treatment of duplicated, repeated, and missing observations;
- an empirical description of the relevant distributions;
- an appropriate baseline;
- an initial ranking, regression, classification, or other analysis;
- a train–validation–test design or another appropriate evaluation protocol; and
- a distinction between supported claims and limitations.

**Expected timing:** Near Lectures 13–15
**Exact due date:** `[TBD]`

Midterm presentations will take place on October 13 and October 15. The presentation schedule and team order will be announced after teams are formed.

Each student will also submit an individual component that explains one important analytical choice, the evidence supporting that choice, and one unresolved risk or next step.

Each member will submit a confidential and honest report of their own contribution and their teammates’ contributions. Free riding, which means claiming the benefits of team work without making a responsible contribution or understanding the submitted analysis, is prohibited.

## Final Project Package and Presentation

The final project is worth 25% of the course grade. The detailed allocation among the final package, presentation, individual component, and contribution assessment is TBD.

The team project will be submitted as a portfolio-ready, reproducible analysis package.

It will include:

1. a Python notebook;
2. a claim–evidence table;
3. a fair comparison between a baseline and any candidate method;
4. an uncertainty or stability analysis;
5. calibration, subgroup, temporal, spatial, or causal analysis when relevant;
6. conditions under which the analysis or model should not be used; and
7. a final recommendation of `use`, `conditional use`, `hold`, or `reject`.

Teams are not required to use a modern AI model. A team that uses one must show why it is more appropriate than a simpler baseline.

Each student will submit an individual component that states the supported claim, recommends an action, explains the relevant uncertainty, and identifies conditions under which the result should not be used.

Each member will submit a confidential and honest report of their own contribution and their teammates’ contributions. Free riding is prohibited.

Final presentations will take place on December 1, December 3, and December 8. The presentation schedule and team order will be announced after teams are formed.

**Due date:** `[TBD]`

# Week-by-Week Topic Schedule

Schedule and deliverables are subject to change.

## Week 1

### Lecture 1 — Tuesday, August 25

**Statistics and Data Science in Practice**

**Goal:** Students will learn how statistics and data science translate practical problems into statistical tasks and evidence-based decisions.

### Lecture 2 — Thursday, August 27

**Populations, Random Variables, and Data-Generating Processes**

**Goal:** Students will learn the formal definitions of observational units, populations, random variables, and data-generating processes.

## Week 2

### Lecture 3 — Tuesday, September 1

**Joint, Marginal, and Conditional Probability; Independence and Bayes’ Rule**

**Goal:** Students will learn how joint, marginal, and conditional probability, independence, and Bayes’ rule describe relationships among random variables.

### Lecture 4 — Thursday, September 3

**Probability Distributions, Likelihood, and Distribution Selection**

**Goal:** Students will learn how probability distributions and likelihood are used to represent and compare data-generating processes.

## Week 3

### Lecture 5 — Tuesday, September 8

**Empirical Data and Sample Statistics**

**Goal:** Students will learn how empirical distributions and sample statistics summarize observed data and differ from population quantities.

### Lecture 6 — Thursday, September 10

**Sampling Distributions, Standard Errors, and Bootstrap**

**Goal:** Students will learn how sampling distributions, standard errors, and bootstrap methods quantify uncertainty in sample statistics.

## Week 4

### Lecture 7 — Tuesday, September 15

**Statistical Estimation: MLE, MAP, and VI Recognition**

- Maximum likelihood estimation chooses parameters that make the observed data comparatively plausible under a specified model.
- A prior distribution and a likelihood combine to produce a posterior distribution.
- Maximum a posteriori estimation returns a mode of the posterior distribution rather than a measure of posterior uncertainty.
- A MAP estimate is generally not invariant to nonlinear reparameterization because the transformed posterior density can have a different mode.
- MLE, MAP, and empirical risk minimization are related but distinct estimation principles.
- Variational inference is introduced at recognition level as an optimization-based approximation to a difficult posterior distribution.

### Lecture 8 — Thursday, September 17

**Prediction Tasks, Model Evaluation, and Decision Use**

- A prediction task specifies an observational unit, deployment population, prediction time, outcome horizon, and target.
- A statistical loss function differs from an evaluation metric and from the downstream action based on a prediction.
- Empirical risk minimization selects a prediction rule by minimizing average training loss within a candidate class.
- Training, validation, test, and cross-validation protocols serve different roles in model selection and final evaluation.
- Target, feature, preprocessing, entity, temporal, and document leakage invalidate apparently strong predictive results.
- Error analysis and explicit costs or capacity constraints connect scores, probabilities, thresholds, and rankings to operational action.

## Week 5

### Lecture 9 — Tuesday, September 22

**Ranking Statistics and Ranking Evaluation**

- Scores, ranks, percentiles, ordered lists, and ties represent distinct properties of a ranking system.
- A strictly monotone transformation can change scores without changing their ranking.
- Spearman correlation and Kendall concordance compare ordered outcomes using different rank relationships.
- AUC measures pairwise ranking concordance rather than only classification performance.
- Precision at $k$, recall at $k$, reciprocal rank, mean reciprocal rank, and NDCG evaluate different properties of a ranked list.
- Top-$k$ results depend on the cutoff, candidate set, and outcome prevalence, so ranking stability must be evaluated at the operational cutoff.

### Lecture 10 — Thursday, September 24

**Missingness, Imputation, Duplication, and Pipeline Integrity**

- Exact duplicates, legitimate repeated observations, merge multiplicity, and pseudoreplication have different statistical consequences.
- Unmodeled duplication or dependence exaggerates effective sample size and precision.
- MCAR, MAR, and MNAR describe different relationships between a missingness indicator and complete-data variables.
- MAR and MNAR generally cannot be distinguished from the observed-data distribution alone.
- Complete-case analysis, unconditional mean imputation, conditional imputation, and multiple imputation rely on different assumptions.
- Scaling, encoding, transformation, and imputation belong inside the appropriate training or cross-validation partition.

## Week 6

### Lecture 11 — Tuesday, September 29

**Confidence, Credible, and Conformal Uncertainty**

- A frequentist confidence interval is interpreted through its repeated-sampling coverage property.
- A Bayesian credible interval is a posterior probability statement conditional on a model and prior.
- Parameter uncertainty differs from uncertainty about a future observation.
- Split conformal prediction starts with a supplied predictor and uses separate calibration observations to measure its prediction errors.
- The standard finite-sample conformal guarantee requires exchangeability between calibration observations and the future observation.
- Standard conformal coverage is marginal over future observations and does not guarantee nominal coverage at every individual covariate value or subgroup.

### Lecture 12 — Thursday, October 1

**Linear Regression, Basis Expansion, and Sieve Models**

- Linear regression models a conditional mean rather than establishing a causal relationship.
- Simple and multiple regression coefficients represent conditional associations under the specified model.
- Categorical predictors, interactions, and transformations extend the linear predictor.
- Polynomial and spline basis expansions represent nonlinear conditional-mean relationships.
- A sieve model is a sequence of increasingly flexible finite-dimensional approximations.
- Held-out performance, residual patterns, influential observations, and extrapolation boundaries assess regression adequacy.

## Week 7

### Lecture 13 — Tuesday, October 6

**Logistic Regression and Probability Prediction**

- Binary outcomes, probabilities, odds, and log-odds provide different descriptions of an event.
- Logistic regression models a conditional event probability through a linear log-odds function.
- Logistic coefficients and conditional odds ratios differ from probability differences on the outcome scale.
- Complete or quasi-complete separation can make unregularized maximum-likelihood coefficients unstable or unbounded.
- Held-out probability predictions are assessed for discrimination and calibration before any action threshold is selected.
- A decision threshold converts a probability into an action and depends on prevalence, error costs, and available capacity.

### Lecture 14 — Thursday, October 8

**Trees, Random Forests, and Boosting**

- A decision tree recursively partitions the predictor space into regions with local predictions.
- Split selection, tree depth, and leaf size control the flexibility of a tree.
- Bagging averages predictions across resampled models to reduce instability.
- Random forests add randomized feature selection to an ensemble of decision trees.
- Boosting adds successive learners that approximate loss-reducing corrections, often by fitting the negative gradient of the current empirical loss.
- Held-out performance, stability, computation, and subgroup errors guide comparisons among trees, random forests, and boosting.

## Week 8

### Midterm Project Presentations I — Tuesday, October 13

Teams assigned to the first presentation meeting will present their midterm analyses.

### Midterm Project Presentations II — Thursday, October 15

The remaining teams will present their midterm analyses.

## Week 9

### Lecture 15 — Tuesday, October 20

**Kernel Methods and RKHS**

- A kernel is a similarity function corresponding to an inner product in a feature space.
- A Gram matrix records pairwise kernel similarities among observed units.
- Positive semidefiniteness makes a kernel compatible with an inner-product representation.
- An RKHS is a function space in which point evaluation is represented by an inner product.
- The representer theorem is used without proof to explain why a regularized kernel solution depends on observed training points.
- Kernel choice, bandwidth, regularization, sample size, and computation determine the practical use of kernel ridge regression.

### Lecture 16 — Thursday, October 22

**Neural Networks and Learned Representations**

- Learned representations differ from fixed input features and fixed kernels.
- A multilayer perceptron composes affine transformations with nonlinear activation functions.
- Backpropagation efficiently computes gradients of the loss with respect to network parameters.
- An optimizer such as stochastic gradient descent uses those gradients to update parameters from minibatches.
- Weight decay, dropout, and early stopping provide different forms of regularization.
- Learning curves, seed variability, and baseline comparisons determine whether a learned representation is justified.

## Week 10

### Lecture 17 — Tuesday, October 27

**Time-Series and Sequence Modeling: Dependence, Evaluation, and the Transformer**

- A forecasting problem specifies a time index, forecast origin, forecast horizon, and available information set.
- Naive, seasonal-naive, lag-regression, and autoregressive models provide progressively richer forecasting baselines.
- Temporal splits and rolling-origin evaluation prevent future information from entering model selection.
- Fixed-window features differ from representations learned directly from time-series or text sequences.
- Self-attention forms query, key, and value representations and uses query–key compatibility to weight combinations of the values.
- Positional representations supply order information that self-attention does not contain by itself.
- Temporal, spatial, or sequential dependence requires evaluation procedures that preserve the dependence relevant to deployment.

### Lecture 18 — Thursday, October 29

**Clustering and Unsupervised Validation**

- Representation, scaling, distance, and similarity choices define the structure available to a clustering method.
- $K$-means minimizes within-cluster squared distance around estimated centroids.
- Initialization and the choice of $K$ affect the resulting $K$-means partition.
- A Gaussian mixture model is introduced at recognition level as a probabilistic clustering model with posterior membership responsibilities.
- Clustering on raw variables can differ substantially from clustering on reduced or pretrained representations.
- Stability, external information, decision utility, and the distinction between fluent labels and valid clusters support unsupervised evaluation.

## Week 11

### Lecture 19 — Tuesday, November 3

**Generative AI, Foundation Models, and TabPFN**

- Generative AI produces new structured outputs from a learned conditional probability model.
- The autoregressive factorization $p_\theta(x_{1:T}\mid c)=\prod_{t=1}^{T}p_\theta(x_t\mid x_{<t},c)$ expresses a joint conditional sequence distribution through next-token conditional distributions.
- A foundation model is pretrained on a broad task or data distribution and adapted to downstream uses.
- Zero-shot, few-shot, and in-context use differ in the task information supplied at inference time.
- Frozen representations, retrieval augmentation, prompting, and fine-tuning provide distinct adaptation strategies.
- TabPFN is introduced at recognition level as a pretrained tabular predictor that approximates posterior-predictive inference under a pretraining task distribution.
- Task performance, factual support, abstention, latency, cost, subgroup error, and benchmark contamination jointly determine model suitability.

### Lecture 20 — Thursday, November 5

**Calibration and Probability Quality**

- Calibration requires agreement between predicted probabilities and observed event frequencies.
- Probability calibration differs from discrimination and ranking performance.
- Reliability diagrams, calibration intercepts, and calibration slopes reveal different forms of miscalibration.
- Brier score and log loss are proper scoring rules for probability predictions.
- Platt scaling, isotonic regression, and temperature scaling are introduced as post-hoc recalibration methods.
- Separate calibration and test data preserve an honest evaluation of recalibrated probabilities.

## Week 12

### Lecture 21 — Tuesday, November 10

**Data Reduction: PCA, SVD, and Reconstruction**

- Data reduction serves distinct goals in visualization, compression, denoising, and downstream prediction.
- Centering and scaling affect the directions found by principal component analysis.
- Principal directions, component scores, and low-rank reconstruction provide complementary geometric descriptions.
- Singular value decomposition is introduced as the matrix factorization underlying a standard computation of PCA.
- Explained variance measures variation retained by a linear projection rather than causal or decision-relevant importance.
- Component loadings describe directions of linear variation and do not identify causal effects.

### Lecture 22 — Thursday, November 12

**Data Thinning, Pruning, Vector Quantization, and Distillation**

- Random, stratified, and distribution-aware thinning preserve different properties of a dataset.
- Thinning can disproportionately remove rare subgroups, boundary cases, and distributional tails.
- Coresets are introduced at recognition level as compact weighted summaries designed for a specified objective.
- Structured and unstructured pruning are introduced at recognition level, with emphasis on the gap between nominal sparsity and actual latency.
- Vector quantization is introduced at recognition level as mapping continuous representations to codebook entries with reconstruction distortion.
- Knowledge distillation is introduced at recognition level as transferring teacher outputs to a student while potentially transmitting bias and miscalibration.

## Week 13

### Lecture 23 — Tuesday, November 17

**Causal Analysis I: Randomized Experiments**

- Prediction of an outcome differs from estimation of the effect of an intervention.
- Treatment, outcome, potential outcomes, and the average treatment effect define a randomized causal question.
- The fundamental problem of causal inference arises because both potential outcomes are not observed for the same unit.
- Random assignment justifies a difference-in-means estimate and its associated uncertainty.
- Randomization units, attrition, noncompliance, intention-to-treat, and interference constrain experimental claims.
- Peeking, multiple comparisons, and unplanned stopping motivate prespecified metrics, guardrails, and stopping rules.

### Lecture 24 — Thursday, November 19

**Causal Analysis II: DAGs, Observational Identification, and Estimation**

- A target trial specifies the treatment, outcome, population, assignment procedure, follow-up period, and causal contrast.
- A directed acyclic graph represents assumed causal relationships rather than associations learned automatically from data.
- The backdoor criterion uses d-separation to select covariates that remove noncausal treatment–outcome association under the assumed graph.
- The g-formula, propensity-score methods, and doubly robust estimators use different nuisance models to estimate an identified effect.
- Identification requires causal assumptions such as consistency, conditional exchangeability, and positivity that predictive fit cannot establish.
- Overlap diagnostics, alternative specifications, and recognition-level sensitivity analysis constrain causal claims before action.

## Fall Break

**Tuesday, November 24:** No class
**Thursday, November 26:** No class

## Week 14

### Final Project Presentations I — Tuesday, December 1

Teams assigned to the first final-presentation meeting will present their analyses.

### Final Project Presentations II — Thursday, December 3

Teams assigned to the second final-presentation meeting will present their analyses.

## Week 15

### Final Project Presentations III — Tuesday, December 8

The remaining teams will present their final analyses.

# Assignments and Methods of Assessment

## Graded Components

| Component | Weight | Description |
| --- | ---: | --- |
| In-class quizzes | 60% | A 15-minute quiz given frequently beginning in Week 2, without a fixed announced schedule |
| Midterm project | 15% | Progress report, presentation, individual component, and contribution assessment; detailed internal allocation TBD |
| Final project | 25% | Final report, reproducible analysis and code, presentation, individual component, and contribution assessment; detailed internal allocation TBD |

**Total:** 100%.

There is no midterm examination and no final examination.

## Grading Scale

```
[TBD before student distribution]
```

# Use of Artificial Intelligence

For projects, students are welcome to use AI models. Evaluation will focus on whether every student can independently explain the problem, method, solution, evidence, and error analysis. Students must verify AI-generated output. AI use does not replace individual accountability.

# Late Work and Missed Assessments

Late work is not accepted. An exception is allowed only when both conditions are met:

1. the student provides formal documentation or proof of the delay; and
2. the instructor approves the exception.

The quiz make-up conditions stated in the Quizzes section apply to missed quizzes.

Students experiencing an emergency or extended circumstance should contact the instructor as early as possible.

# Incomplete Grades

Incomplete grades are granted only in exceptional circumstances, such as a documented medical emergency, and in accordance with university policy. Students should contact the instructor as early as possible to discuss eligibility, required documentation, and a completion plan.

# Course Policies

## Attendance and Participation

Regular attendance is expected because class meetings include decision exercises and may include timed quizzes. Quizzes begin in Week 2 and do not follow a fixed announced schedule. Participation means meaningful engagement with questions, discussions, notebook activities, and peer feedback. It does not require speaking during every meeting.

N/A. Participation is not separately graded.

## Academic Integrity

Students must follow University of Illinois academic-integrity standards. Plagiarism, unauthorized collaboration, fabrication, concealed use of outside assistance, and misrepresentation of work violate these standards.

## Teamwork and Individual Accountability

Project partners may collaborate fully on the team report, analysis package, and presentation. Every team member is responsible for understanding and explaining the complete analysis. Individual components must represent the submitting student's own reasoning. Each member must submit an honest contribution report and peer assessment. Free riding is prohibited. Students may discuss general concepts across teams, but they may not copy another team's analysis, writing, code, or results.

## Disruptive Behavior

Behavior that persistently or substantially interferes with classroom activities may be treated as disruptive behavior and may be subject to action under university policy.

# Student Resources

## Statement of Inclusion

The University of Illinois is committed to a welcoming and inclusive learning environment. Students are expected to contribute to a respectful classroom that values diverse perspectives, experiences, disciplinary backgrounds, and levels of prior statistical or programming experience.

## Religious Observances

Students who need accommodation for a religious observance should notify the instructor as early as possible so that appropriate arrangements can be made.

## Accessibility

Students who need disability-related accommodations should contact the instructor and Disability Resources and Educational Services to arrange academic adjustments or auxiliary aids.

## Community of Care

Students experiencing circumstances that affect their wellbeing or academic performance are encouraged to reach out. The university provides counseling, wellbeing, accessibility, and academic-support resources.

## Land Acknowledgement

The University of Illinois provides an official land acknowledgement. Current university-approved language may be incorporated into the published syllabus or course materials.

------

# Items to Resolve Before Student Distribution

1. Grading scale
2. Project proposal, midterm, and final deadlines
3. Quiz resource, counted-score, and dropped-score policies
4. Final software-package list
5. Office hours and preferred contact format
6. Current official prerequisite wording
