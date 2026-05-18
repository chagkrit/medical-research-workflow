# Deterministic Statistical Scripts

Use `scripts/clinical_stats.py` when a task needs reproducible first-pass descriptive statistics, missingness tables, Table 1 comparisons, or simple 2x2 effect estimates from a CSV file.

Use `scripts/advanced_stats.py` when a task needs reproducible advanced analyses with explicit formulas, seeds, and audit outputs.

## Scope

The script supports:

- Missingness counts and percentages for all columns.
- Continuous summaries: n, missing, mean, SD, median, Q1, Q3, min, max.
- Categorical summaries: counts and percentages.
- Two-group continuous comparisons with Welch t-test.
- Categorical group comparisons with Pearson chi-square.
- 2x2 tables with Fisher exact test plus risk difference, risk ratio, odds ratio, and 95% Wald confidence intervals.
- JSON and Markdown outputs.

`clinical_stats.py` uses only the Python standard library. It does not perform multivariable regression, survival analysis, multiple imputation, propensity methods, prediction modeling, or multiplicity correction.

`advanced_stats.py` requires external packages: `pandas`, `numpy`, `statsmodels`, `lifelines`, and `scikit-learn`. It supports:

- Multivariable regression: linear, logistic, Poisson, negative-binomial with optional robust or cluster-robust covariance.
- Clustered/repeated-measures analysis: GEE with Gaussian, binomial, or Poisson family and independence/exchangeable/autoregressive working correlation.
- Survival analysis: Cox proportional hazards with optional strata, robust variance, and proportional hazards test.
- Imputation: deterministic single numeric iterative imputation.
- Propensity methods: propensity-score estimation, stabilized/unstabilized IPTW, and standardized mean difference balance diagnostics.
- Prediction modeling: deterministic train/test classification or regression metrics.

## Usage

```bash
python3 scripts/clinical_stats.py \
  --input data.csv \
  --group treatment \
  --continuous age,bmi,followup_days \
  --categorical sex,diabetes,outcome \
  --json-out results/stats_report.json \
  --md-out results/stats_report.md
```

Advanced examples:

```bash
python3 scripts/advanced_stats.py regression \
  --input data.csv \
  --formula "outcome ~ age + C(sex) + treatment" \
  --family logistic \
  --robust HC3 \
  --json-out results/logistic.json \
  --md-out results/logistic.md

python3 scripts/advanced_stats.py survival \
  --input data.csv \
  --duration followup_days \
  --event death \
  --covariates age,treatment,bmi \
  --robust \
  --check-ph \
  --json-out results/cox.json

python3 scripts/advanced_stats.py gee \
  --input longitudinal.csv \
  --formula "score ~ visit + treatment + visit:treatment" \
  --group patient_id \
  --family gaussian \
  --cov-struct exchangeable \
  --json-out results/gee.json

python3 scripts/advanced_stats.py impute \
  --input data.csv \
  --variables age,bmi,lab_value \
  --output results/imputed.csv \
  --json-out results/imputation_report.json

python3 scripts/advanced_stats.py propensity \
  --input data.csv \
  --treatment treatment \
  --covariates age,sex,bmi,diabetes \
  --stabilized \
  --output-scores results/propensity_scores.csv \
  --json-out results/propensity.json

python3 scripts/advanced_stats.py prediction \
  --input data.csv \
  --task classification \
  --target outcome \
  --predictors age,sex,bmi,lab_value \
  --json-out results/prediction.json
```

## Interpretation Rules

- Treat outputs as deterministic analysis evidence, not automatic manuscript conclusions.
- Confirm that variable coding makes the first row/column of a 2x2 table match the intended exposure and event direction before reporting OR/RR.
- Use full statistical software for adjusted models, repeated measures, time-to-event analysis, clustered designs, or sparse RxC exact tests.
- For advanced scripts, verify model formula, contrast direction, coding, convergence, assumptions, and missing-row exclusions before reporting.
- Treat deterministic single imputation as a data-preparation sensitivity tool, not a replacement for pooled multiple imputation in primary inference.
- Include the generated JSON or Markdown report in the audit trail.
- If a reviewer could challenge the statistical method, document why the script output is sufficient or escalate to a full analysis plan.

## Output Review Checklist

- Are denominators correct after missing data handling?
- Are group levels sorted and labeled as intended?
- Are expected cell counts below 5 flagged?
- Are unadjusted comparisons clearly labeled as unadjusted?
- Do reported effect estimates match the clinical contrast in the protocol?
