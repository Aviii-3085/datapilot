# Datapilot v0.4 Specification

## 1. Release Objective

### Core Principle

Datapilot should distinguish between what it observes,
what it calculates, what it interprets, and what it cannot assess.

### v0.4 Goal

Move Datapilot from basic dataset quality reporting toward
contextual dataset intelligence.

Datapilot v0.4 must provide users with a more realistic
understanding of:

- Dataset Health
- Statistical characteristics
- ML preparation
- Notebook workflow readiness
- Data integrity signals
- Analytical limitations

The system must prioritize mathematical transparency,
deterministic behavior, explainability, and clear boundaries.

---

# 2. Dataset Health 2.0

## 2.1 Definition

Dataset Health measures the structural and data-quality condition
of a dataset based only on observable properties.

It does NOT represent:

- ML model performance
- Business validity
- Domain correctness
- Factual correctness
- Causal validity
- Statistical usefulness for a specific task

Dataset Health is a quality assessment, not a guarantee of
dataset usefulness.

---

## 2.2 Dimensions

Dataset Health consists of four dimensions:

1. Completeness
2. Duplicates
3. Structure
4. Consistency

Each dimension produces a score from 0 to 100.

The overall Dataset Health score is derived from these dimensions
using documented weights.

---

## 2.3 Dimension Weights

| Dimension | Weight |
|---|---:|
| Completeness | 30% |
| Duplicates | 20% |
| Structure | 25% |
| Consistency | 25% |
| Total | 100% |

Weights must remain fixed and deterministic for a given Datapilot
version.

They must not be adjusted to produce a desired result for a
specific dataset.

---

## 2.4 Completeness

### Purpose

Measure how completely the dataset is populated.

### Observed Metrics

- Total cells
- Missing cells
- Overall missing-cell percentage
- Missing percentage per column
- Number of columns containing missing values
- Highest column-level missingness
- Missingness concentration

### Primary Metric

missing_rate = missing_cells / total_cells * 100

completeness_rate = 100 - missing_rate

### Dimension Score

Completeness Score = completeness_rate

The score is bounded:

0 <= Completeness Score <= 100

### Missingness Concentration

Overall missingness must not hide severe column-level missingness.

Datapilot must separately expose:

- Overall missingness
- Per-column missingness
- Highest column-level missingness
- Missingness concentration

Example:

Overall missingness: 2.64%
Customer ID missingness: 20.5%

The concentration signal must remain visible even when the
overall Completeness Score is high.

### Interpretation

Completeness measures the proportion of populated cells.

A missing value is not automatically a data error.

---

## 2.5 Duplicates

### Purpose

Measure the proportion of rows identified as duplicates.

### Observed Metrics

- Total rows
- Duplicate rows
- Duplicate percentage

### Primary Metric

duplicate_rate = duplicate_rows / total_rows * 100

### Dimension Score

Duplicate Score = 100 * (1 - duplicate_rate / 100)

The score is bounded:

0 <= Duplicate Score <= 100

### Interpretation

A duplicate row is not automatically invalid.

Duplicates may be legitimate depending on the dataset's intended
grain and domain.

Datapilot must therefore report duplicates as a signal requiring
review rather than automatically treating every duplicate as an
error.

---

## 2.6 Structure

### Purpose

Measure whether Datapilot can reliably understand the basic
structural representation of the dataset.

### Observed Metrics

- Row count
- Column count
- Recognized data types
- Unrecognized or unsupported data types
- Empty columns
- Constant columns
- Column-name availability
- Datetime detection
- Boolean detection
- Numeric detection
- Categorical detection

### Structural Components

The Structure Score consists of:

1. Type Recognition
2. Empty Column Signal
3. Constant Column Signal

### Type Recognition

type_recognition_rate =
    recognized_columns / total_columns * 100

### Empty Column Rate

empty_column_rate =
    empty_columns / total_columns * 100

### Constant Column Rate

constant_column_rate =
    constant_columns / total_columns * 100

### Dimension Score

The initial Structure Score is defined as:

Structure Score =
    Type Recognition Score * 0.50
  + Empty Column Score * 0.25
  + Constant Column Score * 0.25

Where:

Type Recognition Score = type_recognition_rate

Empty Column Score = 100 - empty_column_rate

Constant Column Score = 100 - constant_column_rate

Each component is bounded from 0 to 100.

### Interpretation

Structural quality measures whether Datapilot can reliably
represent and analyze the dataset.

Structural quality does not imply semantic correctness.

A constant column is not automatically erroneous, but it provides
a structural signal that may matter for downstream analysis.

---

## 2.7 Consistency

### Purpose

Measure detectable internal irregularities that can be evaluated
without assuming unknown domain rules.

### Observable Signals

Potential signals include:

- Type inconsistencies
- Mixed representations
- Structurally inconsistent values
- Detectable invalid-looking values
- Suspicious categorical representations
- Other internally inconsistent patterns

### Domain Boundary

Datapilot must not assume domain rules that have not been provided.

For example:

Negative value != automatically invalid

unless the dataset context explicitly establishes that negative
values are not permitted.

### Dimension Score

The Consistency Score must only incorporate signals that can be
defined objectively and reproducibly.

For v0.4, consistency scoring must use only implemented,
deterministic consistency signals.

Signals that cannot be objectively evaluated must be reported as
Not Assessed rather than converted into arbitrary penalties.

### Interpretation

Consistency measures detectable internal irregularities.

It does not establish:

- Business validity
- Domain validity
- Factual correctness

---

## 2.8 Overall Dataset Health

The overall score is:

Overall Health =
    Completeness Score * 0.30
  + Duplicate Score * 0.20
  + Structure Score * 0.25
  + Consistency Score * 0.25

The result is bounded:

0 <= Overall Health <= 100

The score must be deterministic for identical input data and
configuration.

### Important Principle

The overall score must never be displayed without:

- Component dimension scores
- Raw supporting metrics
- Notable issues
- Relevant limitations

---

## 2.9 Health Interpretation

Provisional status bands:

| Score | Status |
|---:|---|
| 90–100 | Excellent |
| 75–89 | Good |
| 60–74 | Moderate |
| 40–59 | Needs Attention |
| 0–39 | Poor |

These bands must be validated against multiple real-world datasets
before the v0.4 release.

The qualitative label must never replace the numerical score or
underlying dimensions.

---

## 2.10 Notable Issues

The report must expose significant underlying signals even when
the overall score is high.

Example:

Overall missingness: 2.64%
Customer ID missingness: 20.5%

Duplicate rate: 1.31%

Statistical outliers: 6.34%

Notable issues must not be hidden by the aggregate score.

---

## 2.11 Statistical Separation

Outliers, skewness, kurtosis, distributions, and correlations
must not automatically reduce Dataset Health.

These belong primarily to the Statistical Profile and ML
Readiness layers unless a specific structural or data-quality rule
justifies their inclusion.

This prevents unusual but potentially legitimate statistical
patterns from being incorrectly classified as poor dataset quality.

---

## 2.12 Edge Cases

The implementation must explicitly handle:

- Empty datasets
- Single-row datasets
- Single-column datasets
- Completely missing columns
- Completely duplicated datasets
- No missing values
- No duplicates
- Constant columns
- Mixed data types
- Unsupported data types
- Very large datasets

No edge case should produce a misleading score because a metric
cannot be calculated.

---

## 2.13 Evidence Model

Every Dataset Health result should be traceable through:

Observed
    ↓
Calculated
    ↓
Dimension Score
    ↓
Overall Score
    ↓
Interpretation

---

## 2.14 Dataset Health Limitations

Dataset Health does not establish:

- Factual correctness
- Business correctness
- Domain validity
- Causal validity
- Suitability for a specific ML task
- Predictive performance
- Absence of data leakage

---

# 3. ML Readiness

## 3.1 Definition

ML Readiness represents observable preparation signals for a
machine-learning workflow.

It does NOT mean:

"A successful ML model can be trained."

It does NOT predict:

- Model accuracy
- Generalization performance
- Business usefulness
- Causal validity
- Absence of data leakage
- Production readiness

The preferred user-facing terminology is:

ML Preparation

with ML Readiness used as the name of the analytical assessment.

---

## 3.2 Dimensions

ML Readiness consists of:

1. Completeness
2. Feature Quality
3. Data Stability
4. Consistency
5. Distribution
6. Target Readiness

Each dimension produces either:

- A score from 0 to 100
- Not Assessed

Not Assessed must be used when the available dataset does not
contain enough evidence to evaluate a dimension responsibly.

---

## 3.3 ML Dimension Weights

The initial weights are:

| Dimension | Weight |
|---|---:|
| Completeness | 25% |
| Feature Quality | 20% |
| Data Stability | 15% |
| Consistency | 15% |
| Distribution | 15% |
| Target Readiness | 10% |
| Total | 100% |

These weights are versioned design parameters and must remain
deterministic.

They must be validated against multiple real-world datasets
before release.

---

## 3.4 Assessment Coverage

ML Readiness must report not only a score but also assessment
coverage.

Assessment Coverage represents the proportion of the weighted
dimensions that were actually assessed.

For example:

Target Readiness = Not Assessed

does not mean:

Target Readiness = 0

Instead:

Assessment Coverage = 90%

may be reported when the Target Readiness dimension represents
10% of the total assessment.

This prevents unknown information from being interpreted as a
negative result.

---

## 3.5 ML Completeness

### Purpose

Evaluate whether missing data may interfere with feature
preparation.

### Metrics

- Overall missing-cell rate
- Column-level missingness
- Number of columns with missing values
- Highest feature missingness

### Base Score

ML Completeness Score = 100 - missing_rate

The score is bounded:

0 <= ML Completeness Score <= 100

### Important Boundary

The score does not determine whether a particular imputation
strategy is appropriate.

---

## 3.6 Feature Quality

### Purpose

Evaluate observable structural characteristics of potential
features.

### Signals

Potential signals include:

- Recognized feature data types
- Constant columns
- Empty columns
- Identifier-like columns
- Excessively high-cardinality categorical columns
- Unsupported feature types

### Important Boundary

Datapilot must not automatically classify a column as a bad
feature based only on its name or cardinality.

For example:

A high-cardinality column may be a legitimate feature in some
machine-learning problems.

Identifier-like detection is therefore a signal, not proof of
unsuitability.

### Dimension Score

Feature Quality must be derived only from objectively detected
signals implemented in the v0.4 analysis engine.

Each penalty must be documented before implementation.

---

## 3.7 Data Stability

### Purpose

Evaluate observable stability-related signals within the supplied
dataset.

### Important Boundary

A single static dataset cannot establish train/test stability,
production drift, temporal drift, or future distribution stability.

Those require additional data or configuration.

### Observable Signals

Potential signals include:

- Constant features
- Extreme missingness concentration
- Severe duplicate concentration
- Highly irregular feature distributions
- Temporal structure when a datetime column is available

### Assessment Boundary

If train/test, temporal, or reference data is not supplied,
Datapilot must not claim that distribution stability across
datasets has been established.

Such stability may be reported as:

Not Assessed

---

## 3.8 Consistency

### Purpose

Evaluate whether detectable internal inconsistencies could create
problems during feature preparation.

### Signals

Potential signals include:

- Type inconsistencies
- Mixed representations
- Structural irregularities
- Invalid-looking values where objectively detectable

### Boundary

Domain-specific validity rules must not be invented.

Consistency is therefore limited to objectively observable
properties.

---

## 3.9 Distribution

### Purpose

Evaluate observable statistical characteristics that may affect
machine-learning preparation.

### Signals

Potential signals include:

- Skewness
- Kurtosis
- Outlier concentration
- Constant features
- Near-zero variance features
- Extreme distribution imbalance where objectively measurable

### Important Boundary

A non-normal distribution is not automatically unsuitable for ML.

Many machine-learning algorithms do not require normally
distributed features.

Therefore:

"Non-normal"

must not automatically become:

"Bad for ML."

The report should instead describe the observed distribution and
its potential implications.

---

## 3.10 Target Readiness

### Purpose

Evaluate target-related preparation only when a target variable is
provided or explicitly identified.

### Without Target Information

Target Readiness = NOT ASSESSED

Datapilot must not invent a target variable.

### With Target Information

Potential target signals include:

- Target existence
- Missing target values
- Target data type
- Target cardinality
- Class distribution for classification targets
- Numeric distribution for regression targets
- Constant target detection

### Important Boundary

Target Readiness does not establish:

- Model suitability
- Predictive difficulty
- Business relevance
- Causal validity

---

## 3.11 Overall ML Preparation Score

The overall score is a weighted mean of assessed dimensions.

For assessed dimensions:

ML Preparation Score =
    sum(dimension_score * dimension_weight)
    /
    sum(assessed_dimension_weights)

This means Not Assessed dimensions are excluded from the numerical
average rather than treated as zero.

### Assessment Coverage

Assessment Coverage =
    sum(assessed_dimension_weights)
    /
    sum(all_dimension_weights)
    * 100

Example:

If Target Readiness is Not Assessed:

Assessment Coverage = 90%

The user should see both:

ML Preparation Score
and
Assessment Coverage

---

## 3.12 ML Preparation Interpretation

The score must be accompanied by a qualitative interpretation.

Provisional bands:

| Score | Interpretation |
|---:|---|
| 90–100 | Strong preparation signals |
| 75–89 | Generally well prepared |
| 60–74 | Moderate preparation |
| 40–59 | Significant preparation concerns |
| 0–39 | Major preparation concerns |

These are preparation-level interpretations.

They must never be displayed as:

"Model will perform well."

---

## 3.13 ML Readiness Status

The report should combine:

- ML Preparation Score
- Assessment Coverage
- Dimension scores
- Not Assessed dimensions
- Major preparation signals
- Limitations

Example:

ML Preparation: 78 / 100
Assessment Coverage: 90%
Status: Generally well prepared

Target Readiness: Not Assessed

This communicates both the result and the confidence boundary.

---

## 3.14 ML Readiness Limitations

ML Readiness does not establish:

- Model accuracy
- Model generalization
- Best algorithm
- Best hyperparameters
- Feature importance
- Causal relationships
- Absence of leakage
- Production readiness
- Business usefulness
- Future data stability

---

# 4. Evidence Boundaries

Datapilot distinguishes:

## Observed

Directly measured properties.

Examples:

- Row count
- Missing values
- Duplicate count
- Column types
- Outlier count
- Correlation coefficient

## Calculated

Metrics derived from observations.

Examples:

- Missingness percentage
- Duplicate percentage
- Dimension score
- Overall score
- Assessment coverage

## Interpreted

Statistical or analytical interpretation of calculated metrics.

Examples:

- High missingness concentration
- Strong skewness
- Heavy-tailed distribution
- Potential feature preparation concern

Interpretation must remain bounded by available evidence.

## Not Assessed

Properties Datapilot cannot responsibly determine from available
information.

Examples:

- Target suitability without a target
- Train/test drift without separate datasets
- Production drift without reference data
- Business validity without domain rules
- Model performance without training/evaluation

Not Assessed must never be silently converted into a positive or
negative score.

---

# 5. Statistical Interpretation

Datapilot should provide contextual interpretation for:

- Skewness
- Kurtosis
- Outliers
- Distribution characteristics
- Correlation
- Variability

### Statistical Boundaries

Statistical anomalies must not automatically be described as
data errors.

A statistical outlier may be:

- A legitimate observation
- A measurement issue
- A data-entry issue
- A rare but meaningful event

Datapilot should therefore use language such as:

"Statistical outlier detected"

rather than:

"Incorrect value detected"

unless an objective validation rule exists.

### Correlation

Correlation should be interpreted as an association measure.

Correlation must not be presented as:

- Causation
- Proof of a relationship outside the measured data
- Proof that no relationship exists when correlation is weak

---

# 6. Data Integrity Signals

Datapilot may identify:

- Missing values
- Duplicate records
- Suspicious values
- Extreme values
- Invalid-looking values
- Identifier-like columns
- Structural anomalies
- Constant columns
- Potentially problematic representations

These are signals, not proof of factual invalidity.

### Signal Categories

Signals should be classified as:

- Observed Issue
- Statistical Signal
- Structural Signal
- Potential Concern
- Not Assessed

The system must avoid presenting potential concerns as confirmed
errors.

---

# 7. Notebook Readiness

## 7.1 Definition

Notebook Readiness evaluates how readily Datapilot's analysis
workflow can be used in an interactive notebook environment.

It does not claim that every notebook environment is guaranteed to
support every Datapilot capability.

---

## 7.2 Supported Environments

Potential environments:

- Jupyter Notebook
- JupyterLab
- Google Colab
- VS Code Notebooks

Compatibility claims must only be made for environments that are
actually tested and documented.

---

## 7.3 Notebook Readiness Dimensions

Initial dimensions:

1. API Accessibility
2. DataFrame Compatibility
3. Result Inspectability
4. Reproducibility
5. Report Generation
6. Environment Compatibility

Each dimension produces a score from 0 to 100 or Not Assessed.

---

## 7.4 Notebook Readiness Boundaries

Notebook Readiness evaluates Datapilot's workflow compatibility.

It does not guarantee:

- Kernel stability
- Third-party package compatibility
- User environment correctness
- Operating-system compatibility beyond tested environments
- Performance for arbitrary notebook workloads

---

## 7.5 Notebook Workflow

The intended workflow is:

Dataset
    ↓
Notebook
    ↓
Datapilot analysis
    ↓
Report object
    ↓
Interactive inspection
    ↓
HTML report or further analysis

Future notebook widgets may extend this workflow but must not be
documented as implemented until they exist.

---

# 8. Grouped Comparisons

## 8.1 Purpose

Provide users with contextual comparisons between groups within a
dataset.

Examples may include:

- Statistics by category
- Missingness by group
- Outlier rates by group
- Distribution comparisons
- Quality differences between groups

## 8.2 Boundaries

Grouped comparisons must only use grouping variables supplied by
the user or objectively identified as suitable categorical/grouping
columns.

Datapilot must not infer causal explanations from group differences.

## 8.3 API

The exact grouped comparison API must be finalized after reviewing
the existing architecture.

No grouped comparison API should be documented as implemented
until it exists.

---

# 9. Report Architecture

The v0.4 report should contain:

1. Dataset Overview
2. Dataset Health
3. Statistical Profile
4. ML Readiness
5. Notebook Readiness
6. Data Integrity Signals
7. Insights
8. Recommendations
9. Assessment Boundaries

Each major score must expose:

- Overall score
- Dimension scores
- Supporting metrics
- Notable issues
- Not Assessed dimensions
- Interpretation
- Limitations where relevant

The report must avoid presenting a single aggregate score as the
complete description of the dataset.

---

# 10. API Design

Potential APIs:

report.summary()

report.dataset_health()

report.ml_readiness()

report.notebook_readiness()

report.statistical_profile()

report.integrity_signals()

report.insights()

report.recommendations()

No API should be documented as implemented until it exists.

The public API must remain deterministic and inspectable.

---

# 11. Scoring Rules

Every score must define:

- Inputs
- Formula
- Weight
- Range
- Threshold
- Interpretation
- Missing/unknown behavior
- Edge cases

### General Scoring Principles

1. Scores must be deterministic.
2. Scores must be bounded.
3. Scores must be explainable.
4. Unknown information must not automatically become zero.
5. Not Assessed must remain distinguishable from poor performance.
6. Aggregate scores must expose their components.
7. Raw metrics must remain accessible.
8. Scores must not imply conclusions that the underlying metrics
   cannot support.

---

# 12. Testing Strategy

Every v0.4 scoring component must have:

- Unit tests
- Boundary tests
- Empty-data tests
- Missing-data tests
- Edge-case tests
- Regression tests
- Real-dataset validation

### Scoring Tests

Tests must verify:

- Minimum score
- Maximum score
- Intermediate score
- Exact boundary behavior
- Not Assessed behavior
- Weighting
- Deterministic output

### Real-World Validation

Real-world datasets must be used in addition to synthetic test
fixtures.

A score must not be accepted merely because it passes synthetic
tests.

---

# 13. Real-World Validation

Primary validation dataset:

Online Retail II

Known characteristics include:

- Large row count
- Missing values
- Duplicate rows
- Numeric outliers
- Multiple categorical columns
- Datetime data
- Identifier-like customer information

The dataset should be used to verify whether v0.4 produces a
reasonable contextual interpretation rather than a misleading
single score.

Additional datasets should represent substantially different
structures and quality conditions.

Validation should include:

- Clean datasets
- Missing-heavy datasets
- Duplicate-heavy datasets
- Mixed-type datasets
- High-cardinality datasets
- Small datasets
- Large datasets
- Datasets with meaningful outliers
- Datasets with no obvious quality problems

---

# 14. Documentation

v0.4 documentation should explain:

- What Datapilot observes
- What it calculates
- What it interprets
- What it does not assess
- How Dataset Health is calculated
- How ML Readiness is calculated
- How Assessment Coverage works
- How Not Assessed differs from a poor score
- How statistical patterns are interpreted
- How Notebook Readiness works
- What Datapilot cannot establish

Documentation must avoid marketing language that implies guarantees.

---

# 15. Website

The website should provide real internal pages for:

- Documentation
- Getting Started
- User Guide
- API Reference
- Dataset Health
- ML Readiness
- Notebook Readiness
- Examples
- Changelog
- Roadmap

GitHub remains the engineering/source-code platform.

The website becomes the primary user-facing documentation and
product-information platform.

Users should be able to understand and learn the product without
being required to navigate through GitHub for basic documentation.

---

# 16. Release Boundary

v0.4 must prioritize:

- Correctness
- Mathematical transparency
- Explainability
- Clear boundaries
- Real-world usability
- Deterministic behavior
- Testability

### Core v0.4 Features

- Dataset Health 2.0
- Dimensional Dataset Health
- ML Readiness
- Assessment Coverage
- Not Assessed state
- Statistical interpretation
- Data Integrity Signals
- Notebook Readiness
- Grouped Comparisons
- Expanded report architecture
- Real documentation pages
- Examples
- Changelog
- Roadmap

### Future Features

The following remain outside the core v0.4 implementation unless
explicitly promoted into scope:

- Notebook widgets
- Custom signal plugin architecture
- Automated machine-learning model training
- Automated model selection
- Automated hyperparameter optimization
- LLM-generated analytical conclusions
- Production monitoring
- Data drift monitoring requiring external reference datasets

Features outside the agreed v0.4 scope must not be added merely
because they are interesting.

---

# 17. Open Design Questions

Before implementation, resolve:

- Final consistency metrics
- Final consistency weights
- Final Feature Quality metrics
- Final Data Stability metrics
- Final Distribution metrics
- Final Target Readiness metrics
- Final Notebook Readiness metrics
- Exact scoring thresholds
- Score interpretation validation
- Grouped comparison API
- Target-variable API
- Statistical interpretation rules
- Integrity signal classification

These questions must be resolved before the corresponding feature
is implemented.

---

# 18. Implementation Order

Implementation must proceed in this order:

1. Finalize Dataset Health formulas
2. Finalize ML Readiness formulas
3. Finalize Not Assessed and Assessment Coverage behavior
4. Finalize statistical interpretation rules
5. Finalize integrity signals
6. Update analysis models
7. Implement analysis modules
8. Update Report API
9. Implement scoring and interpretation logic
10. Update HTML report architecture
11. Implement Notebook Readiness
12. Implement Grouped Comparisons
13. Add tests
14. Validate against real-world datasets
15. Update documentation
16. Update website
17. Perform release validation
18. Prepare v0.4.0 release

No implementation should begin for a scoring component until its
formula, inputs, boundaries, and edge-case behavior are defined.

---

# 19. Definition of Done

Datapilot v0.4 is considered complete only when:

- All core scoring formulas are documented
- All implemented scores are deterministic
- Dimension scores are visible
- Aggregate scores expose their components
- Not Assessed is distinct from poor performance
- ML Readiness does not claim model performance
- Dataset Health does not claim business validity
- Statistical anomalies are not automatically classified as errors
- Notebook compatibility claims are tested
- Grouped comparisons are tested
- Existing v0.3 functionality remains intact
- Existing tests continue to pass
- New v0.4 tests pass
- Multiple real-world datasets have been validated
- HTML reports accurately represent the new model
- Documentation accurately reflects implemented functionality
- Planned features are not presented as released features
- Website documentation pages are functional
- Release packaging succeeds
- v0.4.0 can be installed and used in a clean environment