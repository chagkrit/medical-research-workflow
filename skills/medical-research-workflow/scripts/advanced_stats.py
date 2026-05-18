#!/usr/bin/env python3
"""Advanced deterministic medical statistics runner.

Subcommands cover common auditable workflows:
- regression: linear/logistic/Poisson/negative-binomial models via statsmodels
- gee: clustered/repeated-measures regression via statsmodels GEE
- survival: Cox proportional hazards via lifelines
- impute: deterministic numeric iterative imputation via scikit-learn
- propensity: propensity score estimation, IPTW, and balance diagnostics
- prediction: deterministic train/test prediction modeling metrics
"""

from __future__ import annotations

import argparse
import importlib
import json
import math
import sys
import warnings
from pathlib import Path
from typing import Any


def require(package: str, import_name: str | None = None) -> Any:
    try:
        return importlib.import_module(import_name or package)
    except ImportError as exc:
        raise SystemExit(
            f"Missing dependency `{package}`. Install it before running this advanced script."
        ) from exc


np = require("numpy")
pd = require("pandas")


def parse_vars(value: str | None) -> list[str]:
    if not value:
        return []
    return [item.strip() for item in value.split(",") if item.strip()]


def clean_float(value: Any, digits: int) -> Any:
    if isinstance(value, (np.floating, float)):
        if math.isnan(float(value)) or math.isinf(float(value)):
            return None
        return round(float(value), digits)
    if isinstance(value, (np.integer, int)):
        return int(value)
    if isinstance(value, np.ndarray):
        return clean_float(value.tolist(), digits)
    if isinstance(value, dict):
        return {str(k): clean_float(v, digits) for k, v in value.items()}
    if isinstance(value, list):
        return [clean_float(item, digits) for item in value]
    return value


def read_data(path: str) -> Any:
    input_path = Path(path)
    if input_path.suffix.lower() in {".xlsx", ".xls"}:
        return pd.read_excel(input_path)
    return pd.read_csv(input_path)


def write_outputs(report: dict[str, Any], args: argparse.Namespace) -> None:
    report = clean_float(report, args.digits)
    text = json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.json_out:
        Path(args.json_out).write_text(text, encoding="utf-8")
    if args.md_out:
        Path(args.md_out).write_text(to_markdown(report), encoding="utf-8")
    if not args.json_out and not args.md_out:
        print(text, end="")


def table_from_params(result: Any) -> list[dict[str, Any]]:
    conf = result.conf_int()
    rows = []
    for name in result.params.index:
        rows.append(
            {
                "term": str(name),
                "estimate": result.params[name],
                "std_error": result.bse[name],
                "statistic": result.tvalues[name] if hasattr(result, "tvalues") else result.zvalues[name],
                "p_value": result.pvalues[name],
                "ci95_low": conf.loc[name].iloc[0],
                "ci95_high": conf.loc[name].iloc[1],
            }
        )
    return rows


def model_fit_metadata(result: Any) -> dict[str, Any]:
    meta: dict[str, Any] = {
        "nobs": getattr(result, "nobs", None),
        "df_model": getattr(result, "df_model", None),
        "df_resid": getattr(result, "df_resid", None),
        "aic": getattr(result, "aic", None),
        "bic": getattr(result, "bic", None),
    }
    return meta


def run_regression(args: argparse.Namespace) -> dict[str, Any]:
    smf = require("statsmodels", "statsmodels.formula.api")
    sm = require("statsmodels", "statsmodels.api")
    df = read_data(args.input)
    family = args.family.lower()
    if family == "linear":
        fit = smf.ols(args.formula, data=df).fit()
    elif family == "logistic":
        fit = smf.logit(args.formula, data=df).fit(disp=False, maxiter=args.maxiter)
    elif family == "poisson":
        fit = smf.glm(args.formula, data=df, family=sm.families.Poisson()).fit(maxiter=args.maxiter)
    elif family == "negative-binomial":
        fit = smf.glm(args.formula, data=df, family=sm.families.NegativeBinomial()).fit(maxiter=args.maxiter)
    else:
        raise SystemExit(f"Unsupported regression family: {args.family}")
    covariance = "nonrobust"
    if args.cluster:
        fit = fit.get_robustcov_results(cov_type="cluster", groups=df[args.cluster])
        covariance = f"cluster:{args.cluster}"
    elif args.robust:
        fit = fit.get_robustcov_results(cov_type=args.robust)
        covariance = args.robust
    return {
        "analysis": "multivariable_regression",
        "input": args.input,
        "formula": args.formula,
        "family": family,
        "covariance": covariance,
        "fit": model_fit_metadata(fit),
        "terms": table_from_params(fit),
        "warnings": ["Rows with missing model variables are dropped by statsmodels formula handling."],
    }


def run_gee(args: argparse.Namespace) -> dict[str, Any]:
    smf = require("statsmodels", "statsmodels.formula.api")
    sm = require("statsmodels", "statsmodels.api")
    cov_struct_mod = require("statsmodels", "statsmodels.genmod.cov_struct")
    df = read_data(args.input)
    family_map = {
        "gaussian": sm.families.Gaussian(),
        "binomial": sm.families.Binomial(),
        "poisson": sm.families.Poisson(),
    }
    cov_map = {
        "independence": cov_struct_mod.Independence(),
        "exchangeable": cov_struct_mod.Exchangeable(),
        "autoregressive": cov_struct_mod.Autoregressive(),
    }
    if args.family not in family_map:
        raise SystemExit(f"Unsupported GEE family: {args.family}")
    if args.cov_struct not in cov_map:
        raise SystemExit(f"Unsupported covariance structure: {args.cov_struct}")
    fit = smf.gee(
        args.formula,
        groups=args.group,
        data=df,
        family=family_map[args.family],
        cov_struct=cov_map[args.cov_struct],
    ).fit(maxiter=args.maxiter)
    return {
        "analysis": "clustered_repeated_measures_gee",
        "input": args.input,
        "formula": args.formula,
        "group": args.group,
        "family": args.family,
        "cov_struct": args.cov_struct,
        "fit": model_fit_metadata(fit),
        "terms": table_from_params(fit),
        "warnings": ["GEE estimates population-averaged associations; verify working correlation and visit/time coding."],
    }


def run_survival(args: argparse.Namespace) -> dict[str, Any]:
    lifelines = require("lifelines")
    df = read_data(args.input)
    covariates = parse_vars(args.covariates)
    columns = [args.duration, args.event] + covariates + parse_vars(args.strata)
    work = df[columns].dropna().copy()
    fitter = lifelines.CoxPHFitter()
    fitter.fit(
        work,
        duration_col=args.duration,
        event_col=args.event,
        strata=parse_vars(args.strata) or None,
        robust=args.robust,
    )
    summary = fitter.summary.reset_index().rename(columns={"index": "term"})
    proportional = None
    if args.check_ph:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            results = lifelines.statistics.proportional_hazard_test(
                fitter, work, time_transform="rank"
            )
        proportional = results.summary.reset_index().to_dict(orient="records")
    return {
        "analysis": "cox_proportional_hazards",
        "input": args.input,
        "duration": args.duration,
        "event": args.event,
        "covariates": covariates,
        "strata": parse_vars(args.strata),
        "n": len(work),
        "events": int(work[args.event].sum()),
        "concordance_index": fitter.concordance_index_,
        "terms": summary.to_dict(orient="records"),
        "proportional_hazards_test": proportional,
        "warnings": ["Interpret hazard ratios only if proportional hazards assumptions are defensible."],
    }


def run_impute(args: argparse.Namespace) -> dict[str, Any]:
    require("sklearn")
    from sklearn.experimental import enable_iterative_imputer  # noqa: F401
    from sklearn.impute import IterativeImputer

    df = read_data(args.input)
    variables = parse_vars(args.variables) or list(df.select_dtypes(include=[np.number]).columns)
    if not variables:
        raise SystemExit("No numeric variables available for imputation.")
    work = df.copy()
    before = work[variables].isna().sum().to_dict()
    imputer = IterativeImputer(
        random_state=args.seed,
        max_iter=args.maxiter,
        sample_posterior=False,
        skip_complete=True,
    )
    work[variables] = imputer.fit_transform(work[variables])
    if args.output:
        output_path = Path(args.output)
        if output_path.suffix.lower() in {".xlsx", ".xls"}:
            work.to_excel(output_path, index=False)
        else:
            work.to_csv(output_path, index=False)
    return {
        "analysis": "deterministic_iterative_imputation",
        "input": args.input,
        "output": args.output,
        "variables": variables,
        "seed": args.seed,
        "max_iter": args.maxiter,
        "missing_before": before,
        "missing_after": work[variables].isna().sum().to_dict(),
        "n_rows": len(work),
        "warnings": [
            "This is single deterministic numeric imputation, not pooled multiple imputation.",
            "Use full multiple imputation with Rubin pooling for primary inferential analyses.",
        ],
    }


def one_hot_matrix(df: Any, variables: list[str]) -> tuple[Any, list[str]]:
    from sklearn.compose import ColumnTransformer
    from sklearn.preprocessing import OneHotEncoder, StandardScaler

    numeric = [v for v in variables if pd.api.types.is_numeric_dtype(df[v])]
    categorical = [v for v in variables if v not in numeric]
    transformer = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), numeric),
            ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), categorical),
        ],
        remainder="drop",
    )
    matrix = transformer.fit_transform(df[variables])
    names: list[str] = []
    names.extend(numeric)
    if categorical:
        encoder = transformer.named_transformers_["cat"]
        names.extend([str(name) for name in encoder.get_feature_names_out(categorical)])
    return matrix, names


def smd_numeric(series: Any, treatment: Any, weights: Any | None = None) -> float | None:
    treated = treatment == 1
    control = treatment == 0
    x1 = series[treated]
    x0 = series[control]
    if len(x1) == 0 or len(x0) == 0:
        return None
    if weights is None:
        mean1, mean0 = x1.mean(), x0.mean()
        var1, var0 = x1.var(ddof=1), x0.var(ddof=1)
    else:
        w1 = weights[treated]
        w0 = weights[control]
        mean1 = np.average(x1, weights=w1)
        mean0 = np.average(x0, weights=w0)
        var1 = np.average((x1 - mean1) ** 2, weights=w1)
        var0 = np.average((x0 - mean0) ** 2, weights=w0)
    pooled = math.sqrt((float(var1) + float(var0)) / 2.0)
    if pooled == 0 or math.isnan(pooled):
        return None
    return float((mean1 - mean0) / pooled)


def balance_table(df: Any, treatment_col: str, covariates: list[str], weights: Any | None = None) -> list[dict[str, Any]]:
    treatment = df[treatment_col].astype(int).to_numpy()
    rows = []
    for var in covariates:
        if pd.api.types.is_numeric_dtype(df[var]):
            rows.append({"variable": var, "type": "numeric", "smd": smd_numeric(df[var].to_numpy(), treatment, weights)})
        else:
            for level in sorted(df[var].dropna().astype(str).unique()):
                indicator = (df[var].astype(str) == level).astype(float).to_numpy()
                rows.append({"variable": f"{var}={level}", "type": "categorical_level", "smd": smd_numeric(indicator, treatment, weights)})
    return rows


def run_propensity(args: argparse.Namespace) -> dict[str, Any]:
    require("sklearn")
    from sklearn.linear_model import LogisticRegression

    df = read_data(args.input)
    covariates = parse_vars(args.covariates)
    required = [args.treatment] + covariates
    work = df[required].dropna().copy()
    work[args.treatment] = work[args.treatment].astype(int)
    x, feature_names = one_hot_matrix(work, covariates)
    model = LogisticRegression(max_iter=args.maxiter, random_state=args.seed, solver="lbfgs")
    model.fit(x, work[args.treatment])
    ps = np.clip(model.predict_proba(x)[:, 1], args.clip, 1.0 - args.clip)
    treated = work[args.treatment].to_numpy() == 1
    p_treated = float(treated.mean())
    if args.stabilized:
        weights = np.where(treated, p_treated / ps, (1 - p_treated) / (1 - ps))
    else:
        weights = np.where(treated, 1 / ps, 1 / (1 - ps))
    if args.output_scores:
        out = df.copy()
        out["propensity_score"] = np.nan
        out["iptw"] = np.nan
        out.loc[work.index, "propensity_score"] = ps
        out.loc[work.index, "iptw"] = weights
        out.to_csv(args.output_scores, index=False)
    return {
        "analysis": "propensity_score_iptw",
        "input": args.input,
        "treatment": args.treatment,
        "covariates": covariates,
        "n_complete": len(work),
        "treated_prevalence": p_treated,
        "seed": args.seed,
        "stabilized": args.stabilized,
        "clip": args.clip,
        "feature_names": feature_names,
        "propensity_summary": {
            "min": float(np.min(ps)),
            "q1": float(np.quantile(ps, 0.25)),
            "median": float(np.quantile(ps, 0.50)),
            "q3": float(np.quantile(ps, 0.75)),
            "max": float(np.max(ps)),
        },
        "weight_summary": {
            "min": float(np.min(weights)),
            "q1": float(np.quantile(weights, 0.25)),
            "median": float(np.quantile(weights, 0.50)),
            "q3": float(np.quantile(weights, 0.75)),
            "max": float(np.max(weights)),
        },
        "balance_before": balance_table(work, args.treatment, covariates),
        "balance_after_iptw": balance_table(work, args.treatment, covariates, weights),
        "output_scores": args.output_scores,
        "warnings": ["Check positivity/overlap before using IPTW estimates."],
    }


def run_prediction(args: argparse.Namespace) -> dict[str, Any]:
    require("sklearn")
    from sklearn.linear_model import LinearRegression, LogisticRegression
    from sklearn.metrics import (
        accuracy_score,
        brier_score_loss,
        mean_absolute_error,
        mean_squared_error,
        r2_score,
        roc_auc_score,
    )
    from sklearn.model_selection import train_test_split

    df = read_data(args.input)
    predictors = parse_vars(args.predictors)
    required = [args.target] + predictors
    work = df[required].dropna().copy()
    x, feature_names = one_hot_matrix(work, predictors)
    y = work[args.target]
    stratify = y if args.task == "classification" and y.nunique() == 2 else None
    x_train, x_test, y_train, y_test = train_test_split(
        x,
        y,
        test_size=args.test_size,
        random_state=args.seed,
        stratify=stratify,
    )
    if args.task == "classification":
        model = LogisticRegression(max_iter=args.maxiter, random_state=args.seed, solver="lbfgs")
        model.fit(x_train, y_train)
        probs = model.predict_proba(x_test)[:, 1]
        preds = model.predict(x_test)
        metrics = {
            "accuracy": accuracy_score(y_test, preds),
            "roc_auc": roc_auc_score(y_test, probs) if len(set(y_test)) == 2 else None,
            "brier_score": brier_score_loss(y_test, probs) if set(y_test).issubset({0, 1}) else None,
        }
    else:
        model = LinearRegression()
        model.fit(x_train, y_train)
        preds = model.predict(x_test)
        metrics = {
            "rmse": math.sqrt(mean_squared_error(y_test, preds)),
            "mae": mean_absolute_error(y_test, preds),
            "r2": r2_score(y_test, preds),
        }
    return {
        "analysis": "prediction_model_holdout",
        "input": args.input,
        "task": args.task,
        "target": args.target,
        "predictors": predictors,
        "feature_names": feature_names,
        "n_complete": len(work),
        "n_train": len(y_train),
        "n_test": len(y_test),
        "test_size": args.test_size,
        "seed": args.seed,
        "metrics": metrics,
        "warnings": [
            "Holdout metrics are a first-pass check, not full TRIPOD-compliant validation.",
            "Assess calibration, optimism, clinical utility, and external validation before manuscript claims.",
        ],
    }


def to_markdown(report: dict[str, Any]) -> str:
    lines = [
        f"# {str(report.get('analysis', 'advanced_statistics')).replace('_', ' ').title()}",
        "",
        "## Audit Metadata",
        "",
    ]
    for key in ["input", "formula", "family", "group", "duration", "event", "target", "task", "seed"]:
        if key in report and report[key] is not None:
            lines.append(f"- {key}: `{report[key]}`")
    if "warnings" in report:
        lines.extend(["", "## Warnings", ""])
        for warning in report["warnings"]:
            lines.append(f"- {warning}")
    lines.extend(["", "## Machine-Readable Results", "", "```json", json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True), "```", ""])
    return "\n".join(lines)


def add_common(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--json-out", help="Write JSON report.")
    parser.add_argument("--md-out", help="Write Markdown report.")
    parser.add_argument("--digits", type=int, default=5, help="Decimal places for numeric output.")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Advanced deterministic medical statistics.")
    sub = parser.add_subparsers(dest="command", required=True)

    regression = sub.add_parser("regression", help="Multivariable regression.")
    regression.add_argument("--input", required=True)
    regression.add_argument("--formula", required=True, help='Example: "outcome ~ age + C(sex) + treatment"')
    regression.add_argument("--family", choices=["linear", "logistic", "poisson", "negative-binomial"], required=True)
    regression.add_argument("--cluster", help="Cluster variable for cluster-robust standard errors.")
    regression.add_argument("--robust", choices=["HC0", "HC1", "HC2", "HC3"], help="Heteroscedasticity-robust covariance.")
    regression.add_argument("--maxiter", type=int, default=200)
    add_common(regression)

    gee = sub.add_parser("gee", help="Clustered or repeated-measures GEE.")
    gee.add_argument("--input", required=True)
    gee.add_argument("--formula", required=True)
    gee.add_argument("--group", required=True, help="Subject/cluster ID column.")
    gee.add_argument("--family", choices=["gaussian", "binomial", "poisson"], default="gaussian")
    gee.add_argument("--cov-struct", choices=["independence", "exchangeable", "autoregressive"], default="exchangeable")
    gee.add_argument("--maxiter", type=int, default=100)
    add_common(gee)

    survival = sub.add_parser("survival", help="Cox proportional hazards model.")
    survival.add_argument("--input", required=True)
    survival.add_argument("--duration", required=True)
    survival.add_argument("--event", required=True)
    survival.add_argument("--covariates", required=True)
    survival.add_argument("--strata", help="Comma-separated strata columns.")
    survival.add_argument("--robust", action="store_true")
    survival.add_argument("--check-ph", action="store_true")
    add_common(survival)

    impute = sub.add_parser("impute", help="Deterministic numeric iterative imputation.")
    impute.add_argument("--input", required=True)
    impute.add_argument("--output", required=True)
    impute.add_argument("--variables", help="Comma-separated numeric variables; defaults to all numeric columns.")
    impute.add_argument("--seed", type=int, default=20260518)
    impute.add_argument("--maxiter", type=int, default=20)
    add_common(impute)

    propensity = sub.add_parser("propensity", help="Propensity score estimation and IPTW balance.")
    propensity.add_argument("--input", required=True)
    propensity.add_argument("--treatment", required=True, help="Binary 0/1 treatment column.")
    propensity.add_argument("--covariates", required=True)
    propensity.add_argument("--output-scores", help="CSV with propensity_score and iptw columns.")
    propensity.add_argument("--stabilized", action="store_true")
    propensity.add_argument("--clip", type=float, default=0.01)
    propensity.add_argument("--seed", type=int, default=20260518)
    propensity.add_argument("--maxiter", type=int, default=1000)
    add_common(propensity)

    prediction = sub.add_parser("prediction", help="Deterministic holdout prediction model.")
    prediction.add_argument("--input", required=True)
    prediction.add_argument("--task", choices=["classification", "regression"], required=True)
    prediction.add_argument("--target", required=True)
    prediction.add_argument("--predictors", required=True)
    prediction.add_argument("--test-size", type=float, default=0.25)
    prediction.add_argument("--seed", type=int, default=20260518)
    prediction.add_argument("--maxiter", type=int, default=1000)
    add_common(prediction)
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    handlers = {
        "regression": run_regression,
        "gee": run_gee,
        "survival": run_survival,
        "impute": run_impute,
        "propensity": run_propensity,
        "prediction": run_prediction,
    }
    try:
        report = handlers[args.command](args)
    except Exception as exc:
        if isinstance(exc, SystemExit):
            raise
        print(f"advanced_stats.py failed: {type(exc).__name__}: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
    write_outputs(report, args)


if __name__ == "__main__":
    main()
